---
In this prompt:

<operations_list> = {{operations_list}}
<design_logs_list> = {{design_logs_list}}
---

# Your mission

Sync lessons learned from <operations_list> back to <design_logs_list>.

## Process

1. **For each operation document:**
   - Read the operation document completely
   - Extract all "Lessons Learned" sections from tasks and phases
   - Extract the "Lessons Learned during Operation" section
   - Identify the related design logs from the References section

2. **Categorize lessons:**
   - **General lessons**: Apply to the overall approach or architecture
   - **Step-specific lessons**: Impact a specific step in the design log
   - **Future considerations**: New insights for future features

3. **For each related design log:**
   - Read the current design log content
   - Identify where each lesson should be added:
     - General lessons → Add to "Implementation Results" or new "Lessons Learned" section
     - Step-specific lessons → Add as notes under the relevant step in the Plan
     - Future considerations → Add to "Future Improvements" section or create one

4. **Update design logs:**
   - Add lessons concisely (minimal but clear)
   - Preserve existing content
   - Use clear attribution: "From [op_xxx]: lesson text"
   - Avoid duplicating lessons already present

## Output format

For each operation processed, report:

```txt
Operation: <operation_name>
Related Design Log: <design_log_name>
Lessons synced: <count>
- [General] <lesson_summary>
- [Step X] <lesson_summary>
...
```

## After syncing

1. Summarize total operations processed and lessons synced
2. Highlight any operations without a linked design log
3. Highlight any design logs that couldn't be updated (file not found, etc.)