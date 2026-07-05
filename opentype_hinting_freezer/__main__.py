#!/usr/bin/env python3
# this_file: opentype_hinting_freezer/__main__.py
"""Command-line entry point for the OpenType hinting freezer."""

from __future__ import annotations

from typing import IO, Any

import fire

from .hintingfreezer import freezehinting


def custom_display(lines: list[str], out: IO[Any]) -> None:
    print(*lines, file=out)


def cli() -> None:
    fire.core.Display = custom_display
    fire.Fire(freezehinting)


if __name__ == "__main__":
    cli()
