# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import re
from typing import Dict, Iterable, List, Optional
from urllib.parse import parse_qs, urlparse

from portmod.loader import load_all, load_pkg
from portmod.pybuild import Pybuild
from portmodlib.atom import version_gt
from portmodlib.source import Source
from portmodlib.usestr import use_reduce
from ruamel.yaml import YAML

from .sources import PackageSource, Update
from .sources.github import GithubSource
from .sources.gitlab import GitlabSource
from .sources.modhistory import ModhistorySource
from .sources.nexus import NexusSource, get_nexus_updates
from .sources.pypi import PyPISource


def get_pkg_sources(pkg: Pybuild, *, no_implicit: bool) -> List[PackageSource]:
    sources: List[PackageSource] = []
    # FIXME: explicit metadata field for upstream sources
    metadata = _get_metadata(pkg)
    if metadata:
        # E.g. explicit package sources can be specified via
        # updates:
        #   source:
        #     "type": gitlab
        #     server: https://gitlab.com
        #     id: portmod/importmod
        source = metadata.get("updates", {}).get("source")
        if source:
            typ = source.get("type")
            if typ == "nexusmods":
                assert "game" in source, "nexus sources must contain the game id"
                assert "modid" in source, "nexus sources must contain the mod id"
                # files: List[str] - Refers to the file "names", which are version-independent
                return [
                    NexusSource(
                        source["game"], source["modid"], files=source.get("files", ())
                    )
                ]
            if typ == "github":
                assert "id" in source, "Github sources must contain the project path"
                return [GithubSource(source["id"])]
            if typ == "gitlab":
                assert "server" in source, "Gitlab sources must contain the server"
                assert "id" in source, "Gitlab sources must contain the project path"
                return [GitlabSource(source["server"], source["id"])]
            if typ == "pypi":
                assert "id" in source, "Pypi sources must contain the project name"
                return [PyPISource(source["id"])]

    if no_implicit:
        return []

    if hasattr(pkg, "NEXUS_URL") or hasattr(pkg, "NEXUS_SRC_URI"):
        if hasattr(pkg, "NEXUS_URL"):
            for url in use_reduce(pkg.NEXUS_URL, matchall=True, flat=True):
                source = guess_package_source(url)
                if source:
                    sources.append(source)
        if hasattr(pkg, "NEXUS_SRC_URI"):
            for url in use_reduce(
                pkg.NEXUS_SRC_URI,
                is_src_uri=True,
                token_class=Source,
                matchall=True,
                flat=True,
            ):
                parsed = urlparse(url)
                # Ignore arrows and filenames
                if parsed.scheme:
                    source = guess_package_source(url)
                    if source:
                        sources.append(source)
    else:
        urls = use_reduce(pkg.HOMEPAGE, matchall=True, flat=True)
        for url in urls:
            source = guess_package_source(url)
            if source:
                sources.append(source)

    return sources


def guess_package_source(url: str) -> Optional[PackageSource]:
    hostname = urlparse(url).hostname
    if not hostname:
        return None
    if re.match(r"^\w*\.?nexusmods.com$", hostname):
        parsed = urlparse(url)
        queries = parse_qs(parsed.query)
        game, modid = parsed.path.split("/mods/")
        file_id = None
        if "file_id" in queries:
            file_id = int(queries.get("file_id", [])[0])
        return NexusSource(game.lstrip("/"), int(modid), filenum=file_id)
    if re.match("^mw.modhistory.com$", hostname):
        modid = urlparse(url).path.split("-")[-1]
        return ModhistorySource(int(modid))
    if re.match(r"^\w*\.?github.com$", hostname):
        basepath = "/".join(urlparse(url).path.lstrip("/").split("/")[:2])
        return GithubSource(basepath)
    if re.match(r"^\w*\.?gitlab.com$", hostname):
        parsed = urlparse(url)
        basepath = "/".join(parsed.path.lstrip("/").split("/")[:2])
        return GitlabSource(f"{parsed.scheme}://{parsed.netloc}", basepath)
    return None


def get_nexus_id_map(
    repository: Optional[str], *, no_implicit: bool
) -> Dict[NexusSource, Pybuild]:
    """
    Returns a dictionary mapping NexusMod game,id to mod for all NexusMods in database
    """
    id_map: Dict[NexusSource, Pybuild] = {}
    for mod in load_all(only_repo_root=repository):
        ids = get_pkg_sources(mod, no_implicit=no_implicit)
        for modid in ids:
            if isinstance(modid, NexusSource):
                if modid in id_map:
                    if version_gt(mod.PV, id_map[modid].PV):
                        id_map[modid] = mod
                else:
                    id_map[modid] = mod
    return id_map


def _get_metadata(pkg: Pybuild):
    """
    Note: Importmod-specific metadata includes:

        update:
            ignore: bool # if true, importmod will not check this package for updates
            copy: bool # if true, importmod will check for updates and will use the previous version of the package verbatim
    """
    metadata_path = os.path.join(os.path.dirname(pkg.FILE), "metadata.yaml")
    if os.path.exists(metadata_path):
        yaml = YAML()
        with open(metadata_path) as file:
            return yaml.load(file)
    return None


def should_skip(pkg: Pybuild, no_implicit: bool) -> bool:
    metadata = _get_metadata(pkg)
    if metadata:
        if metadata.get("updates", {}).get("ignore"):
            return True
        if metadata.get("updates", {}).get("source"):
            return False
    return no_implicit


def should_copy(pkg: Pybuild) -> bool:
    metadata = _get_metadata(pkg)
    if metadata:
        return bool(metadata.get("updates", {}).get("copy"))
    return False


def get_newest(pkg_versions: Iterable[Pybuild]) -> Optional[Pybuild]:
    """Custom version of get_newest which filters out live packages"""
    from portmod.util import get_newest

    # Ignore live packages
    pkg_versions = list(filter(lambda p: "live" not in p.PROPERTIES, pkg_versions))
    # If there is only a live package, ignore this package entirely
    if not pkg_versions:
        return None
    return get_newest(pkg_versions)


def get_updates(
    *,
    period: Optional[str] = None,
    repository: Optional[str] = None,
    no_implicit: bool = False,
):
    """
    Returns a list of updates since the given time

    args:
        period: one of 1d, 1w, 1m
        repository: The path to the repository to process
                    only packages within this repository will be used
    """
    results: List[Update] = []
    if period:
        id_map = get_nexus_id_map(repository, no_implicit=no_implicit)
        games = set(source.game for source in id_map)

        for game in games:
            results.extend(get_nexus_updates(game, period, id_map))
    else:
        pkgs = set()
        for pkg in load_all(only_repo_root=repository):
            newest = get_newest(load_pkg(pkg.CPN))
            if newest:
                pkgs.add(newest)
        for pkg in pkgs:
            if not should_skip(pkg, no_implicit):
                print(f"Checking {pkg} for updates...")
                results += check_for_update(pkg, no_implicit=no_implicit)
    return results


def check_for_update(mod: Pybuild, *, no_implicit: bool) -> List[Update]:
    updates = []

    for source in get_pkg_sources(mod, no_implicit=no_implicit):
        url = source.get_url()
        try:
            update = source.get_update(mod)
            if update:
                updates.append(update)
        except Exception as e:
            print(f"Unable to check {url}")
            print(e)
            updates.append(Update(oldatom=mod.ATOM, location=url))

    return updates
