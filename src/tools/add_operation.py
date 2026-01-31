import os
import re
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from read_an_asset import read_asset


def get_next_op_number(operations_dir: str) -> int:
    """
    Get the next operation number by scanning existing files in the operations directory.
    
    Args:
        operations_dir: Path to the operations directory.
    
    Returns:
        The next available operation number.
    """
    if not os.path.exists(operations_dir):
        return 1
    
    max_number = 0
    pattern = re.compile(r'^op_(\d+)_.*\.md$')
    
    for filename in os.listdir(operations_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_number:
                max_number = num
    
    return max_number + 1


@mcp.tool()
def add_operation(base_dir_path: str, title: str) -> GlyphMCPResponse[None]:
    """
    Add a new operation document file in the operations directory.
    
    Prerequisite: Read the operation rules.
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        title: The title for the operation. The file will be named op_{number}_{title}.md
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        # Construct the operations directory path
        operations_dir = os.path.join(base_dir_path, BASE_NAME, "operations")
        
        # Check if the assistant directory is initialized
        if not os.path.exists(operations_dir):
            response.add_context(f"Operations directory not found at {operations_dir}. Please initialize the assistant directory first.")
            return response
        
        # Get the next operation number
        next_number = get_next_op_number(operations_dir)
        
        # Sanitize the title for use in filename (replace spaces with underscores, remove special chars)
        sanitized_title = re.sub(r'[^\w\s-]', '', title).strip()
        sanitized_title = re.sub(r'[-\s]+', '_', sanitized_title).lower()
        
        # Create the new filename
        new_filename = f"op_{next_number}_{sanitized_title}.md"
        new_filepath = os.path.join(operations_dir, new_filename)
        
        # Read the template
        template_content: str = read_asset("operation_doc_template.md")
        
        # Write the new operation file
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        response.add_context(f"Created new operation document: {new_filename}")
        
        # Append entry to summary.md
        summary_path = os.path.join(operations_dir, "_summary.md")
        
        if os.path.exists(summary_path):
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"\n- **[{new_filename}]({new_filename})**: {title}\n")
            response.add_context(f"Added entry to summary.md")
        else:
            response.add_context(f"Warning: summary.md not found at {summary_path}")
        
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to create operation document: {str(e)}")
    
    return response
