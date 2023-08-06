# Copyright 2023 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re


def parse_name(name_str: str) -> str:
    lowered = name_str.lower().replace(" - ", "-").replace(" ", "-").replace("_", "-")
    stripped = re.sub(r"[^\w\/-]+", "", re.sub(r"-+", "-", lowered))
    nonumbers = re.sub(r"[0-9_-]*$", "", stripped)
    return nonumbers
