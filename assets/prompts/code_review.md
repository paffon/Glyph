Perform a code review of operation: {operation_name}. You may use Glyph's static code analysis tool to get some data about given files.

Additional References: {design_log_name}

**Review Checklist:**

1. **Functionality**
   - Do all implemented features match the requirements?
   - Are there any deviations from the design? Are they justified and documented?
   - Are edge cases handled?

2. **Code Quality**
   - Is the code clean, readable, and well-structured?
   - Does it follow project conventions and patterns?
   - Is there appropriate error handling?
   - Are SOLID, DRY, and KISS principles followed?
   - You may use Glyph's static code analysis tool to get some data about code quality.

3. **Test Coverage**
   - Are there sufficient unit tests?
   - Are integration tests present for key flows?
   - Are edge cases and error scenarios tested?

4. **Documentation**
   - Are inline comments present for complex logic?
   - Is external documentation updated?
   - Are lessons learned documented in the operation?

5. **Performance & Security**
   - Are there any performance concerns?
   - Are there security vulnerabilities?
   - Is input validation present?

**Output:**

Generate a code review report following the example template. Include:

- Summary table with pass/fail/warning status
- Detailed findings for each review category
- Specific code issues with locations and suggestions
- Recommendations categorized by priority (Must Fix, Should Fix, Nice to Have)
- Lessons learned that should propagate back to the design log- and haven't been documented yet

**After review:**

1. Create action items for any issues found
2. If lessons learned are significant, suggest updating the design log
