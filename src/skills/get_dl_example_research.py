from typing import Literal
from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import read_asset_with_response


@mcp.tool()
def get_dl_example(example_type: Literal["research_dl_example", "implementation_dl_example"]) -> GlyphMCPResponse[str]:
    """
    Returns the content of a design log example from the assets directory.
    Use this tool when you need to reference a design log example for research or implementation.
    
    Args:
        example_type: Type of design log example to retrieve. Must be either:
            - "research_dl_example": Returns dl_example_research.md
            - "implementation_dl_example": Returns dl_example_implementation.md
    
    Returns:
        The content of the requested design log example as a string.
    """
    # Map example types to file names
    file_map = {
        "research_dl_example": "dl_example_research.md",
        "implementation_dl_example": "dl_example_implementation.md"
    }
    
    # Get the filename for the requested type
    filename = file_map.get(example_type)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid example type: {example_type}. Must be 'research_dl_example' or 'implementation_dl_example'")
        return response
    
    return read_asset_with_response(filename)
