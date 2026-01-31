from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import read_asset_with_response


@mcp.tool()
def get_operation_rules() -> GlyphMCPResponse[str]:
    """
    Returns the operation methodology rules from the assets directory.
    Use this tool anytime you create, modify, or review an operation to ensure compliance with the methodology.
    Contains guidelines on structure, content, and best practices for operations.
    
    Returns:
        The content of operation_rules.md as a string containing the operation methodology rules.
    """
    return read_asset_with_response("operation_rules.md")
