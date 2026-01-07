from pathlib import Path
from typing import List, Tuple, Dict
from src.services.config_service import ConfigService

import json
from pathlib import Path
from typing import List, Tuple, Dict
from src.services.config_service import ConfigService
from src.core.paths import context

class SystemScanner:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.known_paths = self._load_known_apps()

    def _load_known_apps(self) -> Dict[str, str]:
        """Loads known application paths from JSON resource."""
        json_path = Path(__file__).resolve().parent.parent / "core" / "known_apps.json"
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Fallback in case file is missing
            return {}

    def scan(self) -> List[Tuple[str, Path]]:
        """
        Returns a list of (App Name, Absolute Path) for found unmanaged files.
        """
        candidates = []
        
        # Get set of currently managed real paths for O(1) lookup
        managed_paths = set()
        for df in self.config_service.load_config():
            try:
                # We track the target on the host system
                managed_paths.add(df.expanded_target.resolve())
            except OSError:
                continue

        for app_name, rel_path in self.known_paths.items():
            try:
                full_path = Path.home() / rel_path
                
                # Check existence without following potential broken symlinks first
                if not full_path.exists() and not full_path.is_symlink():
                    continue
                    
                resolved_path = full_path.resolve()
                if resolved_path not in managed_paths:
                    candidates.append((app_name, full_path))
            except (OSError, PermissionError):
                # Skip files we can't access or resolve
                continue
                
        return candidates
