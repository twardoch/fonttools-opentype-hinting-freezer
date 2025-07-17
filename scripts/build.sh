#!/bin/bash
# this_file: scripts/build.sh
# OpenType Hinting Freezer - Build Script

set -e

echo "🔧 Building OpenType Hinting Freezer..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade pip
pip install hatch build twine

# Install project dependencies
echo "📦 Installing project dependencies..."
pip install -e .[dev]

# Run linting and formatting
echo "🔍 Running code quality checks..."
hatch run format
hatch run lint
hatch run typecheck

# Run tests
echo "🧪 Running tests..."
hatch run test

# Build the package
echo "📦 Building package..."
hatch run build

echo "✅ Build completed successfully!"