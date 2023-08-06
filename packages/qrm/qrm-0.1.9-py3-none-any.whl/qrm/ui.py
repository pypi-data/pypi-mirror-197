#!/usr/bin/env python3

"""QrM - Connect to reMarkable and modify contents
"""

# pylint: disable=invalid-name

import logging
import signal
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from qrm import qrm_common


def log() -> logging.Logger:
    """Returns the local logger"""
    return logging.getLogger("qrm_ui")


class QrMWindow(QtWidgets.QMainWindow):
    """The one and only application window"""

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.rm_ftp = None
        self.rm_ssh = None
        uic.loadUi(Path(__file__).parent / "qrm.ui", self)
        self.documents.horizontalHeader().setStretchLastSection(True)
        self.setAcceptDrops(True)

        self.txt_hostname.setText(config.hostname)
        self.txt_username.setText(config.username)
        self.txt_password.setText(config.password)
        self.txt_hostname.textChanged.connect(self.on_txt_hostname_textChanged)
        self.txt_username.textChanged.connect(self.on_txt_username_textChanged)
        self.txt_password.textChanged.connect(self.on_txt_password_textChanged)
        self.pb_connect.clicked.connect(self.connect)
        self.pb_reboot.clicked.connect(self.on_pb_reboot_clicked)
        self.pb_reboot.setEnabled(False)

        if config.window_geometry:
            self.setGeometry(*config.window_geometry)

        self.show()

    def on_txt_hostname_textChanged(self, text: str) -> None:
        """React on hostname modification"""
        self.config.hostname = text

    def on_txt_username_textChanged(self, text: str) -> None:
        """React on username modification"""
        self.config.username = text

    def on_txt_password_textChanged(self, text: str) -> None:
        """React on password modification"""
        self.config.password = text

    def on_pb_reboot_clicked(self) -> None:
        """React on reboot button click"""
        if self.rm_ssh:
            qrm_common.reboot(self.rm_ssh)


    @QtCore.pyqtSlot()
    def connect(self) -> None:
        """Connects to a reMarkable device via SSH and lists documents"""
        self.pb_reboot.setEnabled(False)

        try:
            self.rm_ssh = qrm_common.ssh_connection(self.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

        self.rm_ftp = qrm_common.sftp_connection(self.rm_ssh)
        self.pb_reboot.setEnabled(True)
        self.populate()

    def populate(self) -> None:
        self.documents.setRowCount(0)
        self.documents.clear()
        content = dict(sorted(qrm_common.list_docs(self.rm_ftp), key=lambda e: e[1]["visibleName"]))
        for uid, metadata in content.items():
            if metadata["type"] == "DocumentType":
                parent_str = (
                    p["visibleName"]
                    if (p := content.get(metadata["parent"]))
                    else metadata["parent"]
                )
                print(f"{uid.split('-', 1)[0]}: {metadata['visibleName']} ({parent_str})")
                rc = self.documents.rowCount()
                self.documents.insertRow(rc)
                self.documents.setItem(rc, 0, QtWidgets.QTableWidgetItem(uid.split("-", 1)[0]))
                self.documents.setItem(rc, 1, QtWidgets.QTableWidgetItem(metadata["visibleName"]))

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.DragEnter:
            if self.rm_ftp and any(
                Path(u.url()).suffix.lower() in {".pdf", ".epub"} for u in event.mimeData().urls()
            ):
                event.accept()
        elif event.type() == QtCore.QEvent.Drop:
            urls = [
                path
                for u in event.mimeData().urls()
                if (path := Path(u.url().split(":", 1)[-1])).suffix.lower() in {".pdf", ".epub"}
            ]
            print(urls)
            for url in urls:
                qrm_common.upload_file(self.rm_ftp, url)
            self.populate()

        elif not event.type() in {
            QtCore.QEvent.UpdateRequest,
            QtCore.QEvent.Paint,
            QtCore.QEvent.Enter,
            QtCore.QEvent.HoverEnter,
            QtCore.QEvent.HoverMove,
            QtCore.QEvent.HoverLeave,
            QtCore.QEvent.KeyPress,
            QtCore.QEvent.KeyRelease,
            QtCore.QEvent.DragMove,
            QtCore.QEvent.DragLeave,
        }:
            # log().warn("unknown event: %r %r", event.type(), event)
            pass
        return super().event(event)

    def closeEvent(self, _event: QtGui.QCloseEvent) -> None:
        """save state before shutting down"""
        logging.info("got some closish signal, bye")
        geom = self.geometry()
        self.config.window_geometry = (geom.x(), geom.y(), geom.width(), geom.height())


def main(args) -> None:
    """Typical PyQt5 boilerplate main entry point"""
    logging.getLogger().setLevel(logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    window = QrMWindow(args)

    for s in (signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(s, lambda signal, frame: window.close())

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    app.exec_()


if __name__ == "__main__":
    main()
