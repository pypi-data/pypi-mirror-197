# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with nexusmods.com"""

import json
import os
import urllib.parse
from collections import namedtuple
from datetime import datetime
from logging import error, warning
from typing import Iterable, List, Optional, Tuple

import requests
from portmod.download import get_download
from portmod.prompt import prompt_num_multi
from portmod.pybuild import Pybuild
from portmod.util import get_max_version
from portmodlib.atom import Atom, version_gt
from portmodlib.fs import get_hash
from portmodlib.source import HashAlg, Source

from ..atom import parse_name, parse_version
from ..config import NEXUS_KEY
from . import PackageData, PackageSource, Update

NexusData = namedtuple(
    "NexusData",
    [
        "atom",
        "modid",
        "name",
        "desc",
        "files",
        "homepage",
        "author",
        "nudity",
        "file_updates",
    ],
)


class APILimitExceeded(Exception):
    """Exception indicating that the NexusApi's daily limit has been exceeded"""


API_LIMIT_EXCEEDED = False


class NexusSource(PackageSource):
    def __init__(
        self,
        game: str,
        idnum: int,
        *,
        filenum: Optional[int] = None,
        files: Iterable[str] = (),
    ):
        self.game = game
        self.idnum = idnum
        self.filenum = filenum
        # The "name" field in the data returned by the nexus API
        # can be used to identify the different versions of a single file.
        # This is the name shown on the files tab prior to the download page
        # If this list is nonempty, it will be used to filter the files
        self.files = list(files)

    def get_newest_version(self) -> str:
        nexus_info = get_nexus_info(self.game, self.idnum, self.filenum)
        return parse_version(nexus_info.atom.PV)

    def get_url(self) -> str:
        return f"https://www.nexusmods.com/{self.game}/mods/{self.idnum}"

    def __hash__(self):
        return hash((self.game, self.idnum))

    def get_update(self, pkg: Pybuild) -> Optional[Update]:
        nexus_info = get_nexus_info(self.game, self.idnum)
        newest = parse_version(nexus_info.atom.PV)
        if version_gt(newest, pkg.PV):
            print(f"Found update for {pkg}. New version: {newest}")
            return Update(
                oldatom=pkg.ATOM,
                newatom=Atom(f"{pkg.CPN}-{newest}"),
                location=self.get_url(),
            )
        # TODO: if filenum is set, only check if that file has been replaced

        manifest = pkg.get_manifest()
        for update in nexus_info.file_updates:
            old_file_name = update["old_file_name"]
            new_file_name = update["new_file_name"]
            time = datetime.fromisoformat(update["uploaded_time"])
            if manifest.get(old_file_name.replace(" ", "_")):
                # Ignore file changes older than the package file
                if os.path.getmtime(pkg.FILE) < time.timestamp():
                    return Update(
                        oldatom=pkg.ATOM,
                        title=f"[{pkg.CPN}] File has been changed without a version bump",
                        description=f"File {old_file_name} was replaced by {new_file_name} on {time}",
                        location=self.get_url(),
                    )

        return None

    def get_pkg_data(self, package: PackageData) -> bool:
        # Get Nexus API data, but if we've exceeded out limit,
        # just print an error and return
        global API_LIMIT_EXCEEDED
        if API_LIMIT_EXCEEDED:
            return False
        else:
            try:
                nexus_data = get_nexus_info(
                    self.game, self.idnum, self.filenum, self.files
                )
            except APILimitExceeded:
                error("Nexus API limit has been exceeded. Try again tomorrow")
                API_LIMIT_EXCEEDED = True
                return False

        if nexus_data is None:
            return False

        package.homepage = package.homepage or nexus_data.homepage
        package.atom = package.atom or nexus_data.atom
        package.name = package.name or nexus_data.name

        package.update_atom(version=nexus_data.atom.PV)
        package.desc = package.desc or nexus_data.desc

        if self.filenum:
            data = list(nexus_data.files.values())[0]
            package.manual_download_url = f'https://nexusmods.com/{self.game}/mods/{self.idnum}?tab=files&file_id={data["file_id"]}'
        else:
            package.manual_download_url = f"{nexus_data.homepage}?tab=files"
        package.src_uri = None
        package.sources = [Source(file, file) for file in nexus_data.files]
        package.other_fields["NEXUS_SRC_URI"] = (
            '"'
            + " ".join(
                [
                    f'https://nexusmods.com/{self.game}/mods/{self.idnum}?tab=files&file_id={data["file_id"]} -> {name}'
                    for name, data in nexus_data.files.items()
                ]
            )
            + '"'
        )
        if nexus_data.nudity:
            package.required_use.append("nudity")
        package.authors.append(nexus_data.author)
        package.classes.append("NexusMod")
        package.imports["common.nexus"].add("NexusMod")
        return True

    def validate_downloads(self, files: List[Source]):
        for file in files:
            path = get_download(file)
            if path is None:
                raise FileNotFoundError(f"The file {file} is missing!")
            if not validate_file(
                self.game, self.idnum, path, get_hash(path, (HashAlg.MD5,))[0]
            ):
                raise Exception(f"File {file} has invalid hash!")


def parse_nexus_url(url: str) -> Tuple[str, int]:
    parsed = urllib.parse.urlparse(url)
    game = parsed.path.split("/")[1]
    mod_id = int(parsed.path.split("/")[3])
    return game, mod_id


NEXUS_KEY_MESSAGE = "Setting NEXUS_KEY in importmod.cfg (section [importmod]) is \
    required for querying the NexusMods API"


def get_nexus_info(
    game: str,
    modid: int,
    filenum: Optional[int] = None,
    file_names: Optional[List[str]] = None,
) -> NexusData:
    """
    Fetches mod information from nexusmods.com and parses it into a NexusData object
    """
    info_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/"
    files_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/files/"

    assert NEXUS_KEY, NEXUS_KEY_MESSAGE
    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    rinfo = requests.get(info_url, headers=headers)
    if rinfo.headers.get("X-RL-Daily-Remaining") == 0:
        raise APILimitExceeded()

    rfiles = requests.get(files_url, headers=headers)

    if (
        rinfo.status_code
        == rfiles.status_code
        == requests.codes.ok  # pylint: disable=no-member
    ):
        info = json.loads(rinfo.text)
        files = json.loads(rfiles.text)
    else:
        rinfo.raise_for_status()
        rfiles.raise_for_status()

    version = parse_version(info["version"]) or "0.1"

    # Select all files except those in the OLD_VERSION category
    tmpfiles = [
        file
        for file in files["files"]
        if file["category_name"] not in ("OLD_VERSION", "ARCHIVED")
        and file["category_name"]
    ]

    file_names = list(file_names or [])
    if filenum:
        # Filter tempfiles by the displayed name of the target file
        found = False
        for file in files["files"]:
            if file["file_id"] == filenum:
                file_names.append(file["name"])
        if not found:
            warning(
                f"Nexus mod with id {game}/{modid} was tracking "
                f"the file with id {filenum}, which can no longer be found"
            )
    elif os.environ.get("INTERACTIVE") and len(tmpfiles) > 1:
        for index, file in enumerate(tmpfiles):
            print(str(index) + ")", file["name"])
            print(
                "  ", "Version:", file["version"], "Size:", str(file["size_kb"]) + "kB"
            )
            print("  ", "Filename:", file["file_name"])
            print("  ", "Desc:", file["description"])
        file_indices = prompt_num_multi(
            f"Which files would you like to import?{os.linesep}"
            "Enter One or more numbers or ranges, separated by commas (E.g. 0,1,2-10)",
            len(tmpfiles),
        )
        tmpfiles = [
            file for index, file in enumerate(tmpfiles) if index in file_indices
        ]

    if file_names:
        tmpfiles = [file for file in tmpfiles if file["name"] in file_names]

    allversions = [version]
    for file in tmpfiles:
        tmp_ver = parse_version(file["version"])
        if tmp_ver:
            allversions.append(tmp_ver)

    # Mod author may not have updated the mod version.
    # Version used should be the newest file version among the files we selected
    version = get_max_version(allversions)

    atom = Atom(parse_name(info["name"]) + "-" + version)

    files_list = []
    for file in tmpfiles:
        skip = False

        # Ignore exe files. We can't use them anyway
        _, ext = os.path.splitext(file["file_name"])
        if ext == ".exe":
            skip = True

        if not skip:
            files_list.append(file)

    return NexusData(
        atom=Atom(atom),
        modid=modid,
        name=info["name"],
        desc=info["summary"].replace("\\", ""),
        files={file["file_name"].replace(" ", "_"): file for file in files_list},
        homepage=f"https://www.nexusmods.com/{game}/mods/{modid}",
        author=info["author"],
        nudity=info["contains_adult_content"],
        file_updates=files["file_updates"],
    )


def validate_file(game, mod_id, file, hash):
    hash_url = f"https://api.nexusmods.com/v1/games/{game}/mods/md5_search/{hash}.json"

    assert NEXUS_KEY, NEXUS_KEY_MESSAGE
    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    response = requests.get(hash_url, headers=headers)

    if response.status_code == requests.codes.not_found:  # pylint: disable=no-member
        return False

    mods = json.loads(response.text)
    for mod in mods:
        if mod["mod"]["mod_id"] == mod_id:
            return True

    modnames = [mod.get("mod").get("name") for mod in mods]
    if all(mod.get("mod").get("status") == "hidden" for mod in mods):
        warning("Hidden mods matched the file!")
        return True
    Exception(f"Invalid response {modnames} from NexusMods API when hashing {file}")


def get_nexus_updates(game: str, period: str, mod_map) -> List[Update]:
    """
    Returns a list of updates to nexusmods.com mods in the given period

    Valid periods are 1d, 1w, 1m
    """
    assert period in ["1d", "1w", "1m"]
    update_url = (
        f"https://api.nexusmods.com/v1/games/{game}/mods/updated.json?period={period}"
    )

    assert NEXUS_KEY, NEXUS_KEY_MESSAGE
    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    uinfo = requests.get(update_url, headers=headers)
    if uinfo.headers["X-RL-Daily-Remaining"] == 0:
        raise APILimitExceeded()

    if uinfo.status_code == requests.codes.ok:  # pylint: disable=no-member
        info = json.loads(uinfo.text)
    else:
        uinfo.raise_for_status()

    updates = []
    for mod in info:
        source = NexusSource(game, mod["mod_id"])
        if source in mod_map:
            update = source.get_update(mod_map[source])
            if update:
                updates.append(update)
    return updates
