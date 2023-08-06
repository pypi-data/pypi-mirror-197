#!/usr/bin/env python

# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from setuptools import find_packages, setup

setup(
    name="importmod_core",
    author="Portmod Authors",
    description="A tool for integrating upstream mods into Portmod",
    license="GPLv3",
    url="https://gitlab.com/portmod/importmod",
    packages=find_packages(include=["importmod_core"]),
    entry_points=({"console_scripts": ["importmod = importmod_core.main:main"]}),
    install_requires=["tomlkit", "prompt_toolkit"],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.7",
    use_scm_version=True,
)
