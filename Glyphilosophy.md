# Glyphilosophy

Glyph is an MCP aimed to help developers manage long-term tasks and projects while leveraging the power of AI and yet allowing them to maintain full control over their work.

## Primitives

### References

To keep the system dynamic, a reference mechanism is used to link various components of the project. References allow design logs, operations, and artifacts to interlink, providing context and traceability throughout the development process.

A design log, operation or artifact may refer to any number of other design logs, operations and artifacts.

Reference syntax:

- Referencing a design log: `[dl_1](.assistant/design_logs/dl_1_title.md)` - use standard markdown file references
- Referencing an operation: `[op_2](.assistant/operations/op_2_title.md)` - use standard markdown file references
- Referencing an artifact: `[art_3](.assistant/artifacts/art_3_name.ext)` - use standard markdown file references with extension

You can use descriptive link text: `[See operation about X](.assistant/operations/op_2_title.md)`

### Design Log

A design log is a markdown file which contains an overview of step in the development process. It consists of background of a project state, problem description, Q&As, approaches, overview of tasks, decisions made, and lessons learned.

A design log may not be changed retroactively. Once a new design log is created, the previous one is never to be modified again. This ensures that the development process is fully traceable and auditable.

Design logs are stored in the `.assistant/design_logs/` directory with filenames following the pattern `design_log_{serial_number}_{some descriptive title}.md`, where `{serial_number}` is an incrementing integer.

### Operation

A checklist for achieving a complex goal.

**Operation**:

- Has a background section, overarching the entire operation.
- Has a mermaid chart showing phases & tasks dependencies.
- Has a Phases section with up to 4 phases.

**Phase**:

- Has a background section, describing the issue, state before the phase, and desired outcome.
- Has a small checklist for D.O.D. (Definition of Done) items.
- Has up to 4 tasks.

**Task**:

- Has a background section, describing the issue, state before the task, and desired outcome.
- Has a list of files involved (to be modified, created, or deleted).
- Has a checklist of up to 5 subtasks.
- Has a lessons learned section.
- Ideally, before and after a task, the project should be in a working state. If not possible, should be stated explicitly in the task background with a warning (⚠️) emoji.

**Subtask**:

- Each subtask is a checklist item in a list, e.g. "- [ ] this is a subtask."
- Describes a small, manageable piece of work contributing to the completion of the task.
- Complexity level of a subtask should be such that a junior developer can complete it in a reasonable timeframe.
- Each subtask may engage (modify, create or delete) with 2 files at maximum, 3 if absolutely necessary. Reading more files is allowed for context, but not modifying them.

### Ad-hoc directory

- A directory in which anything goes. It may contain temporary files, experiments, or any other content that does not fit into the structured parts of the project.
- Being reset every time a new operation begins.
- To persist important content from the ad-hoc directory, a special `persist_artifact` tool exists, which copies files from the ad-hoc directory to the `.assistant/artifacts/` directory and renames them to template `art_{serial_number}_{original_file_name}.{original_extension}`.

### Artifacts

Artifacts are files persisted from the ad-hoc directory using the `persist_artifact` tool. They are stored in the `.assistant/artifacts/` directory with a specific naming convention to ensure traceability.

### Reference graph

`.csv` file named `reference_graph.csv` stored directly in `.assistant/` directory. It represents a reference graph which is a directed graph where nodes are files and edges represent references or dependencies between those files. Has two columns: `start_point` and `end_point`, indicating a directed edge from one file to another.

Since the references syntax is uniform across design logs, operations, and artifacts, the reference graph can be created/maintained by parsing all these files and extracting the references.
