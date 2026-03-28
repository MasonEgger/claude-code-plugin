# Mason Egger-Specific Writing Patterns

This document captures Mason Egger's unique voice characteristics that go beyond the general style guide. Use this to match the author's specific patterns and rhythm.

## Unique Transition Phrases

These specific transition patterns appear frequently in Mason Egger's writing:

**"Now that..." pattern (very common):**
- "Now that you have Java installed, you will download..."
- "Now that we have our database, we can begin..."
- "Now that you've setup your application, it's time to..."

**"Once you've done..." pattern:**
- "Once you've done that you'll see..."
- "Once you've done this you should see..."
- "Once the installation process is done..."

**"After... is done" pattern:**
- "After the installation process is done you'll be prompted..."

**"With... active/installed" pattern:**
- "With your virtual environment active, install..."
- "With Docker connected to the WSL you'll learn..."

**"From here" / "From this":**
- "From here select **Open a Folder**"
- "From this terminal navigate into..."

## Pronoun Usage Pattern

Unlike strict second-person-only guides, Mason Egger uses strategic "we":

**Use "we" when:**
- Performing shared discovery: "We can now perform our initial configuration..."
- Working through problems together: "We need to use this user to perform administrative tasks"
- Setting up environments: "We'll use the method *getenv* from *os* library"

**Use "you" when:**
- Reader takes individual action: "You will install Django..."
- Reader makes decisions: "You can choose to add a picture..."
- Reader observes results: "You should see your bot in the member list..."

**Common pattern: Start with "we" context, then "you" action:**
> "We need to update the local `apt` package index and then download and install the packages. The packages we install depend on which version of Python your project will use. Type the following command..."

## Sentence Rhythm Pattern

Characteristic Mason Egger rhythm mixes:
1. **Short declarative** (5-8 words): "Now that you have Java installed..."
2. **Medium explanatory** (12-20 words): "This will create a directory called `discord` within your `.venvs` directory."
3. **Longer detailed** (20-30 words, less common): "Inside, it will install a local version of Python and a local version of `pip` that you can use to install and configure an isolated Python environment."

**Avoid:**
- Many consecutive short sentences (feels choppy)
- Many consecutive long sentences (feels dense)

## Error Handling Voice

When errors are expected, Mason Egger treats them as normal workflow:

**Pattern: Show error → Explain cause → Provide solution:**

> "When we run this command we will see the following errors generated:
> ```
> [error output]
> ```
> These errors were generated because the server could not find two necessary files... Fortunately, since the server was unable to find these files it created them in our current working directory."

**Key phrases:**
- "These errors were generated because..."
- "Fortunately..."
- "This is normal/expected..."

## Note and Warning Voice

**Note pattern:**
```
**Note:** [Reminder or context]. [Explanation or reason].
```

**Examples:**
- "**Note:** When the virtual environment is activated (when your prompt has `(discord)` preceding it), use `pip` instead of `pip3`..."
- "**Note:** Be sure to include `localhost` as one of the options since we will be proxying connections..."

**Warning pattern:**
```
**Warning:** [What to avoid or be aware of]. [Consequence or reason].
```

## Introduction Structure (Mason Egger-specific)

While the general guide covers introduction structure, Mason Egger adds these specific elements:

**Technology popularity/context (when relevant):**
- "As of late 2019 it is the second best selling video game of all time."
- "It has been gaining in popularity for the past few years..."

**Version/variant clarifications:**
- Addresses common confusion upfront
- Example: The Minecraft Java vs Microsoft version distinction

**Acronym pattern:**
- "WSGI for short" / "ASGI for short"
- Define acronym inline immediately after first use

## Vocabulary Preferences

**Contractions in prose (not in headings):**
- "You'll" over "You will"
- "We'll" over "We will"
- "You've" over "You have"

**Specific word choices:**
- "Navigate to" (not "go to")
- "Click on" (not "click" or "select")
- "Type the following command" (not "run" or "execute" for first instruction)
- "Your prompt should change to indicate..." (not "you'll see")

**Technical precision:**
- "Operating system" (spell out first use, then "OS")
- "Terminal" consistently (not switching between "terminal", "console", "command line")

## Code Block Introduction Pattern

**Standard pattern: Purpose → File → Action:**

> "Now add the following imports to the file: *os*, *random*, and *discord*. The *os* library will allow you to read valuable information, such as *API Tokens* and *Guild Name* from your environment variables."
>
> ```python
> [label bot.py]
> import os
> import random
> import discord
> ```

**When opening files for editing:**
> "Open the settings file in your text editor:"
>
> ```command
> nano ~/myprojectdir/myproject/settings.py
> ```

## Explanatory Depth Balance

Mason Egger provides **just enough** explanation without over-explaining:

**Good balance examples:**
- Explains "peer authentication" with one clear sentence
- Defines "headless JRE" in context: "This is a minimal version of Java that removes the support for GUI applications."
- Links to docs for deep dives rather than expanding inline

**Pattern: Define → Context → Link (if needed)**

## Prerequisites Style

**Mason Egger-specific prerequisite voice:**

> "In order to follow along with this guide, you'll need:"
> "To complete this tutorial, you'll need:"

**Bullet format with bold lead-in:**
- **Thing needed**: Description with link if applicable

## Step Closing Pattern

Mason Egger consistently ends steps with forward motion:

**Patterns:**
- "Now that [completed action], you'll [next step]..."
- "Now that [completed action], let's [next action]..."
- "You should now have [outcome]. [Preview of next step]."

**Examples:**
- "Now that you have Docker connected to the WSL you'll learn how to develop within the WSL directly..."
- "You should now have the libraries necessary to build a discord bot."
- "Now that your bot is added to your server let's add some code to bring the bot to life."

## Quick Mason Egger Voice Checklist

**To sound like Mason Egger, ensure:**

- [ ] Use "Now that..." transitions between steps
- [ ] Mix "we" (shared work) and "you" (reader actions) naturally
- [ ] Vary sentence length: short → medium → short rhythm
- [ ] Use contractions in prose (you'll, we'll, you've)
- [ ] Define acronyms inline: "WSGI for short"
- [ ] Treat expected errors as normal workflow
- [ ] End steps with "Now that... you'll/you will..."
- [ ] Use "Navigate to" and "Click on" consistently
- [ ] Balance detail without over-explaining
- [ ] Add context about popularity/adoption when relevant

## Example of Mason Egger Voice vs Generic Voice

**Generic style:**
> Install the necessary packages. Run the apt update command. Then install Python. This will install the required software. After installation, you can proceed to the next step.

**Mason Egger style:**
> To begin the process, we'll download and install all of the items we need from the Ubuntu repositories. We will use the Python package manager `pip` to install additional components a bit later.
>
> Type the following command to install the necessary system packages:
>
> ```command
> sudo apt update && sudo apt install python3-venv
> ```
>
> This will install the python libraries needed to setup a virtual environment later.
>
> Now that we have our packages installed, we can begin setting up our development environment.

**Key differences:**
- "To begin the process, we'll..." (Mason Egger sets context)
- "We will use... a bit later" (Mason Egger previews future steps)
- "Type the following command" (Mason Egger specific phrasing)
- Explains what installs do, not just that they install
- "Now that..." transition with forward motion
