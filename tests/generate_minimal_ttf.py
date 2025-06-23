from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.pens.ttGlyphPen import TTGlyphPen

def create_minimal_ttf(filepath="tests/data/minimal.ttf"):
    """
    Creates a very minimal, valid TTF file with a single .notdef glyph.
    """
    fb = FontBuilder(1024, isTTF=True)
    fb.setupGlyphOrder([".notdef"])
    fb.setupCharacterMap({0: ".notdef"})  # Map U+0000 to .notdef

    # Create a .notdef glyph (e.g., a simple box)
    pen = TTGlyphPen(None)
    pen.moveTo((100, 100))
    pen.lineTo((100, 500))
    pen.lineTo((400, 500))
    pen.lineTo((400, 100))
    pen.closePath()
    glyph = pen.glyph()

    # Setup glyf table before assigning to it
    fb.setupGlyf({})
    fb.font["glyf"][".notdef"] = glyph
    glyph.recalcBounds(fb.font["glyf"]) # Now this should work

    fb.font["hmtx"] = {".notdef": (500, 100)} # width, lsb
    # fb.font["loca"] # loca is built by setupMaxp/save if not explicitly done

    # Add other required tables in a more robust order
    name_records = {
        1: "Minimal Test Font",  # Family Name
        2: "Regular",            # Style Name (Subfamily)
        3: "Minimal Test Font Regular Unique", # Unique font identifier
        4: "Minimal Test Font Regular",      # Full font name
        6: "MinimalTestFont-Regular",        # PostScript name
        5: "Version 0.1"         # Version string
    }
    fb.setupNameTable(name_records)
    fb.setupHead(unitsPerEm=1024, created=0, modified=0) # Add created/modified
    fb.setupHorizontalHeader(ascent=800, descent=-200) # Provide some default values
    fb.setupHorizontalMetrics(fb.font["hmtx"]) # Pass the hmtx dict
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800, usWinDescent=200, achVendID="TEST") # Add some required OS/2 fields
    fb.setupPost(isFixedPitch=0, minMemType42=0, maxMemType42=0, minMemType1=0, maxMemType1=0)
    fb.setupMaxp() # Crucial, calculates numGlyphs etc.

    fb.save(filepath)
    print(f"Minimal TTF saved to {filepath}")

if __name__ == "__main__":
    import os
    if not os.path.exists("tests/data"):
        os.makedirs("tests/data")
    create_minimal_ttf()
