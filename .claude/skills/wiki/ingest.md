# Wiki Ingest Operation

You are ingesting source documents into the wiki. The argument can be a local file path (e.g., `sources/article-title.md`), a URL (PDF, plain-text, or web page), or a directory/glob for batch ingestion (e.g., `sources/` or `sources/*.md`).

## Pre-flight

0. Read `.wiki-config.json` if it exists at the project root. Resolve `{SOURCES}` and `{WIKI}` per the **Path Resolution** rules in SKILL.md. If no config, use `sources/` and `wiki/` relative to project root. Always double-quote paths containing spaces in Bash commands.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{WIKI}/index.md` to understand existing wiki content
3. Read `{WIKI}/log.md` (last 5-10 entries) to understand recent activity
4. **Resolve the source** — determine the input type and get readable content:

### 4a. Local file
If the argument is a file path (not a URL), resolve it relative to `{SOURCES}` (e.g., `sources/article.md` → `{SOURCES}/article.md`). If it's an absolute path, use it directly. Read the file. If it doesn't exist, list available files in `{SOURCES}/`.

### 4b. PDF URL
If the argument is a URL ending in `.pdf` (or pointing to a known PDF host like `arxiv.org/pdf/`):
1. Download with curl: `curl -sL "{{url}}" -o "{SOURCES}/{{kebab-case-name}}.pdf"`
2. Extract text with pdftotext: `pdftotext "{SOURCES}/{{kebab-case-name}}.pdf" "{SOURCES}/{{kebab-case-name}}.md"` (requires poppler — if `pdftotext` is not found, tell the user to install it: `brew install poppler`)
3. Add a metadata header to the `.md` file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
4. Read the extracted markdown file
5. Both the PDF and extracted `.md` are kept in `{SOURCES}/` as the permanent raw source

### 4c. Plain-text URL (.md, .txt, .rst, etc.)
If the URL points directly to a plain-text or markdown file (e.g., raw GitHub URLs, `.txt`, `.md`, `.rst`, `.org`):
1. Download directly: `curl -sL "{{url}}" -o "{SOURCES}/{{kebab-case-name}}.md"`
2. Add a metadata header to the top of the file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
3. Read the file and proceed with ingestion — no conversion needed

Detect by file extension in the URL, or by `Content-Type` header if ambiguous. Common cases: `raw.githubusercontent.com/.../*.md`, URLs ending in `.txt`, `.md`, `.rst`.

### 4d. Web page URL (HTML)
If the argument is a URL to a regular web page (HTML), follow the same download-then-convert pattern as PDFs:
1. Download the raw HTML: `curl -sL "{{url}}" -o "{SOURCES}/{{kebab-case-name}}.html"`
2. Convert to markdown using one of these methods (in preference order):
   - `pandoc -f html -t markdown -o "{SOURCES}/{{kebab-case-name}}.md" "{SOURCES}/{{kebab-case-name}}.html"` (if pandoc is available — if not, suggest `brew install pandoc`)
   - Python text extraction via Bash: strip `<script>`, `<style>`, `<svg>` tags, convert headers/lists to markdown, remove remaining HTML tags, decode entities
3. Add a metadata header to the `.md` file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
4. Both the `.html` and extracted `.md` are kept in `{SOURCES}/` as permanent raw sources
5. Read the extracted `.md` file and proceed with ingestion

**Tip**: For best quality, use [Obsidian Web Clipper](https://obsidian.md/clipper) to save articles as clean markdown first, then ingest the local file. Direct URL fetching is convenient but may include navigation cruft or miss dynamic content.

### 4e. Unsupported format
If the URL points to a format that can't be processed (e.g., video, binary), tell the user and suggest alternatives (transcript, summary article, etc.).

### URL handling summary

| URL type | Download | Convert | Keep in `{SOURCES}/` |
|----------|----------|---------|----------------------|
| PDF | `curl → .pdf` | `pdftotext → .md` | both `.pdf` + `.md` |
| Plain text (.md, .txt) | `curl → .md` | none needed | `.md` only |
| HTML web page | `curl → .html` | `pandoc` or Python → `.md` | both `.html` + `.md` |

## Batch Mode

If the argument is a directory path (e.g., `sources/`) or a glob pattern (e.g., `sources/*.md`), switch to batch mode:

1. **List files**: Glob the path to find all matching source files. Show the list to the user and confirm before proceeding.
2. **For each source**: Run Steps 0.5 through 5 (Assess Size → Analyze → Create source summary → Create/update entity pages → Create/update concept pages), but **skip Step 2** (Discuss with User) — auto-proceed without per-source confirmation.
3. **Cross-reference pass**: Run Step 6 (Cross-Reference Pass) **once at the end** covering ALL new/updated pages, rather than per-source. This is more efficient and catches cross-source links.
4. **Update index**: Run Step 7 once at the end, adding all new pages.
5. **Single log entry**: Append one combined entry to `wiki/log.md`:
   ```markdown
   ## [{{today}}] ingest | Batch: {{N}} sources

   Batch ingested {{N}} sources: `source1.md`, `source2.md`, ... Pages created: [[list]]. Pages updated: [[list]].
   ```
6. **Report**: Summarize all pages created/updated across all sources.
7. **Git commit**: Offer a single commit at the end covering all changes.

Batch mode trades per-source human oversight for throughput. Recommend it for ingesting a backlog; recommend single-source mode for careful, guided ingestion.

## Step 0.5: Assess Source Size

Check the source file size (line count via `wc -l`). If the source exceeds ~2000 lines:

1. **Read in priority order**: title/abstract/introduction first, then results/discussion/conclusion, then methods, then appendix
2. **Skip low-value sections**: author contributions, acknowledgements, dataset generation details, supplementary tables, full reference lists
3. **Focus extraction on**: claims, findings, entities, concepts, and notable quotes — not exhaustive methodological detail
4. If the source is very long (5000+ lines), tell the user the size and confirm which sections to prioritize before reading everything

## Step 1: Analyze the Source

If the source is too large to read in one pass (the Read tool returns a size error or truncated output), read it in sections: first ~500 lines (intro/abstract), then scan for section headings (Grep for `^#` patterns) to identify key parts, then read those parts selectively. You do not need to read every line of a long document — focus on extractable knowledge.

Identify:

- **Key entities**: people, organizations, products, places, events mentioned
- **Key concepts**: ideas, theories, techniques, patterns, methodologies discussed
- **Key claims**: factual assertions, data points, statistics, conclusions
- **Relationships**: how entities and concepts relate to each other
- **Notable quotes**: important or quotable passages (with attribution)

### Image handling

If the source contains image references (e.g., `![alt](path)` or `<img>` tags):
1. List the image references found and note what they appear to depict (from alt text or context)
2. If images are local files in `{SOURCES}/assets/` or elsewhere on disk, offer to read important ones via the Read tool (which can view images) to extract additional context
3. Note any image-derived insights in the source summary under a "Figures" subsection
4. If images are remote URLs that no longer resolve, note them as broken references

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
status: complete
importance: {{high if foundational/seminal/widely-cited, medium for typical sources, low for minor/supplementary}}
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

**If the entity page doesn't exist**, create it if ANY of:
- Mentioned substantively in this source (not just in passing)
- Already exists as a tag on existing wiki pages (promote tag → page per SKILL.md Tag Policy)
- Mentioned by name on 1+ existing wiki pages without being linked

Default to a `status: draft` page when uncertain — drafts can be enriched on future ingests and are still queryable and linkable. Better a draft page than an inert tag.

When creating:
- Create `wiki/entities/{{kebab-case-name}}.md` with full frontmatter
- Set `status: draft` if created from limited info in a single source; `status: complete` if substantial
- Set `importance: high` for major entities (key researchers, foundational models), `medium` default, `low` for minor mentions
- Write a description based on what this source says about the entity
- Link to the source summary page and any related entity/concept pages

## Step 5: Create or Update Concept Pages

Same logic as entities, but in `wiki/concepts/`:

**If exists**: integrate new information, update sources, add cross-references

**If the concept page doesn't exist**, create it if ANY of:
- Mentioned substantively in this source (not just in passing)
- Already exists as a tag on existing wiki pages (promote tag → page per SKILL.md Tag Policy)
- Mentioned by name on 1+ existing wiki pages without being linked

Default to a `status: draft` page when uncertain. Set `importance` based on centrality to the wiki's domain.

Concept pages should explain:
- What the concept is
- Why it matters
- How it relates to other concepts in the wiki
- What different sources say about it (synthesis, not just repetition)

## Step 5.5: Tag Selection

Apply the Tag Policy from SKILL.md to every page you created or updated.

1. List the candidate tags you considered.
2. For each candidate, run the three tests from SKILL.md:
   - Existing page → DROP, link instead.
   - Page-worthy concept → DROP, CREATE the page (re-enter Step 4 or 5), link it from the body.
   - Purely organizational → KEEP.
3. Cap at 3 tags per page. If you have more candidates than that, the surplus are almost certainly page-worthy.

This step is mandatory — do not skip it even in batch mode.

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
