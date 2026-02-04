from typing_extensions import Literal
from mcp_object import mcp
from read_an_asset import read_asset

@mcp.prompt()
def implementation_command_prompt(
    phase_number: int,
    task_number: int
) -> str:
    """
    A useful prompt to instruct the assistant to implement a phase/task.

    Args:
        phase_number (int): The phase number to implement
        task_number (int): The task number to implement

    Returns:
        str: The implementation command prompt
    """
    template = read_asset("implementation_command.md")
    return template.format(
        phase_number=phase_number,
        task_number=task_number
    )
