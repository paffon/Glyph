import os
import csv
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import validate_absolute_path


def get_all_filenames(directory: str) -> list[str]:
    """
    Get all filenames from a directory recursively.
    
    Args:
        directory: Path to the directory to scan.
    
    Returns:
        List of filenames in the directory and its subdirectories.
    """
    filenames = []
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            filenames.extend(files)
    return filenames


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


def build_reference_edges(assistant_dir: str, all_filenames: list[str]) -> tuple[list[tuple[str, str]], dict[str, str]]:
    """
    Scan all files and build reference edges.
    
    Args:
        assistant_dir: Path to the .assistant directory.
        all_filenames: List of all filenames to check for references.
    
    Returns:
        Tuple of (edges, file_to_dir_mapping) where:
        - edges: List of tuples representing edges (source_file, referenced_file)
        - file_to_dir_mapping: Dict mapping filename to its directory type
    """
    dirs_names = ["design_logs", "operations", "artifacts"]
    
    edges = []
    file_to_dir = {}
    
    for dir_name in dirs_names:
        directory = os.path.join(assistant_dir, dir_name)
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            for filename in files:
                # Skip _summary.md files as they trivially contain many filenames
                if filename == "_summary.md":
                    continue
                    
                file_path = os.path.join(root, filename)
                
                # Track which directory this file belongs to
                file_to_dir[filename] = dir_name
                
                referenced_files = find_file_references(file_path, all_filenames)
                
                # Add edges (excluding self-references)
                for referenced_file in referenced_files:
                    if referenced_file != filename:
                        edges.append((filename, referenced_file))
    
    return edges, file_to_dir


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


def write_reference_mermaid(md_path: str, edges: list[tuple[str, str]], file_to_dir: dict[str, str]) -> None:
    """
    Write reference edges as a Mermaid graph in a Markdown file.
    
    Args:
        md_path: Path to the Markdown file to create/update.
        edges: List of edge tuples to write.
        file_to_dir: Dict mapping filename to its directory type.
    """
    # Detect and consolidate bidirectional links
    edges_set = set(edges)
    bidirectional_pairs = set()
    consolidated_edges = []
    
    for source, target in edges:
        # Check if reverse edge exists
        reverse = (target, source)
        edge_pair = (min(source, target), max(source, target))
        
        if reverse in edges_set and edge_pair not in bidirectional_pairs:
            # This is a bidirectional link - mark it and add only once
            bidirectional_pairs.add(edge_pair)
            consolidated_edges.append((source, target, True))  # True = bidirectional
        elif (source, target) not in [(s, t) for s, t, _ in consolidated_edges]:
            # Check if we haven't already added this as part of a bidirectional pair
            reverse_pair = (min(target, source), max(target, source))
            if reverse_pair not in bidirectional_pairs:
                consolidated_edges.append((source, target, False))  # False = directional
    
    # Collect all unique nodes from consolidated edges
    nodes = set()
    for source, target, _ in consolidated_edges:
        nodes.add(source)
        nodes.add(target)
    
    # Build Mermaid diagram
    lines = ["```mermaid", "graph TD"]
    
    # Add style classes
    lines.append("    classDef designLog fill:#FFC0CB,stroke:#000,color:#000")
    lines.append("    classDef operation fill:#006400,stroke:#000,color:#fff")
    lines.append("    classDef artifact fill:#FF8C00,stroke:#000,color:#fff")
    lines.append("")
    
    # Group nodes by directory and add them with styling
    for node in sorted(nodes):
        dir_type = file_to_dir.get(node)
        if dir_type:
            # Sanitize node name for Mermaid (replace special chars)
            safe_node = node.replace(".", "_").replace("-", "_").replace(" ", "_")
            
            # Determine class
            if dir_type == "design_logs":
                node_class = "designLog"
            elif dir_type == "operations":
                node_class = "operation"
            elif dir_type == "artifacts":
                node_class = "artifact"
            else:
                node_class = ""
            
            # Add node definition with label
            lines.append(f"    {safe_node}[\"{node}\"]")
            if node_class:
                lines.append(f"    class {safe_node} {node_class}")
    
    lines.append("")
    
    # Add edges (using --- for bidirectional, --> for directional)
    for source, target, is_bidirectional in consolidated_edges:
        safe_source = source.replace(".", "_").replace("-", "_").replace(" ", "_")
        safe_target = target.replace(".", "_").replace("-", "_").replace(" ", "_")
        arrow = " --- " if is_bidirectional else " --> "
        lines.append(f"    {safe_source}{arrow}{safe_target}")
    
    lines.append("```")
    
    # Write to file
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))


@mcp.tool()
def update_reference_graph(abs_path: str) -> GlyphMCPResponse[None]:
    """
    Scan all design logs, operations, and artifacts for references and update reference_graph.csv.
    
    This tool will:
    1. Get all filenames from design_logs, operations, and artifacts directories
    2. For each file in these directories, find which other filenames are mentioned in it
    3. Create or update the reference_graph.csv file in the .assistant directory
    
    The CSV has two columns: start_point and end_point, representing directed edges in the reference graph.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
    
    Returns:
        GlyphMCPResponse indicating success or failure with statistics.
    """
    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response
    
    try:
        assistant_dir = os.path.join(abs_path, BASE_NAME)
        
        if not os.path.exists(assistant_dir):
            response.add_context(
                f"Assistant directory not found at {assistant_dir}. "
                "Please initialize the assistant directory first."
            )
            return response
        
        # Collect all filenames, build edges, and write both CSV and Mermaid MD
        all_filenames = collect_all_filenames(assistant_dir)
        edges, file_to_dir = build_reference_edges(assistant_dir, all_filenames)
        
        csv_path = os.path.join(assistant_dir, "reference_graph.csv")
        md_path = os.path.join(assistant_dir, "reference_graph.md")
        
        write_reference_csv(csv_path, edges)
        write_reference_mermaid(md_path, edges, file_to_dir)
        
        # Statistics
        unique_sources = len(set(edge[0] for edge in edges))
        total_edges = len(edges)
        
        response.add_context(f"Reference graph updated successfully")
        response.add_context(f"CSV: {csv_path}")
        response.add_context(f"Mermaid: {md_path}")
        response.add_context(f"Statistics: {unique_sources} files with references, {total_edges} reference edges")
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to update reference graph: {str(e)}")
    
    return response


def _query_reference_graph(abs_path: str, file_name: str, match_column: str, return_column: str, context_msg: str) -> GlyphMCPResponse[list[str]]:
    """
    Helper function to query the reference graph CSV.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located.
        file_name: The name of the file to search for.
        match_column: The column name to match against (e.g., 'start_point' or 'end_point').
        return_column: The column name to return values from.
        context_msg: The success message template (should contain {count} and {file_name}).
    
    Returns:
        GlyphMCPResponse containing a list of matching filenames.
    """
    response = GlyphMCPResponse[list[str]]()
    
    try:
        # First update the reference graph to ensure it's current
        update_response = update_reference_graph(abs_path)
        if not update_response.success:
            response.add_context("Failed to update reference graph")
            response.add_context(update_response.context)
            return response
        
        assistant_dir = os.path.join(abs_path, BASE_NAME)
        csv_path = os.path.join(assistant_dir, "reference_graph.csv")
        
        if not os.path.exists(csv_path):
            response.add_context(f"Reference graph CSV not found at {csv_path}")
            return response
        
        matching_files = []
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row[match_column] == file_name:
                    matching_files.append(row[return_column])
        
        response.success = True
        response.result = matching_files
        response.add_context(context_msg.format(count=len(matching_files), file_name=file_name))
        
    except Exception as e:
        response.add_context(f"Failed to query reference graph for {file_name}: {str(e)}")
    
    return response


@mcp.tool()
def get_references_from(abs_path: str, file_name: str) -> GlyphMCPResponse[list[str]]:
    """
    Get all files that are referenced by the specified file.
    
    This tool will:
    1. Update the reference graph to ensure it's current
    2. Read the reference_graph.csv file
    3. Return all files that the specified file references
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        file_name: The name of the file to find references from.
    
    Returns:
        GlyphMCPResponse containing a list of filenames that are referenced by the specified file.
    """
    return _query_reference_graph(
        abs_path, 
        file_name, 
        match_column='start_point',
        return_column='end_point',
        context_msg="Found {count} files referenced by {file_name}"
    )


@mcp.tool()
def find_references_to(abs_path: str, file_name: str) -> GlyphMCPResponse[list[str]]:
    """
    Find all files that reference the specified file.
    
    This tool will:
    1. Update the reference graph to ensure it's current
    2. Read the reference_graph.csv file
    3. Return all files that reference the specified file
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        file_name: The name of the file to find references to.
    
    Returns:
        GlyphMCPResponse containing a list of filenames that reference the specified file.
    """
    return _query_reference_graph(
        abs_path, 
        file_name, 
        match_column='end_point',
        return_column='start_point',
        context_msg="Found {count} files that reference {file_name}"
    )
