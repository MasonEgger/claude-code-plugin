---
description: "Convert voice transcript to Obsidian journal entry (blog section only)"
argument-hint: "<MM-DD-YYYY>"
---

## Required Checks
You MUST perform these checks and they must BOTH be true before you proceed

- Check to see if the directory you are working in is an Obsidian Vault. If it isn't, tell the user this command is only for use in an Obsidian Vault and do no more work.
- Calculate the year using `date +%Y` and save at {year}. Check to see if there is a Journal entry in @Journal/{year}/current/$ARGUMENTS.md. If there isn't, tell the user to create the journal entry for that day and do NO MORE WORK.

## Writing my Journal Entry
- My writing tone/voice is stored in @CLAUDE.md. Read this entire section and understand how I write and speak.
- Look for a @transcript.md file. This is a transcript of a voice recording for my daily journal entry. You will read this file and clean it up according to my voice. You should clean it up and make it coherent. Keep my tone and voice, but make it read like a journal.
    - Remove conversational tone and filler words. This has to act like a record for the future but still sound like me.
    - However, you should put things in chronological order. The transcript may say something like "Oh, before that we did this" and you should rewrite that part in my voice so the blog for the day flows organically.    - You can also make sub header 3s for different sections. The sections you can make are Personal, Work, and PyTexas.
- Write this cleaned up content to the #Blog section to $ARGUMENTS.md file you checked above.
    - You should add Obsidian cross links to things you think are relevant or pages I have already created.
    - Before adding a new cross link, check the vault and see if a link already exists you can use and use that link.
    - When determining if a link is worth cross linking too, analyze the layout of my vault and see if that's the kind of thing I'd like to store. If so, create a cross link, even if the other file doesn't exist, and I'll fill it in later.
    - You can add to the Highlights/Lowlights section.
- Do **NOT** add anything to the `Learning` or `Ideas & Insights` sections. Instead you should tell me what you would put in there and if I want it I'll tell you what to do.

