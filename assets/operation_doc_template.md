# How to Create a Tasks File

This document provides guidelines for creating a tasks file. The tasks file should outline the overall goal, provide background information, and be divided into phases, tasks, and subtasks. Each phase and task should include clear checklists to ensure completeness and quality.

## Key Guidelines

1. **Structure**:
   - Include the overall goal and background information.
   - Divide the document into phases, tasks, and subtasks.
   - Use the provided template below for consistency.

2. **Phases**:
   - Each phase must have a Definition of Done (D.O.D.) checklist.
   - The last task of any phase with more than 1 task must verify that the D.O.D. checklist is complete. If only one task exists in the phase, the D.O.D. check is done within that task.
   - Checking for D.O.D. completeness must be done against the actual code, not the tasks being crossed off in that phase.
   - Checking for D.O.D. completeness may lead to the addition of new tasks if items are incomplete.
   - At the end of each phase, the project should be functional and runnable. If this is not achievable, highlight this clearly.

3. **Tasks**:
   - List the files involved in each task.
   - Include a subtasks checklist for each task.
   - Subtasks should involve a maximum of two files (three in exceptional cases).

4. **Dynamic Updates**:
   - Document any new tasks identified during implementation.
   - Lessons learned or actions taken during a given phase/task that impact other phases or tasks should be added as a note in the phase/task they impact.
   - Record lessons learned that impact other phases or tasks.

5. **Validation**:
   - Ensure the build passes and all tests (unit and component) are successful after completing each task.
   - Update relevant documentation to reflect changes.

6. **Checklist Management**:
   - Cross out completed checklist items (subtasks and D.O.D. items).
   - Add new tasks if the D.O.D. checklist is incomplete upon checking.

7. **Misc**:
   - Keep descriptions concise and to the point.
   - Avoid unnecessary details that do not contribute to understanding the task.
   - Always keep it simple, don't over engineer, and don't preparare for hypothetical future scenarios that aren't specified in the current requirements.
   - Testing is generally done within subtasks, not as a task/phase on its own. Testing is part of the development process.
   - At the end of each task- the build must pass and all unit/component tests must be successful.
   - Optional: End each task by providing a ```txt snippet with a commit message for that task.
   - Note: The tasks list doesn't live in a vacuum. It's possible that, during implementation or  etween phases the code base would change. Therefore, the first subtask of each task should be to review the current code base and determine whether the task is still valid as is, or whether it needs to be adjusted (in which case- stop execution and inform the user).
   - If a task is the last in a phase, ensure to include verification of the phase D.O.D. as a subtask.
   - For each actionable task (i.e. tasks that change code), the task must start with a build, run and test verification to establish a baseline. At the end of the task, the same verification must be performed to ensure no regressions were introduced.
   - If, during implementation of a task, you discover something, learn something, or do something which might be relevant to other tasks/phases, document it in these other tasks/phases as well- so your comment will be seen by whoever implements them next.

## Template

```markdown
# <Document Title>

## Background

<Provide background information about the operation.>

### Lessons Learned during Operation

<Dynamic Section: Record lessons learned during the operation that impact the overall operation. Leave empty if none.>

## Phases

**Phases overview**: <Briefly describe each phase and its purpose. Add a directed acyclic graph (DAG) inside a mermaid chart snippet if necessary to illustrate dependencies between phases (each phase as a subgraph) and tasks (each task as a node in the subgraphs)>

### Phase 1: <Phase Title>

<Background information about Phase 1: Describe the issue, current state, and desired outcome.>

**Definition of Done (D.O.D.):**

- [ ] <D.O.D. Item 1>
- [ ] <D.O.D. Item 2>
- [ ] ...

#### P1/Task 1: <Task Title>

<Background information about Task 1.>

**Files Involved:**

- `<File Path 1>`
- `<File Path 2>`
- ...

**P1/Task 1 Subtasks:**

- [ ] <Subtask 1>
- [ ] <Subtask 2>

**P1/Task 1 Lessons Learned:**
<Briefly write here what you learned or important considerations. Be concise!>

### Phase 2: <Phase Title>

<Repeat structure for additional phases.>
```

## Notes

- Ensure the document is clear and concise.
- Use formatting (e.g., bold, headings) to improve readability.
- Highlight critical information (e.g., incomplete tasks, non-functional phases) using emojis, colors, or fonts.
