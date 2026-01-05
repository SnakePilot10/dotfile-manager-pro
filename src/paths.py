from pathlib import Path
import os

# Define standard locations
# Using ~/.config/dotfile-manager-pro as the main data directory
APP_NAME = "dotfile-manager-pro"
USER_CONFIG_HOME = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
APP_DIR = USER_CONFIG_HOME / APP_NAME

# The directory where the git repository will be stored (containing the actual dotfiles)
DOTFILES_REPO_PATH = APP_DIR / "dotfiles"

# The configuration file path
CONFIG_FILE = APP_DIR / "config.json"

def ensure_app_dirs():
    """Ensure the application directories exist."""
    APP_DIR.mkdir(parents=True, exist_ok=True)
    DOTFILES_REPO_PATH.mkdir(parents=True, exist_ok=True)
