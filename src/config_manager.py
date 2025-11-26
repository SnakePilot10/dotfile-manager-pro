from typing import List
from .dotfile import Dotfile

class ConfigManager:
    def __init__(self, dotfiles: List[Dotfile] = None):
        self.dotfiles = dotfiles if dotfiles else []

    def add_dotfile(self, dotfile: Dotfile):
        self.dotfiles.append(dotfile)

    def get_dotfiles_by_profile(self, profile: str) -> List[Dotfile]:
        if profile.lower() == "all":
            return self.dotfiles
        return [d for d in self.dotfiles if d.profile.lower() == profile.lower()]
