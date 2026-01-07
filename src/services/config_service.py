import json
import tempfile
import os
from typing import List, Dict, Any
from pathlib import Path
from src.core.models import Dotfile
from src.core.paths import context
from src.core.exceptions import ConfigError

class ConfigService:
    def __init__(self):
        self.config_path = context.config_path

    def load_config(self) -> List[Dotfile]:
        if not self.config_path.exists():
            return []
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [
                    Dotfile(
                        source=Path(item["source"]),
                        target=Path(item["target"]),
                        profile=item.get("profile", "default")
                    )
                    for item in data
                ]
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load config: {e}")

    def save_config(self, dotfiles: List[Dotfile]) -> None:
        data = [
            {
                "source": str(df.source),
                "target": str(df.target),
                "profile": df.profile
            }
            for df in dotfiles
        ]
        
        # Atomic write: Write to temp file then rename
        try:
            dir_name = self.config_path.parent
            with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name, encoding="utf-8") as tmp:
                json.dump(data, tmp, indent=4)
                tmp_path = Path(tmp.name)
            
            # Atomic replacement
            os.replace(tmp_path, self.config_path)
        except Exception as e:
            if 'tmp_path' in locals() and tmp_path.exists():
                os.unlink(tmp_path)
            raise ConfigError(f"Failed to save config atomically: {e}")

    def add_dotfile(self, dotfile: Dotfile) -> None:
        current_list = self.load_config()
        # Avoid duplicates based on source AND target
        for existing in current_list:
            if existing.source == dotfile.source and existing.target == dotfile.target:
                return # Already exists
        
        current_list.append(dotfile)
        self.save_config(current_list)
