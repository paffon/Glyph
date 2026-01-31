from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import read_asset_with_response


@mcp.tool()
def get_task_implementation_guidelines() -> GlyphMCPResponse[str]:
    """
    Returns the task planning and implementation guidelines from the assets directory.
    ALWAYS use this tool when asked to plan/implement a phase/task to ensure you follow best practices.
    Contains essential guidelines on how to approach task implementation effectively.
    
    Returns:
        The content of read_before_task_planning_and_implementation.md as a string containing the implementation guidelines.
    """
    return read_asset_with_response("read_before_task_planning_and_implementation.md")
