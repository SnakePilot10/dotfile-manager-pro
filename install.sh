#!/usr/bin/env bash
set -e

echo "🔧 Installing Dotfile Manager Pro (Refactored)..."

# Ensure Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found."
    exit 1
fi

# Create Virtual Environment if missing
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Install Dependencies
echo "⬇️ Installing requirements..."
./.venv/bin/pip install -r requirements.txt

# Setup Alias or Symlink
SHELL_CONFIG="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] && SHELL_CONFIG="$HOME/.zshrc"

# Try to use make install if 'make' is available
if command -v make &> /dev/null; then
    echo "🛠️ Make found. Using Makefile for robust installation..."
    make setup
    make install
    echo "✅ Installation via Makefile complete."
    exit 0
fi

# Fallback: Manual Alias Setup
echo "⚠️ Make not found. Falling back to manual setup..."

# Reinstall package to update entry points
./.venv/bin/pip install -e .

ALIAS_CMD="alias dotfile-pro='$(pwd)/.venv/bin/dotfile-pro'"

if ! grep -Fq "dotfile-pro" "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "# Dotfile Manager Pro" >> "$SHELL_CONFIG"
    echo "$ALIAS_CMD" >> "$SHELL_CONFIG"
    echo "✅ Alias added to $SHELL_CONFIG"
else
    echo "⚠️ Alias already exists."
fi

echo "✨ Installation Complete. Run 'source $SHELL_CONFIG' then 'dotfile-pro'"