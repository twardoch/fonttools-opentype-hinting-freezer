# this_file: tests/test_performance.py
"""
Performance tests for OpenType Hinting Freezer.
"""

import pytest
import time
from pathlib import Path
from opentype_hinting_freezer.hintingfreezer import freezehinting


@pytest.mark.slow
def test_freezehinting_performance_benchmark(sample_ttf_path, temp_dir):
    """Test freezehinting performance benchmark."""
    output_file = temp_dir / "benchmark_output.ttf"
    
    # Measure performance
    start_time = time.time()
    freezehinting(sample_ttf_path, out=output_file, ppm=12, mode="mono")
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    # Check that output exists
    assert output_file.exists()
    
    # Performance assertion - should complete in reasonable time
    # This is a basic test, adjust threshold based on your needs
    assert processing_time < 10.0, f"Processing took too long: {processing_time:.2f}s"
    
    # Log the performance for monitoring
    print(f"Processing time: {processing_time:.2f}s")


@pytest.mark.slow
def test_freezehinting_memory_usage(sample_ttf_path, temp_dir):
    """Test memory usage during freezehinting."""
    import psutil
    import os
    
    output_file = temp_dir / "memory_test_output.ttf"
    
    # Get process
    process = psutil.Process(os.getpid())
    
    # Measure memory before
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Run freezehinting
    freezehinting(sample_ttf_path, out=output_file, ppm=12, mode="mono")
    
    # Measure memory after
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    
    memory_increase = memory_after - memory_before
    
    # Check that output exists
    assert output_file.exists()
    
    # Memory assertion - should not use excessive memory
    assert memory_increase < 100, f"Memory usage too high: {memory_increase:.2f}MB"
    
    # Log the memory usage for monitoring
    print(f"Memory increase: {memory_increase:.2f}MB")


@pytest.mark.slow
def test_multiple_ppm_values_performance(sample_ttf_path, temp_dir):
    """Test performance with multiple PPM values."""
    ppm_values = [10, 12, 14, 16, 18, 20, 24, 32, 48]
    
    start_time = time.time()
    
    for ppm in ppm_values:
        output_file = temp_dir / f"multi_ppm_{ppm}.ttf"
        freezehinting(sample_ttf_path, out=output_file, ppm=ppm, mode="mono")
        assert output_file.exists()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(ppm_values)
    
    # Should complete all PPM values in reasonable time
    assert total_time < 60.0, f"Total processing time too long: {total_time:.2f}s"
    assert avg_time < 10.0, f"Average processing time too long: {avg_time:.2f}s"
    
    print(f"Total time for {len(ppm_values)} PPM values: {total_time:.2f}s")
    print(f"Average time per PPM: {avg_time:.2f}s")


@pytest.mark.slow
def test_all_modes_performance(sample_ttf_path, temp_dir):
    """Test performance with all rendering modes."""
    modes = ["mono", "lcd", "lcdv", "light"]
    
    start_time = time.time()
    
    for mode in modes:
        output_file = temp_dir / f"mode_{mode}.ttf"
        freezehinting(sample_ttf_path, out=output_file, ppm=12, mode=mode)
        assert output_file.exists()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(modes)
    
    # Should complete all modes in reasonable time
    assert total_time < 30.0, f"Total processing time too long: {total_time:.2f}s"
    assert avg_time < 10.0, f"Average processing time too long: {avg_time:.2f}s"
    
    print(f"Total time for {len(modes)} modes: {total_time:.2f}s")
    print(f"Average time per mode: {avg_time:.2f}s")


def test_cli_performance_benchmark(cli_runner, sample_ttf_path, temp_dir):
    """Test CLI performance benchmark."""
    output_file = temp_dir / "cli_benchmark_output.ttf"
    
    start_time = time.time()
    
    result = cli_runner([
        str(sample_ttf_path),
        "--ppm=12",
        "--mode=mono",
        f"--out={output_file}"
    ])
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert output_file.exists()
    
    # CLI should complete in reasonable time (includes Python startup overhead)
    assert processing_time < 15.0, f"CLI processing took too long: {processing_time:.2f}s"
    
    print(f"CLI processing time: {processing_time:.2f}s")