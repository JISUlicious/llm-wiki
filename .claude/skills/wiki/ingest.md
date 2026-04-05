# Wiki Ingest Operation

You are ingesting a source document into the wiki. The source path is provided as an argument (e.g., `sources/article-title.md`).

## Pre-flight

0. Read `.wiki-config.json` if it exists at the project root. Resolve `{SOURCES}` and `{WIKI}` per the **Path Resolution** rules in SKILL.md. If no config, use `sources/` and `wiki/` relative to project root. Always double-quote paths containing spaces in Bash commands.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{WIKI}/index.md` to understand existing wiki content
3. Read `{WIKI}/log.md` (last 5-10 entries) to understand recent activity
4. Verify the source file exists and read it completely. The source path argument is relative to `{SOURCES}` (e.g., if user says `sources/article.md`, resolve to `{SOURCES}/article.md`). If the source path is an absolute path or a URL, use it directly.

If the source file doesn't exist, tell the user and list available files in `{SOURCES}/`.

## Step 1: Analyze the Source

Read the entire source document. Identify:

- **Key entities**: people, organizations, products, places, events mentioned
- **Key concepts**: ideas, theories, techniques, patterns, methodologies discussed
- **Key claims**: factual assertions, data points, statistics, conclusions
- **Relationships**: how entities and concepts relate to each other
- **Notable quotes**: important or quotable passages (with attribution)

If the source contains image references, note them but focus on the text content. You can read images separately if they seem important to understanding the content.

## Step 2: Discuss with User

Before writing anything, share a brief summary of what you found:
- 3-5 key takeaways from the source
- Which existing wiki pages will be updated (if any)
- Which new pages you plan to create
- Any contradictions with existing wiki content

Ask the user if they want to adjust emphasis or skip anything. Wait for confirmation before proceeding.

## Step 3: Create Source Summary Page

Create `wiki/sources/{{kebab-case-title}}.md`:

```markdown
---
title: "{{Source Title}}"
type: source
created: {{today}}
updated: {{today}}
sources:
  - {{original-filename}}
tags:
  - {{relevant tags}}
---

# {{Source Title}}

**Source**: `sources/{{original-filename}}`
**Author**: {{if known}}
**Date**: {{if known}}

## Summary

{{2-4 paragraph summary of the source, focusing on key claims and contributions}}

## Key Points

- {{Bullet points of the most important claims/data/insights}}

## Entities Mentioned

- [[entity-name]] — {{role/relevance in this source}}

## Concepts Discussed

- [[concept-name]] — {{how it's discussed in this source}}

## Notable Quotes

> "{{quote}}" — {{attribution}}

## References

_Original source: `sources/{{filename}}`_
```

## Step 4: Create or Update Entity Pages

For each significant entity identified:

**If the entity page already exists** (`wiki/entities/{{name}}.md`):
- Read the existing page
- Add new information from this source as a new section or integrate into existing sections
- Add the source to the frontmatter `sources` list
- Update the `updated` date
- Add any new `[[wikilinks]]` discovered
- If new info contradicts existing content, add a `> [!warning] Contradiction` callout

**If the entity page doesn't exist** and the entity is significant enough (mentioned substantively, not just in passing):
- Create `wiki/entities/{{kebab-case-name}}.md` with full frontmatter
- Write a description based on what this source says about the entity
- Link to the source summary page and any related entity/concept pages

## Step 5: Create or Update Concept Pages

Same logic as entities, but in `wiki/concepts/`:

**If exists**: integrate new information, update sources, add cross-references
**If new and significant**: create `wiki/concepts/{{kebab-case-name}}.md`

Concept pages should explain:
- What the concept is
- Why it matters
- How it relates to other concepts in the wiki
- What different sources say about it (synthesis, not just repetition)

## Step 6: Cross-Reference Pass

This is critical. After creating/updating pages:

1. **Forward links**: Scan every page you created or updated. Anywhere another wiki page is mentioned by name, add a `[[wikilink]]` if not already present.

2. **Backlinks**: Scan OTHER existing wiki pages (use Grep to find mentions of new entity/concept names). Add `[[wikilinks]]` in those pages pointing to the new pages you created.

3. **Source summary links**: Ensure the source summary page links to all entity and concept pages it references.

4. **Overview check**: Read `wiki/overview.md`. If this source significantly changes the big picture (new major theme, shifts understanding, introduces important new area), update the overview.

## Step 7: Update Index

Read `wiki/index.md` and add entries for every new page created. Update descriptions for any existing pages that were significantly modified.

Each entry format: `- [[page-name]] — One-line description`

Place entries under the correct category header (Entities, Concepts, Sources, Comparisons, Queries).

## Step 8: Update Log

Prepend a new entry to `wiki/log.md` (after the header, before existing entries):

```markdown
## [{{today}}] ingest | {{Source Title}}

Ingested `sources/{{filename}}`. Pages created: [[list]]. Pages updated: [[list]]. Key takeaways: {{1-2 sentences}}.
```

## Step 9: Report

Tell the user:
- Pages created (with links)
- Pages updated (with what changed)
- Any contradictions found
- Suggested follow-up: related sources to look for, questions to explore, concepts that need their own page
