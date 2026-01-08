import json
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Set
from services.config_service import ConfigService

class SystemScanner:
    # Carpetas a ignorar completamente para evitar ruido y lentitud
    EXCLUDE_DIRS = {
        "node_modules", ".git", ".svn", "__pycache__", ".venv", "venv", "env",
        ".cache", ".local", ".npm", ".cargo", ".gnupg", ".mozilla", ".chrome",
        "Downloads", "Music", "Pictures", "Videos", "Documents", "Android",
        ".gemini", ".termux/boot" # Ignorar boot scripts, solo configs
    }

    # Extensiones de configuración válidas para el escaneo heurístico
    CONFIG_EXTENSIONS = {
        ".conf", ".ini", ".toml", ".yaml", ".yml", ".json", ".lua", ".cfg", ".rc", ""
    }

    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.known_paths = self._load_known_apps()
        self.home = Path.home()

    def _load_known_apps(self) -> Dict[str, str]:
        """Carga rutas conocidas desde el JSON."""
        json_path = Path(__file__).resolve().parent.parent / "core" / "known_apps.json"
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def scan(self) -> List[Tuple[str, Path]]:
        """
        Escaneo híbrido: Conocidos + Heurístico.
        """
        candidates: List[Tuple[str, Path]] = []
        seen_paths: Set[Path] = set()

        # 1. Obtener archivos ya gestionados
        managed_paths = set()
        for df in self.config_service.load_config():
            try:
                managed_paths.add(df.expanded_target.resolve())
            except OSError:
                continue

        # 2. Escaneo de Apps Conocidas (Alta prioridad)
        for app_name, rel_path in self.known_paths.items():
            try:
                full_path = self.home / rel_path
                if not self._is_valid_candidate(full_path):
                    continue
                
                resolved = full_path.resolve()
                if resolved not in managed_paths and resolved not in seen_paths:
                    candidates.append((app_name, full_path))
                    seen_paths.add(resolved)
            except (OSError, PermissionError):
                continue

        # 3. Escaneo Heurístico en ~/.config (Profundidad 2)
        # Busca ~/.config/app/config.toml
        config_dir = self.home / ".config"
        if config_dir.exists():
            candidates.extend(
                self._scan_directory(
                    config_dir, 
                    managed_paths, 
                    seen_paths, 
                    max_depth=2, 
                    prefix="Config"
                )
            )

        # 4. Escaneo Heurístico en ~/.termux (Específico Termux)
        termux_dir = self.home / ".termux"
        if termux_dir.exists():
             candidates.extend(
                self._scan_directory(
                    termux_dir, 
                    managed_paths, 
                    seen_paths, 
                    max_depth=1, 
                    prefix="Termux"
                )
            )

        # 5. Escaneo Heurístico en ~ (Solo archivos ocultos, Profundidad 0)
        # Busca .editorconfig, .mytorc, etc.
        candidates.extend(self._scan_root(managed_paths, seen_paths))

        return sorted(candidates, key=lambda x: x[0])

    def _is_valid_candidate(self, path: Path) -> bool:
        """Verifica si el archivo existe y no es un enlace roto."""
        return path.exists() or path.is_symlink()

    def _scan_directory(self, root: Path, managed: Set[Path], seen: Set[Path], max_depth: int, prefix: str) -> List[Tuple[str, Path]]:
        found = []
        root_depth = len(root.parts)

        for dirpath, dirnames, filenames in os.walk(root):
            path_obj = Path(dirpath)
            current_depth = len(path_obj.parts) - root_depth
            
            # Control de profundidad y exclusiones
            if current_depth >= max_depth:
                dirnames[:] = [] # Stop recursion
                continue

            # Eliminar carpetas ignoradas in-place
            dirnames[:] = [d for d in dirnames if d not in self.EXCLUDE_DIRS]

            for file in filenames:
                file_path = path_obj / file
                
                # Filtrar por extensión
                if file_path.suffix not in self.CONFIG_EXTENSIONS and not file.startswith("."):
                    continue
                
                # Ignorar archivos temporales comunes
                if file.endswith("~") or file.endswith(".bak") or file.endswith(".swp"):
                    continue

                try:
                    resolved = file_path.resolve()
                    if resolved not in managed and resolved not in seen:
                        # Nombre amigable: "Config: nvim/init.lua"
                        rel_name = file_path.relative_to(root)
                        name = f"{prefix}: {rel_name}"
                        found.append((name, file_path))
                        seen.add(resolved)
                except (OSError, PermissionError):
                    continue
        return found

    def _scan_root(self, managed: Set[Path], seen: Set[Path]) -> List[Tuple[str, Path]]:
        found = []
        try:
            for item in self.home.iterdir():
                # Solo archivos, solo ocultos (dotfiles)
                if item.is_file() and item.name.startswith("."):
                    # Exclusiones específicas de raíz
                    if item.name in [".bash_history", ".zsh_history", ".lesshst", ".viminfo", ".DS_Store"]:
                        continue
                        
                    # Filtrar extensiones o nombres conocidos
                    if item.suffix in self.CONFIG_EXTENSIONS or "rc" in item.name or "config" in item.name or "profile" in item.name:
                        try:
                            resolved = item.resolve()
                            if resolved not in managed and resolved not in seen:
                                found.append((f"Root: {item.name}", item))
                                seen.add(resolved)
                        except Exception:
                            continue
        except PermissionError:
            pass
        return found