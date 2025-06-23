import pytest
from pathlib import Path
import subprocess
import sys

# Helper to get the path to the pyfthintfreeze executable script
# This might need adjustment depending on how the CLI is installed/run in test env
# For an editable install, `pyfthintfreeze` should be on the PATH within the venv.
CLI_EXECUTABLE = "pyfthintfreeze"
TEST_DIR = Path(__file__).parent
SAMPLE_TTF = TEST_DIR / "data" / "minimal.ttf"
OUTPUT_DIR = TEST_DIR / "output"


def run_cli_command(args: list[str]) -> subprocess.CompletedProcess:
    """Runs the CLI tool with the given arguments."""
    command = [CLI_EXECUTABLE] + args
    # In some environments, it might be necessary to run `python -m opentype_hinting_freezer ...`
    # or directly sys.executable + ["-m", "opentype_hinting_freezer..."]
    # For now, assume pyfthintfreeze is on the PATH (e.g., in an activated venv with editable install)
    return subprocess.run(command, capture_output=True, text=True, check=False)


@pytest.fixture(scope="module", autouse=True)
def ensure_sample_ttf_exists():
    """Ensure the sample TTF exists before tests run."""
    if not SAMPLE_TTF.exists():
        pytest.fail(
            f"Sample TTF file missing: {SAMPLE_TTF}. "
            "Run tests/generate_minimal_ttf.py to create it."
        )

@pytest.fixture(autouse=True)
def manage_output_dir():
    """Creates and cleans up the output directory for each test."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    yield
    # Cleanup: Remove files from output directory after test
    for item in OUTPUT_DIR.iterdir():
        item.unlink()
    # Try to remove the directory if it's empty, ignore if it fails (e.g. other files)
    try:
        OUTPUT_DIR.rmdir()
    except OSError:
        pass


def test_cli_basic_run_creates_output():
    """Test a basic CLI run creates an output file."""
    output_filename = "minimal.fhf-12-mono.ttf"
    args = [
        str(SAMPLE_TTF),
        "--ppm=12",
        "--mode=mono",
        f"--out={OUTPUT_DIR / output_filename}",
    ]
    result = run_cli_command(args)

    assert result.returncode == 0, f"CLI errored: {result.stderr}"
    output_file = OUTPUT_DIR / output_filename
    assert output_file.exists(), f"Output file was not created: {output_file}"
    assert output_file.stat().st_size > 0, "Output file is empty"

    # TODO: Add more checks, e.g., try to load the output with fontTools
    # from fontTools.ttLib import TTFont
    # try:
    #     TTFont(output_file)
    # except Exception as e:
    #     pytest.fail(f"Output file is not a valid TTF: {e}")


def test_cli_help_message():
    """Test that the CLI shows a help message."""
    result_help = run_cli_command(["--help"])
    # Python-fire prints help to stderr.
    command_name_in_help = "NAME\n    pyfthintfreeze"
    synopsis_in_help = "SYNOPSIS\n    pyfthintfreeze FONTPATH <flags>"
    # The specific description from the docstring's first line might not appear
    # in the main --help output in a straightforward way with Fire for single functions.
    # Focusing on essential help components.

    # Fire usually exits with 0 when displaying help.
    assert result_help.returncode == 0, \
        f"CLI --help exited with {result_help.returncode}.\nstderr: {result_help.stderr}\nstdout: {result_help.stdout}"

    # Check that key structural elements are in stderr
    assert command_name_in_help in result_help.stderr, \
        f"Command name section not found in stderr.\nstderr: {result_help.stderr}"
    assert synopsis_in_help in result_help.stderr, \
        f"Synopsis section not found in stderr.\nstderr: {result_help.stderr}"
    # Check for presence of key arguments/flags
    assert "FONTPATH" in result_help.stderr, \
        f"Positional argument 'FONTPATH' not found in help (stderr).\nstderr: {result_help.stderr}"
    assert "--ppm" in result_help.stderr, \
        f"Flag '--ppm' not found in help (stderr).\nstderr: {result_help.stderr}"
    assert "--mode" in result_help.stderr, \
        f"Flag '--mode' not found in help (stderr).\nstderr: {result_help.stderr}"


# More integration tests can be added here:
# - Different modes
# - Different PPM values
# - Output path auto-generation
# - Handling of TTC files (if sample TTC is available)
# - Variable font functionality (if sample variable font is available and func is complete)
# - Error conditions (e.g., invalid font file, invalid params)
