# Memory Init Operation

You are initializing a new agent memory store. Follow these steps exactly.

## Step 1: Gather Context

Ask the user:
1. **What kind of agent is this?** (purpose, domain, what it does)
2. **What environment does it operate in?** (tools, APIs, systems, users it interacts with)
3. **What kinds of inputs will you be recording?** (conversations, system logs, error traces, manual observations, task results, etc.)
4. **Any special conventions?** (terminology, important actor types, memory retention policies)
5. **Do you want to use an existing Obsidian vault?** If yes, provide the full path (e.g., `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault`). If no, the memory store will be created locally in the project directory.
6. **Manual or auto mode?** Manual = human reviews all operations. Auto = agent self-manages memory without confirmation prompts.

Wait for their response before proceeding.

## Step 1.5: Create .memory-config.json

Create `.memory-config.json` at the **project root** (not inside the vault):

```json
{
  "vault_path": null,
  "inputs_dir": "inputs",
  "memory_dir": "memory",
  "mode": "manual",
  "auto_consolidate_threshold": 5,
  "stale_days": 30,
  "access_count_prune_threshold": 2
}
```

- If the user provided a vault path, set `vault_path` to that path (keep `~` — the skill will expand it at runtime).
- If the user chose local mode, set `vault_path` to `null`.
- Set `mode` to `"manual"` or `"auto"` based on user's answer.
- If a vault path was given, verify it exists by running: `ls "$(eval echo <vault_path>)"`. If the path doesn't exist, warn the user and ask them to double-check before continuing.

From this point forward, resolve all `inputs/` and `memory/` paths per the **Path Resolution** rules in SKILL.md. Use `{INPUTS}` and `{MEMORY}` as shorthand for the resolved paths. Always double-quote paths in Bash commands.

## Step 2: Create Directory Structure

Create the following directories (use `mkdir -p`). If using a vault, create these inside the vault path. Always double-quote paths.

```
{INPUTS}/
{INPUTS}/conversations/
{INPUTS}/logs/
{INPUTS}/observations/
{INPUTS}/assets/
{MEMORY}/
{MEMORY}/episodes/
{MEMORY}/actors/
{MEMORY}/schemas/
{MEMORY}/evaluations/
{MEMORY}/reflections/
```

Example for iCloud vault:
```bash
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault/inputs/conversations"
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault/memory/episodes"
# ... etc
```

## Step 3: Generate CLAUDE.md

Create `CLAUDE.md` at the project root. Tailor it to the agent's domain based on the user's answers in Step 1. Use this template as a starting point, but customize the domain-specific sections:

```markdown
# Agent Memory Schema

## Domain

{{Description of the agent's purpose and environment, based on user's answer}}

## Input Types

{{List of expected input types and how to handle each, e.g.:}}
- **Conversations**: Chat logs, transcripts. Extract: decisions made, commitments, action items, who said what.
- **System logs**: Error traces, performance logs. Extract: what happened, root cause, resolution, affected systems.
- **Observations**: Manual notes, environment snapshots. Extract: key facts, changes noticed, hypotheses.
- **Task results**: Completed task outputs. Extract: approach taken, outcome, what worked/didn't.

## Page Types

### Episodes
Discrete experiences: a conversation, a task execution, an error encountered, an observation.
- Directory: `memory/episodes/`
- Naming: `kebab-case-name.md`
- {{Domain-specific episode guidance — what constitutes a "significant" episode worth recording}}

### Actors
Agents, tools, users, systems, APIs — anything that does things or is acted upon.
- Directory: `memory/actors/`
- Naming: `kebab-case-name.md`
- {{Domain-specific actor guidance — key actor types, what metadata to capture}}

### Schemas
Strategies, patterns, procedures, heuristics — reusable knowledge distilled from episodes.
- Directory: `memory/schemas/`
- Naming: `kebab-case-name.md`
- {{Domain-specific schema guidance — what kinds of patterns matter most}}

### Evaluations
Strategy comparisons, approach tradeoffs, tool assessments, what-worked-vs-what-didn't.
- Directory: `memory/evaluations/`
- Naming: `kebab-case-comparison-title.md`

### Reflections
Synthesized lessons, answers to "what have I learned about X?", meta-observations.
- Directory: `memory/reflections/`
- Naming: `kebab-case-question-slug.md`

## Conventions

- All memory pages use YAML frontmatter with: title, type, created, updated, sources, tags, status, importance, confidence, last_accessed, access_count, memory_type, validity_window, supersedes
- Use `[[wikilinks]]` for internal links (Obsidian-compatible)
- File names are kebab-case, no spaces
- Dates use YYYY-MM-DD format
- When new information contradicts existing content, use `> [!warning] Contradiction` callouts
- {{Any domain-specific conventions from user}}

## Frontmatter Schema

\`\`\`yaml
title: string (required)
type: episode | actor | schema | evaluation | reflection (required)
created: YYYY-MM-DD (required)
updated: YYYY-MM-DD (required)
sources: list of input filenames (required)
tags: list of strings (required)
status: draft | active | consolidated | archived (required)
importance: high | medium | low (required)
confidence: high | medium | low | uncertain (required)
last_accessed: YYYY-MM-DD (required)
access_count: integer (required, default 0)
memory_type: episodic | semantic | procedural (required)
validity_window: permanent | YYYY-MM-DD (required)
supersedes: list of page filenames (optional, default [])
\`\`\`

## Maintenance Notes

This file is co-evolved between you and the agent. As you work with the memory store, update this schema to reflect new conventions, page types, or workflows that emerge.
```

## Step 4: Create {MEMORY}/index.md

```markdown
---
title: Memory Index
type: index
created: {{today's date}}
updated: {{today's date}}
---

# Memory Index

A catalog of all pages in this memory store, organized by category.

## Actors

_No actors yet._

## Schemas

_No schemas yet._

## Episodes

_No episodes yet._

## Evaluations

_No evaluations yet._

## Reflections

_No reflections yet._
```

## Step 5: Create {MEMORY}/log.md

```markdown
---
title: Activity Log
type: log
created: {{today's date}}
updated: {{today's date}}
---

# Activity Log

Chronological record of memory operations. Newest entries first.

---

## [{{today's date}}] init | Memory store initialized

Memory store created for: {{agent description}}.
Directories created: inputs/, memory/episodes/, memory/actors/, memory/schemas/, memory/evaluations/, memory/reflections/.
Schema generated: CLAUDE.md.
Mode: {{manual | auto}}.
```

## Step 6: Create {MEMORY}/overview.md

```markdown
---
title: Overview
type: overview
created: {{today's date}}
updated: {{today's date}}
tags: []
status: active
importance: high
confidence: uncertain
last_accessed: {{today's date}}
access_count: 0
memory_type: semantic
validity_window: permanent
supersedes: []
---

# Overview

_This overview will be updated as experiences are recorded. It provides a high-level synthesis of what the agent knows._

## Summary

No experiences have been recorded yet. Add input documents to `inputs/` and run `/memory record <input-path>` to begin building the memory store.

## Key Patterns

_Will emerge as episodes are recorded and consolidated._

## Open Questions

_Will be tracked as the memory store grows._
```

## Step 7: Initialize Git (if needed)

Check if the project root is already a git repository. If not, run:
```bash
git init
```

Create a `.gitignore` if one doesn't exist, with sensible defaults:
```
.DS_Store
*.swp
*.swo
*~
```

## Step 8: Report

Tell the user what was created and suggest next steps:
- Drop input documents into `inputs/` (conversations, logs, observations)
- Run `/memory record inputs/<filename>` to process them into memory
- Run `/memory query <question>` to recall information
- Run `/memory reflect` to generate meta-observations after recording several episodes
- Run `/memory consolidate` to merge related episodes into reusable schemas
- Open the directory in Obsidian to browse the memory store
- Review and customize `CLAUDE.md` as conventions evolve
- **Recommended Obsidian settings**:
  - Settings > Files and links > set "Attachment folder path" to `inputs/assets/` — this ensures images are saved locally where the agent can read them
  - Consider installing the **Dataview** plugin for dynamic queries over page frontmatter
