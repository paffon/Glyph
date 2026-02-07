In this prompt:

<phase_number> = {{phase_number}}
<task_display> = {{task_display}}
<operation_document> = {{operation_document}}
<additional_context> = {{additional_context}}
---

# Your mission

Plan Phase <phase_number> / <task_display> from <operation_document>

## Before you start

1. Check if the task is still relevant. This is a living project—if it's changed significantly, inform me before proceeding.
2. Read the Background section of the operation document.
3. Read previous task/phase bottom lines and lessons learned, if any.
4. <additional_context>

## Planning principles

1. **Reuse over creation:** Check if reusable/adaptable solutions exist, but only if it doesn't add unnecessary complexity. If creating something new is simpler—do that instead.
2. **Balance SOLID, DRY, and KISS:** Do not overengineer. For complex tasks, explain how you'll keep them simple.
3. **Clarify ambiguity:** If the task description is unclear, ask me with specific options (e.g., "A, B, or C?"). Avoid assumptions.

## Define your plan

Create a detailed plan for <phase_number> / <task_display> which includes:

- **Current state:** Brief description of the current situation
- **Objectives:** What the task aims to achieve
- **Steps:** Clear sequence of actions. Start with benchmarking (warnings, errors, test fails). End with cleanup and verification (no new warnings/errors, tests pass). Final action: generate commit message format shown below.
- **Dependencies:** Prerequisites or external factors
- **Risk Assessment:** Possible risks and mitigation strategies (free-text paragraph)

## Getting feedback

- For **complex plans** (anything beyond straightforward steps): Present with enumerated options and wait for approval
- For **straightforward plans:** Simply ask for go-ahead

## After implementation

1. Add lessons learned/bottom line to the operation doc specifically under <phase_number> / <task_display>'s section (succinct; skip obvious items. e.g. No need to mention success as it's the norm).
2. Add comments to future tasks/phases if you discovered something affecting them, such that the comments await future developers.
3. Generate a commit message (Base the commit message on what you actually did, not just the task description. If you deviated, reflect that in the message.):

```txt
[operation name] P-<phase_number>/T-<task_display> - <short task title>: Description of actual change
```