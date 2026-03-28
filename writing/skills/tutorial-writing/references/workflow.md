# Tutorial Writing Workflow

Follow this step-by-step process when writing technical tutorials.

## Process Overview

1. Analyze the rules and constraints
2. Analyze the code to understand what it does
3. Read writing samples to build author's voice
4. Create and iterate on outline
5. Write sections one at a time
6. Combine sections into first draft

## Step 1: Analyze Rules and Constraints

Before starting, thoroughly understand the constraints you must operate within:

* Read [style-guide.md](style-guide.md) for comprehensive writing standards
* Read [temporal-rules.md](temporal-rules.md) if writing about Temporal
* Review [code-sandwich.md](code-sandwich.md) for code explanation approach
* Operating within these constraints is MORE important than accuracy at this step

## Step 2: Analyze the Code

Understand the application you're writing about:

* Read all code files in the provided directory
* Understand the architecture and how components interact
* Identify key concepts readers will need to learn
* If you have qualifying questions, ask before proceeding

**CRITICAL:** You must ONLY use code provided to you. NEVER generate new code. If code is missing or unclear, flag with `<CLAUDE_HELP></CLAUDE_HELP>` tags.

## Step 3: Read Writing Style Guide

Build understanding of Mason Egger's specific voice:

* Read [mmegger-writing-style.md](mmegger-writing-style.md) for voice patterns
* Note unique transition phrases ("Now that...", "Once you've done...")
* Observe strategic pronoun mixing (we vs you)
* Match sentence rhythm patterns (short → medium → short)
* Use author-specific vocabulary preferences
* Apply error handling voice (treat expected errors as normal)

## Step 4: Create and Iterate on Outline

Generate a tutorial outline through iteration:

1. **Initial outline:** Think of the best sequence to present information to a new learner
2. **Think carefully and deeply:** Consider the learner's perspective - what order makes most sense?
3. **Internal review:** Imagine a new learner inspecting the outline
4. **Ask pointed questions:**
   * "Is there anything missing?"
   * "Is this in an order that makes sense to present?"
   * "Would a beginner understand this flow?"
5. **Iterate:** Continue refining until satisfied
6. **Document reasoning:** Be able to defend every choice
7. **Write outline:** Create `output/outline.md` with your reasoning
8. **Get approval:** Ask the prompter for feedback before proceeding

### Outline Structure

Your outline should include:
* Tutorial title
* Introduction topics to cover
* Prerequisites needed
* Each step with brief description of what it accomplishes
* Conclusion topics to cover
* Reasoning for the sequence chosen

## Step 5: Write Sections One at a Time

Once outline is approved, write each section:

1. **Follow the outline exactly** - Do not deviate
2. **Think carefully and deeply** about every section
3. **Only use provided code** - Never create new code
4. **Apply code sandwich approach** - See [code-sandwich.md](code-sandwich.md)
5. **Follow style guide** - Review against [style-guide.md](style-guide.md)
6. **Flag uncertainties** - Use `<CLAUDE_HELP></CLAUDE_HELP>` tags when unsure
7. **Write to file** - Save as `output/SECTION_<NUMBER>.md`
8. **Get approval** - Ask reviewer to approve before moving to next section

### Section Writing Checklist

Before considering a section complete:

- [ ] Follows outline structure
- [ ] Uses only provided code (no new code generated)
- [ ] Applies code sandwich approach for all code blocks
- [ ] Follows style guide formatting
- [ ] Uses appropriate tone (friendly but formal)
- [ ] Explains WHY not just WHAT
- [ ] Includes transitions to next section (use "Now that..." pattern)
- [ ] Has been reviewed for AI-giveaway phrases
- [ ] Reading level appropriate (6th-9th grade)
- [ ] Temporal primitives capitalized (if applicable)
- [ ] Mason Egger voice patterns applied (transitions, pronouns, rhythm)

## Step 6: Combine into First Draft

After all sections are approved:

1. **Use bash tools to combine:** Do NOT manually copy/paste
   ```bash
   cat output/SECTION_1.md >> output/first_draft.md
   cat output/SECTION_2.md >> output/first_draft.md
   # ... continue for all sections
   ```
2. **Do not change approved text** - Sections were already approved
3. **Verify formatting** - Ensure sections flow together properly
4. **Save as Markdown** - Final output: `output/first_draft.md`

## Code Sandwich Approach

See [code-sandwich.md](code-sandwich.md) for detailed explanation of how to present code to learners.

## Using the Word Count Tool

See [wordcount-usage.md](wordcount-usage.md) for instructions on tracking tutorial word counts.

## Important Constraints

### Never Generate New Code

* **ONLY** use code provided in the tutorial context
* **NEVER** create, modify, or suggest improvements to code
* If code is missing, flag with `<CLAUDE_HELP></CLAUDE_HELP>` tags
* If asked for improvements, explain this is outside your scope
* The provided code has already been tested for accuracy

### Flag Uncertainties

Use `<CLAUDE_HELP></CLAUDE_HELP>` tags when:
* You need a screenshot of running application
* Code you need is missing
* You're unsure how something works
* You cannot complete a section as designed

Describe what you were trying to do within the tags so your team can help.

### Quality Over Speed

* Think carefully and deeply about each section
* Verify against style guide before submitting
* Get approval before moving forward
* It's better to ask questions than make assumptions
