# Glyph overview

Glyph is an MCP that helps developers manage long-term tasks and projects with AI assistance while maintaining full control. It provides structured documentation through design logs (research/decisions), operations (task checklists), and artifacts (persisted outputs), all linked together in a traceable reference graph.

## Primitives

- **Design Log**: Markdown file documenting research, decisions, and implementation details. Immutable once created. Stored in `.assistant/design_logs/` as `dl_{number}_{title}.md`
- **Operation**: Checklist for achieving complex goals, broken into phases and tasks. Stored in `.assistant/operations/` as `op_{number}_{title}.md`
- **Artifact**: Important files persisted from `ad_hoc/` directory. Stored in `.assistant/artifacts/` as `art_{number}_{filename}.ext`
- **Ad-hoc Directory**: Temporary workspace (`.assistant/ad_hoc/`) for experiments and intermediate work. Reset between operations.
- **Reference Graph**: CSV file tracking all references between design logs, operations, and artifacts

## Reference Syntax

Link files using standard markdown syntax:

```markdown
[dl_1](.assistant/design_logs/dl_1_title.md)
[op_2](.assistant/operations/op_2_title.md)
[art_3](.assistant/artifacts/art_3_name.ext)
```

Or use descriptive text: `[See research on X](.assistant/design_logs/dl_1_title.md)`

## Core Structural Principle

**Design logs should be linked to operations or artifacts.** This is a best practice for maintaining a well-organized Glyph workspace. When possible, every design log should reference or be referenced by at least one operation or artifact. This helps create:

- A coherent knowledge graph with minimal orphaned documents
- Clear traceability from work (operations) to decisions and research (design logs)
- Better categorization and context for your documentation
- More meaningful reference graphs that reflect your project structure

However, this is not a strict requirement. If you create a design log without an immediate connection, consider proposing to link it to an operation or artifact later, but it's optional.

## Tools & Skills Quick Reference

| Action | Tool |
| - | - |
| Initialize Glyph | `init_assistant_dir` |
| Create operation doc | `add_operation` |
| Create design log | `add_design_log` |
| Save important files | `persist_artifacts` |
| Find what a file references | `get_references_from` |
| Find what references a file | `find_references_to` |
| Rebuild reference graph | `update_reference_graph` |
| Parse markdown to dict | `md_to_dict` |
| Get operation rules | `get_operation_rules` |
| Get design log rules | `get_dl_rules` |
| Get design log examples | `get_dl_example` |
| Get task guidelines | `get_task_implementation_guidelines` |

## Working with the Ad Hoc Directory

The `.assistant/ad_hoc` directory is a workspace for temporary files created during operations.

### Purpose

- Store intermediate work products
- Hold files that may or may not have lasting value
- Provide a scratch space during active work

### Best Practices

1. **Use ad hoc for temporary work:** Any file that might be discarded or is only relevant to the current task should go in `ad_hoc`.

2. **Persist valuable files:** If an ad hoc file has significance beyond the immediate task:
   - Use the `persist_artifacts` tool to move it to the `artifacts` directory
   - This ensures proper naming (`art_{number}_{name}`) and permanent storage
   - Persisted artifacts can be referenced by design logs and operations
   - **Link any related design logs to the persisted artifact** to maintain structural integrity

3. **Clean up regularly:** Files left in `ad_hoc` may be cleaned up between sessions. Don't rely on them for long-term storage.

4. **When to persist:**
   - The file documents important findings
   - The file will be referenced by future work
   - The file contains reusable templates, scripts, or configurations
   - The file represents a deliverable or milestone

5. **When NOT to persist:**
   - Temporary debugging outputs
   - Draft files that have been superseded
   - Test files that served their purpose
   - Files specific to a single session's experimentation

## Typical Workflow

1. **Init** → `init_assistant_dir` sets up the `.assistant` structure
2. **Work** → `add_operation` documents what you're doing
3. **Research** → `add_design_log` captures decisions/findings (link to your operation)
4. **Produce** → Create files in `ad_hoc`, then `persist_artifacts` for keepers
5. **Connect** → Reference design logs from operations, operations from artifacts
6. **Verify** → `update_reference_graph` to visualize relationships
7. **Query** → Use `get_references_from` / `find_references_to` to navigate structure

**Key insight:** Design logs should reference or be referenced by operations/artifacts. Use the reference tools to verify your knowledge graph is coherent.

## Before Starting Work

- **Task planning?** → `get_task_implementation_guidelines`
- **Creating an operation?** → `get_operation_rules`
- **Creating a design log?** → `get_dl_rules`
- **Need examples?** → `get_dl_example`

## Communication Guidelines

If something is unclear or ambiguous, the assistant should ask for clarification.
