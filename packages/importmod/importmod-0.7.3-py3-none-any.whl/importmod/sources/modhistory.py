# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with mw.modhistory.com"""

import requests
from bs4 import BeautifulSoup
from portmodlib.source import Source

from ..atom import parse_version
from . import PackageData, PackageSource


class ModhistorySource(PackageSource):
    def __init__(self, idnum: int):
        self.id = idnum

    def get_url(self) -> str:
        return f"http://mw.modhistory.com/download--{self.id}"

    def get_newest_version(self) -> str:
        info = get_modhistory_info(self.get_url())
        return parse_version(info["Version"])

    def __hash__(self):
        return hash(self.id)

    def get_pkg_data(self, package: PackageData):
        package.homepage = self.get_url()
        package.sources = [
            Source(f"http://mw.modhistory.com/file.php?id={self.id}", package.atom.P)
        ]
        package.src_uri = (
            f"http://mw.modhistory.com/file.php?id={self.id} -> {package.atom.P}"
        )
        info = get_modhistory_info(self.get_url())

        package.name = info["title"]
        package.authors.append(info["author"])
        package.update_atom(version=info["Version"])
        return package


def get_modhistory_info(url):
    """
    Returns information in the hompage for the given modhistory mod

    Generally contains the following fields:
    Version, Added, Last Edited, File Size, Downloads, Requires, Submitted by
    """
    rinfo = requests.get(url)
    if rinfo.status_code != requests.codes.ok:  # pylint: disable=no-member
        rinfo.raise_for_status()

    soup = BeautifulSoup(rinfo.text)
    data = {}
    for elem in soup.find_all("td"):
        info = elem.find_all("span")
        if info and len(info) >= 2:
            title = info[0].string.rstrip(":")
            value = info[1].string
            data[title] = value
    for author_elem in soup.find_all("p", class_="author"):
        data["author"] = author_elem.text

    for title in soup.find_all("h2", class_="cattitle"):
        data["title"] = title.string
    return data
