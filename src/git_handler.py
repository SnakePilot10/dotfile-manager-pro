import subprocess
from pathlib import Path
from rich.console import Console
from .paths import DOTFILES_REPO_PATH, ensure_app_dirs

console = Console()

class GitHandler:
    @staticmethod
    def _ensure_repo():
        """Ensure the git repository is initialized."""
        ensure_app_dirs()
        if not (DOTFILES_REPO_PATH / ".git").exists():
            console.print(f"[yellow]⚠️ Inicializando repositorio Git en {DOTFILES_REPO_PATH}...[/yellow]")
            # Use subprocess directly to avoid recursion loop in run_command
            try:
                subprocess.run(["git", "init"], check=True, cwd=DOTFILES_REPO_PATH, capture_output=True)

                # Create a README to avoid empty repo issues
                readme_path = DOTFILES_REPO_PATH / "README.md"
                if not readme_path.exists():
                    readme_path.write_text("# My Dotfiles\nManaged by dotfile-manager-pro", encoding="utf-8")
                    subprocess.run(["git", "add", "README.md"], check=True, cwd=DOTFILES_REPO_PATH, capture_output=True)
                    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, cwd=DOTFILES_REPO_PATH, capture_output=True)
            except subprocess.CalledProcessError as e:
                console.print(f"[red]❌ Error inicializando Git:[/red] {e}")

    @staticmethod
    def run_command(command: list) -> bool:
        GitHandler._ensure_repo()
        try:
            # cwd=DOTFILES_REPO_PATH obliga al comando a ejecutarse en la carpeta de datos del usuario
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True, 
                cwd=DOTFILES_REPO_PATH
            )
            if result.stdout:
                console.print(f"[dim]{result.stdout.strip()}[/dim]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error Git:[/red] {e.stderr.strip()}")
            return False

    @staticmethod
    def save_changes(message: str):
        GitHandler._ensure_repo()
        console.print(f"\n[bold yellow]📦 Guardando cambios en el repositorio...[/bold yellow]")
        console.print(f"[dim]Ubicación del repo: {DOTFILES_REPO_PATH}[/dim]")
        
        if GitHandler.run_command(["git", "add", "."]):
            if GitHandler.run_command(["git", "commit", "-m", message]):
                console.print("[green]✅ Cambios confirmados localmente.[/green]")
                console.print("[yellow]🚀 Subiendo a GitHub...[/yellow]")
                if GitHandler.run_command(["git", "push"]):
                    console.print("[bold green]✨ ¡Sincronización Completada con Éxito![/bold green]")
            else:
                console.print("[yellow]⚠️ No hay cambios para confirmar.[/yellow]")

    @staticmethod
    def pull_updates():
        GitHandler._ensure_repo()
        console.print(f"\n[bold cyan]⬇️ Descargando actualizaciones...[/bold cyan]")
        if GitHandler.run_command(["git", "pull"]):
            console.print("[bold green]✅ Sistema actualizado.[/bold green]")
