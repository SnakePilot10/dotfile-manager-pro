#!/bin/bash

# install.sh - Improved installation script aligning with XDG paths

set -e  # Exit on error
set -o pipefail  # Catch errors in pipelines

# Variables
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
DOTFILES_DIR="$XDG_CONFIG_HOME/dotfiles"
BACKUP_DIR="$XDG_CONFIG_HOME/dotfiles_backup"
DOTFILES_REPO="https://github.com/SnakePilot10/dotfiles-repo.git"

# Helper Functions
backup_old_file() {
  local file=$1
  if [[ -e "$file" ]]; then
    echo "Backing up $file to $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
    mv "$file" "$BACKUP_DIR/"
  fi
}

create_symlink() {
  local target=$1
  local link_name=$2
  backup_old_file "$link_name"
  ln -s "$target" "$link_name"
  echo "Symlink created: $link_name -> $target"
}

# Installation Logic
mkdir -p "$DOTFILES_DIR"
echo "Cloning dotfiles repository to $DOTFILES_DIR..."
git clone "$DOTFILES_REPO" "$DOTFILES_DIR"

# Example of syncing XDG_CONFIG_HOME files
for file in "$DOTFILES_DIR/.config/"*; do
  base_name=$(basename "$file")
  create_symlink "$file" "$XDG_CONFIG_HOME/$base_name"
done

# Example of symlinking common home dotfiles
for file in "$DOTFILES_DIR/.*"; do
  case "$file" in
    "."|".."|*.git|*.config) continue;;
  esac
  base_name=$(basename "$file")
  create_symlink "$file" "$HOME/$base_name"
done

echo "Installation complete! Backup available in $BACKUP_DIR."