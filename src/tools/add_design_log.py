import os
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import add_document, validate_absolute_path


def append_to_summary(summary_path: str, filename: str, short_desc: str) -> tuple[bool, str]:
    """
    Append an entry to a summary.md file.
    
    Args:
        summary_path: Path to the summary.md file.
        filename: The filename of the new document.
        title: The title of the new document.
        short_desc: A short description for the new document.
    
    Returns:
        A tuple of (success: bool, message: str).
    """
    if os.path.exists(summary_path):
        with open(summary_path, 'a', encoding='utf-8') as f:
            f.write(f"- `{filename}`: {short_desc}\n")
        return True, "Added entry to summary.md"
    else:
        return False, f"Warning: summary.md not found at {summary_path}"


def update_design_log_summary(response: GlyphMCPResponse[None], abs_path: str, title: str, short_desc: str) -> None:
    """
    Update the _summary.md file with the newly created design log entry.
    
    Args:
        response: The response object from add_document.
        abs_path: The absolute path of the project's root where the .assistant folder is located.
        title: The title of the design log.
        short_desc: A short description for the design log.
    """
    if not response.success:
        return
    
    design_logs_dir = os.path.join(abs_path, BASE_NAME, "design_logs")
    summary_path = os.path.join(design_logs_dir, "_summary.md")
    
    # Extract filename from the context message
    for context in response.context:
        if "Created new design log:" in context:
            filename = context.split(": ")[1]
            success, message = append_to_summary(summary_path, filename, short_desc)
            response.add_context(message)
            break


@mcp.tool()
def add_design_log(abs_path: str, title: str, short_desc: str) -> GlyphMCPResponse[None]:
    """
    Add a new design log file in the design log directory.

    Prerequisite: Read the design log rules.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        title: The title for the design log. The file will be named dl_{number}_{title}.md
        short_desc: A short description for the design log. Will be used in the summary.
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    if not validate_absolute_path(abs_path, response):
        return response
    
    response = add_document(
        abs_path=abs_path,
        title=title,
        subdirectory="design_logs",
        prefix="dl",
        template_asset="dl_template.md",
        doc_type="design log"
    )
    
    update_design_log_summary(response, abs_path, title, short_desc)
    
    return response
