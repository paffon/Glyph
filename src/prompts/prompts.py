"""
Consolidated prompts module.

All Glyph prompts (slash commands) in one place.
"""
from typing import Literal
from mcp_object import mcp
from read_an_asset import read_asset


# =============================================================================
# DESIGN LOG & OPERATION CREATION
# =============================================================================

@mcp.prompt()
def create_design_log_prompt(
    topic: str,
    design_log_type: Literal["research", "implementation", "both"] = "both",
    additional_context: str = ""
) -> str:
    """
    Trigger the creation of a new design log.

    Args:
        topic: The topic or feature for the design log
        design_log_type: Type - "research", "implementation", or "both"
        additional_context: Any additional context or constraints

    Returns:
        The prompt for creating a design log.
    """
    template = read_asset("create_design_log.md")
    return template.format(
        topic=topic,
        design_log_type=design_log_type,
        additional_context=additional_context or "No additional context provided."
    )


@mcp.prompt()
def create_operation_doc_prompt(step_to_create_doc_for: float) -> str:
    """
    Trigger the creation of an operation document from a design log step.

    Args:
        step_to_create_doc_for: The step number to create the operation document for

    Returns:
        The prompt for creating an operation document.
    """
    template = read_asset("create_an_operation_doc.md")
    return template.format(step_to_create_doc_for=step_to_create_doc_for)


# =============================================================================
# PLANNING & IMPLEMENTATION
# =============================================================================

@mcp.prompt()
def planning_prompt(phase_number: int, task_number: int) -> str:
    """
    Trigger planning of a phase/task from an operation document.

    Args:
        phase_number: The phase number to plan
        task_number: The task number to plan

    Returns:
        The planning prompt.
    """
    template = read_asset("planning_command.md")
    return template.format(phase_number=phase_number, task_number=task_number)


@mcp.prompt()
def implementation_prompt(phase_number: int, task_number: int) -> str:
    """
    Trigger implementation of a phase/task from an operation document.

    Args:
        phase_number: The phase number to implement
        task_number: The task number to implement

    Returns:
        The implementation prompt.
    """
    template = read_asset("implementation_command.md")
    return template.format(phase_number=phase_number, task_number=task_number)


# =============================================================================
# CODE REVIEW & SYNC
# =============================================================================

@mcp.prompt()
def code_review_prompt(
    operation_name: str = "No operation name provided",
    design_log_name: str = "No design log provided"
) -> str:
    """
    Trigger a code review of an operation.

    Args:
        operation_name: (Optional) Name of the operation being reviewed
        design_log_name: (Optional) Name of the related design log

    Returns:
        The code review prompt.
    """
    template = read_asset("code_review.md")
    return template.format(
        operation_name=operation_name,
        design_log_name=design_log_name
    )


@mcp.prompt()
def sync_lessons_learned_prompt(
    sync_mode: Literal["single", "batch", "scan"] = "single",
    operation_list: str = ""
) -> str:
    """
    Sync lessons learned from operations back to design logs.

    Args:
        sync_mode: Mode - "single", "batch", or "scan" (find all unsynced)
        operation_list: Comma-separated operation doc paths, or "all" for scan mode

    Returns:
        The sync lessons learned prompt.
    """
    template = read_asset("sync_lessons_learned.md")
    return template.format(
        sync_mode=sync_mode,
        operation_list=operation_list or "Please specify operation document paths"
    )


# =============================================================================
# UTILITY
# =============================================================================

@mcp.prompt()
def compact_conversation_prompt() -> str:
    """
    Summarize a long conversation for context transfer to a new session.

    Returns:
        The compact conversation prompt.
    """
    return read_asset("compact_conversation.md")
