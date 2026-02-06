"""
Consolidated knowledge/skills module.

Provides access to all Glyph knowledge assets: principles, examples, and guidelines.
"""
from typing import Literal
from mcp_object import mcp
from response import GlyphMCPResponse
from read_an_asset import read_asset, read_asset_exact as _read_asset_exact


def _read_asset_with_response(filename: str) -> GlyphMCPResponse[str]:
    """Read an asset file and return it wrapped in a GlyphMCPResponse."""
    response = GlyphMCPResponse[str]()
    content = read_asset(filename)
    
    if content.startswith("Asset file") or content.startswith("Error reading"):
        response.add_context(content)
    else:
        response.success = True
        response.result = content
    
    return response


# =============================================================================
# PRINCIPLES & GUIDELINES
# =============================================================================

@mcp.tool()
def get_glyph_overview() -> GlyphMCPResponse[str]:
    """
    Returns a comprehensive guide to all Glyph tools and skills.
    Use this tool when you need to understand which tools and skills are available,
    when to use them, how they work together, and how to work with the ad hoc directory 
    and artifact persistence.

    Returns:
        The complete Glyph usage guide.
    """
    return _read_asset_with_response("_how_to_glyph.md")


@mcp.tool()
def get_principles(
    topic: Literal["design_log", "operation", "task"]
) -> GlyphMCPResponse[str]:
    """
    Returns methodology principles for the specified topic.
    Use this tool when creating, modifying, or reviewing design logs, operations, or tasks.

    Args:
        topic: The topic to get principles for:
            - "design_log": Guidelines for creating and maintaining design logs
            - "operation": Guidelines for creating and managing operations
            - "task": Guidelines for planning and implementing tasks

    Returns:
        The principles/guidelines for the requested topic.
    """
    file_map = {
        "design_log": "design_log_rules.md",
        "operation": "operation_rules.md",
        "task": "read_before_task_planning_and_implementation.md"
    }
    
    filename = file_map.get(topic)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid topic: {topic}. Must be one of: {', '.join(file_map.keys())}")
        return response
    
    return _read_asset_with_response(filename)


# =============================================================================
# EXAMPLES
# =============================================================================

@mcp.tool()
def get_example(
    example_type: Literal["design_log_research", "design_log_implementation", "operation", "code_review"]
) -> GlyphMCPResponse[str]:
    """
    Returns an example file for the specified document type.
    Use this tool when you need to reference an example for creating design logs, 
    operations, or code reviews.

    Args:
        example_type: Type of example to retrieve:
            - "design_log_research": Example design log focused on research
            - "design_log_implementation": Example design log focused on implementation
            - "operation": Example operation document
            - "code_review": Example code review report

    Returns:
        The content of the requested example.
    """
    file_map = {
        "design_log_research": "dl_example_research.md",
        "design_log_implementation": "dl_example_implementation.md",
        "operation": "operation_example.md",
        "code_review": "code_review_example.md"
    }

    filename = file_map.get(example_type)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid example type: {example_type}. Must be one of: {', '.join(file_map.keys())}")
        return response

    return _read_asset_with_response(filename)


# =============================================================================
# GENERIC ASSET READER
# =============================================================================

@mcp.tool()
def read_asset_exact(relative_path: str) -> GlyphMCPResponse[str]:
    """
    Reads the content of a file from the assets directory using an exact relative path.
    
    Use this tool when:
    - You know the exact location of the asset you want to read
    - You need to read a file not covered by get_principles() or get_example()
    
    Example paths:
    - 'prompts/compact_conversation.md'
    - 'rules/design_log_rules.md'
    - 'templates/dl_template.md'
    - 'examples/dl_example_research.md'

    Args:
        relative_path: Path relative to the assets directory.

    Returns:
        The file content or error information.
    """
    response = GlyphMCPResponse[str]()
    content = _read_asset_exact(relative_path)
    
    if content.startswith("Asset file") or content.startswith("Error reading"):
        response.add_context(content)
    else:
        response.success = True
        response.result = content
    
    return response


@mcp.tool()
def mermaid_whisperer() -> GlyphMCPResponse[str]:
    """
    Retrieve examples of how different mermaid charts look.

    Returns:
        GlyphMCPResponse containing the complete mermaid chart examples.
    """
    return _read_asset_with_response("examples/mermaid_chart_types.md")

