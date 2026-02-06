---
In this prompt:

<phase_number> = {{phase_number}}
<task_display> = {{task_display}}
<operation_document> = {{operation_document}}
<additional_context> = {{additional_context}}
---

# Your mission

Implement Phase <phase_number> / <task_display> from <operation_document>.

## Before you start

1. Check if the task is still relevant. This is a living project—if it's changed significantly, inform me before proceeding.
2. Read the Background section of the operation document.
3. Read previous task/phase bottom lines and lessons learned, if any.
4. <additional_context>
5. If you find any ambiguities, inconsistencies, or missing information in the task description, ask me for clarification.
6. Check if something you're about to implement already exists and can be reused or slightly adapted. If so, let me know before proceeding.

## How to implement

1. Identify relevant documents and read them (use Glyph tools if needed to find related materials).
2. Build and run all tests to establish a benchmark (if applicable).
3. Implement the task, adhering to SOLID, DRY, and KISS principles.
4. Build/Run tests and compare to benchmark (if applicable).

## After implementation

1. Checkmark [x] the task(s) in the task list in the document if applicable.
2. If this is the last task of the phase, verify that the phase's D.O.D. checklist is complete and mark [x] on done items.
3. Add lessons learned / bottom line for this task/phase in the document (succinct; skip obvious items).
4. Consider future phases/tasks. If you discovered something affecting them, add a comment to the relevant task/phase.
5. Generate a commit message (base it on what you actually did, not just the task description):

```txt
[operation name] P-<phase_number>/T-<task_display> - <short task title>: Description of actual change
```