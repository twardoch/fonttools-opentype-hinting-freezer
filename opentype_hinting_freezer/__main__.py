#!/usr/bin/env python3
import fire  # type: ignore[import-untyped]
from typing import List, Any, IO
from .hintingfreezer import freezehinting


def custom_display(lines: List[str], out: IO[Any]) -> None:
    print(*lines, file=out)


def cli() -> None:
    fire.core.Display = custom_display
    fire.Fire(freezehinting)


if __name__ == "__main__":
    cli()
