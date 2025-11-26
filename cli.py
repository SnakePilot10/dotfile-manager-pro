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

# Configuración (En una versión futura esto vendría de un archivo config.json)
dotfiles_config = [
    Dotfile(Path("dotfiles/bash/.bashrc"), Path("~/.bashrc"), "Home"),
    Dotfile(Path("dotfiles/kde/kdeglobals"), Path("~/.config/kdeglobals"), "Work"),
    Dotfile(Path("dotfiles/alacritty/alacritty.toml"), Path("~/.config/alacritty/alacritty.toml"), "Work"),
]
manager = ConfigManager(dotfiles=dotfiles_config)

@app.command(name="status")
def status(profile: str = typer.Option("all", "--profile", "-p")):
    """Muestra el estado de los enlaces y archivos."""
    console.print(f"\n[bold blue]Estado de Dotfiles - Perfil: {profile.upper()}[/bold blue]\n")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Perfil", style="cyan")
    table.add_column("Origen")
    table.add_column("Destino")
    table.add_column("Estado")

    for dotfile in manager.get_dotfiles_by_profile(profile):
        table.add_row(dotfile.profile, str(dotfile.source_path), str(dotfile.target_path), dotfile.check_status())
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
            console.print(f"[red]❌ Fuente no encontrada en repo: {dotfile.source_path}[/red]")

@app.command(name="save")
def save(message: str = typer.Argument(..., help="Mensaje del commit")):
    """[NUEVO] Guarda y sube los cambios a GitHub automáticamente."""
    GitHandler.save_changes(message)

@app.command(name="update")
def update():
    """[NUEVO] Descarga cambios desde GitHub."""
    GitHandler.pull_updates()

if __name__ == "__main__":
    app()
