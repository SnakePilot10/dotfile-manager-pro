from pathlib import Path
import os
import sys

class AppContext:
    def __init__(self):
        # 1. Try Environment Variable
        env_repo = os.getenv("DOTFILE_REPO")
        if env_repo:
            self.repo_root = Path(env_repo).resolve()
        else:
            # 2. Default to CWD (Standard "Stow-like" behavior)
            self.repo_root = Path(os.getcwd()).resolve()

        self.config_path = self.repo_root / "dotfiles.json"
        self.backup_dir = self.repo_root / ".backups"

    def verify_repo(self) -> bool:
        """Returns True if a valid repo structure is found."""
        return self.config_path.exists()

    def get_absolute_source(self, relative_source: Path) -> Path:
        return (self.repo_root / relative_source).resolve()

# Singleton instance
context = AppContext()
