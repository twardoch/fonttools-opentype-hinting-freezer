---
title: How it works
layout: default
nav_order: 3
---

# How it works

FreeType measures everything in 26.6 fixed point — units of 1/64 pixel. A font,
meanwhile, measures its outlines in font units, `units_per_EM` (UPM) of them to
the em. To freeze hinting at a given pixels-per-em (PPM), the tool has to move
between those two worlds and land back in font units.

## The scaling

The freezer sets FreeType's char size to `ppm * 64` (the PPM expressed in 26.6),
then hands FreeType a transform that undoes the scaling on the way out:

```
rescale = UPM / PPM / 64
```

Loading a glyph with hinting enabled gives FreeType's hinter a pixel grid to fit
to. The fitted outline comes back in 26.6 pixel space; multiplying by `rescale`
carries it back into font units — the same coordinate system the original
outline lived in. The glyph now has the shape the hinter chose for that size,
stored as an ordinary outline with no instructions attached.

Advance width and left side bearing get the same treatment, so the frozen glyph
keeps its metrics.

## TrueType versus CFF

For `glyf` (TrueType) fonts the frozen points are written back through a
`TTGlyphPointPen`. This is the fully supported path.

For `CFF ` (OTF) fonts the outlines are desubroutinized and re-encoded as Type 2
charstrings. FreeType's hinting of CFF and the round-trip back to charstrings are
both lossy in practice, so this path is experimental and the tool warns when it
takes it.

## The render mode

`--mode` selects the FreeType load target — `lcd`, `lcdv`, `mono`, or `light`.
Each asks the hinter to fit for a different output device, so the same font at
the same PPM can freeze to slightly different outlines depending on the screen
you have in mind.
