"""
Consolidated prompts module.

All Glyph prompts (slash commands) in one place.
"""
from typing import Any, Dict, List, Literal
from mcp_object import mcp
from read_an_asset import read_asset


def replace_in_prompts(prompt: str, replacements_dict: Dict[str, Any]) -> str:
    """
    Replace placeholders in a prompt string based on a replacements dictionary.

    Args:
        prompt: The original prompt string with placeholders
        replacements_dict: A dictionary mapping placeholders to their replacements

    Returns:
        The prompt string with placeholders replaced
    """
    warnings: List[str] = []

    for k, v in replacements_dict.items():
        this = "{{" + k + "}}"
        that = str(v)

        if this not in prompt:
            warnings.append(f"Placeholder {this} not found in prompt.")
            continue
        
        prompt = prompt.replace(this, that)
    
    if warnings:
        prompt += "\n\n-----WARNING:\n\n" + "\n".join(warnings)

    return prompt


def _normalize_number(value: int | float | str) -> str:
    """Convert numeric value to clean string (float 1.0 → int 1 → str '1')."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _format_task_display(task_number: str | int | float) -> str:
    """
    Convert task_number to grammatically correct display format.
    
    Examples:
        - 1 → "Task 1"
        - "3" → "Task 3"
        - "1-3" → "Tasks 1-3"
        - "1, 2, 5" → "Tasks 1, 2, 5"
        - "all" → "all tasks"
    """
    task_str = _normalize_number(task_number)
    
    if task_str == "all":
        return "all tasks"
    elif task_str.isdigit():
        return f"Task {task_str}"
    else:
        # It's a range like "1-3" or comma-separated like "1, 2, 5"
        return f"Tasks {task_str}"


def _load_phase_prompt(
    asset_filename: str,
    phase_number: int | float,
    task_number: str | int | float,
    operation_document: str,
    additional_context: str = "Nothing specific, but feel free to read more files"
) -> str:
    """
    Load and format a phase prompt (planning or implementation).
    
    Args:
        asset_filename: The markdown asset file to load (e.g., "planning_command.md")
        phase_number: The phase number
        task_number: The task(s) to display
        operation_document: The operation document name/path
        additional_context: Optional context to include in the prompt
        
    Returns:
        Formatted prompt text
        
    Raises:
        ValueError: If phase_number < 1
    """
    # Normalize and validate phase number
    phase_int = int(phase_number) if isinstance(phase_number, float) and phase_number.is_integer() else phase_number
    if isinstance(phase_int, int) and phase_int < 1:
        raise ValueError(f"phase_number must be >= 1, got {phase_int}")
    
    template = read_asset(asset_filename)
    task_display = _format_task_display(task_number)
    return replace_in_prompts(template, {
        "phase_number": _normalize_number(phase_number),
        "task_display": task_display,
        "operation_document": operation_document,
        "additional_context": additional_context
    })


# =============================================================================
# DESIGN LOG & OPERATION CREATION
# =============================================================================

@mcp.prompt()
def create_design_log_prompt(
    topic: str,
    design_log_type: Literal["research", "implementation", "both"] = "both",
    additional_context: str = "Nothing specific, but feel free to read more files"
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
    return replace_in_prompts(template, {
        "topic": topic,
        "design_log_type": design_log_type,
        "additional_context": additional_context or "No additional context provided."
    })


@mcp.prompt()
def create_operation_doc_prompt(
    step_to_create_doc_for: int | float | str,
    design_log_name: str
) -> str:
    """
    Trigger the creation of an operation document from a design log step.

    Args:
        step_to_create_doc_for: The step number or identifier to create the operation document for
        design_log_name: Name or path of the design log (default: "Design Log")

    Returns:
        The prompt for creating an operation document.
    """
    template = read_asset("create_an_operation_doc.md")
    return replace_in_prompts(template, {
        "step_to_create_doc_for": _normalize_number(step_to_create_doc_for),
        "design_log_name": design_log_name
    })


# =============================================================================
# PLANNING & IMPLEMENTATION
# =============================================================================

@mcp.prompt()
def planning_prompt(
    phase_number: int | float,
    task_number: str | int | float = "all",
    operation_document: str = "Operation Document",
    additional_context: str = "Nothing specific, but feel free to read more files"
) -> str:
    """
    Trigger planning of a phase/task from an operation document.

    Args:
        phase_number: The phase number to plan
        task_number: The task(s) to plan. Can be:
                     - Single task: 1, 2, 5
                     - Range: "1-3"
                     - Multiple: "1, 2, 5"
                     - All tasks: "all" (default)
        operation_document: Name or path of the operation document (default: "Operation Document")
        additional_context: Optional context to include in the prompt

    Returns:
        The planning prompt.
    """
    return _load_phase_prompt(
        "planning_command.md",
        phase_number,
        task_number,
        operation_document,
        additional_context
    )


@mcp.prompt()
def implementation_prompt(
    phase_number: int | float,
    task_number: str | int | float = "all",
    operation_document: str = "Operation Document",
    additional_context: str = "Nothing specific, but feel free to read more files"
) -> str:
    """
    Trigger implementation of a phase/task from an operation document.

    Args:
        phase_number: The phase number to implement
        task_number: The task(s) to implement. Can be:
                     - Single task: 1, 2, 5
                     - Range: "1-3"
                     - Multiple: "1, 2, 5"
                     - All tasks: "all" (default)
        operation_document: Name or path of the operation document (default: "Operation Document")
        additional_context: Optional context to include in the prompt

    Returns:
        The implementation prompt.
    """
    return _load_phase_prompt(
        "implementation_command.md",
        phase_number,
        task_number,
        operation_document,
        additional_context
    )


# =============================================================================
# CODE REVIEW & SYNC
# =============================================================================

@mcp.prompt()
def code_review_prompt(
    operation_name: str = "No operation name provided",
    design_log_name: str = "No design log provided",
    additional_context: str = "Nothing specific, but feel free to read more files"
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
    return replace_in_prompts(template, {
        "operation_name": operation_name,
        "design_log_name": design_log_name,
        "additional_context": additional_context
    })


@mcp.prompt()
def sync_lessons_learned_prompt(
    operations_list: str = "Please specify operation document paths",
    design_logs_list: str = "Design logs will be auto-detected from operation references"
) -> str:
    """
    Sync lessons learned from operations back to design logs.

    Args:
        operations_list: Comma-separated operation doc paths to sync from
        design_logs_list: Comma-separated design log paths to sync to (auto-detected if not specified)

    Returns:
        The sync lessons learned prompt.
    """
    template = read_asset("sync_lessons_learned.md")
    return replace_in_prompts(template, {
        "operations_list": operations_list,
        "design_logs_list": design_logs_list
    })


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
