import atexit
import os
import subprocess
import sys
import tempfile
from shutil import rmtree
from tempfile import TemporaryDirectory
from typing import Optional

import requests
from bs4 import BeautifulSoup
from portmod.source import Source
from portmodlib.atom import Atom
from pypi_simple import PyPISimple
from virtualenv import cli_run

from importmod.atom import parse_version

from . import PackageData, PackageSource

if sys.version_info >= (3, 8):
    from importlib.metadata import metadata
else:
    from importlib_metadata import metadata

VENV_DIR = None

if sys.platform != "win32":
    tempfile.tempdir = "/var/tmp"


def setup_venv():
    global VENV_DIR
    VENV_DIR = TemporaryDirectory().name
    cli_run([VENV_DIR])
    activate_this_file = os.path.join(VENV_DIR, "bin", "activate_this.py")
    exec(
        compile(open(activate_this_file, "rb").read(), activate_this_file, "exec"),
        dict(__file__=activate_this_file),
    )


def get_python_data(project: str):
    if VENV_DIR is None:
        setup_venv()
        atexit.register(exit_handler)
    subprocess.run(["pip", "install", "--upgrade", project])
    pkg_metadata = metadata(project)
    return pkg_metadata


def exit_handler():
    global VENV_DIR
    if VENV_DIR:
        print(f"Cleaning up virtualenv dir {VENV_DIR}")
        rmtree(VENV_DIR)
        VENV_DIR = None


def get_source_file(project: str, version: Optional[str] = None) -> Source:
    filespage = requests.get(f"https://pypi.org/simple/{project}")
    root = BeautifulSoup(filespage.text)
    for elem in reversed(root.find_all("a")):
        # Ignore wheels
        name, ext = os.path.splitext(elem.text)
        if name.endswith(".tar"):
            name, ext = os.path.splitext(name)
        if ext != ".whl" and (not version or name == f"{project}-{version}"):
            return Source(elem.get("href"), elem.text)


class PyPISource(PackageSource):
    def __init__(self, identifier: str):
        self.id = identifier

    def get_newest_version(self):
        data = get_python_data(self.id)
        return data["Version"]

    def get_url(self) -> str:
        return f"https://pypi.org/project/{self.id}"

    def __hash__(self):
        return hash(self.id)

    def get_pkg_data(self, package: PackageData) -> bool:
        data = get_python_data(self.id)
        package.atom = f"dev-python/{self.id}"
        python_version = data["Version"]
        package.atom = Atom(package.atom + "-" + parse_version(python_version))
        package.name = package.name or data.get("Name")
        package.desc = package.desc or data.get("Summary")
        package.homepage = package.homepage or data.get("Home-page")

        # FIXME: Also include Maintainer
        author = data.get("Author")
        if data.get("Author-email"):
            author += " <" + data.get("Author-email") + ">"
        package.authors.append(author)

        package.other_fields["LICENSE"] = '"' + data.get("License") + '"'
        # Cannot be platform-specific
        # FIXME: Could blindly add this into required_use for now...
        if data.get("Platform", "Any") not in ("UNKNOWN", "Any"):
            raise Exception("Invalid Platform " + data.get("Platform"))
        package.sources = []
        package.category = package.category or "dev-python"

        package.classes = ["Distutils"]
        package.imports["pybuild"].discard("Pybuild1")
        package.imports["common.distutils"].add("Distutils")

        # FIXME: This may not be a valid url
        # pypi-simple could be used to pull the actual file names https://pypi.org/project/pypi-simple/

        with PyPISimple() as client:
            simple_page = client.get_project_page(self.id)

        assert simple_page is not None, f"Python package {self.id} could not be found!"
        for pkg in simple_page.packages:
            # TODO: Support for wheels?
            if pkg.package_type == "sdist":
                package.src_uri = pkg.url + " -> " + pkg.filename
                break

        for keyword in data.get("Requires-Python", []):
            if keyword.startswith(">="):
                if int(keyword[2:]) > 3.6:
                    raise Exception(
                        "Requires-Python had incompatible keyword {keyword}"
                    )
            if keyword.startswith("!="):
                if int(keyword[2:].rstrip(".*")) >= 3.6:
                    raise Exception(
                        "Requires-Python had incompatible keyword {keyword}"
                    )
        return True
