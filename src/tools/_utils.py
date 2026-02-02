"""
Utility functions for tool operations.
"""
import os
import re
from config import BASE_NAME
from response import GlyphMCPResponse
from read_an_asset import read_asset


def validate_absolute_path(abs_path: str, response: GlyphMCPResponse) -> bool:
    """
    Validate that the provided path is an absolute path.
    
    Args:
        abs_path: The path to validate.
        response: Response object to add context messages to.
    
    Returns:
        True if the path is absolute, False otherwise.
    """
    if abs_path.startswith(('.', '..')):
        response.add_context(
            f"Invalid path: '{abs_path}'. "
            "The path must be absolute and full (e.g., 'C:\\Users\\...\\project' on Windows or '/home/user/.../project' on Linux/Mac). "
            "Relative paths (like '.', '..', or 'folder/subfolder') are not allowed."
        )
        return False
    if not os.path.isabs(abs_path):
        response.add_context(
            f"Invalid path: '{abs_path}'. "
            "The path must be absolute and full (e.g., 'C:\\Users\\...\\project' on Windows or '/home/user/.../project' on Linux/Mac). "
            "Relative paths (like '.', '..', or 'folder/subfolder') are not allowed."
        )
        return False
    return True


def get_next_number(directory: str, prefix: str, extension: str = ".md") -> int:
    """
    Get the next document number by scanning existing files in a directory.
    
    Args:
        directory: Path to the directory to scan.
        prefix: The file prefix to look for (e.g., 'dl' or 'op').
        extension: The file extension to filter by (default: '.md'). Use empty string for any extension.
    
    Returns:
        The next available document number.
    """
    if not os.path.exists(directory):
        return 1
    
    max_number = 0
    if extension:
        pattern = re.compile(rf'^{prefix}_(\d+)_.*{re.escape(extension)}$')
    else:
        pattern = re.compile(rf'^{prefix}_(\d+)_.*')
    
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_number:
                max_number = num
    
    return max_number + 1


def sanitize_title(title: str) -> str:
    """
    Sanitize a title for use in a filename.
    
    Replaces spaces with underscores.
    
    Args:
        title: The title to sanitize.
    
    Returns:
        The sanitized title.
    """
    return title.replace(' ', '_')

def add_document(
    abs_path: str,
    title: str,
    subdirectory: str,
    prefix: str,
    template_asset: str,
    doc_type: str
) -> GlyphMCPResponse[None]:
    """
    Generic function to add a new document file.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located.
        title: The title for the document.
        subdirectory: The subdirectory name (e.g., 'operations', 'design_logs').
        prefix: The file prefix (e.g., 'op', 'dl').
        template_asset: The name of the template asset file.
        doc_type: The document type for messages (e.g., 'operation document', 'design log').
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        # Construct the document directory path
        doc_dir = os.path.join(abs_path, BASE_NAME, subdirectory)
        
        # Check if the assistant directory is initialized
        if not os.path.exists(doc_dir):
            response.add_context(
                f"{subdirectory.replace('_', ' ').title()} directory not found at {doc_dir}. "
                "Please initialize the assistant directory first."
            )
            return response
        
        # Get the next document number
        next_number = get_next_number(doc_dir, prefix)
        
        # Sanitize the title for use in filename
        sanitized_title = sanitize_title(title)
        
        # Create the new filename
        new_filename = f"{prefix}_{next_number}_{sanitized_title}.md"
        new_filepath = os.path.join(doc_dir, new_filename)
        
        # Read the template
        template_content = read_asset(template_asset)
        
        # Write the new document file
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        response.add_context(f"Created new {doc_type}: {new_filename}")
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to create {doc_type}: {str(e)}")
    
    return response
