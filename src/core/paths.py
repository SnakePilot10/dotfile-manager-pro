from pathlib import Path
import os
import sys

class AppContext:
    def __init__(self):
        # 1. Environment Variable (Explicit override)
        env_repo = os.getenv("DOTFILE_REPO")
        
        # 2. Current Working Directory (Standard behavior)
        cwd = Path(os.getcwd()).resolve()
        
        # 3. Convention fallback
        home_repo = Path.home() / "dotfiles"

        if env_repo:
            self.repo_root = Path(env_repo).resolve()
        elif (cwd / "dotfiles.json").exists():
            self.repo_root = cwd
        elif (home_repo / "dotfiles.json").exists():
            self.repo_root = home_repo
        else:
            # Fallback: Assume CWD is where we want to initialize or operate
            self.repo_root = cwd

        self.config_path = self.repo_root / "dotfiles.json"
        self.backup_dir = self.repo_root / ".backups"

    def verify_repo(self) -> bool:
        """Returns True if a valid repo structure is found."""
        return self.config_path.exists()

    def get_absolute_source(self, relative_source: Path) -> Path:
        return (self.repo_root / relative_source).resolve()

# Singleton instance
context = AppContext()
