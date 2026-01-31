"""
Utility functions shared across skill modules.
"""
from response import GlyphMCPResponse
from read_an_asset import read_asset


def read_asset_with_response(filename: str) -> GlyphMCPResponse[str]:
    """
    Read an asset file and return it wrapped in a GlyphMCPResponse.
    
    Args:
        filename: Name of the file in the assets directory to read.
    
    Returns:
        GlyphMCPResponse containing the file content or error information.
    """
    response = GlyphMCPResponse[str]()
    content = read_asset(filename)
    
    # Check if content is an error message
    if content.startswith("Asset file") or content.startswith("Error reading"):
        response.add_context(content)
    else:
        response.success = True
        response.result = content
    
    return response
