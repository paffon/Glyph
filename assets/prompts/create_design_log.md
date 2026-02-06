---
In this prompt:

<topic> = {{topic}}
<design_log_type> = {{design_log_type}}
<additional_context> = {{additional_context}}
---

# Your mission

Create a design log for <topic>

**Design Log Type:** <design_log_type>
<!-- Options: research, implementation, or both -->

## Before starting

1. Read the design log principles using `get_design_log_principles`
2. Read the `how_to_glyph` skill to understand the workflow
3. Ask clarifying questions if the scope is unclear

## Context

- <additional_context>

## Process

1. **Understand the scope**: What problem are we solving? What decisions need to be made?
2. **Gather information**: What existing code, documentation, or constraints are relevant?
3. **Ask questions**: List unknowns that need answers before proceeding
4. **Research options**: For research logs, explore alternatives and trade-offs
5. **Design solution**: For implementation logs, detail the architecture and plan
6. **Create the log**: Use Glyph's `add_design_log` tool to create the file, then populate it

## When creating the log

- Use clear, descriptive title (will become filename)
- Include Background, Problem, Q&A sections
- For research: focus on options, trade-offs, recommendations
- For implementation: include architecture, file structure, implementation plan
- Add references to related design logs, operations, or artifacts
- Define verification criteria: how do we know we've solved the problem?

## After creating

1. Review with the user for completeness
2. Identify any open questions that need answering
3. If implementation type, outline the phases for the operation doc