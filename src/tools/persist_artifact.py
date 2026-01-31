import os
import shutil
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import get_next_number


def validate_source_file(source_file_path: str, response: GlyphMCPResponse[None]) -> bool:
    """
    Validate that the source file exists and is a file.
    
    Args:
        source_file_path: Path to the source file to validate.
        response: Response object to add context messages to.
    
    Returns:
        True if the file is valid, False otherwise.
    """
    if not os.path.exists(source_file_path):
        response.add_context(f"Source file not found: {source_file_path}")
        return False
    
    if not os.path.isfile(source_file_path):
        response.add_context(f"Source path is not a file: {source_file_path}")
        return False
    
    return True


def validate_artifacts_directory(artifacts_dir: str, response: GlyphMCPResponse[None]) -> bool:
    """
    Validate that the artifacts directory exists.
    
    Args:
        artifacts_dir: Path to the artifacts directory.
        response: Response object to add context messages to.
    
    Returns:
        True if the directory exists, False otherwise.
    """
    if not os.path.exists(artifacts_dir):
        response.add_context(
            f"Artifacts directory not found at {artifacts_dir}. "
            "Please initialize the assistant directory first."
        )
        return False
    
    return True


def copy_artifact(source_file_path: str, artifacts_dir: str) -> tuple[str, str]:
    """
    Copy the source file to the artifacts directory with proper naming.
    
    Args:
        source_file_path: Path to the source file.
        artifacts_dir: Path to the artifacts directory.
    
    Returns:
        A tuple of (new_filename, new_filepath).
    """
    # Get the next artifact number (using 'art' prefix, accepting any extension)
    next_number = get_next_number(artifacts_dir, "art", extension="")
    
    # Extract the original filename
    original_filename = os.path.basename(source_file_path)
    
    # Create the new artifact filename
    new_filename = f"art_{next_number}_{original_filename}"
    new_filepath = os.path.join(artifacts_dir, new_filename)
    
    # Copy the file to artifacts directory
    shutil.copy2(source_file_path, new_filepath)
    
    return new_filename, new_filepath


@mcp.tool()
def persist_artifact(base_dir_path: str, source_file_path: str) -> GlyphMCPResponse[None]:
    """
    Persist a file from any location to the artifacts directory.
    
    Copies a file to the .assistant/artifacts/ directory and renames it with the pattern:
    art_{serial_number}_{original_file_name}.{original_extension}
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        source_file_path: The full path to the file to persist as an artifact.
    
    Returns:
        GlyphMCPResponse indicating success or failure, with the new artifact filename.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        # Validate source file
        if not validate_source_file(source_file_path, response):
            return response
        
        # Construct and validate artifacts directory
        artifacts_dir = os.path.join(base_dir_path, BASE_NAME, "artifacts")
        if not validate_artifacts_directory(artifacts_dir, response):
            return response
        
        # Copy the artifact
        new_filename, new_filepath = copy_artifact(source_file_path, artifacts_dir)
        
        # Add success context
        response.add_context(f"Persisted artifact: {new_filename}")
        response.add_context(f"Source: {source_file_path}")
        response.add_context(f"Destination: {new_filepath}")
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to persist artifact: {str(e)}")
    
    return response
