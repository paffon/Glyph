from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import add_document, validate_absolute_path


@mcp.tool()
def add_operation(abs_path: str, title: str) -> GlyphMCPResponse[None]:
    """
    Add a new operation document file in the operations directory.
    
    Prerequisite: Read the operation rules.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        title: The title for the operation. The file will be named op_{number}_{title}.md
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    if not validate_absolute_path(abs_path, response):
        return response
    
    return add_document(
        abs_path=abs_path,
        title=title,
        subdirectory="operations",
        prefix="op",
        template_asset="operation_doc_template.md",
        doc_type="operation document"
    )
