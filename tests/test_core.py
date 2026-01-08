import pytest
from pathlib import Path
from core.models import Dotfile
from services.file_service import FileService
from services.config_service import ConfigService

# Mocks or temporary directories would be used in a real scenario
# Here we define the test structure

def test_dotfile_model():
    d = Dotfile("zshrc", "~/.zshrc")
    assert isinstance(d.source, Path)
    assert str(d.target) == "~/.zshrc"

def test_atomic_config_save(tmp_path):
    # Setup Context Mock (if we were using dependency injection, this would be cleaner)
    # For now, we rely on the fact ConfigService uses context.config_path
    
    service = ConfigService()
    service.config_path = tmp_path / "test_config.json"
    
    dots = [Dotfile("a", "b")]
    service.save_config(dots)
    
    assert service.config_path.exists()
    loaded = service.load_config()
    assert len(loaded) == 1
    assert str(loaded[0].source) == "a"
