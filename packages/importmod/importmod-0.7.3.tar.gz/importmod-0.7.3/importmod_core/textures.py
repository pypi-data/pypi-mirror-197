# Copyright 2023 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Tuple


class NotDDSException(Exception):
    """Exception indicating that the given file was not a DDS file"""


def get_texture_size(path: str) -> Tuple[int, int]:
    """Determines the texture size of the given dds file"""
    with open(path, mode="rb") as file:
        buffer = file.read(24)
        if buffer[0:4] != bytes([0x44, 0x44, 0x53, 0x20]):
            raise NotDDSException(f"{path} is not a DDS file!")
        height = buffer[12:16]
        width = buffer[16:20]
    return int.from_bytes(height, "little"), int.from_bytes(width, "little")
