# Design Log Methodology Rules

The project follows a rigorous design log methodology for all significant features and architectural changes.

## Before Making Changes

1. **Check design logs** in `.assistant/design_logs/_summary.md` for existing designs and implementation notes, then read the relevant logs
2. **For new features**: Create design log first, get approval, then implement
3. **Read related design logs** to understand context and constraints

## When Creating Design Logs

1. **Structure**: Background → Problem → Questions and Answers → Design → Implementation Plan → Examples → Trade-offs
2. **Be specific**: Include file paths, type signatures, validation rules
3. **Show examples**: Use ✅/❌ for good/bad patterns, include realistic code
4. **Explain why**: Don't just describe what, explain rationale and trade-offs
5. **Ask Questions (in the file)**: For anything that is not clear, or missing information
6. **When answering question**: keep the questions, just add answers
7. **Be brief**: write short explanations and only what most relevant
8. **Draw Diagrams**: Use mermaid inline diagrams when it makes sense
9. **Define verification criteria**: how do we know the implementation solves the original problem

## When Implementing

1. **Follow the implementation plan** phases from the design log
2. **Write tests first** or update existing tests to match new behavior
3. **Do not Update design log** initial section once implementation started
4. **Append design log** with "Implementation Results" section as you go
5. **Document deviations**: Explain why implementation differs from design
6. **Run tests**: Include test results (X/Y passing) in implementation notes
7. **After Implementation** add a summary of deviations from original design

## When Answering Questions

1. **Reference design logs** by number when relevant (e.g., "See Design Log #50")
2. **Use codebase terminology**: Adapt to your project's conventions
3. **Show type signatures**: Include relevant type definitions for your language
4. **Consider backward compatibility**: Default to non-breaking changes

## References

Writing references in a design log is encouraged, using standard markdown file references:

- Referencing another design log: `[dl_123](.assistant/design_logs/dl_123_title.md)` - use the full filename
- Referencing an artifact: `[art_123](.assistant/artifacts/art_123_name.ext)` - use the full filename with extension
- Referencing an operation: `[op_123](.assistant/operations/op_123_title.md)` - use the full filename

You can also use descriptive link text: `[See design log about feature X](.assistant/design_logs/dl_123_feature_x.md)`