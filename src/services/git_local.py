import subprocess
from rich.console import Console
from src.core.paths import context

class LocalGit:
    """
    Handles ONLY local git operations. 
    No remote interaction (push/pull) to ensure privacy and decoupling.
    """
    
    @staticmethod
    def _run(args: list) -> bool:
        try:
            subprocess.run(
                ["git"] + args,
                cwd=context.repo_root,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def is_repo() -> bool:
        return (context.repo_root / ".git").is_dir()

    @staticmethod
    def init_repo():
        if not LocalGit.is_repo():
            LocalGit._run(["init"])

    @staticmethod
    def commit_changes(message: str) -> bool:
        """
        Stages tracked files (updates) and commits. 
        Does NOT stage untracked files automatically for safety.
        """
        if not LocalGit.is_repo():
            LocalGit.init_repo()
            
        # Add only modified tracked files
        LocalGit._run(["add", "-u"])
        
        # Try to commit
        return LocalGit._run(["commit", "-m", message])
