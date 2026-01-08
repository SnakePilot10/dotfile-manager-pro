import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from pathlib import Path
from src.core.models import Dotfile
from src.services.config_service import ConfigService
from src.services.file_service import FileService
from src.services.git_local import LocalGit
from src.services.scanner import SystemScanner

app = typer.Typer(name="dotfile-pro", add_completion=False)
console = Console()
config_service = ConfigService()

@app.command()
def scan():
    """Scan system for unmanaged dotfiles."""
    scanner = SystemScanner(config_service)
    console.print("\n[bold cyan]🔍 Scanning system...[/bold cyan]")
    
    candidates = scanner.scan()
    
    if not candidates:
        console.print("[green]✨ System clean! No unmanaged files found.[/green]")
        return

    table = Table(show_header=True)
    table.add_column("App", style="bold cyan")
    table.add_column("Path detected")
    
    for app_name, path in candidates:
        table.add_row(app_name, str(path))
    
    console.print(table)
    console.print("")

    if Confirm.ask("Do you want to import detected files?"):
        imported_files = False
        for app_name, path in candidates:
            if Confirm.ask(f"Add [cyan]{app_name}[/cyan] ({path.name})?"):
                # Preguntar por el perfil
                profile = Confirm.ask(f"Assign to 'default' profile?", default=True)
                if not profile:
                    profile_name = console.input("[bold yellow]Enter profile name: [/bold yellow]")
                else:
                    profile_name = "default"

                try:
                    # Fix: Use app_name as subfolder to avoid collisions (e.g. nvim/init.lua vs emacs/init.el)
                    safe_app_name = "".join(c for c in app_name if c.isalnum() or c in ('-', '_')).strip()
                    rel_path = Path("auto-scan") / safe_app_name / path.name
                    new_dotfile = FileService.safe_import(path, rel_path, profile_name)
                    config_service.add_dotfile(new_dotfile)
                    console.print(f"[green]✅ Imported {app_name} to profile '{profile_name}'[/green]")
                    imported_files = True
                except Exception as e:
                    console.print(f"[red]❌ Failed to import {app_name}: {e}[/red]")
        
        if imported_files:
            LocalGit.commit_changes("Imported files via scan")

@app.command()
def ui():
    """Launch Terminal UI"""
    try:
        from src.interface.tui import DotfileTUI
        DotfileTUI().run()
    except ImportError as e:
        console.print(f"[red]Error loading TUI: {e}[/red]")

@app.command()
def add(
    file: Path = typer.Argument(..., exists=True, help="Archivo a gestionar"), 
    profile: str = typer.Option("default", "-p", help="Perfil de configuración"), 
    folder: str = typer.Option("misc", "-f", help="Subcarpeta dentro del repositorio")
):
    """Añade de forma segura un archivo al repositorio de dotfiles."""
    try:
        # Sanitización de la carpeta para evitar directory traversal
        clean_folder = "".join(c for c in folder if c.isalnum() or c in ('-', '_')).strip()
        if not clean_folder: clean_folder = "misc"
        
        rel_path = Path(clean_folder) / file.name
        
        with console.status(f"[bold yellow]Importando {file.name}...[/bold yellow]"):
            new_dotfile = FileService.safe_import(file, rel_path, profile)
            config_service.add_dotfile(new_dotfile)
            
        console.print(f"[bold green]✨ ¡Éxito![/bold green] {file.name} añadido al perfil [bold cyan]{profile}[/bold cyan]")
        
        # Auto-commit local
        if LocalGit.commit_changes(f"Add: {file.name} (profile: {profile})"):
            console.print("[dim]Punto de restauración creado en Git local.[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error crítico:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def status(profile: str = "all"):
    """Check status of managed files."""
    dotfiles = config_service.load_config()
    if profile != "all":
        dotfiles = [d for d in dotfiles if d.profile == profile]
        
    table = Table(show_header=True)
    table.add_column("Profile", style="cyan")
    table.add_column("Source")
    table.add_column("Target")
    table.add_column("Status")
    
    for df in dotfiles:
        status_msg = FileService.check_status(df)
        table.add_row(df.profile, str(df.source), str(df.target), status_msg)
        
    console.print(table)

@app.command()
def link(profile: str = "all", force: bool = False):
    """Re-link dotfiles."""
    dotfiles = config_service.load_config()
    if profile != "all":
        dotfiles = [d for d in dotfiles if d.profile == profile]
    
    for df in dotfiles:
        msg = FileService.create_symlink(df, force)
        console.print(f"{df.source.name}: {msg}")

@app.command()
def commit(message: str):
    """Create a local git commit."""
    if LocalGit.commit_changes(message):
        console.print("[green]Changes committed locally.[/green]")
    else:
        console.print("[yellow]Nothing to commit or git error.[/yellow]")

if __name__ == "__main__":
    app()
