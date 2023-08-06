#!/usr/bin/env python3

"""QrM CLI
"""

from argparse import ArgumentParser, ArgumentTypeError
from argparse import Namespace as Args
from contextlib import suppress
import json
# from collections.abc import Iterable, Mapping
from pathlib import Path

from qrm import qrm_common
from dataclasses import dataclass

# from treelib import Tree

CFG_FILE = Path("~/.config/qrm.cfg")

def first_not_none(*values: int|str|None) -> int|str:
    for value in values:
        if value is not None:
            return value

def load_json(path: Path):
    """Convenience wrapper for reading a JSON file"""
    with suppress(FileNotFoundError, json.JSONDecodeError):
        with open(path.expanduser()) as file:
            return json.load(file)
    return {}


@dataclass
class Config:
    hostname: str
    username: str
    password: str
    timeout: int 
    window_geometry: tuple[int, int, int, int]|None=None


class ConfigManager:
    def __init__(self, args):
        self.config_file_path = args.config_file
        persisted = load_json(self.config_file_path)
        self.config = Config(
            hostname = first_not_none(args.hostname, persisted.get("hostname"), "reMarkable"),
            username = first_not_none(args.username, persisted.get("username"), "root"),
            password = first_not_none(args.password, persisted.get("password"), ""),
            timeout = first_not_none(args.timeout, persisted.get("timeout"), 6),
            window_geometry = persisted.get("window_geometry"),
        )

    def __enter__(self):
        return self

    def __exit__(*args):
        ...

    def persist(self):
        with open(self.config_file_path.expanduser(), "w") as file:
            json.dump(self.config, file, default=lambda o: o.__dict__, indent=4, sort_keys=True)
    

def split_kw(string: str) -> tuple[str, str]:
    """Config element splitter"""
    try:
        key, value = string.split("=", 1)
    except ValueError as exc:
        raise ArgumentTypeError("Syntax: '<KEY>=<VALUE> ...'") from exc
    return key, value


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--hostname", type=str)
    parser.add_argument("--username", "-u", type=str)
    parser.add_argument("--password", "-p", type=str)

    parser.add_argument("--timeout", "-t", type=int)
    parser.add_argument("--config-file", "-c", type=Path, default=CFG_FILE)

    subparsers = parser.add_subparsers(help="types of A")
    parser.set_defaults(func=fn_ui)

    parser_show = subparsers.add_parser("info")
    parser_show.set_defaults(func=fn_info)

    parser_show = subparsers.add_parser("reboot")
    parser_show.set_defaults(func=fn_reboot)

    parser_show = subparsers.add_parser("config-auth")
    parser_show.set_defaults(func=fn_config)
    parser_show.add_argument("auth_kwargs", type=split_kw, nargs="+")

    parser_show = subparsers.add_parser("list", aliases=["ls"])
    parser_show.set_defaults(func=fn_list)
    parser_show.add_argument("path", type=str, nargs="*")

    parser_build = subparsers.add_parser("upload", aliases=["push"])
    parser_build.set_defaults(func=fn_upload)
    parser_build.add_argument("path", type=Path, nargs="+")

    return parser.parse_args()


def fn_config(args: Args) -> None:
    """Entry point for configuration"""
    with ConfigManager(args) as config:
        auth_kwargs = dict(args.auth_kwargs)
        if "hostname" in auth_kwargs:
            config.config.hostname = auth_kwargs["hostname"]
        if "username" in auth_kwargs:
            config.config.username = auth_kwargs["username"]
        if "password" in auth_kwargs:
            config.config.password = auth_kwargs["password"]
        config.persist()
    

def fn_info(args: Args) -> None:
    """Entry point for info"""
    with ConfigManager(args) as config:
        print(f"Config file located at '{args.config_file}'")
        for key, value in config.config.__dict__.items():
            print(key, value)


def fn_reboot(args: Args) -> None:
    """Entry point for info"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = qrm_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return
    qrm_common.reboot(rm_ssh)


def fn_upload(args: Args) -> None:
    """Entry point for file upload via CLI"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = qrm_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

    rm_ftp = qrm_common.sftp_connection(rm_ssh)

    for path in args.path:
        qrm_common.upload_file(rm_ftp, path)


def fn_list(args: Args) -> None:
    """Entry point for content listing via CLI"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = qrm_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

    rm_ftp = qrm_common.sftp_connection(rm_ssh)
    content = dict(qrm_common.list_docs(rm_ftp))

    for uid, metadata in content.items():
        if metadata["type"] == "DocumentType":
            parent_str = (
                parent["visibleName"]
                if (parent := content.get(metadata["parent"]))
                else metadata["parent"]
            )
            print(f"{uid.split('-', 1)[0]}: {metadata['visibleName']} ({parent_str})")


def fn_ui(args: Args) -> None:
    """Entry point for UI"""

    # pylint: disable=import-outside-toplevel (late import to allow headless operation)
    from qrm.ui import main as ui_main
    with ConfigManager(args) as config:
        print(config.config.timeout)
        ui_main(config.config)
        config.persist()


def main() -> None:
    """Entry point for everything else"""
    (args := parse_args()).func(args)

if __name__ == "__main__":
    main()