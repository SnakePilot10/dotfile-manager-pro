from pathlib import Path
import shutil
from typing import Optional
import os

class Dotfile:
    def __init__(self, source_path: Path, target_path: Path, profile: str = "default"):
        self.source_path = source_path
        self.target_path = target_path
        self.profile = profile

    def create_symlink(self, force: bool = False) -> bool:
        expanded_target = self.target_path.expanduser() 
        
        if expanded_target.exists():
            if expanded_target.is_symlink():
                 print(f"🔄 Enlace ya existe: {expanded_target.name}")
                 return True
            
            if force:
                try:
                    if expanded_target.is_dir() and not expanded_target.is_symlink():
                        shutil.rmtree(expanded_target)
                        print(f"🗑️ Directorio existente eliminado: {expanded_target.name}")
                    else:
                        expanded_target.unlink()
                        print(f"🗑️ Archivo existente eliminado: {expanded_target.name}")
                except Exception as e:
                    print(f"❌ Error al eliminar {expanded_target.name}: {e}")
                    return False
            else:
                print(f"⚠️ Archivo existente en destino: {expanded_target.name}. Use --force para sobrescribir.")
                return False

        try:
            expanded_target.parent.mkdir(parents=True, exist_ok=True)
            expanded_target.symlink_to(self.source_path.resolve())
            print(f"✅ Symlink creado: {self.source_path.name} -> {expanded_target}")
            return True
        except Exception as e:
            print(f"❌ Error al crear symlink para {self.source_path.name}: {e}")
            return False

    def check_status(self) -> str:
        expanded_target = self.target_path.expanduser()
        if expanded_target.is_symlink():
            if expanded_target.resolve() == self.source_path.resolve():
                return "[green]LINKED[/green]"
            else:
                return "[yellow]MISSING (Target changed)[/yellow]"
        elif expanded_target.exists():
            return "[red]FILE EXISTS (Not linked)[/red]"
        else:
            return "[red]NOT FOUND[/red]"
