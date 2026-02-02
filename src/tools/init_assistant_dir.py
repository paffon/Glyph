import os
from sys import stdout
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import validate_absolute_path

def create_tree_recursive(abs_path: str, structure: dict): 
    """
    Recursively create a directory tree based on the provided structure.
    
    Args:
        abs_path: The absolute path where the tree should be created.
        structure: A dictionary defining the directory and file structure.
    """
    for item in structure.get("contains", []):
        if "dir_name" in item:
            dir_path = os.path.join(abs_path, item["dir_name"])
            os.makedirs(dir_path, exist_ok=True)
            create_tree_recursive(dir_path, item)
        elif "file_name" in item:
            file_path = os.path.join(abs_path, item["file_name"])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(item.get("content", ""))

def is_initialized(path: str) -> bool:
    """
    Check if the assistant directory is already initialized at the given path.
    
    Args:
        path: The path to check for initialization.
    Returns:
        True if initialized, False otherwise.
    """
    assistant_dir = os.path.join(path, BASE_NAME)
    return os.path.exists(assistant_dir)

@mcp.tool()
def init_assistant_dir(abs_path: str, overwrite: bool) -> GlyphMCPResponse:
    """
    User may refer to this tool as `glyph init`.
    Initialize the assistant directory at the given path. Recommended to use at the root of the project.
    Use this tool to set up the necessary directory structure for Glyph.
    If the directory already exists, please confirm with the user before overwriting.
    
    Args:
        abs_path: str, Path to the assistant directory. Recommended to use at the root of the project. Absolute path is required.
        overwrite: bool, Whether to overwrite the existing directory if it exists. Must only be True if the user has explicitly confirmed or asked for it.
    
    Returns:
        True if initialization is successful, False otherwise.
    """

    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response

    if is_initialized(abs_path):
        if overwrite:
            # Backup
            existing_dir_name = os.path.join(abs_path, BASE_NAME)
            backup_dir_name = os.path.join(abs_path, f"{BASE_NAME}_backup_{int(os.path.getmtime(existing_dir_name))}")
            os.rename(existing_dir_name, backup_dir_name)
            response.add_context(f"Existing assistant directory backed up to {backup_dir_name}.")
        else:
            response.add_context(f"Assistant directory already exists at {os.path.join(abs_path, BASE_NAME)}. Set overwrite=True to overwrite. Ask the user 'Looks like Glyph already initialized the assistant directory here. Do you want to overwrite it? Yes/No'")
            return response

    design_logs_summary_content = """# Design Logs summary

This file contains a summary of design logs. Each log is documented by file name and a brief description.
The main purpose of this file is to provide a quick overview of the design logs for easy reference, without having to read the entire content of each log.

## Design Logs

"""

    reference_graph_content = """start_point,end_point
"""

    dir_structure = [
        {
            "dir_name": BASE_NAME,
            "contains": [
                {"dir_name": "ad_hoc"},
                {"dir_name": "artifacts", "contains": [{"dir_name": "archived"}]},
                {"dir_name": "design_logs", "contains": [
                    {
                        "file_name": "_summary.md",
                        "content": design_logs_summary_content
                    },
                    {"dir_name": "archived"}
                ]},
                {"dir_name": "operations", "contains": [{"dir_name": "archived"}]},
                {
                    "file_name": "reference_graph.csv",
                    "content": reference_graph_content
                }
            ]
        }
    ]

    try:
        create_tree_recursive(abs_path, {"contains": dir_structure})
        response.success = True
        response.add_context(f"Assistant directory initialized at {os.path.join(abs_path, BASE_NAME)}.")

    except Exception as e:
        response.add_context(f"Failed to initialize assistant directory: {str(e)}")
    
    return response