import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

# --- INGENIERÍA: Calcular ruta raíz del proyecto ---
# __file__ = .../src/git_handler.py
# parent   = .../src
# parent.parent = .../dotfile-manager-pro (La raíz donde está .git)
REPO_DIR = Path(__file__).resolve().parent.parent

class GitHandler:
    @staticmethod
    def run_command(command: list) -> bool:
        try:
            # cwd=REPO_DIR obliga al comando a ejecutarse en la carpeta del proyecto
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True, 
                cwd=REPO_DIR
            )
            if result.stdout:
                console.print(f"[dim]{result.stdout.strip()}[/dim]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error Git:[/red] {e.stderr.strip()}")
            return False

    @staticmethod
    def save_changes(message: str):
        console.print(f"\n[bold yellow]📦 Guardando cambios en el repositorio...[/bold yellow]")
        # Forzamos la ubicación explícita en el log para depuración
        console.print(f"[dim]Ubicación del repo: {REPO_DIR}[/dim]")
        
        if GitHandler.run_command(["git", "add", "."]):
            if GitHandler.run_command(["git", "commit", "-m", message]):
                console.print("[green]✅ Cambios confirmados localmente.[/green]")
                console.print("[yellow]🚀 Subiendo a GitHub...[/yellow]")
                if GitHandler.run_command(["git", "push"]):
                    console.print("[bold green]✨ ¡Sincronización Completada con Éxito![/bold green]")

    @staticmethod
    def pull_updates():
        console.print(f"\n[bold cyan]⬇️ Descargando actualizaciones...[/bold cyan]")
        if GitHandler.run_command(["git", "pull"]):
            console.print("[bold green]✅ Sistema actualizado.[/bold green]")
