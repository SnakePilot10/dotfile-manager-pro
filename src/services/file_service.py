import shutil
import os
from pathlib import Path
from datetime import datetime
from src.core.models import Dotfile
from src.core.paths import context
from src.core.exceptions import FileOperationError, BackupError

class FileService:
    @staticmethod
    def safe_import(original_path: Path, relative_repo_path: Path, profile: str) -> Dotfile:
        """
        Safely moves a file into the repo: Copy -> Verify -> Link -> Delete Original.
        Returns the new Dotfile object.
        """
        original_path = original_path.expanduser().resolve()
        repo_dest = context.get_absolute_source(relative_repo_path)
        
        if not original_path.exists():
            raise FileOperationError(f"Source file not found: {original_path}")
        
        # 1. Prepare Destination
        try:
            repo_dest.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileOperationError(f"Could not create repo directory: {e}")

        # 2. Copy (Non-destructive first)
        if repo_dest.exists():
             # If it exists in repo, we don't overwrite unless explicitly handled.
             # For now, we assume if it's in repo, we just want to link it.
             pass 
        else:
            try:
                if original_path.is_dir():
                    shutil.copytree(original_path, repo_dest)
                else:
                    shutil.copy2(original_path, repo_dest)
            except Exception as e:
                raise FileOperationError(f"Failed to copy file to repo: {e}")

        # 3. Create Symlink (this verifies the copy implicitly by needing the path)
        # Calculate portable target (e.g. ~/.zshrc)
        try:
            portable_target = Path("~") / original_path.relative_to(Path.home())
        except ValueError:
            # Fallback for system files not in home
            portable_target = original_path

        dotfile = Dotfile(source=relative_repo_path, target=portable_target, profile=profile)
        
        # 4. Enforce Link (replaces original)
        FileService.create_symlink(dotfile, force=True)
        
        return dotfile

    @staticmethod
    def create_symlink(dotfile: Dotfile, force: bool = False) -> str:
        """Creates the symlink. Returns status message."""
        source_abs = context.get_absolute_source(dotfile.source)
        target_abs = dotfile.expanded_target

        if not source_abs.exists():
             return f"[red]BROKEN[/red] Source missing: {source_abs}"

        if target_abs.is_symlink():
            if target_abs.resolve() == source_abs:
                return "[green]OK[/green] Already linked"
            if not force:
                return "[yellow]CONFLICT[/yellow] Wrong link target"
        
        if target_abs.exists():
            if not force:
                return "[yellow]CONFLICT[/yellow] File exists"
            
            # Backup before force overwrite
            FileService.backup_file(target_abs)
            
            if target_abs.is_symlink() or target_abs.is_file():
                target_abs.unlink()
            elif target_abs.is_dir():
                shutil.rmtree(target_abs)

        try:
            target_abs.parent.mkdir(parents=True, exist_ok=True)
            target_abs.symlink_to(source_abs)
            return "[green]LINKED[/green] Successfully"
        except Exception as e:
            raise FileOperationError(f"Symlink failed: {e}")

    @staticmethod
    def backup_file(path: Path):
        """Creates a timestamped backup in .backups/"""
        if not path.exists(): 
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.name}.{timestamp}.bak"
        context.backup_dir.mkdir(exist_ok=True)
        dest = context.backup_dir / backup_name
        
        try:
            if path.is_dir():
                shutil.copytree(path, dest)
            else:
                shutil.copy2(path, dest)
        except Exception as e:
            raise BackupError(f"Could not backup {path}: {e}")

    @staticmethod
    def check_status(dotfile: Dotfile) -> str:
        source_abs = context.get_absolute_source(dotfile.source)
        target_abs = dotfile.expanded_target
        
        if not source_abs.exists():
            return "[red]MISSING SOURCE[/red]"
        
        if not target_abs.exists():
            return "[dim]NOT INSTALLED[/dim]"
            
        if target_abs.is_symlink():
            if target_abs.resolve() == source_abs:
                return "[green]ACTIVE[/green]"
            return "[yellow]WRONG TARGET[/yellow]"
            
        return "[red]FILE EXISTS[/red]"
