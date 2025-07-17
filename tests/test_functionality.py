# this_file: tests/test_functionality.py
"""
Tests for core functionality of OpenType Hinting Freezer.
"""

import pytest
from pathlib import Path
from opentype_hinting_freezer.hintingfreezer import freezehinting
from fontTools.ttLib import TTFont


def test_freezehinting_basic_functionality(sample_ttf_path, temp_dir):
    """Test basic freezehinting functionality."""
    output_file = temp_dir / "output.ttf"
    
    # Run freezehinting
    freezehinting(sample_ttf_path, out=output_file, ppm=12, mode="mono")
    
    # Check that output file exists and is non-empty
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    
    # Check that output is a valid TTF
    try:
        font = TTFont(output_file)
        assert len(font.getGlyphNames()) > 0
    except Exception as e:
        pytest.fail(f"Output file is not a valid TTF: {e}")


def test_freezehinting_different_ppm_values(sample_ttf_path, temp_dir):
    """Test freezehinting with different PPM values."""
    ppm_values = [10, 12, 16, 24, 48]
    
    for ppm in ppm_values:
        output_file = temp_dir / f"output_{ppm}.ttf"
        freezehinting(sample_ttf_path, out=output_file, ppm=ppm, mode="mono")
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0


def test_freezehinting_different_modes(sample_ttf_path, temp_dir):
    """Test freezehinting with different rendering modes."""
    modes = ["mono", "lcd", "lcdv", "light"]
    
    for mode in modes:
        output_file = temp_dir / f"output_{mode}.ttf"
        freezehinting(sample_ttf_path, out=output_file, ppm=12, mode=mode)
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0


def test_freezehinting_auto_output_name(sample_ttf_path, temp_dir):
    """Test freezehinting with automatic output filename generation."""
    # Change to temp directory to control where output goes
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(temp_dir)
        
        freezehinting(sample_ttf_path, ppm=12, mode="mono")
        
        # Check for auto-generated filename
        expected_filename = f"{sample_ttf_path.stem}.fhf-12-mono.ttf"
        output_file = temp_dir / expected_filename
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        
    finally:
        os.chdir(original_cwd)


def test_freezehinting_preserves_basic_font_structure(sample_ttf_path, temp_dir):
    """Test that freezehinting preserves basic font structure."""
    output_file = temp_dir / "output.ttf"
    
    # Load original font
    original_font = TTFont(sample_ttf_path)
    original_glyphs = set(original_font.getGlyphNames())
    
    # Run freezehinting
    freezehinting(sample_ttf_path, out=output_file, ppm=12, mode="mono")
    
    # Load output font
    output_font = TTFont(output_file)
    output_glyphs = set(output_font.getGlyphNames())
    
    # Check that glyph names are preserved
    assert original_glyphs == output_glyphs
    
    # Check that basic tables are present
    required_tables = ['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post']
    for table in required_tables:
        if table in original_font:
            assert table in output_font, f"Table {table} missing from output"


def test_freezehinting_with_variable_font_location(sample_ttf_path, temp_dir):
    """Test freezehinting with variable font location (if applicable)."""
    output_file = temp_dir / "output.ttf"
    
    # This test will pass for non-variable fonts (var parameter is ignored)
    # For variable fonts, it should work with valid locations
    var_location = {"wght": 400}
    
    freezehinting(sample_ttf_path, out=output_file, ppm=12, mode="mono", var=var_location)
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_cli_basic_functionality(cli_runner, sample_ttf_path, temp_dir):
    """Test CLI basic functionality."""
    output_file = temp_dir / "cli_output.ttf"
    
    result = cli_runner([
        str(sample_ttf_path),
        "--ppm=12",
        "--mode=mono",
        f"--out={output_file}"
    ])
    
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_cli_auto_output_name(cli_runner, sample_ttf_path, temp_dir):
    """Test CLI with automatic output filename generation."""
    # Change to temp directory
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(temp_dir)
        
        result = cli_runner([
            str(sample_ttf_path),
            "--ppm=12",
            "--mode=mono"
        ])
        
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        
        # Check for auto-generated filename
        expected_filename = f"{sample_ttf_path.stem}.fhf-12-mono.ttf"
        output_file = temp_dir / expected_filename
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        
    finally:
        os.chdir(original_cwd)


def test_cli_help_shows_all_options(cli_runner):
    """Test that CLI help shows all expected options."""
    result = cli_runner(["--help"])
    
    assert result.returncode == 0
    help_text = result.stderr.lower()
    
    # Check for key options
    expected_options = ["ppm", "mode", "out", "subfont", "var"]
    for option in expected_options:
        assert option in help_text, f"Option {option} not found in help text"
    
    # Check for mode descriptions
    expected_modes = ["mono", "lcd", "lcdv", "light"]
    for mode in expected_modes:
        assert mode in help_text, f"Mode {mode} not found in help text"


def test_freezehinting_consistent_output(sample_ttf_path, temp_dir):
    """Test that freezehinting produces consistent output for same parameters."""
    output_file_1 = temp_dir / "output1.ttf"
    output_file_2 = temp_dir / "output2.ttf"
    
    # Run freezehinting twice with same parameters
    freezehinting(sample_ttf_path, out=output_file_1, ppm=12, mode="mono")
    freezehinting(sample_ttf_path, out=output_file_2, ppm=12, mode="mono")
    
    # Files should be identical
    assert output_file_1.read_bytes() == output_file_2.read_bytes()


def test_freezehinting_different_outputs_for_different_params(sample_ttf_path, temp_dir):
    """Test that different parameters produce different outputs."""
    output_file_1 = temp_dir / "output1.ttf"
    output_file_2 = temp_dir / "output2.ttf"
    
    # Run with different PPM values
    freezehinting(sample_ttf_path, out=output_file_1, ppm=12, mode="mono")
    freezehinting(sample_ttf_path, out=output_file_2, ppm=24, mode="mono")
    
    # Files should be different
    assert output_file_1.read_bytes() != output_file_2.read_bytes()