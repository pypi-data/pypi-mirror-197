# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with Github"""
import os

from github import Github
from portmodlib.source import Source

from ..atom import parse_version
from . import PackageData, PackageSource


class GithubSource(PackageSource):
    def __init__(self, identifier: str):
        self.id = identifier

    def _get_project(self):
        gh = Github(os.environ.get("GITHUB_ACCESS_TOKEN"))
        return gh.get_repo(self.id)

    def get_newest_release(self):
        repo = self._get_project()
        releases = repo.get_releases()
        if releases and releases.totalCount > 0:
            return releases[0]

    def get_newest_version(self):
        release = self.get_newest_release()
        if release:
            return parse_version(release.tag_name)
        return "0"

    def get_url(self) -> str:
        return f"https://github.com/{self.id}"

    def __hash__(self):
        return hash(self.id)

    def get_pkg_data(self, package: PackageData) -> bool:
        # FIXME: Update
        proj = self._get_project()
        package.name = proj.name
        package.desc = proj.description
        package.homepage = proj.html_url
        package.authors = [user.name for user in proj.get_contributors()]
        package.bugs_to = proj.html_url + "/issues"
        # TODO: detect license from license file
        # package.license = detect_license(proj.get_license())

        release = self.get_newest_release()
        if release:
            src_uri = []
            assets = list(release.get_assets())
            for asset in assets:
                package.sources.append(Source(asset.browser_download_url, asset.name))
                src_uri.extend([asset.browser_download_url, "->", asset.name])

            # If there are no custom assets, just use the zipball with the sources
            if len(assets) == 0:
                url = f"https://github.com/{self.id}/archive/refs/tags/{release.tag_name}.zip"
                assert package.name, "GitHub repos should always have a name..."
                asset_name = package.name + "-" + release.tag_name + ".zip"
                package.sources.append(Source(url, asset_name))
                src_uri.extend([url, "->", asset_name])

            package.src_uri = " ".join(src_uri)

            package.update_atom(version=release.tag_name)
        else:
            # TODO: Fallback to basic gitrepo support
            pass
        return True
