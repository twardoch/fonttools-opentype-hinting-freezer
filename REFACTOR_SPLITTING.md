# Refactoring Plan: Splitting Large Code Files

## Executive Summary

This document outlines a detailed plan for refactoring the `opentype_hinting_freezer/hintingfreezer.py` file, which currently contains the majority of the core logic for the OpenType Hinting Freezer project. The goal is to split this large file into smaller, more focused modules, improving maintainability, readability, and adherence to the Single Responsibility Principle, while ensuring that all existing functionality remains absolutely intact.

This plan aligns with the "Refactor Core Architecture" goal outlined in the project's `PLAN.md`.

## File to Refactor

-   `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py`

## Current Structure Analysis of `hintingfreezer.py`

The `hintingfreezer.py` file currently encompasses:
-   Necessary imports from `io`, `pathlib`, `fontTools`, and `freetype`.
-   The `renderModeFlags` dictionary, mapping rendering mode strings to FreeType constants.
-   The `FontHintFreezer` class, which is a monolithic class handling:
    -   Font loading and initialization (`__init__`).
    -   Variable font instance setting (`set_var_location`).
    -   Glyph preparation (`prep_glyph`).
    -   Generic outline drawing (`draw_glyph_to_point_pen`, `draw_glyph_to_pen`).
    -   TrueType-specific glyph processing (`draw_glyph_to_tt_glyph`).
    -   CFF-specific glyph processing (`draw_glyph_to_ps_glyph`).
    -   Orchestration of the hint freezing process across all glyphs (`freeze_hints`).
-   The `read_from_path` utility function for reading font file data.
-   The `freezehinting` function, which serves as the main public API and CLI entry point, orchestrating the `FontHintFreezer` class.

## Proposed Splitting Strategy

The core idea is to separate concerns into distinct modules, following the proposed `core/`, `cli/`, and `utils/` structure from `PLAN.md`.

### New Module Structure:

```
opentype_hinting_freezer/
├── __init__.py
├── constants.py                  # New: For shared constants like renderModeFlags
├── core/                         # New: Core logic for font processing
│   ├── __init__.py
│   ├── font_freezer.py           # Renamed/Refactored: Main FontHintFreezer class (orchestrator)
│   └── glyph_processors.py       # New: Classes for TTF and CFF glyph processing
├── cli/                          # New: Command-line interface logic
│   ├── __init__.py
│   └── main_cli.py               # New: Contains the freezehinting function (CLI entry point)
└── utils/                        # New: General utility functions
    ├── __init__.py
    └── font_io.py                # New: For font file I/O operations
```

## Detailed Plan for Junior Developer

Follow these steps meticulously. After each step, ensure the project still builds and, if possible, run relevant tests to verify functionality.

---

### Step 1: Create New Directory Structure

1.  **Create `core` directory:**
    ```bash
    mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core
    ```
2.  **Create `cli` directory:**
    ```bash
    mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/cli
    ```
3.  **Create `utils` directory:**
    ```bash
    mkdir -p /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/utils
    ```
4.  **Create `__init__.py` in new directories:**
    ```bash
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/__init__.py
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/cli/__init__.py
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/utils/__init__.py
    ```

---

### Step 2: Move `renderModeFlags` to `constants.py`

1.  **Create `constants.py`:**
    ```bash
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/constants.py
    ```
2.  **Move content:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py`.
    *   Cut the `renderModeFlags` dictionary definition.
    *   Paste it into `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/constants.py`.
    *   Add necessary imports to `constants.py` if `FT_LOAD_TARGET_LCD`, etc., are not defined there (they are from `freetype`, so `from freetype import *` will be needed).
3.  **Update import in `hintingfreezer.py`:**
    *   In `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py`, add:
        ```python
        from .constants import renderModeFlags
        ```
    *   Remove `from freetype import *` from `hintingfreezer.py` if `renderModeFlags` was the only thing using `FT_LOAD_TARGET_*` constants directly. Otherwise, keep it. (It's used by `FontHintFreezer` directly, so keep it for now).

---

### Step 3: Move `read_from_path` to `utils/font_io.py`

1.  **Create `font_io.py`:**
    ```bash
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/utils/font_io.py
    ```
2.  **Move content:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py`.
    *   Cut the `read_from_path` function definition.
    *   Paste it into `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/utils/font_io.py`.
    *   Add necessary imports to `font_io.py`:
        ```python
        from pathlib import Path
        from typing import Union
        ```
3.  **Update import in `hintingfreezer.py`:**
    *   In `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py`, add:
        ```python
        from ..utils.font_io import read_from_path
        ```
4.  **Update import in `tests/test_hintingfreezer_unit.py`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/tests/test_hintingfreezer_unit.py`.
    *   Change:
        ```python
        from opentype_hinting_freezer.hintingfreezer import read_from_path
        ```
        to:
        ```python
        from opentype_hinting_freezer.utils.font_io import read_from_path
        ```

---

### Step 4: Refactor `FontHintFreezer` and Create Glyph Processors

This is the most involved step.

1.  **Rename `hintingfreezer.py` to `font_freezer.py`:**
    ```bash
    mv /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/hintingfreezer.py /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/font_freezer.py
    ```

2.  **Create `glyph_processors.py`:**
    ```bash
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/glyph_processors.py
    ```

3.  **Populate `glyph_processors.py`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/glyph_processors.py`.
    *   Add necessary imports:
        ```python
        from typing import Any, Dict, Iterator, List, Optional, Tuple, Mapping
        from fontTools.pens.pointPen import PointToSegmentPen
        from fontTools.pens.t2CharStringPen import T2CharStringPen
        from fontTools.pens.ttGlyphPen import TTGlyphPointPen
        from freetype import Face, GlyphSlot, Matrix, Vector, FT_LOAD_RENDER, FT_Fixed, FT_Set_Var_Design_Coordinates
        ```
    *   Define `BaseGlyphProcessor` (or a `Protocol` if preferred for more strict typing, but for simplicity, an abstract base class is fine for now):
        ```python
        from abc import ABC, abstractmethod

        class BaseGlyphProcessor(ABC):
            def __init__(self, tt_font_instance: Any, ft_face_instance: Face, glyph_set: Mapping[str, Any], ft_flag: int, rescale_metrics: float, rescale_glyphs: int):
                self.ttFont = tt_font_instance
                self.ftFace = ft_face_instance
                self.glyphSet = glyph_set
                self.ft_flag = ft_flag
                self.rescale_metrics = rescale_metrics
                self.rescale_glyphs = rescale_glyphs
                self.ftGlyph: Optional[GlyphSlot] = None
                self.width: int = 0
                self.lsb: int = 0

            def prep_glyph(self, glyph_name: str) -> None:
                glyph_id: int = self.ttFont.getGlyphID(glyph_name)
                self.ftFace.load_glyph(glyph_id, FT_LOAD_RENDER | self.ft_flag)
                self.ftGlyph = self.ftFace.glyph
                self.lsb = int(self.ftGlyph.metrics.horiBearingX * self.rescale_metrics)
                self.width = int(self.ftGlyph.metrics.horiAdvance * self.rescale_metrics)

            def draw_glyph_to_point_pen(self, pen: Any) -> None:
                if not self.ftGlyph:
                    raise RuntimeError("Glyph not prepared. Call prep_glyph first.")
                contours: Iterator[int] = (i + 1 for i in self.ftGlyph.outline.contours)
                points: List[Tuple[int, int]] = self.ftGlyph.outline.points
                flags: List[int] = self.ftGlyph.outline.tags
                curve_type: str = "curve" if any(t & 0x02 for t in flags) else "qcurve"
                from_index: int = 0
                for to_index in contours:
                    c_points: List[Tuple[int, int]] = points[from_index:to_index]
                    c_flags: List[int] = flags[from_index:to_index]
                    pen.beginPath()
                    for i_idx, (pt_x, pt_y) in enumerate(c_points):
                        point_coord: Tuple[int, int] = (pt_x, pt_y)
                        segment_type: Optional[str] = None
                        if not c_flags[i_idx] & 0x01:
                            segment_type = None
                        elif c_flags[i_idx -1] & 0x01:
                            segment_type = "line"
                        else:
                            segment_type = curve_type
                        pen.addPoint(point_coord, segmentType=segment_type)
                    pen.endPath()
                    from_index = to_index

            def draw_glyph_to_pen(self, pen: Any) -> None:
                self.draw_glyph_to_point_pen(PointToSegmentPen(pen))

            @abstractmethod
            def process_glyph(self, glyph_name: str) -> None:
                pass

        class TTFGlyphProcessor(BaseGlyphProcessor):
            def process_glyph(self, glyph_name: str) -> None:
                self.prep_glyph(glyph_name)
                pen = TTGlyphPointPen(glyphSet=self.glyphSet, handleOverflowingTransforms=True)
                self.draw_glyph_to_point_pen(pen)
                self.ttFont["glyf"][glyph_name] = pen.glyph()
                self.ttFont["hmtx"][glyph_name] = (self.width, self.lsb)

        class CFFGlyphProcessor(BaseGlyphProcessor):
            def process_glyph(self, glyph_name: str) -> None:
                cff = self.ttFont["CFF "].cff
                top_dict: Any = cff.topDictIndex[0]
                self.prep_glyph(glyph_name)
                pen = T2CharStringPen(
                    width=self.width, glyphSet=self.glyphSet, roundTolerance=0.5, CFF2=False
                )
                self.draw_glyph_to_pen(pen)
                top_dict.CharStrings.charStringsIndex.items.append(None)
                i: int = len(top_dict.CharStrings.charStringsIndex) - 1
                top_dict.CharStrings.charStringsIndex[i] = pen.getCharString(
                    private=top_dict.Private
                )
                top_dict.CharStrings.charStrings[glyph_name] = i
                self.ttFont["hmtx"][glyph_name] = (self.width, self.lsb)
        ```

4.  **Modify `opentype_hinting_freezer/core/font_freezer.py`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/font_freezer.py`.
    *   Remove the `read_from_path` function and the `freezehinting` function (they will be moved in subsequent steps).
    *   Remove the `renderModeFlags` dictionary.
    *   Update imports:
        ```python
        import io
        from pathlib import Path
        from typing import Any, Dict, List, Optional, Mapping, KeysView
        from fontTools.ttLib import TTFont
        from freetype import Face, Matrix, Vector, FT_Fixed, FT_Set_Var_Design_Coordinates, FT_LOAD_TARGET_LCD, FT_LOAD_TARGET_MONO, FT_LOAD_TARGET_LCD_V, FT_LOAD_TARGET_LIGHT

        from ..constants import renderModeFlags as RENDER_MODE_FLAGS # Use alias to avoid conflict
        from .glyph_processors import TTFGlyphProcessor, CFFGlyphProcessor, BaseGlyphProcessor
        ```
    *   Modify the `FontHintFreezer` class:
        *   Remove `glyphName`, `width`, `lsb`, `ftGlyph` attributes from the class definition (they are now part of the glyph processors).
        *   In `__init__`, after setting up `self.ttFont` and `self.ftFace`, determine the font type and instantiate the correct `GlyphProcessor`:
            ```python
            class FontHintFreezer:
                ttFont: TTFont
                ftFace: Face
                glyphSet: Mapping[str, Any]
                glyphNames: KeysView[str]
                upm: int
                ppm: int
                rescale_metrics: float
                rescale_glyphs: int
                ft_flag: int
                _glyph_processor: BaseGlyphProcessor # New attribute

                def __init__(
                    self,
                    font_data: bytes,
                    font_number: int = 0,
                    ppm: Optional[int] = None,
                    render_mode: str = "lcd",
                ) -> None:
                    stream = io.BytesIO(font_data)
                    self.ttFont = TTFont(stream, fontNumber=font_number, lazy=False)
                    stream = io.BytesIO(font_data)
                    self.ftFace = Face(stream, index=font_number)
                    self.glyphSet = self.ttFont.getGlyphSet()
                    self.glyphNames = self.glyphSet.keys()
                    self.upm = self.ftFace.units_per_EM
                    self.ppm = ppm or self.upm
                    self.rescale_metrics = float(self.upm) / float(self.ppm) / 64.0
                    self.rescale_glyphs = int(float(self.upm) / float(self.ppm) / 64.0 * 0x10000)
                    self.ftFace.set_char_size(self.ppm * 64, 0, 72, 0)
                    self.ftFace.set_transform(
                        Matrix(self.rescale_glyphs, 0, 0, self.rescale_glyphs), Vector(0, 0)
                    )
                    self.ft_flag = RENDER_MODE_FLAGS.get(render_mode, FT_LOAD_TARGET_LCD)

                    # Instantiate the correct glyph processor
                    if "glyf" in self.ttFont:
                        self._glyph_processor = TTFGlyphProcessor(
                            self.ttFont, self.ftFace, self.glyphSet, self.ft_flag, self.rescale_metrics, self.rescale_glyphs
                        )
                    elif "CFF " in self.ttFont:
                        cff = self.ttFont["CFF "].cff
                        cff.desubroutinize() # CFF processing needs this
                        self._glyph_processor = CFFGlyphProcessor(
                            self.ttFont, self.ftFace, self.glyphSet, self.ft_flag, self.rescale_metrics, self.rescale_glyphs
                        )
                    else:
                        raise ValueError("Unsupported font type: neither 'glyf' nor 'CFF ' table found.")
            ```
        *   Remove `prep_glyph`, `draw_glyph_to_point_pen`, `draw_glyph_to_pen`, `draw_glyph_to_tt_glyph`, `draw_glyph_to_ps_glyph` methods from `FontHintFreezer`.
        *   Modify `freeze_hints` to delegate to the `_glyph_processor`:
            ```python
            def freeze_hints(self) -> None:
                for glyph_name_loopvar in self.glyphNames:
                    self._glyph_processor.process_glyph(glyph_name_loopvar)
            ```
        *   The `set_var_location` method remains in `FontHintFreezer` as it operates on the `ftFace` and `ttFont` directly.

---

### Step 5: Refactor `freezehinting` to `cli/main_cli.py`

1.  **Create `main_cli.py`:**
    ```bash
    touch /Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/cli/main_cli.py
    ```
2.  **Move content:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/core/font_freezer.py` (the file that was `hintingfreezer.py`).
    *   Cut the `freezehinting` function definition.
    *   Paste it into `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/cli/main_cli.py`.
    *   Add necessary imports to `main_cli.py`:
        ```python
        from pathlib import Path
        from typing import Optional, Dict, Union
        from ..core.font_freezer import FontHintFreezer
        from ..utils.font_io import read_from_path
        ```
    *   Ensure the `freezehinting` function's docstring and parameters are correct.

3.  **Update `opentype_hinting_freezer/__main__.py`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/__main__.py`.
    *   Change:
        ```python
        from .hintingfreezer import freezehinting
        ```
        to:
        ```python
        from .cli.main_cli import freezehinting
        ```
    *   Modify the `cli()` function to call `fire.Fire(freezehinting)` directly, as `freezehinting` is now the main entry point for the CLI.
        ```python
        import fire
        from typing import List, Any, IO # Keep these if custom_display is still used
        from .cli.main_cli import freezehinting

        def custom_display(lines: List[str], out: IO[Any]) -> None:
            print(*lines, file=out)

        def cli() -> None:
            fire.core.Display = custom_display # Keep this if you want custom display
            fire.Fire(freezehinting)

        if __name__ == "__main__":
            cli()
        ```

---

### Step 6: Update `__init__.py` files

1.  **Update `opentype_hinting_freezer/__init__.py`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/opentype_hinting_freezer/__init__.py`.
    *   Change:
        ```python
        from .hintingfreezer import freezehinting
        ```
        to:
        ```python
        from .cli.main_cli import freezehinting
        ```
    *   This ensures `freezehinting` is still importable from the top-level package.

---

### Step 7: Update `pyproject.toml`

1.  **Update `project.scripts`:**
    *   Open `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/pyproject.toml`.
    *   Under `[project.scripts]`, ensure the `pyfthintfreeze` entry points to the correct CLI function:
        ```toml
        [project.scripts]
        pyfthintfreeze = "opentype_hinting_freezer.cli.main_cli:freezehinting"
        ```
        (Note: If `__main__.py` is still the entry point and calls `cli()`, then `opentype_hinting_freezer.__main__:cli` is correct. The plan assumes `freezehinting` becomes the direct target for `fire.Fire`.)

2.  **Review `tool.hatch.build.targets.wheel`:**
    *   Ensure `packages = ["opentype_hinting_freezer"]` is still correct. This should automatically pick up the new submodules.

---

### Step 8: Update Tests

1.  **Review and update imports in test files:**
    *   `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/tests/test_cli_integration.py`: No direct imports from `hintingfreezer.py`, so this should be fine. It calls the CLI executable.
    *   `/Users/adam/Developer/vcs/github.twardoch/pub/fonttools-opentype-hinting-freezer/tests/test_hintingfreezer_unit.py`: Already updated `read_from_path`. If any new unit tests are added for `FontHintFreezer` or `GlyphProcessor` classes, their imports will need to be updated accordingly (e.g., `from opentype_hinting_freezer.core.font_freezer import FontHintFreezer`).

2.  **Consider adding new unit tests:**
    *   It would be beneficial to add specific unit tests for `TTFGlyphProcessor` and `CFFGlyphProcessor` to ensure their isolated functionality.

---

### Step 9: Verification

1.  **Run quality checks:**
    ```bash
    hatch run check
    ```
    Address any linting or type-checking errors.

2.  **Run tests:**
    ```bash
    hatch run test
    ```
    Ensure all existing tests pass.

3.  **Manual CLI testing:**
    *   Run the CLI with various font types (TTF, OTF, TTC if available) and parameters (`--ppm`, `--mode`, `--out`, `--var`).
    *   Verify that the output fonts are generated correctly and behave as expected.

---

## Important Considerations for Junior Developer

*   **Relative Imports:** Pay extremely close attention to relative imports (`.`, `..`) when moving code between modules. A common mistake is incorrect pathing.
*   **Dependencies:** Ensure that every new or modified Python file has all the necessary `import` statements at the top. If a function or class uses something, it must import it.
*   **Functionality Preservation:** The absolute highest priority is to ensure that the tool's functionality remains identical to its state before refactoring. Test thoroughly after each significant change.
*   **Incremental Changes:** Do not try to do all steps at once. Complete one step, verify, and then move to the next. This makes debugging much easier.
*   **Type Hints:** Preserve and update all existing type hints. If new code is written, add appropriate type hints.
*   **Docstrings:** Ensure that any moved functions or classes retain their docstrings, and update them if their context or parameters change.
*   **Error Handling:** Be mindful of how errors are handled. Ensure that exceptions are still caught and propagated correctly.
*   **Git:** Commit frequently with clear, concise commit messages after each successful small change. This creates a good history and allows for easy rollback if issues arise.
