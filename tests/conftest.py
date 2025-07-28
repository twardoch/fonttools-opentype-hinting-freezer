# this_file: tests/conftest.py
"""
Pytest configuration and fixtures for OpenType Hinting Freezer tests.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import subprocess
import sys
from typing import Generator

# Test directories
TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / "data"
OUTPUT_DIR = TEST_DIR / "output"

# Sample files
SAMPLE_TTF = DATA_DIR / "minimal.ttf"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Returns the test data directory."""
    return DATA_DIR


@pytest.fixture(scope="session")
def sample_ttf_path() -> Path:
    """Returns the path to the sample TTF file."""
    if not SAMPLE_TTF.exists():
        pytest.fail(
            f"Sample TTF file missing: {SAMPLE_TTF}. "
            "Run tests/generate_minimal_ttf.py to create it."
        )
    return SAMPLE_TTF


@pytest.fixture
def output_dir() -> Generator[Path, None, None]:
    """Creates a temporary output directory for each test."""
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    yield output_dir
    
    # Cleanup: Remove files from output directory after test
    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        try:
            output_dir.rmdir()
        except OSError:
            pass


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Creates a temporary directory for each test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def cli_runner():
    """Returns a function to run CLI commands."""
    def run_command(args: list[str]) -> subprocess.CompletedProcess:
        """Runs the CLI tool with the given arguments."""
        # Try different ways to run the CLI
        cli_commands = [
            ["pyfthintfreeze"] + args,
            [sys.executable, "-m", "opentype_hinting_freezer"] + args,
            [sys.executable, "-m", "opentype_hinting_freezer.__main__"] + args,
        ]
        
        for cmd in cli_commands:
            try:
                return subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    check=False,
                    timeout=30
                )
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        # If all methods fail, raise an error
        raise RuntimeError("Could not find a way to run the CLI")
    
    return run_command


@pytest.fixture(scope="session", autouse=True)
def ensure_test_data():
    """Ensures test data files exist before running tests."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    
    # Generate minimal TTF if it doesn't exist
    if not SAMPLE_TTF.exists():
        generate_script = TEST_DIR / "generate_minimal_ttf.py"
        if generate_script.exists():
            subprocess.run([sys.executable, str(generate_script)], check=True)
        else:
            pytest.fail(f"Cannot generate test data: {generate_script} not found")