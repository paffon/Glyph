In this prompt:

<step_to_create_doc_for> = {{step_to_create_doc_for}}
<design_log_name> = {{design_log_name}}

# Your mission

Plan the creation of a new operation document for step <step_to_create_doc_for> from <design_log_name>.

## Instructions

- First read the glyph rules; then:
- Read the operation document guidelines; and finally:
- write the creation plan for the operation document.

The operation document's Background section must be comprehensive, exhaustive and detailed- Taking all of the relevant information from the design log you can find (anywhere in the design log, not just the step itself). The Background section is encouraged to include mermaid charts where appropriate (glyph's mermaid tool can advise on this).

## Before you create the doc

1. Prove you read through the design log doc and understood what relevant information is there for the operation doc.
2. Prove you read through the operation document guidelines and understood them, showing me how you will apply them.
3. You'll keep it SOLID, DRY and Simple.
4. Tell me how many phases and tasks in each phase you plan to have in the operation doc.
5. For each phase, include a **Phase Difficulty** label and for each task include a **Task Difficulty** label. Choose from: `Breezy`, `Low`, `Medium`, `High`, `Nightmare`.

- For every chosen difficulty level provide a one-line justification explaining why that level was selected.
- Describe how testing and validation will scale with the difficulty (e.g., baseline build/tests for Breezy/Low, unit+integration for Medium, broader integration/manual testing for High/Nightmare).

The operation document must reflect these difficulty assignments in its phases and tasks so implementers know expected scope and verification effort.

6. In your phases overview, include both:
   - A markdown table with columns: **Phase**, **# Tasks**, **Difficulties**, **Description**. The **Difficulties** column must list each task's individual difficulty as a comma-separated list (e.g., `High, Medium, Low`).
   - A DAG (Mermaid flowchart) showing phase and task dependencies with task nodes labeled `P{n}/T{m}` (e.g., `P1/T1`, `P2/T1`).