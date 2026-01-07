from dataclasses import dataclass
from pathlib import Path

@dataclass
class Dotfile:
    source: Path  # Path relative to the repo (e.g., "zsh/.zshrc")
    target: Path  # Path on the host system (e.g., "~/.zshrc")
    profile: str = "default"

    def __post_init__(self):
        # Ensure paths are Path objects
        if isinstance(self.source, str):
            self.source = Path(self.source)
        if isinstance(self.target, str):
            self.target = Path(self.target)

    @property
    def expanded_target(self) -> Path:
        """Returns the fully resolved target path (expands ~)."""
        return self.target.expanduser().resolve()
