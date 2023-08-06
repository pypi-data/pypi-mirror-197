# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with Github"""

import os

from gitlab import Gitlab
from portmodlib.source import Source

from ..atom import parse_version
from . import PackageData, PackageSource


class GitlabSource(PackageSource):
    def __init__(self, server: str, identifier: str):
        self.server = server
        self.id = identifier

    def _get_project(self):
        gl = Gitlab(self.server)
        return gl.projects.get(self.id)

    def get_newest_release(self):
        releases = self._get_project().releases.list(get_all=False)
        if releases:
            return releases[0]

    def get_newest_version(self):
        release = self.get_newest_release()
        if release:
            return parse_version(release.tag_name)

        return "0"

    def get_url(self) -> str:
        return f"{self.server}/{self.id}"

    def __hash__(self):
        return hash((self.server, self.id))

    def get_pkg_data(self, package: PackageData) -> bool:
        proj = self._get_project()
        package.name = proj.name
        package.desc = proj.description
        package.homepage = proj.web_url
        package.authors = [user["name"] for user in proj.repository_contributors()]
        package.bugs_to = proj.web_url + "/-/issues"

        release = self.get_newest_release()
        if release:
            src_uri = []
            for asset in release.assets["sources"]:
                if asset["format"] == "zip":
                    package.sources.append(
                        Source(asset["url"], os.path.basename(asset["url"]))
                    )
                    src_uri.extend([asset["url"], "->", os.path.basename(asset["url"])])
            package.src_uri = " ".join(src_uri)

            package.update_atom(version=release.tag_name)
        else:
            # TODO: Fallback to basic gitrepo support
            pass
        return True
