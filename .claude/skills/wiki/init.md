# Wiki Init Operation

You are initializing a new LLM Wiki. Follow these steps exactly.

## Step 1: Gather Domain Context

Ask the user:
1. **What is this wiki about?** (topic, domain, scope)
2. **What kinds of sources will you be adding?** (articles, papers, books, notes, transcripts, etc.)
3. **Any special conventions?** (terminology preferences, important entity types, output formats)
4. **Do you want to use an existing Obsidian vault?** If yes, provide the full path (e.g., `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault`). If no, the wiki will be created locally in the project directory.

Wait for their response before proceeding.

## Step 1.5: Create .wiki-config.json

Create `.wiki-config.json` at the **project root** (not inside the vault):

```json
{
  "vault_path": null,
  "sources_dir": "sources",
  "wiki_dir": "wiki"
}
```

- If the user provided a vault path, set `vault_path` to that path (keep `~` — the skill will expand it at runtime).
- If the user chose local mode, set `vault_path` to `null`.
- If a vault path was given, verify it exists by running: `ls "$(eval echo <vault_path>)"`. If the path doesn't exist, warn the user and ask them to double-check before continuing.

From this point forward, resolve all `sources/` and `wiki/` paths per the **Path Resolution** rules in SKILL.md. Use `{SOURCES}` and `{WIKI}` as shorthand for the resolved paths. Always double-quote paths in Bash commands.

## Step 2: Create Directory Structure

Create the following directories (use `mkdir -p`). If using a vault, create these inside the vault path. Always double-quote paths.

```
{SOURCES}/
{SOURCES}/assets/
{WIKI}/
{WIKI}/entities/
{WIKI}/concepts/
{WIKI}/sources/
{WIKI}/comparisons/
{WIKI}/queries/
```

Example for iCloud vault:
```bash
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault/sources/assets"
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault/wiki/entities"
# ... etc
```

## Step 3: Generate CLAUDE.md (domain schema only)

Create `CLAUDE.md` at the project root. Keep it **strictly domain-specific** — skill mechanics (directory layout, frontmatter shape, ingest steps, link format) live in `.claude/skills/wiki/SKILL.md` and must NOT be duplicated here. Use this minimal template, customized from the user's Step 1 answers:

```markdown
# {{Domain}} Wiki — Project Schema

This file is project-specific guidance for the wiki. It defines what this wiki covers and any domain conventions. Skill mechanics live in `.claude/skills/wiki/SKILL.md`.

## Domain

{{Description of what this wiki covers, based on user's answer — topic, scope, intended audience}}

## Source Types

{{Bullet list of expected source types and what to extract from each — e.g., "Research papers: extract method, results, limitations"; "Podcast transcripts: extract speaker attributions and notable quotes". Be specific to this domain.}}

## Domain-Specific Page Guidance

Augments the skill's generic page-type definitions. Only include entries where there's domain-specific guidance worth saying:

- **{{entity subtype 1}}** (entity pages): {{what to capture, e.g., "include affiliation, key contributions"}}
- **{{entity subtype 2}}** (entity pages): {{...}}
- **Concepts**: {{any domain-specific conventions for concept pages, e.g., "include mathematical formulation when applicable"}}

## Domain Conventions

{{Only include conventions that are specific to this domain. Skip generic markdown/wiki conventions — those live in SKILL.md. Examples worth including: domain notation (LaTeX for math, code-block language for snippets), citation styles, terminology preferences.}}

## Maintenance Notes

This file is co-evolved between you and the LLM. As you work with the wiki, update this schema to reflect new domain conventions or important entity types that emerge. Skill-level mechanics (link format, frontmatter shape, directory layout) belong in `.claude/skills/wiki/`, not here.
```

## Step 4: Create {WIKI}/index.md

```markdown
---
title: Wiki Index
type: index
created: {{today's date}}
updated: {{today's date}}
---

# Wiki Index

A catalog of all pages in this wiki, organized by category.

## Entities

_No entities yet._

## Concepts

_No concepts yet._

## Sources

_No sources yet._

## Comparisons

_No comparisons yet._

## Queries

_No queries yet._
```

## Step 5: Create {WIKI}/log.md

```markdown
---
title: Activity Log
type: log
created: {{today's date}}
updated: {{today's date}}
---

# Activity Log

Chronological record of wiki operations. Newest entries first.

---

## [{{today's date}}] init | Wiki initialized

Wiki created for: {{domain description}}.
Directories created: sources/, wiki/entities/, wiki/concepts/, wiki/sources/, wiki/comparisons/, wiki/queries/.
Schema generated: CLAUDE.md.
```

## Step 6: Create {WIKI}/overview.md

```markdown
---
title: Overview
type: overview
created: {{today's date}}
updated: {{today's date}}
tags: []
---

# Overview

_This overview will be updated as sources are ingested. It provides a high-level synthesis of the wiki's contents._

## Summary

No sources have been ingested yet. Add source documents to `sources/` and run `/wiki ingest <source-path>` to begin building the knowledge base.

## Key Themes

_Will emerge as sources are added._

## Open Questions

_Will be tracked as the wiki grows._
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
- Drop source documents into `sources/`
- Run `/wiki ingest sources/<filename>` to process them
- Open the directory in Obsidian to browse the wiki
- Review and customize `CLAUDE.md` as conventions evolve
- **Recommended Obsidian settings**:
  - Settings → Files and links → set "Attachment folder path" to `sources/assets/` — this ensures images from clipped articles are saved locally where the LLM can read them
  - Consider installing the **Dataview** plugin for dynamic queries over page frontmatter
  - Consider installing the **Marp** plugin if you want slide deck generation from wiki content
