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
            # 2. Try to find relative to this source file (useful if running from source/venv)
            # path: src/core/paths.py -> repo_root is parents[2]
            source_loc = Path(__file__).resolve()
            possible_root = source_loc.parent.parent.parent
            if (possible_root / "dotfiles.json").exists():
                self.repo_root = possible_root
            else:
                 # 3. Default fallback: ~/dotfiles (Common convention)
                 home_repo = Path.home() / "dotfiles"
                 if (home_repo / "dotfiles.json").exists():
                     self.repo_root = home_repo
                 else:
                    # 4. Fallback to CWD (Legacy behavior, but risky)
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
