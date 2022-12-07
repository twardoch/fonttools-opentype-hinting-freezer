#!/usr/bin/env python3
from pathlib import Path
import io
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPointPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.fontBuilder import FontBuilder
from freetype import *

renderModeFlags = {
    "lcd": FT_LOAD_TARGET_LCD,
    "mono": FT_LOAD_TARGET_MONO,
    "lcdv": FT_LOAD_TARGET_LCD_V,
    "light": FT_LOAD_TARGET_LIGHT,
}


class FontHintFreezer:
    def __init__(
        self,
        fontData,
        fontNumber=0,
        ppm=None,
        varLocation=None,
        renderMode="lcd",
    ):
        stream = io.BytesIO(fontData)
        self.ttFont = TTFont(stream, fontNumber=fontNumber, lazy=False)
        stream = io.BytesIO(fontData)
        self.ftFace = Face(stream, index=fontNumber)
        self.glyphSet = self.ttFont.getGlyphSet()
        self.glyphNames = self.glyphSet.keys()
        self.glyphName = ""
        self.width = 0
        self.lsb = 0
        self.upm = self.ftFace.units_per_EM
        self.ppm = ppm if ppm else self.upm
        self.rescale_metrics = self.upm / self.ppm / 64
        self.rescale_glyphs = int(self.upm / self.ppm / 64 * 0x10000)
        self.ftFace.set_char_size(self.ppm * 64, 0, 72, 0)
        self.ftFace.set_transform(
            Matrix(self.rescale_glyphs, 0, 0, self.rescale_glyphs), Vector(0, 0)
        )
        self.ft_flag = renderModeFlags.get(renderMode, FT_LOAD_TARGET_LCD)

    def setVarLocation(self, varLocation):
        if "fvar" not in self.ttFont:
            return
        coordinates = []
        for axis in self.ttFont["fvar"].axes:
            coordinates.append(varLocation.get(axis.axisTag, axis.defaultValue))
        coordinates = [round(v * 0x10000) for v in coordinates]
        c_coordinates = (FT_Fixed * len(coordinates))(*coordinates)
        FT_Set_Var_Design_Coordinates(
            self.ftFace._FT_Face, len(coordinates), c_coordinates
        )

    def prepGlyph(self):
        glyphID = self.ttFont.getGlyphID(self.glyphName)
        self.ftFace.load_glyph(glyphID, FT_LOAD_RENDER | self.ft_flag)
        self.ftGlyph = self.ftFace.glyph
        self.lsb = int(self.ftGlyph.metrics.horiBearingX * self.rescale_metrics)
        self.width = int(self.ftGlyph.metrics.horiAdvance * self.rescale_metrics)

    def drawGlyphToPointPen(self, pen):
        contours = (i + 1 for i in self.ftGlyph.outline.contours)
        points = self.ftGlyph.outline.points
        flags = self.ftGlyph.outline.tags
        # print(self.glyphName, self.ftFace.glyph.get_glyph().get_cbox(FT_GLYPH_BBOX_PIXELS))
        curveType = "curve" if any(t & 0x02 for t in flags) else "qcurve"
        fromIndex = 0
        for toIndex in contours:
            cPoints = points[fromIndex:toIndex]
            cFlags = flags[fromIndex:toIndex]
            pen.beginPath()
            for i in range(len(cPoints)):
                if not cFlags[i] & 0x01:
                    segmentType = None
                elif cFlags[i - 1] & 0x01:
                    segmentType = "line"
                else:
                    segmentType = curveType
                pen.addPoint(cPoints[i], segmentType)
            pen.endPath()
            fromIndex = toIndex

    def drawGlyphToPen(self, pen):
        self.drawGlyphToPointPen(PointToSegmentPen(pen))

    def drawGlyphToTTGlyph(self):
        self.prepGlyph()
        pen = TTGlyphPointPen(glyphSet=self.glyphSet, handleOverflowingTransforms=True)
        self.drawGlyphToPointPen(pen)
        self.ttFont["glyf"][self.glyphName] = pen.glyph()
        self.ttFont["hmtx"][self.glyphName] = (self.width, self.lsb)

    def drawGlyphToPSGlyph(self):
        # This is ugly and does not properly work with advance widths
        cff = self.ttFont["CFF "].cff
        topDict = cff.topDictIndex[0]
        self.prepGlyph()
        print(self.glyphName, self.lsb, self.width)
        pen = T2CharStringPen(
            width=self.width, glyphSet=self.glyphSet, roundTolerance=0.5, CFF2=False
        )
        self.drawGlyphToPen(pen)
        topDict.CharStrings.charStringsIndex.items.append(None)
        i = len(topDict.CharStrings.charStringsIndex) - 1
        topDict.CharStrings.charStringsIndex[i] = pen.getCharString(
            private=topDict.Private
        )
        topDict.CharStrings.charStrings[self.glyphName] = i
        # self.ttFont["glyf"][self.glyphName] = pen.glyph()
        self.ttFont["hmtx"][self.glyphName] = (self.width, self.lsb)

    def freezeHints(self):
        if "glyf" in self.ttFont:
            for glyphName in self.glyphNames:
                self.glyphName = glyphName
                self.drawGlyphToTTGlyph()
        elif "CFF " in self.ttFont:
            cff = self.ttFont["CFF "].cff
            cff.desubroutinize()
            for glyphName in self.glyphNames:
                self.glyphName = glyphName
                self.drawGlyphToPSGlyph()


def readFromPath(path, **kwargs):
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
        readFromPath(fontpath),
        fontNumber=subfont,
        ppm=ppm,
        varLocation=var,
        renderMode=mode,
    )
    fhf.freezeHints()
    outpath = (
        Path(out)
        if out
        else Path(f"{Path(fontpath).stem}.fhf-{ppm}-{mode}{Path(fontpath).suffix}")
    )
    fhf.ttFont.save(outpath)
