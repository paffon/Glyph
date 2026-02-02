from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import read_asset_with_response


@mcp.tool()
def get_how_to_glyph() -> GlyphMCPResponse[str]:
    """
    Returns a comprehensive guide to all Glyph tools and skills.
    Use this tool when you need to understand which tools and skills are available,
    when to use them, how they work together, and how to work with the ad hoc directory and artifact persistence.
    
    Returns:
        The content of _how_to_glyph.md as a string containing the complete Glyph usage guide.
    """
    return read_asset_with_response("_how_to_glyph.md")
