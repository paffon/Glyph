import os
from response import GlyphMCPResponse


def read_asset(filename: str) -> str:
    """
    Reads the content of a file from the assets directory.
    
    Args:
        filename: The name of the file to read (e.g., 'example.txt').
    
    Returns:
        The content of the asset file as a string.
    """    
    try:
        assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
        file_path = os.path.join(assets_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
        
    except FileNotFoundError:
        return f"Asset file '{filename}' not found."
    except Exception as e:
        return f"Error reading asset file '{filename}': {str(e)}"