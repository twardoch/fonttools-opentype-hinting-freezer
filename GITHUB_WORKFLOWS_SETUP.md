# GitHub Workflows Setup Instructions

Due to GitHub App permissions restrictions, the workflow files couldn't be created directly in the `.github/workflows/` directory. Please follow these steps to set up the GitHub Actions workflows:

## 1. Create GitHub Workflows Directory

In your local repository, create the GitHub workflows directory:

```bash
mkdir -p .github/workflows
```

## 2. Move Workflow Files

Copy the workflow files from the `github-workflows/` directory to the `.github/workflows/` directory:

```bash
cp github-workflows/ci.yml .github/workflows/ci.yml
cp github-workflows/release.yml .github/workflows/release.yml
```

## 3. Configure PyPI Token (for automated releases)

To enable automated PyPI publishing, you'll need to set up a PyPI token:

1. Go to your repository settings on GitHub
2. Navigate to "Secrets and variables" → "Actions"
3. Add a new repository secret named `PYPI_TOKEN`
4. Get your PyPI token from https://pypi.org/manage/account/token/
5. Paste the token value (including the `pypi-` prefix)

## 4. Commit and Push

```bash
git add .github/workflows/
git commit -m "Add GitHub Actions workflows for CI/CD"
git push origin main
```

## 5. Test the Setup

### Test CI Pipeline
1. Create a feature branch
2. Make a small change
3. Push the branch
4. Create a pull request
5. The CI pipeline should run automatically

### Test Release Pipeline
1. Ensure all tests pass
2. Create and push a git tag:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
3. The release pipeline should run automatically

## Workflow Features

### CI Pipeline (`ci.yml`)
- **Triggers**: Push to main, Pull requests to main
- **Tests**: Python 3.9-3.12 on Linux/macOS/Windows
- **Checks**: Linting, formatting, type checking, tests
- **Coverage**: Reports coverage to Codecov

### Release Pipeline (`release.yml`)
- **Triggers**: Push of tags matching `v*` pattern
- **Builds**: Python packages (wheel/sdist) and standalone binaries
- **Publishes**: To PyPI automatically
- **Releases**: Creates GitHub release with artifacts

### Binary Artifacts
The release pipeline creates standalone binaries for:
- `pyfthintfreeze-linux-x86_64`
- `pyfthintfreeze-macos-x86_64`
- `pyfthintfreeze-windows-x86_64.exe`

## Troubleshooting

### If CI fails:
1. Check the Actions tab in your GitHub repository
2. Look for error messages in the workflow logs
3. Ensure all dependencies are properly specified in `pyproject.toml`

### If release fails:
1. Verify the `PYPI_TOKEN` secret is correctly set
2. Check that the git tag follows semantic versioning (`v1.0.0`)
3. Ensure the repository has proper write permissions

### If binary builds fail:
1. Check that PyInstaller can build the application locally
2. Verify all dependencies are properly bundled
3. Test the binary generation script manually

## Manual Alternative

If you prefer not to use GitHub Actions, you can still use the local scripts:

```bash
# Run tests and build locally
./scripts/build.sh

# Create release locally
./scripts/release.sh v1.0.0

# Upload to PyPI manually
hatch build
twine upload dist/*
```