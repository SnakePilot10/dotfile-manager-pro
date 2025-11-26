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

# Detectar dónde vive el script
BASE_DIR = Path(__file__).resolve().parent

# Inicializar Manager (Ahora carga desde JSON automáticamente)
manager = ConfigManager()

@app.command(name="add")
def add(
    file: Path = typer.Argument(..., help="Ruta del archivo en tu sistema (ej: ~/.zshrc)", exists=True),
    profile: str = typer.Option("Home", "--profile", "-p", help="Perfil (Home, Work, Server)"),
    folder: str = typer.Option("misc", "--folder", "-f", help="Subcarpeta en el repo donde se guardará")
):
    """[NUEVO] Agrega un archivo al gestor, lo mueve al repo y crea el symlink."""
    
    # 1. Definir rutas
    # El archivo original del usuario (ej: /home/snake/.zshrc)
    original_path = file.expanduser().resolve()
    
    # Dónde lo vamos a guardar en el repo (ej: .../dotfiles/misc/.zshrc)
    repo_dest = BASE_DIR / "dotfiles" / folder / original_path.name
    
    console.print(f"\n[bold cyan]🔄 Procesando:[/bold cyan] {original_path.name}")

    # 2. Validar si ya está gestionado
    if repo_dest.exists():
        console.print(f"[yellow]⚠️  Este archivo ya parece estar en el repositorio: {repo_dest}[/yellow]")
        # Aquí podríamos preguntar si quiere sobrescribir, por ahora abortamos para seguridad
        
    # 3. Mover el archivo original al repositorio
    try:
        if not repo_dest.parent.exists():
            repo_dest.parent.mkdir(parents=True)
            
        # IMPORTANTE: Movemos el archivo real al repo
        import shutil
        shutil.move(str(original_path), str(repo_dest))
        console.print(f"📦 Archivo movido al repositorio: [green]{repo_dest}[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error moviendo archivo:[/red] {e}")
        return

    # 4. Registrar en la configuración (JSON)
    # Guardamos rutas relativas para portabilidad
    # Source: Ruta relativa desde el repo (ej: dotfiles/misc/.zshrc)
    # Target: Ruta absoluta del usuario (ej: ~/.zshrc) - guardada como string con ~
    
    relative_source = repo_dest.relative_to(BASE_DIR)
    # Reconstruimos la ruta destino usando ~ para que sea portable entre usuarios
    portable_target = Path("~") / original_path.relative_to(Path.home())
    
    new_dotfile = Dotfile(relative_source, portable_target, profile)
    manager.add_dotfile(new_dotfile)
    
    # 5. Crear el enlace simbólico de vuelta (Restaurar funcionalidad)
    # Ahora usamos la instancia con rutas absolutas para crear el link
    # (El manager guarda relativas, pero necesitamos absolutas para operar)
    dotfile_ops = Dotfile(repo_dest, original_path, profile)
    dotfile_ops.create_symlink(force=True)

@app.command(name="status")
def status(profile: str = typer.Option("all", "--profile", "-p")):
    """Muestra el estado de los enlaces y archivos."""
    console.print(f"\n[bold blue]Estado de Dotfiles - Perfil: {profile.upper()}[/bold blue]\n")
    
    if not manager.dotfiles:
        console.print("[yellow]📭 No hay dotfiles gestionados aún. Usa 'dotfile-pro add <archivo>'[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Perfil", style="cyan")
    table.add_column("Origen (Repo)")
    table.add_column("Destino (Sistema)")
    table.add_column("Estado")

    for dotfile_data in manager.get_dotfiles_by_profile(profile):
        # Reconstruir rutas absolutas para verificación
        abs_source = BASE_DIR / dotfile_data.source_path
        
        # Objeto temporal para chequeo
        checker = Dotfile(abs_source, dotfile_data.target_path, dotfile_data.profile)
        
        table.add_row(
            checker.profile, 
            str(dotfile_data.source_path), 
            str(checker.target_path), 
            checker.check_status()
        )
    console.print(table)

@app.command(name="link")
def link_dotfiles(profile: str = typer.Option("all", "--profile", "-p"), force: bool = typer.Option(False, "--force", "-f")):
    """Crea los enlaces simbólicos en el sistema."""
    console.print(f"\n[bold green]Creando Symlinks: {profile.upper()}[/bold green]")
    target_files = manager.get_dotfiles_by_profile(profile)
    for dotfile_data in target_files:
        # Reconstruir rutas absolutas
        abs_source = BASE_DIR / dotfile_data.source_path
        linker = Dotfile(abs_source, dotfile_data.target_path, dotfile_data.profile)
        
        if abs_source.exists():
            linker.create_symlink(force=force)
        else:
            console.print(f"[red]❌ Fuente no encontrada en repo: {abs_source}[/red]")

@app.command(name="save")
def save(message: str = typer.Argument(..., help="Mensaje del commit")):
    """Guarda y sube los cambios a GitHub automáticamente."""
    GitHandler.save_changes(message)

@app.command(name="update")
def update():
    """Descarga cambios desde GitHub."""
    GitHandler.pull_updates()
    manager.load_config() # Recargar configuración tras update

if __name__ == "__main__":
    app()
