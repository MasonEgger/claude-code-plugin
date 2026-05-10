---
description: Implement the next unchecked step from plan.md using strict TDD
---

# Execute Plan Command

1. Read @plan.md and @todo.md
   - These files complement each other. @todo.md should track the current state of the implementation of @plan.md
2. Check to see if a directory named `.ai-sessions/` exists
   1. If the directory doesn't exist, do nothing
   2. If the directory exists, identify the most recent session summary by sorting filenames lexicographically (the embedded `{YYYYMMDD}-{HHMM}` timestamp makes lexicographic order equal chronological order — do not rely on filesystem mtime). Read that summary in full. It contains detailed information about what work was completed and lessons learned in the previous session.
3. **Invoke relevant skills via the Skill tool**: For the project's tech stack (per CLAUDE.md and @plan.md), invoke each matching skill via the `Skill` tool BEFORE proceeding to step 4. Examples:
   - Python project → invoke `python:python` (or `python` if unscoped)
   - Temporal project → invoke `temporal:temporal-developer`
   - Available skills are listed in the available-skills system reminder.

   Bias toward invoking. If a skill plausibly matches the stack, invoke it — double-loading is harmless, skipping is not. Auto-loaded CLAUDE.md rules (e.g. python.md arriving as a system-reminder) are NOT the same as invoking the skill; the skill carries additional toolchain, workflow, and reference guidance that only loads on invocation.

   Before moving to step 4, make an explicit decision in user-facing text: either "Invoked: <skill names>" or "No matching skill for this stack." Only ask the user if you are genuinely unsure which skill applies.
4. Open @todo.md and select the first unchecked item to work on.
5. **CRITICAL**: Open @plan.md and locate the specific step being implemented
   - Find the detailed numbered prompts for this step (e.g., "1. RED: Write tests...", "2. GREEN: Implement...")
   - Follow these prompts EXACTLY in the specified order
   - Do NOT deviate from the file paths, test scenarios, or implementation approach specified
6. If you have any questions about the task at hand, ask the user.
7. Implement the plan for this item as specified in @plan.md:
   - **Follow the exact numbered sub-steps** in the plan.md prompt
   - **Use the specific file paths** mentioned in the prompts
   - **Implement the exact test scenarios** described
   - Follow strict TDD procedures (RED-GREEN-REFACTOR as specified)
   - Write robust, well-documented code
   - Focus tests on YOUR application logic, not framework functionality
   - Skip testing trivial code, framework features, or library behavior
   - Verify that all tests and linting passes
   - Make sure the tests pass, and the program builds/runs
8. **Update documentation as specified** in the @plan.md prompts for this step
9. **CRITICAL** Update @todo.md and mark off the item that was completed
10. Ask the user if there is anything else they want you to do or review for this session.

## Key Requirements:
- **NEVER** skip or reorder the numbered steps in plan.md
- **NEVER** skip step 3 (skill loading). Auto-loaded CLAUDE.md rules are not the same as an invoked skill — when in doubt, invoke.
- **ALWAYS** use the exact file paths specified in the prompts
- **FOLLOW** the RED-GREEN-REFACTOR cycle as outlined in each step
- **COMPLETE** all documentation updates mentioned in the step
- **VERIFY** all application logic is tested (not framework/library code)
- Treat @plan.md prompts as **implementation instructions**, not suggestions
