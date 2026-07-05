# Plan

## What this is

`pyfthintfreeze` runs a font's TrueType hinting once, at a chosen pixels-per-em,
and bakes the fitted outlines back into the glyphs. The instructions become
redundant; the shapes already sit where the hinter would put them.

## Current state

- Single package `opentype_hinting_freezer` with `hintingfreezer.py` (the
  `FontHintFreezer` engine + `freezehinting` entry point) and `__main__.py`
  (the Fire CLI).
- Packaging: `pyproject.toml` + hatchling + hatch-vcs (version from git tags).
- Quality gates: ruff, mypy, a 34-test pytest suite. CI + release workflows
  under `.github/workflows/`.
- TTF (`glyf`) support is solid; CFF/OTF is experimental and warns.

## Roadmap

1. **Make CFF/OTF trustworthy.** The `draw_glyph_to_ps_glyph()` CharString
   round-trip is the weak point. Fix indexing, then add CFF fixtures and drop
   the experimental warning.
2. **Variable fonts.** `set_var_location()` exists but is untested and has no CLI
   surface. Add an `--instance` flag and test against a real variable font.
3. **Ergonomics.** `--verbose`/`--quiet`, batch globbing with `--output-dir`,
   and defaulting output next to the input rather than the working directory.
4. **Docs and release.** Ship the `docs/` site on GitHub Pages; move PyPI
   publishing to trusted publishing (OIDC) so no token is needed.

See `TODO.md` for the itemized list and `CHANGELOG.md` for what has shipped.
