import os
import sys

def validate_file(file_path):
    """Validate if file exists and is accessible."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return False
    
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a file.", file=sys.stderr)
        return False
    
    if not os.access(file_path, os.R_OK):
        print(f"Error: No read permission for '{file_path}'.", file=sys.stderr)
        return False
    
    return True

def show_progress(current, total):
    """Display progress bar in console."""
    width = 50
    progress = current / total
    filled = int(width * progress)
    bar = '=' * filled + '-' * (width - filled)
    percent = progress * 100
    
    print(f'\rProgress: [{bar}] {percent:.1f}%', end='', flush=True)
