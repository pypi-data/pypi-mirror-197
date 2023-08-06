# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import dataclasses
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, DefaultDict, Dict, List, Optional, Set

from portmod.pybuild import Pybuild
from portmod.util import get_max_version
from portmodlib.atom import Atom
from portmodlib.colour import bright
from portmodlib.source import Source

from ..atom import parse_name, parse_version

"""Upstream mod repositories"""


class Update:
    def __init__(
        self,
        *,
        oldatom: Atom,
        location: str,
        newatom: Optional[Atom] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.oldatom = oldatom
        self.newatom = newatom
        self.location = location
        self.available = newatom is not None

        if not title and not description:
            if newatom is not None:
                self.title = f"[{oldatom.CPN}] Version {newatom.PV} is available"
                self.description = (
                    f"Old Version: {oldatom}\\\n"
                    f"New Version: {oldatom.CPN}-{newatom.PVR}\n\n"
                    f"New version can be found here: {location}\n\n"
                    "*Note: this is an automatically generated message. "
                    "Please report any issues [here]"
                    "(https://gitlab.com/portmod/importmod/issues)*"
                )
            else:
                self.title = (
                    f"[{oldatom.CPN}] Mod is no longer available from current source"
                )
                self.description = (
                    f"Attempt to check mod availability from: {location} failed.\n\n"
                    "*Note: this is an automatically generated message. "
                    "Please report any issues [here]"
                    "(https://gitlab.com/portmod/importmod/issues)*"
                )
        else:
            assert title
            assert description
            self.title = title
            self.description = description


@dataclass
class PackageData:
    atom: Atom
    homepage: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    desc: Optional[str] = None
    src_uri: Optional[str] = None
    license: Optional[str] = None
    sources: List[Source] = dataclasses.field(default_factory=list)
    required_use: List[str] = dataclasses.field(default_factory=list)
    classes: List[str] = dataclasses.field(default_factory=list)
    imports: DefaultDict[str, Set[str]] = dataclasses.field(
        default_factory=lambda: defaultdict(set)
    )
    other_fields: Dict[str, Any] = dataclasses.field(default_factory=dict)
    manual_download_url: Optional[str] = None

    authors: List[str] = dataclasses.field(default_factory=list)
    bugs_to: Optional[str] = None
    doc: Optional[str] = None

    def update_atom(self, version: str):
        if not self.atom and self.category and self.name:
            self.atom = Atom(self.category + "/" + parse_name(self.name))
        elif self.atom and not self.atom.PV:
            self.atom = Atom(self.atom + "-" + parse_version(version))

    def pretty_print(self):
        for attr in dir(self):
            if not attr.startswith("_"):
                value = getattr(self, attr)
                if value:
                    if isinstance(value, str):
                        print(bright(f"{attr.title()}:"), value)
                    elif isinstance(value, list) and all(
                        isinstance(elem, str) for elem in value
                    ):
                        print(bright(f"{attr.title()}:"), ", ".join(value))


class PackageSource(ABC):
    @abstractmethod
    def get_newest_version(self) -> str:
        """Returns the newest release version for this source"""

    @abstractmethod
    def get_url(self) -> str:
        """Returns the URL associated with this source"""

    @abstractmethod
    def get_pkg_data(self, package: PackageData) -> bool:
        """Returns data for use in packages"""

    def get_update(self, pkg: Pybuild) -> Optional[Update]:
        newest = self.get_newest_version()
        if newest != pkg.PV and get_max_version([newest, pkg.PV]) == newest:
            print(f"Found update for {pkg}. New version: {newest}")
            return Update(
                oldatom=pkg.ATOM,
                newatom=Atom(f"{pkg.CPN}-{newest}"),
                location=self.get_url(),
            )

        return None

    def validate_downloads(self, files: List[Source]):
        pass
