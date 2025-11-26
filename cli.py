#!/usr/bin/env python
# -*- coding: utf-8 -*-
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from pathlib import Path
from src.dotfile import Dotfile
from src.config_manager import ConfigManager
from src.git_handler import GitHandler

app = typer.Typer(name="dotfile-pro", add_completion=False)
console = Console()

BASE_DIR = Path(__file__).resolve().parent
manager = ConfigManager()

# --- BASE DE DATOS DE APPS COMUNES (Expandible) ---
# Rutas relativas al HOME del usuario
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
    "Picom": ".config/picom/picom.conf",
    "I3 Window Manager": ".config/i3/config",
    "Hyprland": ".config/hypr/hyprland.conf",
    "Waybar": ".config/waybar/config",
    "Rofi": ".config/rofi/config.rasi",
    "Dunst": ".config/dunst/dunstrc",
    "VSCode (Open Source)": ".config/VSCodium/User/settings.json"
}

@app.command(name="scan")
def scan_system():
    """[NUEVO] Escanea el sistema buscando dotfiles no gestionados."""
    console.print("\n[bold cyan]🔍 Escaneando sistema en busca de candidatos...[/bold cyan]")
    
    candidates = []
    
    # 1. Obtener lista de rutas ya gestionadas (para no repetir)
    managed_targets = [str(d.target_path.expanduser().resolve()) for d in manager.dotfiles]

    # 2. Buscar coincidencias
    for app_name, rel_path in KNOWN_APPS.items():
        full_path = Path.home() / rel_path
        
        # Si el archivo existe en el sistema Y NO está gestionado
        if full_path.exists():
            resolved_path = str(full_path.resolve())
            if resolved_path not in managed_targets:
                candidates.append((app_name, full_path))

    if not candidates:
        console.print("[green]✨ ¡Todo limpio! No se encontraron apps conocidas sin gestionar.[/green]")
        return

    # 3. Interacción con el usuario
    console.print(f"[yellow]⚠️  Se encontraron {len(candidates)} archivos de configuración existentes no gestionados:[/yellow]\n")
    
    table = Table(show_header=True)
    table.add_column("App", style="bold cyan")
    table.add_column("Ruta Detectada")
    
    for app_name, path in candidates:
        table.add_row(app_name, str(path))
    
    console.print(table)
    console.print("")

    if Confirm.ask("¿Deseas iniciar el asistente de importación?"):
        for app_name, path in candidates:
            if Confirm.ask(f"¿Agregar [cyan]{app_name}[/cyan] ({path.name})?"):
                # Llamamos a la lógica de ADD
                # Simulamos los argumentos usando la función add directamente (hack de ingeniería)
                # O mejor, invocamos la lógica interna:
                _add_logic(path, profile="Home", folder="auto-scan")

def _add_logic(original_path: Path, profile: str, folder: str):
    """Lógica interna reutilizable para agregar archivos."""
    repo_dest = BASE_DIR / "dotfiles" / folder / original_path.name
    
    try:
        if not repo_dest.parent.exists():
            repo_dest.parent.mkdir(parents=True)
            
        import shutil
        # Copiar en lugar de mover por seguridad en el escaneo masivo, 
        # luego el link sobrescribirá (o preguntará)
        if repo_dest.exists():
             console.print(f"[yellow]Saltando {original_path.name}, ya existe en repo.[/yellow]")
             return

        shutil.move(str(original_path), str(repo_dest))
        
        # Registrar en JSON
        relative_source = repo_dest.relative_to(BASE_DIR)
        portable_target = Path("~") / original_path.relative_to(Path.home())
        new_dotfile = Dotfile(relative_source, portable_target, profile)
        manager.add_dotfile(new_dotfile)
        
        # Crear Link
        dotfile_ops = Dotfile(repo_dest, original_path, profile)
        dotfile_ops.create_symlink(force=True)
        
    except Exception as e:
        console.print(f"[red]Error procesando {original_path.name}: {e}[/red]")


# --- COMANDOS EXISTENTES (Sin cambios mayores) ---

@app.command(name="add")
def add(
    file: Path = typer.Argument(..., help="Ruta del archivo", exists=True),
    profile: str = typer.Option("Home", "--profile", "-p"),
    folder: str = typer.Option("misc", "--folder", "-f")
):
    """Agrega un archivo manualmente."""
    _add_logic(file.expanduser().resolve(), profile, folder)

@app.command(name="status")
def status(profile: str = typer.Option("all", "--profile", "-p")):
    """Muestra el estado."""
    console.print(f"\n[bold blue]Estado de Dotfiles - Perfil: {profile.upper()}[/bold blue]\n")
    if not manager.dotfiles:
        console.print("[yellow]📭 Vacío.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Perfil", style="cyan")
    table.add_column("Origen (Repo)")
    table.add_column("Destino")
    table.add_column("Estado")
    for d in manager.get_dotfiles_by_profile(profile):
        abs_source = BASE_DIR / d.source_path
        checker = Dotfile(abs_source, d.target_path, d.profile)
        table.add_row(checker.profile, str(d.source_path), str(checker.target_path), checker.check_status())
    console.print(table)

@app.command(name="link")
def link_dotfiles(profile: str = typer.Option("all", "--profile", "-p"), force: bool = typer.Option(False, "--force", "-f")):
    """Restaura enlaces."""
    console.print(f"\n[bold green]Creando Symlinks: {profile.upper()}[/bold green]")
    for d in manager.get_dotfiles_by_profile(profile):
        abs_source = BASE_DIR / d.source_path
        linker = Dotfile(abs_source, d.target_path, d.profile)
        if abs_source.exists():
            linker.create_symlink(force=force)
        else:
            console.print(f"[red]❌ Fuente perdida: {abs_source}[/red]")

@app.command(name="save")
def save(message: str = typer.Argument(..., help="Mensaje")):
    GitHandler.save_changes(message)

@app.command(name="update")
def update():
    GitHandler.pull_updates()
    manager.load_config()

if __name__ == "__main__":
    app()
