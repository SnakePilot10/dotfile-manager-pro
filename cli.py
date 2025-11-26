#!/usr/bin/env python
# -*- coding: utf-8 -*-
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from src.dotfile import Dotfile
from src.config_manager import ConfigManager
from src.git_handler import GitHandler

app = typer.Typer(name="dotfile-pro", add_completion=False)
console = Console()

# --- MAGIA DE INGENIERÍA: Detectar dónde vive el script ---
# Esto asegura que funcione sin importar desde qué carpeta lo ejecutes.
BASE_DIR = Path(__file__).resolve().parent

# Configuración usando rutas absolutas basadas en el script
dotfiles_config = [
    Dotfile(BASE_DIR / "dotfiles/bash/.bashrc", Path("~/.bashrc"), "Home"),
    Dotfile(BASE_DIR / "dotfiles/kde/kdeglobals", Path("~/.config/kdeglobals"), "Work"),
    Dotfile(BASE_DIR / "dotfiles/alacritty/alacritty.toml", Path("~/.config/alacritty/alacritty.toml"), "Work"),
]
manager = ConfigManager(dotfiles=dotfiles_config)

@app.command(name="status")
def status(profile: str = typer.Option("all", "--profile", "-p")):
    """Muestra el estado de los enlaces y archivos."""
    console.print(f"\n[bold blue]Estado de Dotfiles - Perfil: {profile.upper()}[/bold blue]\n")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Perfil", style="cyan")
    table.add_column("Origen (Relativo)")
    table.add_column("Destino")
    table.add_column("Estado")

    for dotfile in manager.get_dotfiles_by_profile(profile):
        # Mostramos la ruta relativa para que la tabla no sea gigante
        try:
            display_source = dotfile.source_path.relative_to(BASE_DIR)
        except ValueError:
            display_source = dotfile.source_path
            
        table.add_row(dotfile.profile, str(display_source), str(dotfile.target_path), dotfile.check_status())
    console.print(table)

@app.command(name="link")
def link_dotfiles(profile: str = typer.Option("all", "--profile", "-p"), force: bool = typer.Option(False, "--force", "-f")):
    """Crea los enlaces simbólicos en el sistema."""
    console.print(f"\n[bold green]Creando Symlinks: {profile.upper()}[/bold green]")
    target_files = manager.get_dotfiles_by_profile(profile)
    for dotfile in target_files:
        if dotfile.source_path.exists():
            dotfile.create_symlink(force=force)
        else:
            console.print(f"[red]❌ Fuente no encontrada: {dotfile.source_path}[/red]")

@app.command(name="save")
def save(message: str = typer.Argument(..., help="Mensaje del commit")):
    """Guarda y sube los cambios a GitHub automáticamente."""
    GitHandler.save_changes(message)

@app.command(name="update")
def update():
    """Descarga cambios desde GitHub."""
    GitHandler.pull_updates()

if __name__ == "__main__":
    app()
