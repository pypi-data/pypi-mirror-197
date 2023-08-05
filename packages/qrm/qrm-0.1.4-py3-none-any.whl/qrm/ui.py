#!/usr/bin/env python3

"""RM-Connect - Connect to ReMarkable and modify contents
"""

# pylint: disable=invalid-name

import logging
import signal
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, uic

from qrm import qrm_common


class RmConnectWindow(QtWidgets.QMainWindow):
    """The one and only application window"""

    def __init__(self):
        super().__init__()
        self.rm_ftp = None
        uic.loadUi(Path(__file__).parent / "qrm.ui", self)
        self.config = qrm_common.load_json(qrm_common.CFG_FILE)
        auth = self.config.setdefault("auth", {})

        self.txt_host.setText(auth.setdefault("host", "reMarkable"))
        self.txt_username.setText(auth.setdefault("username", "root"))
        self.txt_password.setText(auth.setdefault("password", "---"))
        self.txt_host.textChanged.connect(self.on_txt_host_textChanged)
        self.txt_username.textChanged.connect(self.on_txt_username_textChanged)
        self.txt_password.textChanged.connect(self.on_txt_password_textChanged)

        self.setGeometry(*self.config.get("window_geometry", (50, 50, 1000, 500)))
        self.show()
        QtCore.QMetaObject.invokeMethod(
            self,
            "connect",
            QtCore.Qt.QueuedConnection,
            # QtCore.Q_ARG(list, [])
        )

    def on_txt_host_textChanged(self, text: str) -> None:
        """React on hostname modification"""
        self.config["auth"]["host"] = text

    def on_txt_username_textChanged(self, text: str) -> None:
        """React on username modification"""
        self.config["auth"]["username"] = text

    def on_txt_password_textChanged(self, text: str) -> None:
        """React on password modification"""
        self.config["auth"]["password"] = text

    @QtCore.pyqtSlot()
    def connect(self) -> None:
        """Connects to a reMarkable device via SSH and lists documents"""
        try:
            rm_ssh = qrm_common.ssh_connection(
                host=self.config["auth"]["host"],
                username=self.config["auth"]["username"],
                password=self.config["auth"]["password"],
            )
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

        self.rm_ftp = qrm_common.sftp_connection(rm_ssh)
        content = dict(qrm_common.list_docs(self.rm_ftp))

        self.documents.setColumnCount(2)
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

    def closeEvent(self, _event):
        """save state before shutting down"""
        logging.info("got some closish signal, bye")
        geom = self.geometry()
        qrm_common.save_json(
            qrm_common.CFG_FILE,
            {
                **self.config,
                **{
                    "window_geometry": (geom.x(), geom.y(), geom.width(), geom.height()),
                },
            },
        )


def main() -> None:
    """Typical PyQt5 boilerplate main entry point"""
    logging.getLogger().setLevel(logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    window = RmConnectWindow()

    for s in (signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(s, lambda signal, frame: window.close())

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
