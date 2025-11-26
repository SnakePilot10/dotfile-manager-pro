import json
from typing import List
from pathlib import Path
from .dotfile import Dotfile

# Ruta al archivo JSON (junto al cli.py)
CONFIG_FILE = Path(__file__).resolve().parent.parent / "dotfiles.json"

class ConfigManager:
    def __init__(self):
        self.dotfiles: List[Dotfile] = []
        self.load_config()

    def load_config(self):
        """Carga la configuración desde el JSON."""
        if not CONFIG_FILE.exists():
            self.dotfiles = []
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.dotfiles = []
                for item in data:
                    self.dotfiles.append(Dotfile(
                        source_path=Path(item["source"]),
                        target_path=Path(item["target"]),
                        profile=item["profile"]
                    ))
        except Exception as e:
            print(f"❌ Error cargando config: {e}")
            self.dotfiles = []

    def save_config(self):
        """Guarda la configuración actual en el JSON."""
        data = []
        for df in self.dotfiles:
            data.append({
                "source": str(df.source_path),
                "target": str(df.target_path),
                "profile": df.profile
            })
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

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
