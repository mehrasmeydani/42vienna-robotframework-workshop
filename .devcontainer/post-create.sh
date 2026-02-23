#!/bin/bash
set -euo pipefail

echo "=== Workshop DevContainer Setup ==="

# Step 1: Verify uv is available (installed by devcontainer feature or install here)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "uv version: $(uv version)"

# Step 2: Install Python dependencies from pyproject.toml + uv.lock
echo "Installing dependencies with uv sync..."
uv sync --locked

# Step 3: Initialize Browser Library (install Playwright + Chromium)
echo "Initializing Browser Library (Chromium only — ~250MB download)..."
uv run rfbrowser init chromium

# Step 4: Verify the environment
echo ""
echo "Running environment checks..."
uv run python scripts/check_environment.py

echo ""
echo "=== Setup complete! You are ready for the workshop. ==="
