#!/usr/bin/env python3

"""This module contains stuff shared between UI and CLI"""

# pylint: disable=unspecified-encoding


import json
import socket
import time
import zipfile
from collections.abc import Iterator, Mapping
from contextlib import suppress
from pathlib import Path
from typing import Any
from uuid import uuid4

from lxml import etree
from paramiko import SFTPClient, SSHClient, ssh_exception

XOCHITL_DIR = Path(".local/share/remarkable/xochitl")


def ssh_connection(config) -> SSHClient:
    """Establishes and returns a paramiko SSH client session"""
    client = SSHClient()
    client.load_system_host_keys()
    try:
        print(f"Try to connect to {config.hostname!r}...")
        client.connect(
            config.hostname,
            username=config.username,
            password=config.password,
            timeout=config.timeout,
        )
        return client
    except socket.gaierror as exc:
        raise RuntimeError(f"{exc}") from exc
    except ssh_exception.SSHException as exc:
        raise RuntimeError(f"{exc}") from exc
    except ssh_exception.NoValidConnectionsError as exc:
        raise RuntimeError(f"{exc}") from exc


def sftp_connection(client: SSHClient) -> SFTPClient:
    """Returns a ready to use SFTP connection"""
    return client.open_sftp()


def list_dir(sftp: SFTPClient, directory: str = XOCHITL_DIR) -> Iterator[Path]:
    """Lists remote directory content"""
    yield from (Path(x) for x in sftp.listdir(str(directory)))


def list_docs(sftp: SFTPClient) -> Iterator[tuple[str, Mapping[str, str]]]:
    """Yields UID and metadata mapping for each document on device"""
    files = set(p.name for p in list_dir(sftp))
    for doc in set(_doc for p in files if f"{(_doc:=p.split('.')[0])}.metadata" in files):
        with sftp.open(filepath := str(XOCHITL_DIR / f"{doc}.metadata")) as file:
            try:
                yield doc, json.loads(file.read().decode())
            except json.JSONDecodeError as exc:
                print(f"Could not read {filepath}: {exc}")


def epub_info(fname: str) -> str:
    def xpath(element, path):
        return (
            results[0]
            if (
                results := element.xpath(
                    path,
                    namespaces={
                        "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                        "pkg": "http://www.idpf.org/2007/opf",
                        "dc": "http://purl.org/dc/elements/1.1/",
                    },
                )
            )
            else None
        )

    with zipfile.ZipFile(fname) as zip_content:
        cfname = xpath(
            etree.fromstring(zip_content.read("META-INF/container.xml")),
            "n:rootfiles/n:rootfile/@full-path",
        )
        metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

    return {
        s: value
        for s in ("title", "language", "creator", "date", "identifier")
        if (value := xpath(metadata, f"dc:{s}/text()"))
    }


def upload_file(rm_sftp: SFTPClient, path: Path) -> None:
    t = time.time()
    info = epub_info(path)
    print(info)

    uuid = uuid4()

    print(f"{time.time() - t:.2f}s")

    print(f"{uuid}")

    print(f"{time.time() - t:.2f}s")
    with path.open("rb") as inputfile:
        with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.epub"), "wb") as payloadfile:
            payloadfile.write(inputfile.read())
            print(f"{time.time() - t}")

    with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.content"), "w") as contentfile:
        json.dump({"coverPageNumber": 0, "fileType": "epub"}, contentfile)

    print(f"{time.time() - t:.2f}s")

    with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.metadata"), "w") as metadatafile:
        json.dump(
            {
                # "deleted": False,
                # "lastModified": "1649503474223",
                # "lastOpened": "1658044625089",
                # "lastOpenedPage": 0,
                # "metadatamodified": False,
                # "modified": True,
                "parent": "",
                # "pinned": False,
                # "synced": False,
                "type": "DocumentType",
                "version": 0,
                "visibleName": info["title"],
            },
            metadatafile,
        )


def reboot(client: SSHClient) -> None:
    """Shortcut for rebooting the device"""
    client.exec_command("/sbin/reboot")
