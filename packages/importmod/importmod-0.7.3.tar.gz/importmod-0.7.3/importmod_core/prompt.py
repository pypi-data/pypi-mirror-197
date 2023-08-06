# Copyright 2023 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from typing import Dict, List, Optional

from prompt_toolkit import HTML, prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.shortcuts import confirm as pt_confirm


def confirm(message: str) -> bool:
    if os.environ.get("INTERACTIVE"):
        return bool(pt_confirm(message))
    return True


def prompt_default(
    message: str,
    default: Optional[str] = None,
    options: List[str] = [],
    options_desc: Optional[Dict[str, str]] = None,
    **kwargs
) -> str:
    if os.environ.get("INTERACTIVE"):
        # FIXME: FuzzyWordCompleter doesn't deal with hyphens very well
        completer = (
            FuzzyWordCompleter(options, meta_dict=options_desc) if options else None
        )
        return str(
            prompt(HTML(message), default=default or "", completer=completer, **kwargs)
        )
    else:
        return default or ""
