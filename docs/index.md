---
title: Home
layout: default
nav_order: 1
---

# OpenType Hinting Freezer

A font carries two things: outlines, and instructions for nudging those outlines onto a pixel grid. That second part — the hinting — runs inside the renderer, and every renderer runs it a little differently. `pyfthintfreeze` runs the hinting once, at a size you pick, and bakes the result straight into the outlines. The instructions become moot; the shapes are already where they should be.

```bash
pip install opentype-hinting-freezer
pyfthintfreeze font.ttf --ppm=14 --mode=mono
```

That writes `font.fhf-14-mono.ttf` — the same font, hinted for 14 pixels per em, frozen.

![Before and after freezing hints into a TrueType font](https://raw.githubusercontent.com/twardoch/fonttools-opentype-hinting-freezer/main/assets/Roboto-Black.fhf-12-mono.png)

## When you'd reach for it

- You render text on a platform whose hinter is weak, disabled, or absent, and you need one predictable shape.
- You ship a web font tuned for a specific size and want it crisp before it reaches the browser.
- You target embedded or headless environments where dynamic hinting is a luxury.

## Render modes

The `--mode` flag chooses which FreeType target drives the hinting:

| Mode | FreeType target | Good for |
|------|-----------------|----------|
| `lcd` (default) | horizontal LCD | subpixel-rendered screens |
| `lcdv` | vertical LCD | rotated LCD panels |
| `mono` | 1-bit | bilevel / low-resolution output |
| `light` | light autohint | gentle vertical-only fitting |

## A caveat worth reading

TrueType (`glyf`) fonts are fully supported. CFF/OTF fonts are experimental — the tool will still run and will warn you, but the frozen result is often imperfect. Freeze a TTF when you can.

## Learn more

- [Usage and API](usage) — every flag, plus using the library from Python.
- [How it works](how-it-works) — the UPM-to-PPM scaling, and why frozen outlines match the screen.
