#!/bin/bash
# this_file: scripts/release.sh
# OpenType Hinting Freezer - Release Script

set -e

# Check if a version tag is provided
if [ -z "$1" ]; then
    echo "❌ Error: Version tag is required"
    echo "Usage: $0 <version>"
    echo "Example: $0 v1.0.0"
    exit 1
fi

VERSION_TAG="$1"

# Validate version tag format (semantic versioning)
if ! [[ "$VERSION_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo "❌ Error: Invalid version format. Expected format: v1.0.0 or v1.0.0-alpha"
    exit 1
fi

echo "🚀 Preparing release $VERSION_TAG..."

# Ensure we're on the main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Warning: Not on main branch. Currently on: $CURRENT_BRANCH"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Error: Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Run full build and test
echo "🔧 Running full build and test..."
./scripts/build.sh

# Create and push the tag
echo "🏷️  Creating tag $VERSION_TAG..."
git tag -a "$VERSION_TAG" -m "Release $VERSION_TAG"
git push origin "$VERSION_TAG"

echo "✅ Release $VERSION_TAG created successfully!"
echo "📦 GitHub Actions will automatically build and publish the release."