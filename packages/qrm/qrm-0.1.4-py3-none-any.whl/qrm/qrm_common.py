#!/usr/bin/env python3

"""This module contains stuff shared between UI and CLI"""

# pylint: disable=unspecified-encoding


import json
import socket
import sys
import time
import zipfile
from collections.abc import Iterator, Mapping
from contextlib import suppress
from pathlib import Path
from uuid import uuid4

from lxml import etree
from paramiko import SFTPClient, SSHClient, ssh_exception

XOCHITL_DIR = Path(".local/share/remarkable/xochitl")

CFG_FILE = Path("~/.config/qrm.cfg")


def load_json(path):
    """Convenience wrapper for reading a JSON file"""
    with suppress(FileNotFoundError, json.JSONDecodeError):
        with open(path.expanduser()) as file:
            return json.load(file)
    return {}


def save_json(path, data):
    """Convenience wrapper for writing a JSON file"""
    with open(path.expanduser(), "w") as file:
        json.dump(data, file)


def load_config_or_defaults():
    """Convenience convenience wrapper for getting stored contents or default values"""
    return {
        **{
            "auth": {
                "host": "reMarkable",
                "username": "root",
                "password": "---",
            }
        },
        **load_json(CFG_FILE),
    }


def save_config(data):
    """Convenience convenience wrapper for storing the configuration to where it belongs"""
    save_json(CFG_FILE, data)


def ssh_connection(host: str, username: str, password=None) -> SSHClient:
    """Establishes and returns a paramiko SSH client session"""
    client = SSHClient()
    client.load_system_host_keys()
    try:
        print(f"Try to connect to {host!r}...")
        client.connect(host, username=username, password=password)
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
        return element.xpath(
            path,
            namespaces={
                "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                "pkg": "http://www.idpf.org/2007/opf",
                "dc": "http://purl.org/dc/elements/1.1/",
            },
        )[0]

    with zipfile.ZipFile(fname) as zip_content:
        cfname = xpath(
            etree.fromstring(zip_content.read("META-INF/container.xml")),
            "n:rootfiles/n:rootfile/@full-path",
        )
        metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

    return {
        s: xpath(metadata, f"dc:{s}/text()")
        for s in ("title", "language", "creator", "date", "identifier")
    }


def upload_file(rm_sftp, path):
    t = time()
    info = epub_info(path)
    print(info)

    uuid = uuid4()

    print(f"{time.time() - t}")

    print(f"{uuid}")

    print(f"{time.time() - t}")
    with path.open("rb") as inputfile:
        with rm_ftp.open(str(XOCHITL_DIR / f"{uuid}.epub"), "wb") as payloadfile:
            payloadfile.write(inputfile.read())
            print(f"{time.time() - t}")

    with rm_ftp.open(str(XOCHITL_DIR / f"{uuid}.content"), "w") as contentfile:
        json.dump({"coverPageNumber": 0, "fileType": "epub"}, contentfile)

    print(f"{time.time() - t}")

    with rm_ftp.open(str(XOCHITL_DIR / f"{uuid}.metadata"), "w") as metadatafile:
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

    print(f"{time.time() - t}")

    rm_ssh.exec_command("/sbin/reboot")

    print(f"{time.time() - t}")
