from typing_extensions import Literal
from mcp_object import mcp
from read_an_asset import read_asset

@mcp.prompt()
def planning_command_prompt(
    phase_number: int,
    task_number: int
) -> str:
    """
    A useful prompt to instruct the assistant to plan a phase/task.

    Args:
        phase_number (int): The phase number to plan
        task_number (int): The task number to plan

    Returns:
        str: The planning command prompt
    """
    template = read_asset("planning_command.md")
    return template.format(
        phase_number=phase_number,
        task_number=task_number
    )