# Wiki Init Operation

You are initializing a new LLM Wiki. Follow these steps exactly.

## Step 1: Gather Domain Context

Ask the user:
1. **What is this wiki about?** (topic, domain, scope)
2. **What kinds of sources will you be adding?** (articles, papers, books, notes, transcripts, etc.)
3. **Any special conventions?** (terminology preferences, important entity types, output formats)

Wait for their response before proceeding.

## Step 2: Create Directory Structure

Create the following directories (use `mkdir -p`):

```
sources/
sources/assets/
wiki/
wiki/entities/
wiki/concepts/
wiki/sources/
wiki/comparisons/
wiki/queries/
```

## Step 3: Generate CLAUDE.md

Create `CLAUDE.md` at the project root. Tailor it to the user's domain based on their answers in Step 1. Use this template as a starting point, but customize the domain-specific sections:

```markdown
# LLM Wiki Schema

## Domain

{{Description of what this wiki covers, based on user's answer}}

## Source Types

{{List of expected source types and how to handle each}}

## Page Types

### Entities
Pages for distinct things: people, organizations, products, places, events.
- Directory: `wiki/entities/`
- Naming: `kebab-case-name.md`
- {{Domain-specific entity guidance}}

### Concepts
Pages for ideas, theories, techniques, patterns, methodologies.
- Directory: `wiki/concepts/`
- Naming: `kebab-case-name.md`
- {{Domain-specific concept guidance}}

### Source Summaries
One page per ingested source document. Captures key claims, data, and takeaways.
- Directory: `wiki/sources/`
- Naming: `kebab-case-short-title.md`

### Comparisons
Side-by-side analyses, comparison tables, tradeoff discussions.
- Directory: `wiki/comparisons/`
- Naming: `kebab-case-comparison-title.md`

### Queries
Filed answers to questions asked against the wiki.
- Directory: `wiki/queries/`
- Naming: `kebab-case-question-slug.md`

## Conventions

- All wiki pages use YAML frontmatter with: title, type, created, updated, sources, tags
- Use `[[wikilinks]]` for internal links (Obsidian-compatible)
- File names are kebab-case, no spaces
- Dates use YYYY-MM-DD format
- When new information contradicts existing content, use `> [!warning] Contradiction` callouts
- {{Any domain-specific conventions from user}}

## Frontmatter Schema

```yaml
title: string (required)
type: entity | concept | source | comparison | query (required)
created: YYYY-MM-DD (required)
updated: YYYY-MM-DD (required)
sources: list of source filenames (required for all except overview/index)
tags: list of strings (optional but encouraged)
```

## Maintenance Notes

This file is co-evolved between you and the LLM. As you work with the wiki, update this schema to reflect new conventions, page types, or workflows that emerge.
```

## Step 4: Create wiki/index.md

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

## Step 5: Create wiki/log.md

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

## Step 6: Create wiki/overview.md

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
