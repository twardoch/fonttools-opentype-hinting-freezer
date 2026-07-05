# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Import crash (regression in v1.0.0/v1.0.1):** the package could not be
  imported at all. Class and function annotations referenced typing names
  (`Mapping`, `Any`, `Optional`, ...) that were never imported, and the CLI
  referenced `List`/`IO`/`Any` in `__main__.py` with no import — both raised
  `NameError` on import.
- The render-mode lookup referenced `RENDER_MODE_FLAGS` while the dict was named
  `renderModeFlags`, so any run raised `NameError`. Unified to `RENDER_MODE_FLAGS`.

### Added
- Input validation in `freezehinting()`: a non-positive `ppm` and an unknown
  `--mode` now raise a clear `ValueError` instead of silently doing the wrong
  thing (zero ppm previously fell back to the em size; a bad mode fell back to
  LCD).
- A `UserWarning` when freezing hints into CFF/OTF outlines, whose support is
  experimental.
- `FontHintFreezer` and `__version__` are now exported from the package root.
- Jekyll + Just-the-Docs site under `docs/`.
- GitHub Actions CI (test matrix + lint/type) and tag-driven release workflow,
  now correctly placed under `.github/workflows/`.

### Changed
- `from freetype import *` replaced with explicit imports of the names used,
  clearing the star-import lint and type-check gaps.
- Type annotations modernized to built-in generics and `X | None`; `__version__`
  now read from installed package metadata instead of a hard-coded string.
- `mypy` target raised to 3.10 (the tool no longer supports a 3.9 target).

### Removed
- `setup.py` (packaging fully handled by `pyproject.toml` + hatch-vcs).
- Stale scaffolding files: `llms.txt`, `IMPLEMENTATION_SUMMARY.md`,
  `REFACTOR_SPLITTING.md`, `REFACTOR_FILELIST.txt`, `GITHUB_WORKFLOWS_SETUP.md`,
  `README_DEVELOPMENT.md`, and the inert `github-workflows/` directory.

## [1.0.0] - [1.0.1]

Packaging modernization (pyproject + hatch-vcs, Ruff, Mypy, pytest suite,
type hints). Note: both tags shipped with an import-time crash, fixed in the
next release.

## [0.1.0] - 2022-01-14

### Added
- Initial release of OpenType Hinting Freezer
- Core functionality to freeze TrueType hinting at specific PPM sizes
- Command-line interface `pyfthintfreeze`
- Support for TTF fonts (OTF support is experimental)
- Multiple rendering modes: LCD, LCD-V, mono, light
- Variable font support (basic)
- TrueType Collection (TTC) support
- Apache 2.0 license

[Unreleased]: https://github.com/twardoch/fonttools-opentype-hinting-freezer/compare/v1.0.1...HEAD
[1.0.0] - [1.0.1]: https://github.com/twardoch/fonttools-opentype-hinting-freezer/compare/v0.1.0...v1.0.1
[0.1.0]: https://github.com/twardoch/fonttools-opentype-hinting-freezer/releases/tag/v0.1.0