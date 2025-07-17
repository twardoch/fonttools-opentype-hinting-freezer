# Development Guide

## Git Tag Based Semversioning

This project uses git tags for semantic versioning. The version is automatically extracted from git tags using `hatch-vcs`.

### Version Format

- Use semantic versioning: `v1.0.0`, `v1.0.1`, `v1.1.0`, `v2.0.0`
- Pre-release versions: `v1.0.0-alpha`, `v1.0.0-beta`, `v1.0.0-rc1`

### Creating a Release

1. **Local Development Setup**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```

2. **Run Tests and Build**
   ```bash
   ./scripts/test.sh
   ./scripts/build.sh
   ```

3. **Create and Push Release Tag**
   ```bash
   ./scripts/release.sh v1.0.0
   ```

### Manual Release Process

If you prefer manual control:

1. **Ensure clean working directory**
   ```bash
   git status
   ```

2. **Run full test suite**
   ```bash
   hatch run test
   hatch run test-cov
   ```

3. **Create and push tag**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

4. **GitHub Actions will automatically**:
   - Run tests on all supported platforms
   - Build Python packages (wheel and sdist)
   - Build standalone binaries for Linux, macOS, and Windows
   - Publish to PyPI
   - Create GitHub release with artifacts

## Local Testing

### Quick Tests (fast)
```bash
hatch run test-fast
```

### Full Test Suite (includes slow tests)
```bash
hatch run test
```

### Performance Tests
```bash
hatch run test-slow
```

### Code Quality Checks
```bash
hatch run check
```

### Coverage Report
```bash
hatch run test-cov
```

## CI/CD Pipeline

**⚠️ SETUP REQUIRED**: The GitHub Actions workflows need to be manually set up due to permissions restrictions. See `GITHUB_WORKFLOWS_SETUP.md` for detailed instructions.

### Continuous Integration (CI)

Triggers on:
- Push to `main` branch
- Pull requests to `main` branch

Runs:
- Tests on Python 3.9, 3.10, 3.11, 3.12
- Tests on Linux, macOS, Windows
- Code quality checks (linting, formatting, type checking)
- Test coverage reporting

### Release Pipeline

Triggers on:
- Push of tags matching `v*` pattern

Runs:
- Full test suite on all platforms
- Package building (Python packages)
- Binary building (standalone executables)
- PyPI publishing
- GitHub release creation

## Binary Releases

The CI pipeline automatically creates standalone binaries for:
- Linux x86_64 (`pyfthintfreeze-linux-x86_64`)
- macOS x86_64 (`pyfthintfreeze-macos-x86_64`)
- Windows x86_64 (`pyfthintfreeze-windows-x86_64.exe`)

Users can download these from the GitHub releases page.

## Development Workflow

1. **Clone and setup**
   ```bash
   git clone https://github.com/twardoch/fonttools-opentype-hinting-freezer.git
   cd fonttools-opentype-hinting-freezer
   ./scripts/build.sh
   ```

2. **Make changes**
   - Edit code
   - Add/update tests
   - Update documentation

3. **Test locally**
   ```bash
   hatch run check
   hatch run test
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin your-branch
   ```

5. **Create pull request**
   - CI will run automatically
   - Review and merge

6. **Create release** (maintainers only)
   ```bash
   ./scripts/release.sh v1.0.0
   ```

## Troubleshooting

### Version not updating from git tags

If the version isn't being picked up from git tags:

1. Ensure you have `hatch-vcs` installed:
   ```bash
   pip install hatch-vcs
   ```

2. Check that git tags are accessible:
   ```bash
   git tag -l
   git describe --tags
   ```

3. For local development, hatch-vcs will use the current git state

### Tests failing

1. Ensure test data exists:
   ```bash
   python tests/generate_minimal_ttf.py
   ```

2. Check that all dependencies are installed:
   ```bash
   pip install -e .[dev]
   ```

3. Run tests with verbose output:
   ```bash
   hatch run test -v
   ```

### Build failures

1. Clean build artifacts:
   ```bash
   hatch run clean
   ```

2. Reinstall dependencies:
   ```bash
   pip install -e .[dev]
   ```

3. Check for environment issues:
   ```bash
   hatch run build
   ```