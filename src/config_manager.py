import json
from typing import List
from pathlib import Path
from .dotfile import Dotfile
from .paths import CONFIG_FILE, ensure_app_dirs

class ConfigManager:
    def __init__(self):
        self.dotfiles: List[Dotfile] = []
        ensure_app_dirs()
        self.load_config()

    def load_config(self):
        """Carga la configuración desde el JSON."""
        if not CONFIG_FILE.exists():
            self.dotfiles = []
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    self.dotfiles = []
                    return
                data = json.loads(content)
                self.dotfiles = []
                for item in data:
                    self.dotfiles.append(Dotfile(
                        source_path=Path(item["source"]),
                        target_path=Path(item["target"]),
                        profile=item["profile"]
                    ))
        except json.JSONDecodeError:
            print(f"❌ Error: Config file corrupted at {CONFIG_FILE}. Starting fresh.")
            self.dotfiles = []
        except Exception as e:
            print(f"❌ Error cargando config: {e}")
            self.dotfiles = []

    def save_config(self):
        """Guarda la configuración actual en el JSON."""
        ensure_app_dirs()
        data = []
        for df in self.dotfiles:
            data.append({
                "source": str(df.source_path),
                "target": str(df.target_path),
                "profile": df.profile
            })
        
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"❌ Error guardando config: {e}")

    def add_dotfile(self, dotfile: Dotfile):
        """Agrega un dotfile y guarda los cambios."""
        # Evitar duplicados
        for existing in self.dotfiles:
            if existing.source_path == dotfile.source_path and existing.target_path == dotfile.target_path:
                print(f"⚠️ El dotfile ya existe en la configuración.")
                return

        self.dotfiles.append(dotfile)
        self.save_config()
        print(f"✅ Configuración guardada: {dotfile.source_path.name} añadido.")

    def get_dotfiles_by_profile(self, profile: str) -> List[Dotfile]:
        if profile.lower() == "all":
            return self.dotfiles
        return [d for d in self.dotfiles if d.profile.lower() == profile.lower()]
