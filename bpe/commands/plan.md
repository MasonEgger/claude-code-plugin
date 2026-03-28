---
description: Transform spec.md into a TDD implementation roadmap (plan.md + todo.md)
---

# Plan Command

Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

## Testing Guidelines for Generated Prompts

When specifying tests in RED phases, focus ONLY on application logic:

**DO test:**
- Business logic you're implementing
- Data validation rules you define
- Error handling you add
- Custom algorithms or calculations
- Integration between YOUR components

**DO NOT test:**
- Framework functionality (e.g., "Django can connect to database")
- Third-party library behavior (e.g., "requests library makes HTTP calls")
- Language features (e.g., "Python dicts work correctly")
- Configuration loading (unless complex custom logic)
- Trivial code (simple getters, setters, pass-through methods)

**Examples:**
- ❌ BAD: "Test that Django User model can be created" (tests Django)
- ✅ GOOD: "Test that custom password validator rejects weak passwords" (tests YOUR logic)
- ❌ BAD: "Test that database connection works" (tests framework)
- ✅ GOOD: "Test that user registration creates audit log entry" (tests YOUR logic)

## Critical Requirements for Execute-Plan Compatibility

**Each prompt must be structured as numbered sub-steps that execute-plan can follow sequentially:**

### Format for Each Step Prompt:
```
### Step X: [Descriptive Title]

**NOTE**: [Any important context about existing implementation]

```text
[Prompt for code-generation LLM with numbered instructions]:

1. RED: Write [specific type] tests first:
   - Create/modify [exact file path]:
     - Test [specific scenario 1]
     - Test [specific scenario 2]
     - Test [specific edge case]

   Example RED phase (GOOD):
   1. RED: Write validation tests first:
      - Create tests/test_user_validation.py:
        - Test that custom password validator rejects passwords without special chars
        - Test that email validator rejects disposable email domains
        - Test that username validator blocks profanity

   Example RED phase (BAD - Don't do this):
   1. RED: Write model tests first:
      - Create tests/test_models.py:
        - Test that User model can be created  ← Testing Django, not your code
        - Test that database saves User correctly  ← Testing Django ORM
        - Test that email field stores email  ← Testing Django field behavior

2. Document [specific component]:
   - Create/update [exact file path]
   - Document [specific behavior/rules]
   - Include [specific examples/configurations]

3. GREEN: Write MINIMAL code to make tests pass:
   - Create [exact file path]
   - Implement [specific functionality]
   - Use [specific patterns/libraries]
   - Just enough to pass tests

4. RED: Add integration tests:
   - Test [specific integration scenario]
   - Test [specific error conditions]

5. GREEN: Wire up integration minimally

6. REFACTOR: Improve [specific aspects]

7. Update documentation with [specific updates]

8. Verify meaningful test coverage of YOUR application logic and run `just check`
```

## Prompt Generation Requirements

1. **Executable Instructions**: Each numbered sub-step must be a specific instruction that execute-plan can follow exactly, not general guidance

2. **File Path Specificity**: Every prompt must specify exact file paths (e.g., "tests/test_activities/test_validation.py", not "test files")

3. **Test Scenario Detail**: Each RED phase must list specific test scenarios to implement, not generic "write tests"

4. **TDD Structure**: Every prompt must follow RED-GREEN-REFACTOR with clear phases

5. **Sequential Dependencies**: Each prompt builds on previous prompts with no orphaned code

6. **Integration Requirements**: Each prompt ends with wiring the new code into existing systems

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts that execute-plan can follow step-by-step, but context and architectural decisions are important as well.

## Output Format

Store the plan in @plan.md with:
- Current Status section showing implementation progress
- Each step as a detailed prompt with numbered sub-instructions
- Implementation Guidelines section
- Success Metrics section

Also create a @todo.md that:
- Mirrors the plan.md structure with checkboxes
- Tracks completion of each numbered sub-step
- Can be updated by execute-plan as work progresses

The spec is in the file called @spec.md
