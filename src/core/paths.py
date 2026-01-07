from pathlib import Path
import os

class AppContext:
    def __init__(self):
        # Allow overriding the repo root via env var, else assume current working dir
        # or a specific standard location. For this refactor, we stick to CWD 
        # as the 'repo' to maintain behavior with the existing structure, 
        # but sanitized.
        self.repo_root = Path(os.getcwd()).resolve()
        self.config_path = self.repo_root / "dotfiles.json"
        self.backup_dir = self.repo_root / ".backups"

    def get_absolute_source(self, relative_source: Path) -> Path:
        return (self.repo_root / relative_source).resolve()

# Singleton instance for easy access
context = AppContext()
