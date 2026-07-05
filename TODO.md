# TODO

Future work, roughly in priority order. Shipped items live in `CHANGELOG.md`.

## Correctness

- [ ] Fix CharString indexing in `draw_glyph_to_ps_glyph()` and make CFF/OTF
      output reliable (currently experimental, emits a warning).
- [ ] Add CFF-specific tests once the path is trustworthy.
- [ ] Validate the font's magic bytes before processing and raise a typed error.

## Variable fonts

- [ ] Finish `set_var_location` support: named instances, an `--instance` flag,
      and tests against a real variable font (Roboto Flex, Inter).

## Usability

- [ ] `--verbose` / `--quiet` flags and structured logging.
- [ ] Batch mode: accept globs, add `--output-dir`.
- [ ] Write output next to the input font by default, not the current directory.

## Docs and release

- [ ] Publish the `docs/` site via GitHub Pages.
- [ ] Configure PyPI trusted publishing so the release workflow needs no token.
