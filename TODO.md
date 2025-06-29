# TODO List

## Critical Tasks (For Stable Release)

### Error Handling and Validation
- [ ] Add file validation in `read_from_path()` - check file exists and is readable
- [ ] Validate font file format before processing (magic bytes check)
- [ ] Add parameter validation for PPM (must be positive integer)
- [ ] Add parameter validation for mode (must be one of: lcd, lcdv, mono, light)
- [ ] Create custom exception classes (InvalidFontError, InvalidParametersError, etc.)
- [ ] Add proper cleanup on errors (close file handles, free FreeType resources)
- [ ] Add try-except blocks around all FreeType operations
- [ ] Improve error messages to be more user-friendly

### Testing
- [ ] Create test fonts with various characteristics (CFF, variable, malformed)
- [ ] Add unit tests for `FontHintFreezer.__init__()`
- [ ] Add unit tests for `prep_glyph()` method
- [ ] Add unit tests for `draw_glyph_to_point_pen()` method
- [ ] Add unit tests for `draw_glyph_to_tt_glyph()` method
- [ ] Add unit tests for `draw_glyph_to_ps_glyph()` method
- [ ] Add integration tests for CFF/OTF fonts
- [ ] Add integration tests for variable fonts
- [ ] Add error handling tests (malformed fonts, invalid parameters)
- [ ] Add performance benchmarks
- [ ] Set up code coverage reporting

### CFF/OTF Support
- [ ] Investigate current CFF processing bugs
- [ ] Fix CharString indexing issues in `draw_glyph_to_ps_glyph()`
- [ ] Test with various CFF fonts (Type 1, CFF2)
- [ ] Add comprehensive CFF tests
- [ ] Update documentation to reflect CFF support status

### Deployment
- [ ] Complete all pyproject.toml metadata
- [ ] Test package installation in clean virtual environment
- [ ] Set up automated PyPI releases via GitHub Actions
- [ ] Create initial release (0.2.0)
- [ ] Submit to PyPI

## High Priority Tasks

### Variable Font Support
- [ ] Implement comprehensive fvar table parsing
- [ ] Add support for named instances
- [ ] Add `--instance` CLI flag
- [ ] Add `--keep-variations` flag
- [ ] Test with common variable fonts (Roboto, Inter, etc.)
- [ ] Update documentation with variable font examples

### User Experience
- [ ] Add progress indicator using tqdm or rich
- [ ] Add `--quiet` flag to suppress output
- [ ] Add `--verbose` flag for detailed logging
- [ ] Show estimated time remaining for large fonts
- [ ] Improve help text with more examples

### Documentation
- [ ] Add docstrings to all public methods
- [ ] Create API documentation with Sphinx
- [ ] Add troubleshooting guide
- [ ] Document performance characteristics
- [ ] Add more usage examples to README

### Performance
- [ ] Profile code to identify bottlenecks
- [ ] Optimize FreeType object reuse
- [ ] Investigate numpy for coordinate transformations
- [ ] Add benchmark suite to CI

## Medium Priority Tasks

### Architecture Improvements
- [ ] Split FontHintFreezer into smaller classes
- [ ] Create abstract base class for font processors
- [ ] Separate TTF and CFF processing logic
- [ ] Implement strategy pattern for rendering modes
- [ ] Create proper module structure (core/, cli/, utils/)

### Batch Processing
- [ ] Accept glob patterns for input files
- [ ] Add `--output-dir` flag
- [ ] Implement parallel processing with multiprocessing
- [ ] Add `--jobs` flag for parallelism control
- [ ] Create batch operation summary report

### Type Safety
- [ ] Add missing type annotations
- [ ] Enable strict mypy mode
- [ ] Fix all mypy errors
- [ ] Use TypedDict for complex dictionaries
- [ ] Add Protocol types for interfaces

### CLI Enhancements
- [ ] Add `--dry-run` flag
- [ ] Implement config file support
- [ ] Add shell completion scripts
- [ ] Create interactive mode for parameter selection

## Low Priority Tasks

### Ecosystem Integration
- [ ] Add fontTools plugin support
- [ ] Create fontbakery check
- [ ] Add UFO format support
- [ ] Integrate with font editors

### Advanced Features
- [ ] GUI development (tkinter/PyQt)
- [ ] Web interface (Flask/FastAPI)
- [ ] Docker image creation
- [ ] Platform-specific optimizations

### Community
- [ ] Create detailed contribution guidelines
- [ ] Set up issue templates
- [ ] Add code of conduct
- [ ] Write blog posts about use cases
- [ ] Create video tutorials

## Completed Tasks
- [x] Migrate to pyproject.toml
- [x] Add Ruff for linting/formatting
- [x] Add Mypy for type checking
- [x] Set up GitHub Actions CI
- [x] Add basic pytest infrastructure
- [x] Create initial test files
- [x] Add pre-commit hooks
- [x] Update README with modern practices