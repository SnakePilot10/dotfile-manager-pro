# cli.py

from config_manager import ConfigManager
import os

# Initialize ConfigManager for XDG-compliant paths
config = ConfigManager()
config_dir = config.get_config_path()

def main():
    # Ensure the config directory exists
    os.makedirs(config_dir, exist_ok=True)
    print(f"Using configuration directory: {config_dir}")

if __name__ == "__main__":
    main()
