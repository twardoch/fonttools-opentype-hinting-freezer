# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with Pytest
  - Unit tests for core functionality
  - Integration tests for CLI
  - Test data generation utilities
- Type hints throughout the codebase
- Pre-commit hooks for code quality (Ruff, Mypy)
- GitHub Actions CI/CD workflow
- Development documentation in README
- Modern Python packaging with pyproject.toml

### Changed
- Migrated from setup.py to pyproject.toml with Hatch build system
- Integrated hatch-vcs for Git tag-based versioning
- Replaced manual code formatting with Ruff
- Enhanced code quality with static type checking (Mypy)
- Updated Python requirement to >=3.9
- Improved CLI error handling and help messages
- Modernized project structure and documentation

### Fixed
- Type safety issues throughout the codebase
- Various code style inconsistencies

### Removed
- Obsolete setup.py file
- requirements.txt (dependencies now in pyproject.toml)

## [0.1.0] - 2022-01-14

### Added
- Initial release of OpenType Hinting Freezer
- Core functionality to freeze TrueType hinting at specific PPM sizes
- Command-line interface `pyfthintfreeze`
- Support for TTF fonts (OTF support is experimental)
- Multiple rendering modes: LCD, LCD-V, mono, light
- Variable font support (basic)
- TrueType Collection (TTC) support
- Apache 2.0 license

[Unreleased]: https://github.com/twardoch/fonttools-opentype-hinting-freezer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/twardoch/fonttools-opentype-hinting-freezer/releases/tag/v0.1.0