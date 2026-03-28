# Using the Wordcount Tool

The `wordcount` tool helps you track tutorial length and meet word count requirements.

## Overview

The wordcount tool is a Python script that counts words in Markdown files while intelligently excluding code blocks. This gives accurate prose word counts for tutorials.

## Location

The wordcount script is available in two locations:

1. **In the skill:** `scripts/wordcount` (bundled with this skill)
2. **System-wide:** `~/.homedir/wordcount` (if installed via homedir setup)

## Basic Usage

### Count words in a single file

```bash
wordcount tutorial.md
```

Output: Just the number (e.g., `2847`)

### Count words in a directory

```bash
wordcount /path/to/tutorial/sections/
```

Output:
```
SECTION_1.md: 523 words
SECTION_2.md: 891 words
SECTION_3.md: 672 words
----------------------------------------
Total word count: 2086 words
```

### Count words recursively

```bash
wordcount . -r
```

This processes all Markdown files in the current directory and subdirectories.

## Advanced Options

### Output Formats

**JSON format:**
```bash
wordcount tutorial.md -f json
```

Output:
```json
{
  "files": [
    {"path": "tutorial.md", "words": 2847}
  ],
  "total": 2847,
  "extensions": [".md", ".markdown"]
}
```

**CSV format:**
```bash
wordcount tutorial.md -f csv
```

Output:
```csv
Path,Words
tutorial.md,2847
```

### Save Output to File

```bash
wordcount tutorial/ -o word_counts.txt
wordcount tutorial/ -f json -o counts.json
```

### Include Code Blocks

By default, wordcount excludes code blocks. To count them:

```bash
wordcount tutorial.md --no-exclude-code-blocks
```

### Custom File Extensions

By default, wordcount processes `.md` and `.markdown` files. To specify different extensions:

```bash
wordcount . -e .txt .text
```

## Using in Tutorial Writing Workflow

### Check Individual Section Length

After writing a section:

```bash
wordcount output/SECTION_3.md
```

This helps ensure sections aren't too long or too short.

### Check Total Tutorial Length

After combining sections:

```bash
wordcount output/first_draft.md
```

### Monitor Progress

Track word counts across all sections:

```bash
wordcount output/ -f json -o progress.json
```

### Quality Checks

For tutorials with target word counts:

```bash
# Check if tutorial meets minimum length
WORDS=$(wordcount output/first_draft.md)
if [ $WORDS -lt 2000 ]; then
  echo "Tutorial needs more content: $WORDS words (minimum 2000)"
fi
```

## Command Reference

```bash
wordcount <path> [options]

Arguments:
  path                  File or directory to process

Options:
  -r, --recursive       Process directories recursively
  -f, --format         Output format: text, json, csv (default: text)
  -o, --output FILE    Save output to file instead of stdout
  -e, --extensions     File extensions to process (default: .md .markdown)
  --no-exclude-code-blocks  Include code blocks in word count
```

## How It Works

1. **File Detection:** Identifies Markdown files by extension
2. **Code Block Removal:** Uses regex to remove content between ``` markers (unless disabled)
3. **Word Counting:** Splits remaining text by whitespace and counts
4. **Reporting:** Displays counts in specified format

## Excluding Code Blocks

The tool automatically excludes fenced code blocks from word counts:

````markdown
This sentence will be counted.

```python
# This code will NOT be counted
def hello():
    print("Not counted")
```

This sentence will be counted.
````

Result: Only the prose sentences are counted, not the code.

## Tips for Tutorial Writers

1. **Check frequently:** Run wordcount after each section to stay on track
2. **Use JSON for scripting:** JSON output is easier to parse in automation
3. **Track section balance:** Use directory mode to see if sections are balanced
4. **Exclude code intentionally:** Default behavior gives true prose length
5. **Use with git:** Track word count changes over revisions

## Troubleshooting

### "Binary file" Error

The tool encountered a non-text file. Check the file encoding or skip the file.

### Unexpected Word Counts

If counts seem wrong:
* Check if code blocks are being included (use `--no-exclude-code-blocks` to test)
* Verify file extensions match (`.md` and `.markdown` by default)
* Look for hidden characters or formatting issues

### Tool Not Found

If the command isn't found:
1. Check if `~/.homedir/` is in your PATH
2. Use the full path: `~/.homedir/wordcount`
3. Or use the skill's bundled version: `.claude/skills/tutorial-writing/scripts/wordcount`

## Examples

**Single file word count:**
```bash
$ wordcount tutorial.md
3421
```

**Directory word count:**
```bash
$ wordcount sections/
sections/intro.md: 245 words
sections/step1.md: 567 words
sections/step2.md: 891 words
sections/conclusion.md: 178 words
----------------------------------------
Total word count: 1881 words
```

**Recursive with JSON output:**
```bash
$ wordcount . -r -f json
{
  "files": [
    {"path": "README.md", "words": 423},
    {"path": "docs/guide.md", "words": 2341},
    {"path": "docs/api.md", "words": 1567}
  ],
  "total": 4331,
  "extensions": [".md", ".markdown"]
}
```
