import os
import shutil
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import get_next_number
from typing import List


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


def get_and_validate_dirs(base_dir_path: str, response: GlyphMCPResponse[None]) -> tuple[str, str] | None:
    """
    Get and validate the ad_hoc and artifacts directories.
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        response: Response object to add context messages to.
    
    Returns:
        A tuple of (ad_hoc_dir, artifacts_dir) if both exist, None otherwise.
    """
    ad_hoc_dir = os.path.join(base_dir_path, BASE_NAME, "ad_hoc")
    artifacts_dir = os.path.join(base_dir_path, BASE_NAME, "artifacts")

    if not os.path.exists(ad_hoc_dir):
        response.add_context(f"ad_hoc directory not found: {ad_hoc_dir}")
        return None
    
    if not os.path.exists(artifacts_dir):
        response.add_context(
            f"Artifacts directory not found at {artifacts_dir}. "
            "Please initialize the assistant directory first."
        )
        return None
    
    return ad_hoc_dir, artifacts_dir


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
    
    # Replace spaces with underscores in the filename
    sanitized_filename = original_filename.replace(' ', '_')
    
    # Create the new artifact filename
    new_filename = f"art_{next_number}_{sanitized_filename}"
    new_filepath = os.path.join(artifacts_dir, new_filename)
    
    # Copy the file to artifacts directory
    shutil.copy2(source_file_path, new_filepath)
    
    return new_filename, new_filepath


@mcp.tool()
def persist_artifacts(base_dir_path: str, files: List[str]) -> GlyphMCPResponse[None]:
    """
    Persist files from the ad_hoc directory to the artifacts directory.
    
    Copies each file to the .assistant/artifacts/ directory and renames it with the pattern:
    art_{serial_number}_{original_file_name}.{original_extension}
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        files: List of filenames to persist (excluding path, assumed to be in `.assistant/ad_hoc` dir).
    
    Returns:
        GlyphMCPResponse indicating success or failure, with the new artifact filenames.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        dirs = get_and_validate_dirs(base_dir_path, response)
        if dirs is None:
            return response
        
        ad_hoc_dir, artifacts_dir = dirs
        
        if not files:
            response.add_context("No files specified to persist.")
            return response
        
        for file_name in files:
            source_file_path = os.path.join(ad_hoc_dir, file_name)
            
            # Validate source file
            if not validate_source_file(source_file_path, response):
                continue  # Skip invalid files but continue with others
            
            # Copy the artifact
            new_filename, new_filepath = copy_artifact(source_file_path, artifacts_dir)
            
            # Add success context
            response.add_context(f"Persisted artifact: {new_filename}")
            response.add_context(f"Source: {source_file_path}")
            response.add_context(f"Destination: {new_filepath}")
        
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to persist artifacts: {str(e)}")
    
    return response
