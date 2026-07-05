# this_file: opentype_hinting_freezer/__init__.py
"""OpenType hinting freezer: bake a font's hinting into its outlines."""

from importlib.metadata import PackageNotFoundError, version

from .hintingfreezer import FontHintFreezer, freezehinting

try:
    __version__ = version("opentype-hinting-freezer")
except PackageNotFoundError:  # running from a source tree without install metadata
    __version__ = "0.0.0+unknown"

__all__ = ["FontHintFreezer", "__version__", "freezehinting"]
