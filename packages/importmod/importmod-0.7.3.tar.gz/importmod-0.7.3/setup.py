#!/usr/bin/env python

# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from setuptools import find_packages, setup

setup(
    name="importmod",
    author="Portmod Authors",
    description="A CLI tool to import mods into the Portmod repository format",
    license="GPLv3",
    url="https://gitlab.com/portmod/importmod",
    packages=find_packages(include=["importmod", "importmod.*", "importmod_core"]),
    entry_points=({"console_scripts": ["importmod = importmod_core.main:main"]}),
    install_requires=[
        "portmod>=2.4",
        "gitpython",
        "requests",
        "redbaron",
        "isort>=5.0.0",
        "black",
        "beautifulsoup4",
        "pygithub",
        "python-gitlab",
        "ruamel.yaml",
        "pypi-simple",
        "virtualenv",
        "tomlkit",
        "prompt_toolkit",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.7",
    use_scm_version=True,
)
