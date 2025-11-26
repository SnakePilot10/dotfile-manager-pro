import subprocess
from rich.console import Console

console = Console()

class GitHandler:
    @staticmethod
    def run_command(command: list) -> bool:
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            if result.stdout:
                console.print(f"[dim]{result.stdout.strip()}[/dim]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error Git:[/red] {e.stderr.strip()}")
            return False

    @staticmethod
    def save_changes(message: str):
        console.print(f"\n[bold yellow]📦 Guardando cambios en el repositorio...[/bold yellow]")
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
