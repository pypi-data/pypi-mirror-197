# Copyright 2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import List


class Game:
    plugin_extensions: List[str]
    archive_extensions: List[str]
    datadir_contents: List[str]


class Morrowind(Game):
    plugin_extensions = ["esm", "esp", "omwaddon", "omwgame"]
    archive_extensions = ["bsa"]
    datadir_contents = [
        "distantland",
        "fonts",
        "icons",
        "menus",
        "meshes",
        "bookart",
        "sound",
        "splash",
        "textures",
        "music",
        "video",
    ]
