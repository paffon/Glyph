# How to handle an Operation

An operation is a is a structured plan for implementing a feature or change in the codebase.
It contains background and phases with tasks and subtasks, each with checklists to ensure quality and completeness.

Once a template has been created for an operation using one of the MCP's tools, the operation file should be filled out before implementation begins.

## Key Guidelines

### Leading principles in creating an operation

- KISS (Keep It Simple, Stupid): Avoid unnecessary complexity. Each phase and task should be as straightforward as possible.
- SOLID principles: Ensure that each task adheres to the principles of good software design.
- Testing is generally done within subtasks, not as a task/phase on its own. Testing is part of the development process.

### Structure

- Background (Doesn't have to include all of these, only relevant ones):
  - Background Information
  - Problem Statement
  - Goals
  - Approach
  - Constraints
  - Assumptions
  - Definitions
  - References
  - Verification Criteria
  - Mermaid chart showing phases and tasks dependency (if applicable)
- Phases
  - Background for each phase (shorter and more concise than the overall background)
  - Definition of Done (D.O.D.) checklist
  - Tasks
    - Background for each task (specific to the task)
    - A list of files involved, with full paths
    - Subtasks as a checklist
    - Lessons learned for each task

### Phases

- Each phase must have a clear Definition of Done (D.O.D.) checklist.
- Phase has more than 1 task? Add another task, numberless, which verifies that the D.O.D. checklist is complete. If only one task exists in the phase, the D.O.D. check is done within that task and no need to add this ghost task.
- Checking for D.O.D. completeness must be done against the actual code, not the tasks being crossed off in that phase.
- Checking for D.O.D. completeness may lead to the addition of new tasks if items are incomplete.
- At the end of each phase, the project must be functional and runnable. If this is not achievable, highlight this clearly with a warning emoji (⚠️) in the phase description.

### Tasks

- Each task must have a clear background description.
- Tasks should be as **functionally** atomic as possible.
- List the files involved in each task.
- Subtasks should engage with a maximum of 2 files (3 in exceptional cases).
- At the end of each task the build must pass and all unit/component tests must be successful.
- The first subtask of each task should be to review the current code base and determine whether the task is still valid as is, or whether it needs to be adjusted (if adjustments are needed, stop and inform the user).
- For each actionable task (i.e., tasks that change code), start with a build, run, and test verification to establish a baseline. At the end of the task, perform the same verification to ensure no regressions were introduced.
- If a task is the last in a phase, ensure to include verification of the phase D.O.D. as a subtask.

### Dynamic Updates

- Document any new tasks identified during implementation.
- Lessons learned or actions taken during a given phase/task that impact other phases or tasks should be added as a note in the phase/task they impact.
- If, during implementation of a task, you discover something, learn something, or do something which might be relevant to other tasks/phases, document it in these other tasks/phases as well so it will be seen by whoever implements them next.

### Validation

- Ensure the build passes and all tests (unit and component) are successful after completing each task.
- Update relevant documentation to reflect changes.

### Checklist Management

- Cross out completed checklist items (subtasks and D.O.D. items).
- Add new tasks if the D.O.D. checklist is incomplete upon checking.

### General Principles

- Keep descriptions concise and to the point.
- Avoid unnecessary details that do not contribute to understanding the task.
- Always keep it simple, don't over engineer, and don't prepare for hypothetical future scenarios that aren't specified in the current requirements.
