---
name: "create-the-best-skills"
description: Turns the work done in the current conversation into a clean, reusable skill that someone else can follow for a similar task with different inputs. Digests a messy, back-and-forth chat into what worked, what failed and why, the core rules to keep, the questions a new user must be asked, and (when the workflow depends on it) a cleaned-up script. Use this whenever the user says "turn this into a skill", "make a skill from this chat", "save this workflow as a skill", "package what we just did", "skill-ify this", or otherwise wants to capture a process from the conversation so others can reuse it, even if they don't say the word "skill".
---

# Chat to Skill

Distill the current conversation into a skill that a different person can use for the same kind of task, with their own project, resources, and conventions.

The people who will use the finished skill are usually architects, designers, and firm staff. They are not technical, and they will have none of the context, trial and error, or know-how that went into the original chat. The skill has to carry that knowledge for them, ask for what it needs, and get them to the result quickly.

Work only from the current conversation. Do not search past chats.

## The process

1. Harvest the conversation (silently)
2. Sort what you found into Core, Variables, Pitfalls, Code, and Noise (silently)
3. Share a one-screen summary and get the user's edits. **Do not write the skill before this is confirmed.**
4. Write the SKILL.md, plus a cleaned-up script if the user approved one
5. Run the pre-delivery check (silently)
6. Package and deliver

### 1. Harvest

Read the whole conversation, start to finish. Late messages usually hold the version that finally worked, and early messages hold the mistakes. Pull out:

- **The goal.** What was the user actually trying to produce, and what did "done" look like?
- **The final working method.** The steps, in order, that led to the accepted result. If the method changed partway through, the later version wins.
- **Inputs used.** Files, references, tools, connectors, data sources, templates, and settings.
- **Decisions and the reasons behind them.** Why one approach was chosen over another.
- **Failures.** Errors, wrong assumptions, tool quirks, outputs the user rejected, and what fixed each one.
- **User corrections.** Every time the user said "no, do it this way", treat it as a strong signal. These usually become core rules.
- **Code.** Any scripts that were written or run. Identify which version actually produced the accepted result. There are often several near-identical versions, and the last one that ran without errors and gave the right output is the one that counts.
- **The output.** Its format, structure, naming, and level of detail.

If the chat never reached a working result, say so plainly. Ask whether to capture the partial process with its open problems clearly marked, or to wait until it works.

If the chat covers two or more unrelated workflows, name them and ask which one to turn into a skill. You can also suggest one skill for each.

### 2. Sort

Put everything you found into one of five buckets.

**Core.** These are things that must stay true no matter who uses the skill or what project it is. Examples are the order of steps that matters, a quality bar, a check that caught errors, or a rule the user insisted on. Core becomes non-negotiable instructions in the skill, each with a short reason.

**Variables.** These are things that were specific to this project and will differ for the next user. Examples are the source document, naming or numbering conventions, units, templates, software version, and available tools. Each variable becomes an intake question. For every variable, work out three things:
- the question to ask
- a sensible default, if one exists
- a fallback path if the user doesn't have that resource (for example, no reference document, so build the list another way)

**Pitfalls.** These are the errors and dead ends. Each becomes an entry in the skill's "Known failure points" section, written as symptom, cause, and fix. The lesson stays even though the failed attempt is dropped.

**Code.** This is script code that the workflow depends on: code doing something mechanical and repeatable, where regenerating it each time would be slow, inconsistent, or likely to reintroduce fixed bugs. Examples are pulling data through a software connector, bulk renaming or tagging, and parsing a document into a list. One-off snippets that only explored or debugged something go to Noise. For each piece of load-bearing code, note:
- what it does, in one plain sentence
- which values inside it are project-specific (these become settings)
- which lines are fixes for errors hit in the chat

**Noise.** Drop tangents, small talk, abandoned ideas that taught nothing, earlier versions of scripts, and all project-specific content. That includes client names, project names, addresses, room lists, file paths, account details, and API keys. None of it goes into the skill. If a concrete example helps, invent a neutral generic one.

### 3. Summary for approval

Before writing anything, show the user this summary. Keep it scannable and fit it on one screen:

```
**Proposed skill:** [name] — [one-line purpose]

**What worked (the method):**
1. ...

**Core rules (always true):**
- [rule] — because [reason]

**Variables (the skill will ask about these):**
- [variable] → default: [x] / if they don't have it: [fallback]

**Known failure points (from this chat):**
- [symptom] → [fix]

**Code:** This workflow depends on [what the script does]. I'd include a
cleaned-up version with your project's values turned into settings.
Include it? (recommended)
[Omit this block if there is no load-bearing code.]

**Leaving out:** [anything notable you are dropping, and why]

**Gaps I couldn't resolve:** [anything ambiguous, e.g. which of two approaches was the real fix]
```

End by asking whether anything is wrong, missing, or should move to a different bucket. Apply the user's edits. If the edits are substantial, show the revised summary again. Once it is confirmed, write the skill.

### 4. Write the skill

The skill is a folder named after the skill:

```
[skill-name]/
├── SKILL.md
└── scripts/            ← only if the user approved code
    └── [descriptive_name].py
```

#### SKILL.md

Use this structure. Leave out any section that has nothing real in it.

```markdown
---
name: [lowercase-hyphenated]
description: [What it produces + when to use it + the phrases a user would
  actually say. Be a little pushy so it triggers: "Use this whenever the user
  mentions X, Y, or Z, even if they don't ask for it by name."]
---

# [Title]

[2–3 sentences: what this produces, who it's for, what a good result looks like.]

**Requires:** [tools/connectors/code execution the workflow depends on, and
what to do if one isn't available]

## Start here: questions to ask
[Only questions that change the outcome. Group them and ask them together,
not one at a time. Show the default in brackets. For any missing resource,
point to the fallback path. If the user already gave an answer, don't ask it
again.]

## Core rules
[The non-negotiables, each with a one-line reason.]

## Workflow
[Numbered steps. Mark checkpoints where the user should confirm before
continuing, especially before anything slow, hard to undo, or that changes
their files or models. At the step where a script runs, name the script,
say which intake answers fill which settings, and say to run it rather
than rewrite it.]

## If your setup is different
[Branches for the main variations: no source document, a different
convention, different software or tools available, and so on.]

## Known failure points
[Symptom → cause → fix, from the original chat.]

## Check the result
[A short checklist to verify the output before calling it done.]
```

Follow these writing rules:

- **Write for someone who wasn't there.** If a step only makes sense because of something said in the original chat, spell it out or cut it.
- **Use plain language.** Define any technical term in a few words the first time it appears. The end user never needs to read or edit the code; Claude runs it.
- **Explain the why.** A rule with a reason gets applied correctly in new situations. A bare "MUST" gets misapplied.
- **Keep it concise.** Aim for under about 250 lines. Cut anything that doesn't change what Claude or the user does.
- **Keep intake fast.** Ask the fewest questions that still guarantee a good result, and use defaults wherever you can. The goal is getting the user to the result quickly, not interviewing them.

#### Code

Include only the final working version, cleaned up. Never include the history of attempts; those lessons live in "Known failure points".

- **Settings block at the top.** Every project-specific value (parameter names, numbering formats, prefixes, units, file paths, category names) becomes a clearly labeled setting at the top of the script, with a generic placeholder or a sensible default. Nothing project-specific stays hardwired in the body. This is the most important step: a script locked to one project's conventions breaks for the next user.
- **Comment the fixes.** Where a line exists because of an error hit in the chat, add a short comment saying what it prevents, so nobody "simplifies" it away. For example: `# Revit returns lengths in feet; convert before comparing`.
- **Remove leftovers.** Delete debug prints, commented-out old versions, unused functions, and test data.
- **Fail clearly.** When a required input is missing or a setting looks wrong, the script should stop with a plain-language message saying what to fix, not a raw error.
- **No secrets or personal data.** No API keys, tokens, account IDs, user names, or local paths.
- **Short snippets stay inline.** If the code is under about 30 lines, put it in the SKILL.md as a code block instead of a separate file.
- **Don't invent untested code.** Only include code that actually ran successfully in the chat. Cleanup should be limited to parameterizing, commenting, and removing leftovers. If you had to change the logic, say so in the delivery note so the user knows to test it.

### 5. Pre-delivery check (silent)

Before delivering, read the draft as a new user whose setup is different from the original chat's: a different document, a different naming convention, or a missing resource. Confirm:

- [ ] No names, numbers, paths, or data from the original project remain, in the SKILL.md or in any script.
- [ ] Every variable has a question, and the ones that need it have a default and a fallback.
- [ ] Every error from the chat appears as a known failure point.
- [ ] Each core rule has a reason.
- [ ] The description would trigger on the phrases a real user would say.
- [ ] Nothing depends on knowledge that exists only in the original chat.
- [ ] If there is a script: every project-specific value is in the settings block, the SKILL.md says when to run it and how intake answers map to its settings, and the file name referenced in SKILL.md matches the actual file.

Fix anything that fails the check before delivering.

### 6. Package and deliver

Build the skill folder in `/home/claude/[skill-name]/`. Then run the packaging script that ships with this skill. It lives in the `scripts/` folder next to this SKILL.md:

```bash
python3 [path-to-this-skill]/scripts/package_skill.py /home/claude/[skill-name] /mnt/user-data/outputs
```

The script checks the folder (SKILL.md present, valid name and description, referenced scripts exist, no obvious leftover secrets or personal paths) and writes `/mnt/user-data/outputs/[skill-name].zip` with the folder correctly at the root of the zip. If it reports errors, fix them and run it again. Treat warnings as items to review, not automatic failures.

Present the zip with `present_files`. Then add two or three lines at most:

- The skill's name and what it's for, in one sentence.
- How to install it: upload the zip in the Skills section of Claude's settings, as is, without unzipping or re-zipping it.
- Any open gap from the summary, or any logic change made to the code, that the user may want to check.
