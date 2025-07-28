import pytest
from pathlib import Path
from opentype_hinting_freezer.hintingfreezer import read_from_path

# Get the directory of the current test file
TEST_DIR = Path(__file__).parent


def test_read_from_path_success():
    """Test successfully reading data from a file."""
    sample_file_path = TEST_DIR / "sample_data.bin"
    # create_file_with_block adds a newline at the end of the file.
    expected_content = b"This is test data.\n"

    # Ensure the file exists for the test (it should, from previous step)
    assert sample_file_path.exists(), "Test data file is missing!"

    file_content = read_from_path(sample_file_path)
    assert file_content == expected_content


def test_read_from_path_file_not_found():
    """Test FileNotFoundError when reading a non-existent file."""
    non_existent_file = TEST_DIR / "non_existent_file.bin"
    with pytest.raises(FileNotFoundError):
        read_from_path(non_existent_file)

# More unit tests will be added here for other functions/methods
# in hintingfreezer.py, such as parts of FontHintFreezer.
# For now, this is a starting point.

# Example of a placeholder for a more complex test:
# def test_font_hint_freezer_initialization():
#     # This would require a minimal TTF/OTF file or mocked font data
#     # from opentype_hinting_freezer.hintingfreezer import FontHintFreezer
#     # sample_ttf_path = TEST_DIR / "sample.ttf" # Create this file
#     # font_data = read_from_path(sample_ttf_path)
#     # freezer = FontHintFreezer(font_data=font_data, ppm=12, render_mode="mono")
#     # assert freezer.ppm == 12
#     # assert freezer.upm > 0 # Basic check
#     pass
