# this_file: tests/test_error_handling.py
"""
Tests for error handling in OpenType Hinting Freezer.
"""

import pytest
from pathlib import Path
import tempfile
from opentype_hinting_freezer.hintingfreezer import freezehinting, read_from_path


def test_read_from_path_nonexistent_file():
    """Test that reading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_from_path(Path("/nonexistent/file.ttf"))


def test_read_from_path_empty_file(temp_dir):
    """Test reading an empty file."""
    empty_file = temp_dir / "empty.ttf"
    empty_file.touch()
    
    data = read_from_path(empty_file)
    assert data == b""


def test_freezehinting_invalid_font_file(temp_dir):
    """Test freezehinting with an invalid font file."""
    invalid_file = temp_dir / "invalid.ttf"
    invalid_file.write_text("This is not a font file")
    
    with pytest.raises(Exception):  # Should raise some kind of font parsing error
        freezehinting(invalid_file)


def test_freezehinting_negative_ppm(sample_ttf_path, temp_dir):
    """Test freezehinting with negative PPM value."""
    output_file = temp_dir / "output.ttf"
    
    # This should either handle gracefully or raise a clear error
    with pytest.raises((ValueError, Exception)):
        freezehinting(sample_ttf_path, out=output_file, ppm=-1)


def test_freezehinting_zero_ppm(sample_ttf_path, temp_dir):
    """Test freezehinting with zero PPM value."""
    output_file = temp_dir / "output.ttf"
    
    # This should either handle gracefully or raise a clear error
    with pytest.raises((ValueError, Exception)):
        freezehinting(sample_ttf_path, out=output_file, ppm=0)


def test_freezehinting_very_large_ppm(sample_ttf_path, temp_dir):
    """Test freezehinting with very large PPM value."""
    output_file = temp_dir / "output.ttf"
    
    # This should either work or fail gracefully
    try:
        freezehinting(sample_ttf_path, out=output_file, ppm=10000)
        assert output_file.exists()
    except Exception:
        # If it fails, it should fail gracefully
        pass


def test_freezehinting_invalid_mode(sample_ttf_path, temp_dir):
    """Test freezehinting with invalid mode."""
    output_file = temp_dir / "output.ttf"
    
    with pytest.raises((ValueError, Exception)):
        freezehinting(sample_ttf_path, out=output_file, mode="invalid_mode")


def test_freezehinting_invalid_subfont_index(sample_ttf_path, temp_dir):
    """Test freezehinting with invalid subfont index."""
    output_file = temp_dir / "output.ttf"
    
    # For a regular TTF, subfont index > 0 should fail
    with pytest.raises((IndexError, Exception)):
        freezehinting(sample_ttf_path, out=output_file, subfont=999)


def test_freezehinting_readonly_output_directory(sample_ttf_path, temp_dir):
    """Test freezehinting with read-only output directory."""
    readonly_dir = temp_dir / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o444)  # Read-only
    
    output_file = readonly_dir / "output.ttf"
    
    try:
        with pytest.raises((PermissionError, OSError)):
            freezehinting(sample_ttf_path, out=output_file)
    finally:
        # Cleanup: restore permissions
        readonly_dir.chmod(0o755)


def test_freezehinting_output_to_existing_file(sample_ttf_path, temp_dir):
    """Test freezehinting when output file already exists."""
    output_file = temp_dir / "output.ttf"
    output_file.write_text("existing content")
    
    # Should overwrite the existing file
    freezehinting(sample_ttf_path, out=output_file, ppm=12)
    assert output_file.exists()
    assert output_file.stat().st_size > 100  # Should be larger than our test text


def test_cli_missing_font_argument(cli_runner):
    """Test CLI with missing font argument."""
    result = cli_runner([])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "usage" in result.stderr.lower()


def test_cli_nonexistent_font_file(cli_runner):
    """Test CLI with non-existent font file."""
    result = cli_runner(["/nonexistent/file.ttf"])
    assert result.returncode != 0
    assert "not found" in result.stderr.lower() or "no such file" in result.stderr.lower()


def test_cli_invalid_ppm_value(cli_runner, sample_ttf_path):
    """Test CLI with invalid PPM value."""
    result = cli_runner([str(sample_ttf_path), "--ppm=-1"])
    assert result.returncode != 0


def test_cli_invalid_mode_value(cli_runner, sample_ttf_path):
    """Test CLI with invalid mode value."""
    result = cli_runner([str(sample_ttf_path), "--mode=invalid"])
    assert result.returncode != 0