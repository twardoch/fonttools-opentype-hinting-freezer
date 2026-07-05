---
title: Usage and API
layout: default
nav_order: 2
---

# Usage and API

## Command line

```
pyfthintfreeze FONTPATH [--out=PATH] [--ppm=N] [--subfont=N] [--mode=MODE]
```

| Flag | Meaning | Default |
|------|---------|---------|
| `FONTPATH` | Path to a TTF, OTF, or TTC file | required |
| `--out` | Output path | `<stem>.fhf-<ppm>-<mode><suffix>` in the current directory |
| `--ppm` | Pixels per em to hint at | the font's units-per-em |
| `--subfont` | Subfont index inside a TTC | `0` |
| `--mode` | `lcd`, `lcdv`, `mono`, or `light` | `lcd` |

Examples:

```bash
# Freeze at 12 ppm, 1-bit rendering
pyfthintfreeze Roboto-Black.ttf --ppm=12 --mode=mono

# Pick the output name yourself
pyfthintfreeze font.ttf --ppm=16 --out=font-16.ttf
```

A `ppm` of zero or a negative number is rejected with a clear error, as is an unknown `--mode`.

## Python library

```python
from opentype_hinting_freezer import freezehinting

freezehinting("font.ttf", out="font-14.ttf", ppm=14, mode="mono")
```

For finer control, drive the `FontHintFreezer` class directly:

```python
from opentype_hinting_freezer import FontHintFreezer

data = open("font.ttf", "rb").read()
fhf = FontHintFreezer(data, ppm=14, render_mode="mono")
fhf.freeze_hints()
fhf.ttFont.save("font-14.ttf")
```

`freeze_hints()` rewrites every glyph in place: TrueType glyphs go through the
`glyf` table, CFF glyphs through the `CFF ` table (with an experimental-quality
warning).

## Requirements

`freetype-py` needs a FreeType library. Its wheels bundle one for common
platforms; if you build from source, install the system `libfreetype`
development package first.
