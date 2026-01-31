import os
import csv
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse


def get_all_filenames(directory: str) -> list[str]:
    """
    Get all filenames from a directory.
    
    Args:
        directory: Path to the directory to scan.
    
    Returns:
        List of filenames in the directory.
    """
    if not os.path.exists(directory):
        return []
    
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def find_file_references(file_path: str, target_filenames: list[str]) -> list[str]:
    """
    Find which target filenames are mentioned in a file.
    
    Args:
        file_path: Path to the file to scan.
        target_filenames: List of filenames to search for.
    
    Returns:
        List of filenames that were found mentioned in the file.
    """
    references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for filename in target_filenames:
                if filename in content:
                    references.append(filename)
    except Exception as e:
        # Silently skip files that can't be read
        pass
    
    return references


def collect_all_filenames(assistant_dir: str) -> list[str]:
    """
    Collect all filenames from design_logs, operations, and artifacts directories.
    
    Args:
        assistant_dir: Path to the .assistant directory.
    
    Returns:
        List of all filenames across the three directories.
    """
    all_filenames = []

    for dir_name in ["design_logs", "operations", "artifacts"]:
        dir_path = os.path.join(assistant_dir, dir_name)
        all_filenames.extend(get_all_filenames(dir_path))
    
    return all_filenames


def build_reference_edges(assistant_dir: str, all_filenames: list[str]) -> list[tuple[str, str]]:
    """
    Scan all files and build reference edges.
    
    Args:
        assistant_dir: Path to the .assistant directory.
        all_filenames: List of all filenames to check for references.
    
    Returns:
        List of tuples representing edges (source_file, referenced_file).
    """
    dirs_names = ["design_logs", "operations", "artifacts"]
    
    edges = []
    
    for dir_name in dirs_names:
        directory = os.path.join(assistant_dir, dir_name)
        if not os.path.exists(directory):
            continue
            
        for filename in os.listdir(directory):
            # Skip _summary.md files as they trivially contain many filenames
            if filename == "_summary.md":
                continue
                
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue
            
            referenced_files = find_file_references(file_path, all_filenames)
            
            # Add edges (excluding self-references)
            for referenced_file in referenced_files:
                if referenced_file != filename:
                    edges.append((filename, referenced_file))
    
    return edges


def write_reference_csv(csv_path: str, edges: list[tuple[str, str]]) -> None:
    """
    Write reference edges to CSV file.
    
    Args:
        csv_path: Path to the CSV file to create/update.
        edges: List of edge tuples to write.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['start_point', 'end_point'])
        writer.writerows(edges)


@mcp.tool()
def update_reference_graph(base_path: str) -> GlyphMCPResponse[None]:
    """
    Scan all design logs, operations, and artifacts for references and update reference_graph.csv.
    
    This tool will:
    1. Get all filenames from design_logs, operations, and artifacts directories
    2. For each file in these directories, find which other filenames are mentioned in it
    3. Create or update the reference_graph.csv file in the .assistant directory
    
    The CSV has two columns: start_point and end_point, representing directed edges in the reference graph.
    
    Args:
        base_path: The base path where the .assistant folder is located.
    
    Returns:
        GlyphMCPResponse indicating success or failure with statistics.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        assistant_dir = os.path.join(base_path, BASE_NAME)
        
        if not os.path.exists(assistant_dir):
            response.add_context(
                f"Assistant directory not found at {assistant_dir}. "
                "Please initialize the assistant directory first."
            )
            return response
        
        # Collect all filenames, build edges, and write CSV
        all_filenames = collect_all_filenames(assistant_dir)
        edges = build_reference_edges(assistant_dir, all_filenames)
        csv_path = os.path.join(assistant_dir, "reference_graph.csv")
        write_reference_csv(csv_path, edges)
        
        # Statistics
        unique_sources = len(set(edge[0] for edge in edges))
        total_edges = len(edges)
        
        response.add_context(f"Reference graph updated successfully at {csv_path}")
        response.add_context(f"Statistics: {unique_sources} files with references, {total_edges} reference edges")
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to update reference graph: {str(e)}")
    
    return response


@mcp.tool()
def get_references_from(base_path: str, file_name: str) -> GlyphMCPResponse[list[str]]:
    """
    Get all files that are referenced by the specified file.
    
    This tool will:
    1. Update the reference graph to ensure it's current
    2. Read the reference_graph.csv file
    3. Return all files that the specified file references
    
    Args:
        base_path: The base path where the .assistant folder is located.
        file_name: The name of the file to find references from.
    
    Returns:
        GlyphMCPResponse containing a list of filenames that are referenced by the specified file.
    """
    response = GlyphMCPResponse[list[str]]()
    
    try:
        # First update the reference graph to ensure it's current
        update_response = update_reference_graph(base_path)
        if not update_response.success:
            response.add_context("Failed to update reference graph")
            response.add_context(update_response.context)
            return response
        
        assistant_dir = os.path.join(base_path, BASE_NAME)
        csv_path = os.path.join(assistant_dir, "reference_graph.csv")
        
        if not os.path.exists(csv_path):
            response.add_context(f"Reference graph CSV not found at {csv_path}")
            return response
        
        referenced_files = []
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['start_point'] == file_name:
                    referenced_files.append(row['end_point'])
        
        response.success = True
        response.result = referenced_files
        response.add_context(f"Found {len(referenced_files)} files referenced by {file_name}")
        
    except Exception as e:
        response.add_context(f"Failed to get references from {file_name}: {str(e)}")
    
    return response


@mcp.tool()
def find_references_to(base_path: str, file_name: str) -> GlyphMCPResponse[list[str]]:
    """
    Find all files that reference the specified file.
    
    This tool will:
    1. Update the reference graph to ensure it's current
    2. Read the reference_graph.csv file
    3. Return all files that reference the specified file
    
    Args:
        base_path: The base path where the .assistant folder is located.
        file_name: The name of the file to find references to.
    
    Returns:
        GlyphMCPResponse containing a list of filenames that reference the specified file.
    """
    response = GlyphMCPResponse[list[str]]()
    
    try:
        # First update the reference graph to ensure it's current
        update_response = update_reference_graph(base_path)
        if not update_response.success:
            response.add_context("Failed to update reference graph")
            response.add_context(update_response.context)
            return response
        
        assistant_dir = os.path.join(base_path, BASE_NAME)
        csv_path = os.path.join(assistant_dir, "reference_graph.csv")
        
        if not os.path.exists(csv_path):
            response.add_context(f"Reference graph CSV not found at {csv_path}")
            return response
        
        referencing_files = []
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['end_point'] == file_name:
                    referencing_files.append(row['start_point'])
        
        response.success = True
        response.result = referencing_files
        response.add_context(f"Found {len(referencing_files)} files that reference {file_name}")
        
    except Exception as e:
        response.add_context(f"Failed to find references to {file_name}: {str(e)}")
    
    return response
