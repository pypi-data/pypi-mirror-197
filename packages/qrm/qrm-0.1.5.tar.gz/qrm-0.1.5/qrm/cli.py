#!/usr/bin/env python3

"""QrM CLI
"""

from argparse import ArgumentParser, ArgumentTypeError
from argparse import Namespace as Args

# from collections.abc import Iterable, Mapping
from pathlib import Path

from qrm import qrm_common

# from treelib import Tree


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
    parser.add_argument("-v", action="store_true")

    subparsers = parser.add_subparsers(help="types of A")
    parser.set_defaults(func=fn_ui)

    parser_show = subparsers.add_parser("info")
    parser_show.set_defaults(func=fn_info)

    parser_show = subparsers.add_parser("config-auth")
    parser_show.set_defaults(func=fn_config)
    parser_show.add_argument("kwargs", type=split_kw, nargs="+")

    parser_show = subparsers.add_parser("list", aliases=["ls"])
    parser_show.set_defaults(func=fn_list)
    parser_show.add_argument("path", type=str, nargs="*")

    parser_build = subparsers.add_parser("upload", aliases=["push"])
    parser_build.set_defaults(func=fn_upload)
    parser_build.add_argument("path", type=Path, nargs="+")

    return parser.parse_args()


def fn_info(_args: Args) -> None:
    """Entry point for info"""
    for key, value in qrm_common.load_config_or_defaults():
        print(key, value)


def fn_config(args: Args) -> None:
    """Entry point for configuration"""
    config = qrm_common.load_config_or_defaults()
    config.setdefault("auth", {}).update(dict(args.kwargs))
    qrm_common.save_config(config)


def fn_upload(args: Args) -> None:
    """Entry point for file upload via CLI"""
    config = qrm_common.load_config_or_defaults()

    try:
        rm_ssh = qrm_common.ssh_connection(**config["auth"])
    except RuntimeError as exc:
        print(f"Connection failed: {exc}")
        return

    rm_ftp = qrm_common.sftp_connection(rm_ssh)

    for path in args.path:
        qrm_common.upload_file(rm_ftp, path)


def fn_list(_args: Args) -> None:
    """Entry point for content listing via CLI"""
    config = qrm_common.load_config_or_defaults()
    try:
        rm_ssh = qrm_common.ssh_connection(**config["auth"])
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


def fn_ui(_args: Args) -> None:
    """Entry point for UI"""

    # pylint: disable=import-outside-toplevel (late import to allow headless operation)
    from .ui import main as ui_main

    ui_main()


def main() -> None:
    """Entry point for everything else"""
    (args := parse_args()).func(args)
