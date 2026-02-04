Implement Phase {phase_number} / Task {task_number} from "file_name_or_hyperlink".

**Context/background:**

- Read the Background section of the document.
- Read previous tasks/phases bottom lines / lessons learned, if any.
- provide_specific_context_or_background_here

**Before starting:**

1. Check if something you're about to implement already exists and can be re-used or slightly adapted. If so, this might even mean you need to adapt the Phase/Task Operation document. Let me know and hold on with the rest of the implementation.
2. Remember SOLID, DRY and KISS. Do not overengineer. If task is complex, tell me how you're going to adhere to these principles. If the task is simple, no need.
3. If you find any ambiguities, inconsistencies, or missing information in the task description, ask me for clarification before proceeding.

**How to implement:**

1. Read the task description carefully, determine which other documents that I haven't mentioned might also be relevant, and read them. You may use Glyph tools to help you find relevant documents if needed.
2. Build and run all tests to establish a benchmark (if applicable).
3. Ask the user if they have any reservations, questions, or clarifications they'd like addressed before proceeding.

**When done:**

1. Build/Run tests and compare to benchmark (if applicable).
2. Checkmark [x] the task in the task list in the document if applicable.
3. If this is the last task of the phase, also verify that the phase's D.O.D. checklist is done and mark [x] on done items.
4. Add lessons learned / bottom line for this task/phase in the document. Make it concise and to the point. Do not mention obvious things (e.g. no need to mention success as it's considered the norm).
5. Consider future phases/tasks in the same document. If during implementation you discovered/did something that influences other tasks/phases- add this as a comment to the relevant task/phase in the document such that it awaits the future implementer/planner when they work on it.
6. In this chat, generate a **one liner** ```txt snippet with a commit message for me to use, based on what's actually done. The message should start like this:

```txt
[operation name] P{phase_number}/T{task_number} - <short task title>: Short description of the change
```

**Note:**

1. This is a breathing project, and it may have changed since the tasks were created. Always check for the latest context and updates. If the codebase changed so much that the task is no longer relevant, inform me before proceeding.
2. Marking tasks/D.O.D. items as done [x] must not just based on the tasks list. Always verify by checking the actual project state.
3. Do not forget about the commit message. It should be based on what you actually did, not just the task description. If you deviated from the original plan, the commit message should reflect what you actually did, not what you planned to do.