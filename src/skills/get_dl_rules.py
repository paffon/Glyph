from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import read_asset_with_response


@mcp.tool()
def get_dl_rules() -> GlyphMCPResponse[str]:
    """
    Returns the design log methodology rules from the assets directory.
    Use this tool anytime you create, modify, or review a design log to ensure compliance with the methodology.
    Contains guidelines on structure, content, and best practices for design logs.
    
    Returns:
        The content of design_log_rules.md as a string containing the design log methodology rules.
    """
    return read_asset_with_response("design_log_rules.md")
