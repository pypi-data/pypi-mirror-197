# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import json
import os
import sys
import traceback
import urllib
from logging import error

from portmod.globals import env
from portmod.repo import get_repo
from portmodlib.atom import Atom

from .generate import generate_build_files
from .update import get_updates
from .validate import validate_all_files


def handle_validate(args):
    validate_all_files()


def handle_update(args):
    if args.interactive:
        env.INTERACTIVE = True
        os.environ["INTERACTIVE"] = "1"
    else:
        env.INTERACTIVE = False

    updates = get_updates(repository=get_repo(args.repo).location, no_implicit=True)

    failed = []
    for update in updates:
        try:
            generate_build_files(
                {"atom": update.newatom},
                repo=args.repo,
            )
        except Exception as e:
            if args.debug:
                traceback.print_exc()
            error(e)
            failed.append(update)

    if failed:
        error("The following updates failed to generate:")
        print("  " + "\n  ".join([str(f.newatom) for f in failed]))
        sys.exit(1)


def handle_import(args):
    if not args.package:
        return
    if args.interactive:
        env.INTERACTIVE = True
        os.environ["INTERACTIVE"] = "1"
    else:
        env.INTERACTIVE = False

    parsedurl = urllib.parse.urlparse(args.package)
    # If input is a url
    if parsedurl.scheme:
        return generate_build_files(
            {"url": args.package},
            noreplace=args.noreplace,
            repo=args.output_repo or "local",
        )

    if not os.path.exists(args.package):
        return generate_build_files(
            {"atom": Atom(args.package)},
            noreplace=args.noreplace,
            repo=args.output_repo or "local",
        )

    (mod_name, ext) = os.path.splitext(os.path.basename(args.package))
    failed = []

    with open(args.package, mode="r") as file:
        if ext == ".json":
            mods = json.load(file)
            for index, mod in enumerate(mods):
                print(f"Importing mod {index}/{len(mods)}")
                try:
                    generate_build_files(
                        mod,
                        noreplace=args.noreplace,
                        repo=args.output_repo or "local",
                    )
                except Exception as e:
                    if args.debug:
                        traceback.print_exc()
                    error(e)
                    failed.append(mod)
        else:
            for line in file.readlines():
                words = line.split()
                if len(words) > 0:
                    d = {"atom": words[0], "url": " ".join(words[1:])}
                    try:
                        generate_build_files(
                            d,
                            noreplace=args.noreplace,
                            repo=args.output_repo or "local",
                        )
                    except Exception as e:
                        if args.debug:
                            traceback.print_exc()
                        error(e)
                        failed.append(d)
    if failed:
        error("The following mods failed to import:")
        print("\n".join([str(f.get("name", f["atom"])) for f in failed]))
        sys.exit(1)


def add_importer_parsers(subparsers):
    imp = subparsers.add_parser("import", help="Subcommand for importing mods")
    imp.add_argument(
        "package",
        metavar="ATOM|FILE",
        help='automatically generates pybuilds for mods specified in the given file. \
        File can be one of the following formats: \nA plaintext file consisting of a \
        mod atom and url per line, separated by a space. \nA json file with any of the \
        fields "atom", "name", "desc"/"description", "homepage", "category", "url", \
        "file" \
        The url should be for either the direct download, or the homepage of a NexusMods \
        GitLab, GitHub, or mw.modhistory.com project. \
        The package version is required for direct downloads, but can otherwise be omitted. \
        Note that it may be useful to include if the remote version is poorly formed.',
    )
    imp.add_argument(
        "-n",
        "--noreplace",
        help="Skips importing mods that have already been installed",
        action="store_true",
    )
    imp.add_argument(
        "-o",
        "--output-repo",
        help="Repository used to store the output file. If this is the same as the "
        "input repository, files may be overwritten",
    )
    imp.add_argument("--debug", help="Enables debug traces", action="store_true")
    imp.add_argument(
        "--interactive",
        help="Enables interactive selection of detected mod components",
        action="store_true",
    )

    validate = subparsers.add_parser(
        "validate",
        help="Validates all nexus sources in the tree by using the API to check that "
        "a remote file matches the file we have locally",
    )

    update = subparsers.add_parser(
        "update",
        help="Updates packages in repository",
    )
    update.add_argument("repo", help="Repository to update")
    update.add_argument(
        "--interactive",
        help="Enables updates to packages which can't be downloaded automatically",
        action="store_true",
    )
    update.add_argument("--debug", help="Enables debug traces", action="store_true")

    update.set_defaults(func=handle_update)
    imp.set_defaults(func=handle_import)
    validate.set_defaults(func=handle_validate)
