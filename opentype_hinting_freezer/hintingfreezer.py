#!/usr/bin/env python3
import io
from pathlib import Path

from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPointPen
from fontTools.ttLib import TTFont
from freetype import *

renderModeFlags = {
    "lcd": FT_LOAD_TARGET_LCD,
    "mono": FT_LOAD_TARGET_MONO,
    "lcdv": FT_LOAD_TARGET_LCD_V,
    "light": FT_LOAD_TARGET_LIGHT,
}


class FontHintFreezer:
    ttFont: TTFont  # Actual type from fontTools
    ftFace: Face    # Actual type from freetype
    glyphSet: Mapping[str, Any] # From ttFont.getGlyphSet()
    glyphNames: KeysView[str]
    glyphName: str
    width: int
    lsb: int
    upm: int
    ppm: int
    rescale_metrics: float
    rescale_glyphs: int
    ft_flag: int  # FreeType load flag (integer)
    ftGlyph: Any  # freetype.GlyphSlot object

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
        # getGlyphSet returns a _TTGlyphSet, which is a Mapping.
        self.glyphSet = self.ttFont.getGlyphSet()
        self.glyphNames = self.glyphSet.keys()
        self.glyphName = ""
        self.width = 0
        self.lsb = 0
        self.upm = self.ftFace.units_per_EM
        self.ppm = ppm or self.upm # ppm can't be 0
        self.rescale_metrics = float(self.upm) / float(self.ppm) / 64.0
        self.rescale_glyphs = int(float(self.upm) / float(self.ppm) / 64.0 * 0x10000)
        self.ftFace.set_char_size(self.ppm * 64, 0, 72, 0)
        self.ftFace.set_transform(
            Matrix(self.rescale_glyphs, 0, 0, self.rescale_glyphs), Vector(0, 0)
        )
        self.ft_flag = RENDER_MODE_FLAGS.get(render_mode, FT_LOAD_TARGET_LCD)

    def set_var_location(self, var_location: Dict[str, float]) -> None:
        if "fvar" not in self.ttFont:
            return
        coordinates_values: List[float] = [
            var_location.get(axis.axisTag, axis.defaultValue)
            for axis in self.ttFont["fvar"].axes
        ]
        ft_coordinates_values: List[int] = [round(v * 0x10000) for v in coordinates_values]
        c_coordinates = (FT_Fixed * len(ft_coordinates_values))(*ft_coordinates_values)
        FT_Set_Var_Design_Coordinates(
            self.ftFace._FT_Face, len(ft_coordinates_values), c_coordinates
        )

    def prep_glyph(self) -> None:
        glyph_id: int = self.ttFont.getGlyphID(self.glyphName)
        self.ftFace.load_glyph(glyph_id, FT_LOAD_RENDER | self.ft_flag)
        self.ftGlyph = self.ftFace.glyph
        self.lsb = int(self.ftGlyph.metrics.horiBearingX * self.rescale_metrics)
        self.width = int(self.ftGlyph.metrics.horiAdvance * self.rescale_metrics)

    def draw_glyph_to_point_pen(self, pen: Any) -> None:  # pen is a PointPen
        # ftGlyph is GlyphSlot, outline is Outline
        contours: Iterator[int] = (i + 1 for i in self.ftGlyph.outline.contours)
        points: List[Tuple[int, int]] = self.ftGlyph.outline.points # points are tuples of int
        flags: List[int] = self.ftGlyph.outline.tags # tags are list of int (bytes really)
        # The commented print line:
        # print(
        #    self.glyphName,
        #    self.ftFace.glyph.get_glyph().get_cbox(freetype.FT_GLYPH_BBOX_PIXELS),
        # )
        curve_type: str = "curve" if any(t & 0x02 for t in flags) else "qcurve"
        from_index: int = 0
        for to_index in contours:
            c_points: List[Tuple[int, int]] = points[from_index:to_index]
            c_flags: List[int] = flags[from_index:to_index]
            pen.beginPath()
            for i_idx, (pt_x, pt_y) in enumerate(c_points): # Iterate properly
                point_coord: Tuple[int, int] = (pt_x, pt_y)
                segment_type: Optional[str] = None
                if not c_flags[i_idx] & 0x01: # current point is off-curve
                    segment_type = None
                elif c_flags[i_idx -1] & 0x01: # previous point was on-curve
                    segment_type = "line"
                else: # previous point was off-curve, current is on-curve
                    segment_type = curve_type
                pen.addPoint(point_coord, segmentType=segment_type)
            pen.endPath()
            from_index = to_index

    def draw_glyph_to_pen(self, pen: Any) -> None:  # pen is a SegmentPen
        # PointToSegmentPen expects a SegmentPen
        self.draw_glyph_to_point_pen(PointToSegmentPen(pen))

    def draw_glyph_to_tt_glyph(self) -> None:
        self.prep_glyph()
        # TTGlyphPointPen expects a glyphSet
        pen = TTGlyphPointPen(glyphSet=self.glyphSet, handleOverflowingTransforms=True)
        self.draw_glyph_to_point_pen(pen)
        self.ttFont["glyf"][self.glyphName] = pen.glyph() # type: ignore[index]
        self.ttFont["hmtx"][self.glyphName] = (self.width, self.lsb) # type: ignore[index]

    def draw_glyph_to_ps_glyph(self) -> None:
        cff = self.ttFont["CFF "].cff # type: ignore[index]
        top_dict: Any = cff.topDictIndex[0]
        self.prep_glyph()
        # print(self.glyphName, self.lsb, self.width) # Removed debug print
        # T2CharStringPen expects width and glyphSet
        pen = T2CharStringPen(
            width=self.width, glyphSet=self.glyphSet, roundTolerance=0.5, CFF2=False
        )
        self.draw_glyph_to_pen(pen)
        top_dict.CharStrings.charStringsIndex.items.append(None)
        i: int = len(top_dict.CharStrings.charStringsIndex) - 1
        top_dict.CharStrings.charStringsIndex[i] = pen.getCharString(
            private=top_dict.Private
        )
        top_dict.CharStrings.charStrings[self.glyphName] = i
        self.ttFont["hmtx"][self.glyphName] = (self.width, self.lsb) # type: ignore[index]

    def freeze_hints(self) -> None:
        if "glyf" in self.ttFont: # type: ignore[operator]
            for glyph_name_loopvar in self.glyphNames:
                self.glyphName = glyph_name_loopvar
                self.draw_glyph_to_tt_glyph()
        elif "CFF " in self.ttFont: # type: ignore[operator]
            cff = self.ttFont["CFF "].cff # type: ignore[index]
            cff.desubroutinize()
            for glyph_name_loopvar in self.glyphNames:
                self.glyphName = glyph_name_loopvar
                self.draw_glyph_to_ps_glyph()


def read_from_path(path: Union[str, Path]) -> bytes:
    with open(path, "rb") as f:
        fontData = f.read()
    return fontData


def freezehinting(fontpath, out=None, ppm=None, subfont=0, var=None, mode="lcd"):
    """
    OpenType font hinting freezer \n
    A tool that applies the hinting of an OT font
    to the contours at a specified PPM size,
    and outputs the font with modified contours
    (Works better with TTF, OTF support is buggy)

    Example:
    pyfthintfreeze font.ttf --ppm=14 --mode="mono"

    :param fontpath: path to an OTF or TTF or TTC file
    :param out: output path, automatic if absent
    :param ppm: pixel-per-em for applying the hinting
    :param subfont: subfont index in a TTC file
    :param var: NOT IMPLEMENTED variable font location as a dict
    :param mode: hinting mode: "lcd" (default), "lcdv", "mono", "light"
    """
    fhf = FontHintFreezer(
        read_from_path(fontpath),
        font_number=subfont,
        ppm=ppm,
        render_mode=mode,
    )

    if var and "fvar" in fhf.ttFont: # type: ignore[operator]
        fhf.set_var_location(var)

    fhf.freeze_hints()

    output_path: Path
    if out:
        output_path = Path(out)
    else:
        # Ensure ppm is not None for path generation if it was None for FontHintFreezer
        # FontHintFreezer defaults ppm to upm if None. We need a value for the filename.
        ppm_for_filename = ppm if ppm is not None else fhf.ppm
        font_path_obj = Path(fontpath)
        output_path = Path(
            f"{font_path_obj.stem}.fhf-{ppm_for_filename}-{mode}{font_path_obj.suffix}"
        )
    fhf.ttFont.save(output_path)
