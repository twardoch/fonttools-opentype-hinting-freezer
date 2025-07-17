#!/bin/bash
# this_file: scripts/test.sh
# OpenType Hinting Freezer - Test Script

set -e

echo "🧪 Running OpenType Hinting Freezer tests..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install hatch
pip install -e .[dev]

# Run different types of tests
echo "🔍 Running linting..."
hatch run lint

echo "🎨 Running formatting check..."
hatch run format --check

echo "🔬 Running type checking..."
hatch run typecheck

echo "🧪 Running unit tests..."
hatch run test

echo "📊 Running tests with coverage..."
hatch run test-cov

echo "✅ All tests passed!"