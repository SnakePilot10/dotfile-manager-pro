class DotfileError(Exception):
    """Base exception for Dotfile Manager."""
    pass

class ConfigError(DotfileError):
    """Configuration file corruption or access error."""
    pass

class FileOperationError(DotfileError):
    """Filesystem permission or I/O error."""
    pass

class BackupError(DotfileError):
    """Backup creation failure."""
    pass
