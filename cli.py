#!/usr/bin/env python
# -*- coding: utf-8 -*-
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from pathlib import Path
import shutil
from src.dotfile import Dotfile
from src.config_manager import ConfigManager
from src.git_handler import GitHandler
from src.paths import DOTFILES_REPO_PATH, ensure_app_dirs

app = typer.Typer(name="dotfile-pro", add_completion=False)
console = Console()

manager = ConfigManager()

# --- BASE DE DATOS DE APPS ---
KNOWN_APPS = {
    "Zsh": ".zshrc",
    "Bash": ".bashrc",
    "Starship": ".config/starship.toml",
    "Neovim": ".config/nvim/init.lua",
    "Vim": ".vimrc",
    "Alacritty": ".config/alacritty/alacritty.toml",
    "Kitty": ".config/kitty/kitty.conf",
    "Git Config": ".gitconfig",
    "Tmux": ".tmux.conf",
    "VSCode": ".config/VSCodium/User/settings.json"
}

# --- COMANDO INTERACTIVO (TUI) ---
@app.command(name="ui")
def launch_ui():
    """[NUEVO] Lanza la Interfaz Gráfica de Terminal (TUI)."""
    # Importamos aquí para no ralentizar los otros comandos si no se usa la UI
    try:
        from src.tui_app import DotfileTUI
        app_tui = DotfileTUI()
        app_tui.run()
    except ImportError:
        console.print("[red]❌ Error: La librería 'textual' no está instalada.[/red]")
        console.print("Ejecuta: pip install textual")

# --- COMANDOS CLI CLÁSICOS ---

@app.command(name="scan")
def scan_system():
    """Escanea el sistema buscando dotfiles no gestionados."""
    console.print("\n[bold cyan]🔍 Escaneando sistema...[/bold cyan]")
    candidates = []
    # Avoid crashing if targets are invalid paths
    managed_targets = []
    for d in manager.dotfiles:
        try:
             managed_targets.append(str(d.target_path.expanduser().resolve()))
        except Exception:
            continue

    for app_name, rel_path in KNOWN_APPS.items():
        full_path = Path.home() / rel_path
        if full_path.exists():
            resolved_path = str(full_path.resolve())
            if resolved_path not in managed_targets:
                candidates.append((app_name, full_path))

    if not candidates:
        console.print("[green]✨ ¡Todo limpio![/green]")
        return

    table = Table(show_header=True)
    table.add_column("App", style="bold cyan")
    table.add_column("Ruta Detectada")
    for app_name, path in candidates:
        table.add_row(app_name, str(path))
    console.print(table)
    console.print("")

    if Confirm.ask("¿Deseas iniciar el asistente de importación?"):
        for app_name, path in candidates:
            if Confirm.ask(f"¿Agregar [cyan]{app_name}[/cyan]?"):
                _add_logic(path, "Home", "auto-scan")

def _add_logic(original_path: Path, profile: str, folder: str):
    ensure_app_dirs()
    repo_dest = DOTFILES_REPO_PATH / folder / original_path.name
    try:
        if not repo_dest.parent.exists(): repo_dest.parent.mkdir(parents=True)
        if repo_dest.exists():
             console.print(f"[yellow]Saltando {original_path.name}, ya existe en el repositorio.[/yellow]")
             return

        # Move file to repo
        shutil.move(str(original_path), str(repo_dest))
        
        rel_source = repo_dest.relative_to(DOTFILES_REPO_PATH)

        # Handle target path. Store as absolute path with ~ if possible for portability,
        # otherwise use absolute path.
        try:
            # Try to make it relative to home for portability
            portable_target = Path("~") / original_path.relative_to(Path.home())
        except ValueError:
            # File is not in home directory, use absolute path
            portable_target = original_path.resolve()

        manager.add_dotfile(Dotfile(rel_source, portable_target, profile))
        
        # Create symlink back
        Dotfile(repo_dest, original_path, profile).create_symlink(force=True)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        # Try to restore if move failed? (Complex rollback logic omitted for simplicity but advisable)

@app.command(name="add")
def add(file: Path = typer.Argument(..., exists=True), profile: str = typer.Option("Home", "-p"), folder: str = typer.Option("misc", "-f")):
    _add_logic(file.expanduser().resolve(), profile, folder)

@app.command(name="status")
def status(profile: str = typer.Option("all", "-p")):
    console.print(f"\n[bold blue]Estado de Dotfiles: {profile.upper()}[/bold blue]\n")
    if not manager.dotfiles:
        console.print("[yellow]No hay dotfiles gestionados.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Perfil", style="cyan")
    table.add_column("Origen (Repo)")
    table.add_column("Destino (Sistema)")
    table.add_column("Estado")
    for d in manager.get_dotfiles_by_profile(profile):
        abs_source = DOTFILES_REPO_PATH / d.source_path
        chk = Dotfile(abs_source, d.target_path, d.profile)
        table.add_row(chk.profile, str(d.source_path), str(chk.target_path), chk.check_status())
    console.print(table)

@app.command(name="link")
def link_dotfiles(profile: str = typer.Option("all", "-p"), force: bool = typer.Option(False, "-f")):
    for d in manager.get_dotfiles_by_profile(profile):
        abs_src = DOTFILES_REPO_PATH / d.source_path
        if abs_src.exists():
            Dotfile(abs_src, d.target_path, d.profile).create_symlink(force=force)
        else:
            console.print(f"[red]❌ Fuente no encontrada: {abs_src}[/red]")

@app.command(name="save")
def save(message: str = typer.Argument(..., help="Mensaje del commit")):
    GitHandler.save_changes(message)

@app.command(name="update")
def update():
    GitHandler.pull_updates()
    manager.load_config()

if __name__ == "__main__":
    app()
