"""
Module for generating pybuilds
"""

import datetime
import os
import re
import shutil
import urllib
from collections import defaultdict
from contextlib import contextmanager
from logging import error, warning
from types import SimpleNamespace
from typing import Iterable, List, Optional, Set, Tuple

import black
import isort
from colorama import Fore
from portmod._cli.pybuild import create_manifest
from portmod.download import download, get_download
from portmod.globals import env
from portmod.loader import load_all, load_file, load_pkg
from prompt_toolkit.validation import ValidationError, Validator

try:
    from portmod.merge import merge
except ImportError:
    from portmod.merge import configure as merge

from portmod.prompt import prompt_bool
from portmod.pybuild import File, InstallDir, Pybuild
from portmod.repo import Repo, get_repo, get_repo_root
from portmod.repo.metadata import get_categories, get_category_metadata
from portmod.repo.metadata import get_masters as get_repo_masters
from portmod.repo.metadata import license_exists
from portmodlib.atom import Atom, Version, version_gt
from portmodlib.colour import colour
from portmodlib.usestr import use_reduce
from redbaron import AtomtrailersNode, CallNode, RedBaron
from ruamel.yaml import YAML

from importmod_core.datadir import find_esp_bsa, get_dominant_texture_size
from importmod_core.install import select_data_dirs, unpack
from importmod_core.prompt import confirm, prompt_default

from .atom import parse_atom
from .deps import DependencyException, get_esp_deps, get_masters
from .sources import PackageData, PackageSource
from .update import get_newest, get_pkg_sources, guess_package_source, should_copy
from .util import clean_plugin, tr_patcher

LOCAL_REPO = Repo("local", os.path.join(env.REPOS_DIR, "local"), False, None, None, 50)


def update_file(file: AtomtrailersNode, new_file: File):
    """Updates plugin to match new_plugin"""
    assert file.value[0].value == "File"
    assert isinstance(file.value[1], CallNode)
    # Plugin name
    inner = file.value[1].value
    inner[0] = f'"{new_file.NAME}"'


def try_find(node, attr, key):
    try:
        return node.find(attr, key)
    except ValueError:
        return None


def update_idir(idir: AtomtrailersNode, new_idir: InstallDir):
    """Updates idir to match new_idir"""
    assert idir.value[0].value == "InstallDir"
    assert isinstance(idir.value[1], CallNode)
    inner = idir.value[1]

    def update_string(idir, new_idir, key):
        if hasattr(new_idir, key) and try_find(idir, "name", key):
            idir.find("name", key).parent.value = f'"{getattr(new_idir, key)}"'
        elif hasattr(new_idir, key) and getattr(new_idir, key):
            idir.append(f'{key}="{getattr(new_idir, key)}"')
        elif try_find(idir, "name", key):
            idir.remove(idir.find("name", key).parent)

    inner[0].value = f'"{new_idir.PATH}"'

    for key in ["S", "RENAME", "SOURCE"]:
        update_string(inner, new_idir, key)

    for key in ["PLUGINS", "ARCHIVES"]:
        if hasattr(new_idir, key) and inner.find("name", key):
            pending_files = {file.NAME: file for file in getattr(new_idir, key)}
            list_for_key = inner.find("name", key).parent.value

            files = [
                file
                for file in list_for_key
                if isinstance(file, AtomtrailersNode) and file.value[0].value == "File"
            ]

            # If there is only one plugin, assume it is the same as the old one
            if len(files) == 1 and len(new_idir.PLUGINS) == 1:
                update_file(files[0], new_idir.PLUGINS[0])
            else:
                # Otherwise, leave any old files that match the new files names,
                # remove files that aren't in the new list,
                # and add any missing files to the list
                for file in files:
                    # File name
                    name = file.value[1].value[0]
                    if name in pending_files:
                        del pending_files[name]
                    else:
                        list_for_key.remove(file)

                for file in pending_files:
                    if getattr(pending_files[file], "comment", None):
                        list_for_key.node_list.append(
                            RedBaron(pending_files[file].comment)
                        )
                        list_for_key.node_list.append(RedBaron("\n"))
                    # Attribute may be present but empty
                    if hasattr(pending_files[file], "comment"):
                        del pending_files[file].comment
                    list_for_key.node_list.append(
                        RedBaron(str(pending_files[file]) + ",")
                    )
        elif inner.find("name", key):
            # New idir doesn't have this element. Delete the old list
            inner.remove(inner.find("name", key).parent)
        elif hasattr(new_idir, key) and getattr(new_idir, key):
            inner.append(f"{key}={getattr(new_idir, key)}")


def get_header_string(end: int, start: Optional[int] = None):
    # Copyright Header
    if start:
        copyright_string = f"{start}-{end}"
    else:
        copyright_string = str(end)
    return [
        f"# Copyright {copyright_string} Portmod Authors",
        "# Distributed under the terms of the GNU General Public License v3",
    ]


YEAR = datetime.datetime.now().year


def get_old_package(package: PackageData) -> Optional[Pybuild]:
    if package.atom.C:
        oldmods = load_pkg(Atom(package.atom.CPN))
    else:
        oldmods = load_pkg(Atom(package.atom.PN))
    if oldmods:
        newest_package = get_newest(oldmods)
        return newest_package

    return None


class CategoryValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Categories must have a non-zero length")

        if not text[0].isalpha():
            raise ValidationError(
                message="Categories must begin with an alphanumeric character"
            )
        if text and not re.match(r"^[A-Za-z0-9][A-Za-z0-9-]*$", text):
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isalnum() and not c == "-":
                    break

            raise ValidationError(
                message="Categories can only contain alphanumeric characters and hyphens",
                cursor_position=i,
            )


class AtomValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Atoms must have a non-zero length")

        if not text[0].isalpha():
            raise ValidationError(
                message="Atoms must begin with an alphanumeric character"
            )
        if text and not re.match(r"^[A-Za-z0-9][A-Za-z0-9_+-]*$", text):
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isalnum() and not c == "-":
                    break

            raise ValidationError(
                message="Categories can only contain alphanumeric characters and hyphens",
                cursor_position=i,
            )


class VersionValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Versions must have a non-zero length")

        def try_parse(version: str):
            try:
                Version(version)
                return True
            except (TypeError, ValueError):
                return False

        if text and not try_parse(text):
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isalnum() and not c == "-":
                    break

            raise ValidationError(
                message="Invalid version. Check docs for format details",
                cursor_position=i,
            )


def get_source_data(mod) -> Tuple[PackageData, PackageSource, Optional[Pybuild]]:
    def get_atom(mod):
        if "atom" in mod:
            atom = Atom(mod["atom"])
        elif "category" in mod and "name" in mod:
            atom = parse_atom(mod["category"] + "/" + mod["name"])
        else:
            atom = None
        return atom

    url = mod.get("url")

    package = PackageData(
        atom=get_atom(mod),
        name=mod.get("name"),
        desc=mod.get("desc") or mod.get("description"),
        homepage=mod.get("homepage"),
        classes=["MW"],
        imports=defaultdict(set, {"common.mw": {"MW"}}),
        src_uri=url,
    )
    if "author" in mod:
        package.authors.append(mod.get("author"))

    upstream_source = None
    if url:
        upstream_source = guess_package_source(url)
        if upstream_source:
            upstream_source.get_pkg_data(package)

    oldpkg = None
    if package.atom:
        oldpkg = get_old_package(package)
        if not upstream_source:
            for possible_source in get_pkg_sources(oldpkg, no_implicit=False):
                if possible_source.get_pkg_data(package):
                    upstream_source = possible_source
                    break

    assert (
        upstream_source is not None
    ), "Unable to find an upstream mod source for this package!"

    if oldpkg:
        package.category = oldpkg.CATEGORY
        package.desc = oldpkg.DESC
        package.license = oldpkg.LICENSE

    if oldpkg and package.atom.PV:
        package.atom = Atom(oldpkg.CPN + "-" + package.atom.PV)
    elif oldpkg:
        package.atom = Atom(oldpkg.CPN)

    return package, upstream_source, oldpkg


def generate_build_files(mod, *, noreplace=False, repo="local"):
    """
    Generates pybuilds from a mod decription dictionary.

    Valid Fields: atom, name, desc, homepage, category, url, file,
      author, needs_cleaning
    Other fields are ignored
    """
    package, upstream_source, oldpkg = get_source_data(mod)

    if repo == "local":
        REPO = LOCAL_REPO
    else:
        REPO = get_repo(repo)

    print("Auto-detected information:")
    package.pretty_print()
    if os.environ.get("INTERACTIVE"):
        print("Starting interactive package generation")
        print()

    if not package.category:
        categories = get_categories(REPO.location)
        category_metadata = {
            category: get_category_metadata(REPO.location, category)
            for category in categories
        }
        category_descriptions = {
            category: metadata.longdescription
            for category, metadata in category_metadata.items()
            if metadata is not None
        }
        package.category = prompt_default(
            "<b>Package Category</b> (type to auto-complete): ",
            "",
            options=categories,
            options_desc=category_descriptions,
            validator=CategoryValidator(),
        )
        if package.category not in categories:
            warning(
                f"The chosen category does not exist. This will create a new category with the name {package.category}"
            )
            if not package.category.islower():
                warning(
                    "It is strongly recommended that categories are always lowercase"
                )
            if confirm("Would you like to continue?"):
                # TODO: Add category
                raise NotImplementedError()

    if not package.atom:
        package.atom = Atom(
            f"{package.category}/"
            + prompt_default(
                "<b>Package Name</b> (slug/atom): ",
                package.atom.PN if package.atom else None,
                validator=AtomValidator(),
            )
            + "-"
            + prompt_default(
                "<b>Package Version: </b>",
                package.atom.PVR if package.atom else None,
                validator=VersionValidator(),
            )
        )

    if noreplace and oldpkg and not version_gt(oldpkg.PVR, package.atom.PVR):
        print(f"Package {package.atom} already exists. Skipping...")
        return

    assert package.atom
    C = package.category
    assert C, "A category must be set!"
    P = package.atom.P
    PN = package.atom.PN

    if not os.environ.get("INTERACTIVE"):
        print(f"Importing {package.atom}...")

    build_file: Optional[str]
    if oldpkg and should_copy(oldpkg):
        print(f"Using file from {oldpkg}")
        with open(oldpkg.FILE) as file:
            pybuild = RedBaron(file.read())
            # KEYWORDS still need to be modified
            clear_keywords(pybuild)
            build_file = pybuild.dumps()
    else:
        build_file = generate_pybuild(
            package, upstream_source, oldpkg, mod.get("needs_cleaning"), REPO
        )
    if build_file is None:
        return

    # User import repo may not exist. If not, create it
    if not os.path.exists(REPO.location):
        os.makedirs(os.path.join(REPO.location, "profiles"), exist_ok=True)
        metadata_file = os.path.join(REPO.location, "profiles", "repo_name")
        with open(metadata_file, "w") as file:
            print("local", file=file)

        layout_file = os.path.join(REPO.location, "metadata", "layout.conf")
        os.makedirs(os.path.dirname(layout_file))
        with open(layout_file, "w") as file:
            print('masters="openmw"', file=file)
        # Add user repo to REPOS so that it can be used in further dependency resolution
        env.REPOS.append(REPO)
        # Write user import repo to repos.cfg
        with open(env.REPOS_FILE, "a") as file:
            userstring = """
[local]
location = {}
auto_sync = False
masters = openmw
priority = 50
"""
            print(userstring.format(REPO.location), file=file)

    if C not in get_categories(REPO.location):
        with open(
            os.path.join(REPO.location, "profiles", "categories"), "a"
        ) as categories:
            print(C, file=categories)

    outdir = os.path.join(REPO.location, C, PN)
    filename = os.path.join(outdir, P + ".pybuild")
    os.makedirs(outdir, exist_ok=True)

    print(f"Writing package file to {filename}")
    with open(filename, "w") as file:
        print(build_file, file=file, end="")

    # Add author to metadata.yaml if provided
    if package.authors:
        create_metadata(
            os.path.join(outdir, "metadata.yaml"),
            authors=package.authors,
            bugs_to=package.bugs_to,
            doc=package.doc,
        )

    # Create manifest file
    try:
        create_manifest(load_file(filename))
    except Exception as e:
        # Manifest generation failed. We need to roll back changes
        error(
            "Encountered error during manifest generation. Removing generated package file..."
        )
        os.remove(filename)
        raise e

    print(colour(Fore.GREEN, f"Finished Importing {package.atom}"))


def clear_keywords(file: RedBaron):
    Package = file.find("class", "Package")

    if Package.find("name", "KEYWORDS"):
        Package.find("name", "KEYWORDS").parent.value = '""'


def generate_pybuild(
    package: PackageData,
    upstream_source: PackageSource,
    oldpkg: Pybuild,
    needs_cleaning: bool,
    repo: Repo,
) -> Optional[str]:
    """Produces a pybuild file in the form of a string"""
    for source in package.sources:
        parsed = urllib.parse.urlparse(source.url)
        if parsed.scheme and not get_download(source):
            download(source.url, source.name)

    if not all([get_download(source) for source in package.sources]):
        if not env.INTERACTIVE:
            print(f"Skipping update to pacakge {package.atom} in non-interactive mode")
            return None
        print("Please download the following files from the url at the bottom")
        print("before continuing and move them to the download directory:")
        print(f"  {env.DOWNLOAD_DIR}")
        print()
        for source in package.sources:
            if not get_download(source):
                print(f"  {source}")
        print()
        assert (
            package.manual_download_url
        ), "PackageData.manual_download_url must be specified if the sources are not fetchable"
        print("  " + package.manual_download_url)
        if not prompt_bool("Continue?"):
            return None

    upstream_source.validate_downloads(package.sources)

    if oldpkg is not None:
        with open(oldpkg.FILE, "r", encoding="utf-8") as pybuild_file:
            pybuild = RedBaron(pybuild_file.read())
    else:
        pybuild = RedBaron("\n".join(get_header_string(YEAR)))

    dep_atoms: Set[Atom] = set()
    dep_uses: Set[str] = set()

    cleanr = re.compile("<.*?>")
    if package.desc is not None:
        package.desc = re.sub(cleanr, "", package.desc)
        package.desc = (
            package.desc.replace("\n", " ").replace("\r", " ").replace('"', '\\"')
        )

    package.name = prompt_default("<b>Package Name</b> (pretty format): ", package.name)
    package.desc = prompt_default("<b>Package Description:</b> ", package.desc)
    package.homepage = prompt_default("<b>Package Homepage:</b> ", package.homepage)

    def get_all_licenses(repo: Repo):
        repo_path = repo.location
        repos = [repo] + get_repo_masters(repo_path)

        for repo in repos:
            license_path = os.path.join(repo.location, "licenses")
            if os.path.exists(license_path):
                yield from os.listdir(license_path)

    package.license = prompt_default(
        "Package License (type to auto-complete): ",
        package.license or "FILLME",
        options=list(get_all_licenses(repo)),
    )
    if os.environ.get("INTERACTIVE") and package.license != "FILLME":
        for license in use_reduce(package.license, flat=True, matchall=True):
            if not license_exists(repo.location, license):
                warning(
                    f"License {license} does not exist, or is not accessible from the {repo.name} repository! {os.linesep}"
                    "You must create a license in the repository licenses directory for this license before the package will pass QA checks."
                )

    data_dirs = []
    TEXTURE_SIZES = set()
    INSTALL_DIRS: List[InstallDir] = []
    build_deps: Set[Atom] = set()

    for source in package.sources:
        # Extract file into tmp
        outdir = os.path.join(env.TMP_DIR, source.name)
        os.makedirs(outdir, exist_ok=True)
        unpack(get_download(source), outdir)

    for source in package.sources:
        # Search for data directories
        outdir = os.path.join(env.TMP_DIR, source.name)
        # Ignore esps and BSAs for now, we need them for each data directory
        dirs, _, _ = select_data_dirs(outdir)
        data_dirs.append((source.name, dirs))

        for directory in dirs:
            (esps, bsas) = find_esp_bsa(os.path.join(outdir, directory.PATH))
            if bsas:
                directory.ARCHIVES = [File(bsa) for bsa in bsas]

            source_name, _ = os.path.splitext(source.name)
            if source_name.endswith(".tar"):
                source_name, _ = os.path.splitext(source_name)

            texture_size = get_dominant_texture_size(
                os.path.join(env.TMP_DIR, source.name, directory.PATH)
            )

            if texture_size:
                TEXTURE_SIZES.add(texture_size)

            PLUGINS = []
            # Get dependencies for the ESP.
            for esp in esps:
                esp_path = os.path.join(outdir, directory.PATH, esp)
                print(f"Masters of esp {esp} are {get_masters(esp_path)}")
                dep_atom = None
                dep_use = None
                # TODO: No longer functional with Pybuild2
                if False:
                    try:
                        (dep_atom, dep_use) = get_esp_deps(
                            esp_path,
                            [
                                os.path.join(env.TMP_DIR, source, data_dir.PATH)
                                for (source, dirs) in data_dirs
                                for data_dir in dirs
                            ],
                            package.atom,
                            repo.name,
                        )
                        print(
                            f'Found esp "{esp}" with deps of: {dep_atom.union(dep_use)}'
                        )
                        dep_atoms |= dep_atom
                        dep_uses |= dep_use
                    except DependencyException as e:
                        warning("{}. Continuing anyway at user's request", e)

                CLEAN = False
                TR_PATCH = False

                if needs_cleaning and dep_atom:
                    # FIXME: This won't work without a prefix
                    # Ideally, a temporary prefix could be set up
                    merge(
                        dep_atom,
                        oneshot=True,
                        update=True,
                    )
                    if clean_plugin(esp_path):
                        CLEAN = True
                        if "CleanPlugin" not in package.classes:
                            package.classes.insert(0, "CleanPlugin")
                        package.imports["common.util"].add("CleanPlugin")
                        build_deps.add(dep_atom)

                if "TR_Data.esm" in get_masters(esp_path):
                    TR_PATCH = True
                    package.imports["common.util"].add("TRPatcher")
                    if "TRPatcher" not in package.classes:
                        package.classes.insert(0, "TRPatcher")
                    print(f"TR Patching file {esp}")
                    tr_patcher(esp_path)

                plugin = File(esp)
                if CLEAN:
                    plugin.CLEAN = True

                if TR_PATCH:
                    plugin.TR_PATCH = True

                if dep_atom is not None and dep_use is not None:
                    plugin.comment = (
                        "# Deps: " + " ".join(sorted(dep_atom | dep_use)) + ""
                    )
                PLUGINS.append(plugin)

            if PLUGINS:
                directory.PLUGINS = PLUGINS

            if texture_size:
                directory.comment = f"# Texture Size: {texture_size}"
            else:
                directory.comment = ""

            if oldpkg:
                directory.comment += "\n# FIXME: New Directory. Please check"

            if len(package.sources) > 1:
                directory.S = source_name

            INSTALL_DIRS.append(directory)

    if "base/morrowind" in dep_atoms and dep_uses:
        dep_atoms.remove("base/morrowind")
        dep_atoms.add("base/morrowind[" + ",".join(sorted(dep_uses)) + "]")

    deps = " ".join(sorted(dep_atoms))

    for source in package.sources:
        # Clean up files
        path = os.path.join(env.TMP_DIR, source.name)
        print(f"Cleaning up {path}")
        shutil.rmtree(path)

    if TEXTURE_SIZES:
        package.other_fields["TEXTURE_SIZES"] = (
            '"' + " ".join(map(str, sorted(TEXTURE_SIZES))) + '"'
        )

    def get_header_start_year(line: str):
        match = re.search(r"Copyright (\d{4})", line)
        if match:
            return match.group(0)

    def is_end_year_correct(line: str, year: int):
        return re.search(r"Copyright \d{4}-" + str(year), line)

    year = datetime.datetime.now().year
    if not pybuild or not is_end_year_correct(str(pybuild[0]), year):
        # Looks like an old copyright statement, but is not correct
        if pybuild and str(pybuild[0]).startswith("# Copyright"):
            pybuild[0:2] = get_header_string(
                year, get_header_start_year(str(pybuild[0]))
            )
        else:
            for line in reversed(get_header_string(year)):
                pybuild.insert(0, line)

    # Import statements
    imports = {}
    for i in pybuild.find("FromImportNode") or []:
        imports[".".join([str(x) for x in i.value])] = i.parent

    if INSTALL_DIRS:
        package.imports["common.mw"].add("InstallDir")
    if any(
        list(
            getattr(d, attr)
            for attr in ["PLUGINS", "ARCHIVES", "GROUNDCOVER"]
            if hasattr(d, attr)
        )
        for d in INSTALL_DIRS
    ):
        package.imports["common.mw"].add("File")

    if imports:
        # Update imports if any imports are missing
        if "portmod.pybuild" in imports:
            imports["portmod.pybuild"].value = "pybuild"
            imports["pybuild"] = imports["portmod.pybuild"]

        for imp in package.imports:
            if imp in imports:
                for other_import in imports[imp]:
                    if not imports[imp].targets.find("name", other_import):
                        imports[imp].targets.append(other_import)
            else:
                if package.imports[imp]:
                    pybuild.insert(
                        3, f'from {imp} import {", ".join(package.imports[imp])}'
                    )
    else:
        index = 3
        for import_name in package.imports:
            if package.imports[import_name]:
                pybuild.insert(
                    index,
                    f'from {import_name} import {", ".join(package.imports[import_name])}',
                )
                index += 1

    Mod = pybuild.find("class", "Package")

    values = {
        "NAME": f'"{package.name}"',
        "DESC": f'"{package.desc}"',
        "HOMEPAGE": f'"{package.homepage}"',
        "LICENSE": f'"{package.license}"',
        "KEYWORDS": '"TODO: test and then FILLME"',
    }

    if deps:
        values["RDEPEND"] = f'"{deps}"'
    if build_deps:
        values["DEPEND"] = '"' + " ".join(sorted(build_deps)) + '"'

    for field in package.other_fields:
        values[field] = package.other_fields[field]
    if package.required_use:
        values["REQUIRED_USE"] = f'"{" ".join(package.required_use)}"'

    if Mod:
        # Add missing superclasses
        for superclass in package.classes:
            if not Mod.inherit_from.find("name", superclass):
                Mod.inherit_from.insert(0, superclass)

        # Make sure keywords are cleared
        # if they already exist in the previous version
        # This is a generated package, and is untested
        clear_keywords(pybuild)

        if "NEXUS_SRC_URI" in package.other_fields:
            if Mod.find("name", "NEXUS_SRC_URI"):
                oldvalue = str(Mod.find("name", "NEXUS_SRC_URI").parent.value)
                for source in package.sources:
                    if source.name not in oldvalue:
                        Mod.find(
                            "name", "NEXUS_SRC_URI"
                        ).parent.value = f'{package.other_fields["NEXUS_SRC_URI"]}'
                        break
            else:
                print("Removing SRC_URI and NEXUS_URL")

                def remove_field(name):
                    node = Mod.find("name", name).parent
                    del node.parent[node.index_on_parent]

                remove_field("SRC_URI")
                remove_field("NEXUS_URL")
                Mod.append(f'NEXUS_SRC_URI={package.other_fields["NEXUS_SRC_URI"]}')
        else:
            # Update SRC_URI unless there are no missing files
            if Mod.find("name", "SRC_URI"):
                old_value = Mod.find("name", "SRC_URI").parent.value

                # Keep old SRC_URI if the old value included substitutions
                # Since it's probably set up to be version independent
                if not re.search("{.*}", str(old_value)) and package.src_uri:
                    for filename in package.src_uri.split():
                        if filename not in str(old_value):
                            Mod.find(
                                "name", "SRC_URI"
                            ).parent.value = f'"{package.src_uri}"'
                            break
            else:
                Mod.append(f'SRC_URI="{package.src_uri}"')

        # Update S if present
        if Mod.find("name", "S", recursive=False) and len(package.sources) == 1:
            source_name, _ = os.path.splitext(package.sources[0].name)
            if source_name.endswith(".tar"):
                source_name, _ = os.path.splitext(source_name)
            Mod.find("name", "S", recursive=False).parent.value = f'"{source_name}"'

        # Add missing variables to mod
        for key in values:
            if not Mod.find("name", key):
                Mod.append(f"{key}={values[key]}")
    else:
        valuestr = "\n    ".join([f"{key}={value}" for key, value in values.items()])
        pybuild.append(
            f'class Package({", ".join(reversed(package.classes))}):\n    {valuestr}'
        )
        Mod = pybuild.find("class", "Package")
        if package.src_uri:
            Mod.append(f'SRC_URI="{package.src_uri}"')

    INSTALL_DIRS = sorted(INSTALL_DIRS, key=lambda x: (getattr(x, "S", None), x.PATH))
    if Mod.find("name", "INSTALL_DIRS"):
        dirs = [
            node
            for node in Mod.find("name", "INSTALL_DIRS").parent.value
            if isinstance(node, AtomtrailersNode)
            and node.value[0].value == "InstallDir"
        ]

        # Simplest case. If there is only one install directory,
        # assume it is the same one, and update its values
        if len(dirs) == 1 and len(INSTALL_DIRS) == 1:
            # Second element is a callnode containing the arguments we care about
            update_idir(dirs[0], INSTALL_DIRS[0])
        else:
            pending_dirs = {
                os.path.join(d.S, d.PATH): d
                for d in INSTALL_DIRS
                if getattr(d, "S", None)
            }
            pending_dirs.update(
                {d.PATH: d for d in INSTALL_DIRS if getattr(d, "S", None) is None}
            )
            for node in dirs:
                if isinstance(node, AtomtrailersNode):
                    # Install dirs are identified uniquely by their source and first
                    # argument
                    idir = node.value[1]
                    path = idir.value[0]
                    S = idir.find("name", "S")
                    if S:
                        entirepath = os.path.join(
                            str(S.parent.value).strip('"'), str(path.value).strip('"')
                        )
                    else:
                        entirepath = str(path.value).strip('"')

                    # Try to find dir in INSTALL_DIRS for new mod that matches.
                    # This is hard because S has probably changed
                    # If S is not specified, it is easier, but the PATH may have changed
                    # We could attempt to match based on other fields, but the simplest
                    # and most reliable way is to throw out old code
                    # and create a new InstallDir
                    if entirepath in pending_dirs:
                        update_idir(node, pending_dirs[entirepath])
                        del pending_dirs[entirepath]
                    else:
                        # If none exists, we remove this node
                        dirs.remove(node)

            # Add missing new directories
            dirlist = Mod.find("name", "INSTALL_DIRS").parent.value
            for new_dir in pending_dirs.values():
                if new_dir.comment:
                    dirlist.node_list.append(RedBaron(new_dir.comment))
                    dirlist.node_list.append(RedBaron("\n"))

                del new_dir.comment
                dirlist.value.append(RedBaron(str(new_dir)))

    else:
        if INSTALL_DIRS:

            def format_installdir(idir):
                comment = idir.comment
                del idir.comment
                if comment:
                    result = f"# {comment}" + "\n" + f"{idir}"
                else:
                    result = f"{idir}"
                return result

            Mod.append(
                "INSTALL_DIRS = [\n"
                + ",\n".join(format_installdir(d) for d in INSTALL_DIRS)
                + "\n]"
            )

    build_file: str = pybuild.dumps()

    print(build_file)

    print("Sorting imports...")
    build_file = isort.code(build_file)
    print("Formatting code...")
    build_file = black.format_str(build_file, mode=black.FileMode())
    return build_file


def create_metadata(
    path: str,
    authors: Iterable[str] = (),
    longdescription: Optional[str] = None,
    bugs_to: Optional[str] = None,
    doc: Optional[str] = None,
    maintainer: Optional[str] = None,
):
    yaml = YAML(typ="rt")  # default, if not specfied, is 'rt' (round-trip)
    if os.path.exists(path):
        with open(path) as file:
            metadata = yaml.load(file) or yaml.map()
    else:
        metadata = yaml.map()

    if longdescription:
        metadata["longdescription"] = longdescription
    if maintainer:
        metadata["maintainer"] = maintainer

    if (authors or bugs_to or doc) and not metadata.get("upstream"):
        metadata["upstream"] = {}
    if authors and not metadata["upstream"].get("maintainer"):
        metadata["upstream"]["maintainer"] = authors
    if bugs_to:
        metadata["upstream"]["bugs-to"] = bugs_to
    if doc:
        metadata["upstream"]["doc"] = doc

    with open(path, "w") as file:
        yaml.dump(metadata, file)


def update_files_in_repo(repo: str):
    """
    Yields objects which can be used to modify all packages in the repository

    The objects have the same attributes as a Pybuild, but are actually a special
    wrapper class which tracks changed attributes.
    If changes are made to the object, the file will be overwritten with the changes.
    Ensure that any field values produce valid python with ``repr``.
    """
    get_repo_root(repo)
    for pkg in load_all(only_repo_root=repo):
        with update_package(pkg) as pkg:
            yield pkg


@contextmanager
def update_package(pkg: Pybuild):
    """
    A contextmanager for updating values in a package.

    Will overwrite pkg.FILE with any changes made.
    """

    class Wrapper(SimpleNamespace):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                super().__setattr__(key, value)
            super().__setattr__("_values", {})

        def __setattr__(self, key, value):
            self._values[key] = value
            super().__setattr__(key, value)

    updates = Wrapper(**pkg.__dict__)
    try:
        yield updates
    finally:
        # Code to release resource, e.g.:
        with open(pkg.FILE, "r", encoding="utf-8") as pybuild_file:
            pybuild = RedBaron(pybuild_file.read())

        package = pybuild.find("class", "Package")
        for key, value in updates._values.items():
            if not package.find("name", key):
                package.append(f"{key}={value}")
            else:
                package.find("name", key).parent.value = repr(value)

        if updates._values:
            build_file: str = pybuild.dumps()
            build_file = black.format_str(build_file, mode=black.FileMode())
            with open(pkg.FILE, "w", encoding="utf-8") as file:
                print(build_file, file=file, end="")
