# Things to keep in mind during task planning and implementation

When planning and implementing tasks, please adhere to the following guidelines to ensure consistency, quality, and maintainability:

## Pre-Implementation

- **Important**: The operation doc doesn't live in a vacuum. It's possible that during implementation or between phases the code base would change. Therefore, the first subtask of each task should be to review the current code base and determine whether the task is still valid as is, or whether it needs to be adjusted (in which case - stop execution and inform the user).
- Any code-changing task (i.e., not research or documentation tasks) must start with a build, run, and test verification to establish a baseline.

## Implementation Principles

- **KISS (Keep It Simple, Stupid)**: When planning and implementing, avoid unnecessary complexity. Each phase and task should be as straightforward as possible.
- **SOLID principles**: Keep each task adhering to the principles of good software design (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
- **Testing**: Testing is generally done within subtasks, not as a task/phase on its own. If a task doesn't include testing, you should notify the user that testing should be added as a subtask.

## Post-Implementation

- At the end of each code-changing task, the build must pass and all unit/component tests must be successful. Perform the same verification as at the start to ensure no regressions were introduced.
- If a task is the last in a phase, ensure to include verification of the phase D.O.D. as a subtask.
- Once a task is done, provide the user in the chat with a concise commit message summarizing the changes made in that task, formatted as a ```txt snippet, like so:

```txt
[operation name]Px/Ty - <short task title>: <details>.
```

Where `x` and `y` are the phase and task numbers respectively.

## Documentation Guidelines

- Keep the operation document clear and concise.
- When documenting lessons learned, include only relevant information that could impact future tasks or phases. Avoid unnecessary details, trivial learnings, lengthy narratives, and reporting of successful implementations which are assumed to be the norm.
- If during implementation you discover something that might be relevant to other tasks/phases, update those sections with a comment so the next implementer will see the new information.

## Dynamic Updates

During implementation, new information may arise that necessitates updates to the operation document:

- New tasks may be added dynamically. New phases may NOT be added.
- Lessons learned or actions taken during a phase, task, or subtask may impact future steps. In such cases, update the relevant sections with a comment so the next implementer will be informed.
