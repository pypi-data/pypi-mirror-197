# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import argparse
import sys
import traceback
from logging import error

from .datadir import get_dominant_texture_size
from .install import add_install_parser


def handle_scan_textures(args):
    print(get_dominant_texture_size(args.directory))


def main():
    parser = argparse.ArgumentParser(
        description="Tool for integrating upstream mods into portmod"
    )
    subparsers = parser.add_subparsers()
    add_install_parser(subparsers)
    try:
        from importmod.main import add_importer_parsers

        add_importer_parsers(subparsers)
    except ModuleNotFoundError:
        pass

    scan = subparsers.add_parser(
        "scan_textures",
        help="Subcommand for scanning textures in data directories. "
        "Displays the dominant texture size, that is, the size of texture "
        "that takes up the most space in total.",
    )
    scan.add_argument("directory", help="Directory to (recursively) scan for textures")

    scan.set_defaults(func=handle_scan_textures)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    try:
        args.func(args)
    except Exception as e:
        traceback.print_exc()
        error(f"{e}")
        sys.exit(1)
