# Updated dotfile handling for better symlink management and error checking.
# Assume this is provided or written explicitly

def create_symlink(source, link_name):
    import os
    try:
        if os.path.lexists(link_name):
            if os.path.islink(link_name) or os.path.isfile(link_name):
                os.remove(link_name)
            elif os.path.isdir(link_name):
                import shutil
                shutil.rmtree(link_name)
        os.symlink(source, link_name)
        print(f"Symlink created: {link_name} -> {source}")
    except (OSError, Exception) as e:
        print(f"Failed to create symlink {link_name} -> {source}: {e}")

def main():
    # Sample usage of create_symlink
    create_symlink("/path/to/source", "/path/to/destination")

if __name__ == "__main__":
    main()