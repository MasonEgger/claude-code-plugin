# Tutorial Writing Style Guide

This style guide is based on a modified DigitalOcean style for technical tutorials.

## Core Principles

Tutorials should be:

* **Comprehensive and written for all experience levels**
* **Technically detailed and correct**
* **Practical, useful, and self-contained**
* **Friendly but formal**
* **Indiscernible from human writing**
* **Assume the natural language being written is the readers second language**

## Comprehensive and Written for All Experience Levels

Write tutorials to be as clear and detailed as possible without making assumptions about the reader's background knowledge.

* Include every command a reader needs to go from their first setup to the final, working configuration
* Provide all explanations and background information needed to understand the tutorial
* Goal: readers should learn concepts, not just copy and paste code

**Avoid assumptive words:** "simple," "straightforward," "easy," "simply," "obviously," and "just"
* These words make assumptions about reader knowledge and can frustrate readers
* Instead, provide the explanations readers need to be successful

## Technically Detailed and Correct

* Follow industry best-practices
* Provide more details than just code and commands
* Don't provide large blocks of code asking readers to paste without explanation
* Every command should have a detailed explanation, including options and flags
* Every block of code should be followed by prose explanations of what it does and why
* First explain what a command/change does, then ask the reader to execute it
* These details give readers the information they need to grow their skills

## Practical, Useful, and Self-Contained

* By the end, readers will have installed, built, or set up something from start to finish
* Emphasize practical approach: reader should have a usable environment or example to build upon
* Cover topics thoroughly
* Link to existing tutorials as prerequisites
* Link to first-party source tutorials for additional information in the body
* Only send readers offsite if no first-party article exists and information can't be summarized

## Friendly but Formal

* Aim for friendly but formal tone
* No jargon, memes, excessive slang, emoji, or jokes
* Write for a global audience across language and cultural boundaries
* Do NOT use first person singular (e.g., "I think...")
* Use second person (e.g., "You will configure...") to keep focus on the reader
* Use motivational language focused on outcomes
  * Example: "In this tutorial, you will install Apache" (not "You will learn how to install Apache")
* Honor diverse human experiences
* Avoid offensive language or content referencing age, disability, ethnicity, gender, experience level, nationality, neurodiversity, appearance, race, religion, politics, sexual orientation, socioeconomic status, or technology choices

## Indiscernible from Human Writing

AI-generated content has negative connotations, so avoid sounding like AI:

* **Use simple language:** Write plainly with short sentences
  * Example: "Start the Worker."

* **Avoid AI-giveaway phrases:** No clichés like "dive into," "unleash your potential," etc.
  * Avoid: "Let's dive into this game-changing solution."
  * Use instead: "Here's how it works."

* **Be direct and concise:** Get to the point; remove unnecessary words
  * Example: "Install the `temporal` CLI in your environment."

* **Maintain a natural tone:** Write as you normally speak
  * Example: "This is not the best way of doing this."

* **Avoid marketing language:** No hype or promotional words
  * Avoid: "This revolutionary product will transform your life."
  * Use instead: "This product can help you."

* **Keep it real:** Be honest; don't force friendliness
  * Example: "That approach has trade-offs worth considering."

* **Stay away from fluff:** Avoid unnecessary adjectives and adverbs
  * Example: "You finished the task."

* **Focus on clarity:** Make your message easy to understand
  * Example: "Please send the file by Monday."

## Assume Natural Language is Reader's Second Language

* Prevent overuse of complex words, phrases, or idioms
* Aim for 6th-9th grade reading level
* Aim for Flesch Reading Ease Score of 70 or above
* Avoid idioms or cultural phrases not immediately understandable to non-native speakers
* No SAT words allowed

---

## Tutorial Structure

### Procedural Tutorials

Most tutorials are procedural (step-by-step):

* Title (Level 1 heading)
* Introduction (Level 3 heading)
* Prerequisites (Level 2 heading)
* Step 1 — Doing the first thing (Level 2 heading)
* Step 2 — Doing the next thing (Level 2 heading)
* ...
* Step n — Doing the last thing (Level 2 heading)
* Conclusion (Level 2 heading)

### Conceptual Tutorials

For concept-focused tutorials:

* Title (Level 1 heading)
* Introduction (Level 3 heading)
* Prerequisites (optional) (Level 2 heading)
* Subtopic 1 (Level 2 heading)
* Subtopic 2 (Level 2 heading)
* ...
* Subtopic n (Level 2 heading)
* Conclusion (Level 2 heading)

### Simple Tutorials

For focused, simple tasks:

* Title (Level 1 heading)
* Introduction paragraph
* Prerequisites (optional) (Level 2 heading)
* Article body
* Conclusion paragraph

---

## Section Details

### Title

* Include the goal of the tutorial, not just the tools
* Keep under 60 characters
* Typical format: **How To <Accomplish a Task> with <Programming Language>/<Software>**
* Example: "How to build a data pipeline with Python"

### Introduction

1-3 paragraphs answering:

* **What is the tutorial about?** What software is involved and what does each component do?
* **Why should the reader learn this?** What are the benefits? What are practical reasons to follow this tutorial?
* **What will the reader do or create?** Be specific about what they'll accomplish
* **What will the reader have when done?** What new skills? What will they be able to do?

Keep focus on the reader:
* Use "you will configure" or "you will build" (not "we will learn how to")
* Focus on the problem being solved rather than the technology

### Prerequisites

* Spell out exactly what the reader should have or do before starting
* Format as a checklist
* Each point must link to an existing tutorial or official documentation
* Start from fresh installation to working setup
* Include local software needed (Git, Node.js, Python, Ruby, Docker, etc.)
* Include additional accounts needed (GitHub, Stripe, OpenAI, etc.)
* Be specific - no vague prerequisites like "Familiarity with JavaScript" without links

### Steps

* Describe what the reader needs to do and why
* Each step begins with Level 2 heading
* Use sentence case
* Procedural tutorials: **Step 1 — Creating user accounts** (use em-dash and gerund)
* After title, add introductory sentence describing what reader will do and its role in overall goal
* Focus on the reader: "You will build" (not "We will learn")

#### Commands in Steps

* All commands on their own line in own code block
* Precede with description of what command does
* After command, provide details about arguments and why using them

Example:
```
Execute the following command to display the contents of the `/home/ziggy` directory, including all hidden files:
```command
ls -al /home/ziggy
```
The `-a` switch shows all files, including hidden ones, and the `-l` switch shows a long listing including timestamps and file sizes.
```

* Display output in separate code block with label
* Separate commands from output with explanatory text
* If moving between directories, provide the commands

#### Files in Steps

* Describe file's general purpose before showing it
* Explain any changes reader will make
* Explicitly tell reader to create or open each file
* Example: "Open the file `my_app/workflow.py` in your editor."
* Reader should always know which file they're working with

#### Code Blocks

* Treat all code as learning opportunity
* Introduce code block with high-level explanation
* Show the code
* Call out important details after

Example structure:
```
Create the file `hello.js` in your text editor:
```command
nano hello.js
```
Add the following code to the file, which prints a message to the screen:
```js
console.log("Hello world!");
```
The `console.log` function takes a string and prints it to the screen.
```

When changing existing files:
* Show relevant parts
* Use highlighting for changes
* Explain what change does and why it's necessary

#### Transitions

* Frame each step with brief intro and closing transition
* Describe what reader accomplished and where they're going next
* Vary language to avoid repetition
* Example: "You have now installed the Let's Encrypt client, but before obtaining certificates, you need to make sure that all required ports are open. To do this, you will update your firewall settings in the next step."

### Conclusion

* Summarize what reader accomplished
* Use "you configured" or "you built" (not "we learned how to")
* Describe what reader can do next
* Include use cases or features to explore
* Link to other tutorials for additional setup
* Link to external documentation

---

## Formatting

### Headers

* Title: H1
* Introduction: H3
* Prerequisites, Steps, Conclusion: H2
* Procedural step headers: include step numbers followed by em-dash (—)
* Step headers use gerund (-ing words)
* Example: **Step 1 — Installing Nginx**
* Use H3 headers sparingly, avoid H4
* If using subheaders, have 2+ of that level or consider making multiple steps

### Line-level Formatting

**Bold text** for:
* Visible GUI text
* Hostnames and usernames (e.g., **wordpress-1**, **ziggy**)
* Term lists
* Emphasis when changing context (switching servers/users)

*Italics* for:
* Introducing technical terms only
* Example: "The Nginx server will be our *load balancer*"

In-line code formatting for:
* Command names: `unzip`
* Package names: `mysql-server`
* Optional commands
* File names and paths: `~/.ssh/authorized_keys`
* Example URLs: `http://<^>your_domain<^>`
* Ports: `:3000`
* Key presses in ALL CAPS: `ENTER`, simultaneous with plus: `CTRL+C`

Every complete sentence on separate line.
Separate paragraphs by space.

### Code Blocks

Use for:
* Commands to execute
* Files and scripts
* Terminal output
* Interactive text dialogues

Indicate excerpts/omissions with ellipses (...)

Do NOT include command prompt (`$` or `#`) in code blocks

### Images and Assets

Use images for:
* Screenshots of GUIs
* Interactive dialogue
* Diagrams of server setups

Don't use images for:
* Code screenshots
* Configuration files
* Output
* Anything that can be copied/pasted

Guidelines:
* Include descriptive alt text
* Include brief caption
* Use .png format
* Use standard link formatting

---

## Terminology

### Users, Hostnames, and Domains

* Default username: `ziggy`
* Default hostname: `your_server` (or more descriptive like `django_replica_1`)
* Default domain: `your_domain` (or `primary-1.your_domain` for multi-server)
* Use ALL CAPS in config files, code, output blocks: `YOUR_SERVER_IP`, `YOUR_DOMAIN`

### Software

* Use official website's capitalization
* If inconsistent, be consistent within article
* Link to software's home page on first mention

### Multi-server Setups

* Use project's terminology and clarify it
* Example: "The Django project refers to the original server as the **primary** and the secondary server as the **replica**."
* For abstract discussions, use **primary**/**replica** or **manager**/**worker**
