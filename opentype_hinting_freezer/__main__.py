#!/usr/bin/env python3
import fire
from .hintingfreezer import freezehinting


def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(freezehinting)


if __name__ == "__main__":
    cli()
