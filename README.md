# fonttools-opentype-hint-freezer

A tool that applies the font's hinting to the contours at a specified PPM size, and outputs the font with modified contours.

## Installation

```
python3 -m pip install --upgrade git+https://github.com/twardoch/fonttools-opentype-hinting-freezer
```

## Usage

```
NAME
    pyfthintfreeze - OpenType font hinting freezer

SYNOPSIS
    pyfthintfreeze FONTPATH <flags>

DESCRIPTION
    A tool that applies the hinting of an OT font
    to the contours at a specified PPM size,
    and outputs the font with modified contours
    (Works better with TTF, OTF support is buggy)

    Example:
    pyfthintfreeze font.ttf --ppm=14 --mode="mono"

POSITIONAL ARGUMENTS
    FONTPATH
        path to an OTF or TTF or TTC file

FLAGS
    --out=OUT
        output path, automatic if absent
    --ppm=PPM
        pixel-per-em for applying the hinting
    --subfont=SUBFONT
        subfont index in a TTC file
    --var=VAR
        NOT IMPLEMENTED variable font location as a dict
    --mode=MODE
        hinting mode: "lcd" (default), "lcdv", "mono", "light"

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## Example

```
pyfthintfreeze font.ttf --ppm=14 --mode="mono"
```

## Credits and License

- Copyright (c) 2022 by [Adam Twardoch and others](./AUTHORS.txt)
- Code by [Adam Twardoch and others](./CONTRIBUTORS.txt)
- Licensed under the [Apache 2.0 license](./LICENSE)
