# Memory Record Operation

You are recording an experience into the agent's memory store. The argument can be a local file path (e.g., `inputs/conversation.md`), a URL (PDF, plain-text, or web page), or a directory/glob for batch recording (e.g., `inputs/` or `inputs/*.md`).

## Pre-flight

0. Read `.memory-config.json` if it exists at the project root. Resolve `{INPUTS}` and `{MEMORY}` per the **Path Resolution** rules in SKILL.md. If no config, use `inputs/` and `memory/` relative to project root. Always double-quote paths containing spaces in Bash commands. Note the `mode` setting (`manual` or `auto`).
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{MEMORY}/index.md` to understand existing memory content
3. Read `{MEMORY}/log.md` (last 5-10 entries) to understand recent activity
4. **Resolve the input** — determine the input type and get readable content:

### 4a. Local file
If the argument is a file path (not a URL), resolve it relative to `{INPUTS}` (e.g., `inputs/conversation.md` -> `{INPUTS}/conversation.md`). If it's an absolute path, use it directly. Read the file. If it doesn't exist, list available files in `{INPUTS}/`.

### 4b. PDF URL
If the argument is a URL ending in `.pdf` (or pointing to a known PDF host like `arxiv.org/pdf/`):
1. Download with curl: `curl -sL "{{url}}" -o "{INPUTS}/{{kebab-case-name}}.pdf"`
2. Extract text with pdftotext: `pdftotext "{INPUTS}/{{kebab-case-name}}.pdf" "{INPUTS}/{{kebab-case-name}}.md"` (requires poppler — if `pdftotext` is not found, tell the user to install it: `brew install poppler`)
3. Add a metadata header to the `.md` file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
4. Read the extracted markdown file
5. Both the PDF and extracted `.md` are kept in `{INPUTS}/` as the permanent raw input

### 4c. Plain-text URL (.md, .txt, .rst, etc.)
If the URL points directly to a plain-text or markdown file (e.g., raw GitHub URLs, `.txt`, `.md`, `.rst`, `.org`):
1. Download directly: `curl -sL "{{url}}" -o "{INPUTS}/{{kebab-case-name}}.md"`
2. Add a metadata header to the top of the file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
3. Read the file and proceed — no conversion needed

### 4d. Web page URL (HTML)
If the argument is a URL to a regular web page (HTML):
1. Download the raw HTML: `curl -sL "{{url}}" -o "{INPUTS}/{{kebab-case-name}}.html"`
2. Convert to markdown using one of these methods (in preference order):
   - `pandoc -f html -t markdown -o "{INPUTS}/{{kebab-case-name}}.md" "{INPUTS}/{{kebab-case-name}}.html"` (if pandoc is available — if not, suggest `brew install pandoc`)
   - Python text extraction via Bash: strip `<script>`, `<style>`, `<svg>` tags, convert headers/lists to markdown, remove remaining HTML tags, decode entities
3. Add a metadata header to the `.md` file: `<!-- Source URL: {{url}} | Fetched: {{today}} -->`
4. Both the `.html` and extracted `.md` are kept in `{INPUTS}/`
5. Read the extracted `.md` file and proceed

### 4e. Unsupported format
If the URL points to a format that can't be processed (e.g., video, binary), tell the user and suggest alternatives (transcript, summary, etc.).

### URL handling summary

| URL type | Download | Convert | Keep in `{INPUTS}/` |
|----------|----------|---------|----------------------|
| PDF | `curl -> .pdf` | `pdftotext -> .md` | both `.pdf` + `.md` |
| Plain text (.md, .txt) | `curl -> .md` | none needed | `.md` only |
| HTML web page | `curl -> .html` | `pandoc` or Python -> `.md` | both `.html` + `.md` |

## Batch Mode

If the argument is a directory path (e.g., `inputs/`) or a glob pattern (e.g., `inputs/*.md`), switch to batch mode:

1. **List files**: Glob the path to find all matching input files. Show the list to the user and confirm before proceeding (skip confirmation in `auto` mode).
2. **For each input**: Run Steps 0.5 through 5 (Assess Size -> Analyze -> Create episode -> Create/update actor pages -> Create/update schema pages -> Confidence assessment), but **skip Step 2** (Discuss with User).
3. **Cross-reference pass**: Run Step 6 **once at the end** covering ALL new/updated pages.
4. **Update index**: Run Step 7 once at the end, adding all new pages.
5. **Single log entry**: Append one combined entry to `memory/log.md`:
   ```markdown
   ## [{{today}}] record | Batch: {{N}} inputs

   Batch recorded {{N}} inputs: `input1.md`, `input2.md`, ... Pages created: [[list]]. Pages updated: [[list]].
   ```
6. **Report**: Summarize all pages created/updated across all inputs.
7. **Git commit**: Offer a single commit at the end covering all changes.

## Step 0.5: Assess Input Size

Check the input file size (line count via `wc -l`). If the input exceeds ~2000 lines:

1. **Read in priority order**: beginning/introduction first, then key events/decisions, then context/background
2. **Skip low-value sections**: boilerplate, auto-generated headers, repetitive log entries, full stack traces (summarize instead)
3. **Focus extraction on**: events, decisions, outcomes, actors involved, strategies used, and lessons learned
4. If the input is very long (5000+ lines), tell the user the size and confirm which sections to prioritize before reading everything

## Step 1: Analyze the Input

If the input is too large to read in one pass, read it in sections: first ~500 lines, then scan for section headings or timestamps to identify key parts, then read those parts selectively.

Identify:

- **Key actors**: agents, tools, users, systems, APIs involved
- **Key schemas**: strategies, patterns, procedures, heuristics discussed or demonstrated
- **Key events**: what happened, in what order, what triggered what
- **Outcome**: success, failure, partial — and why
- **Decisions**: choices made and their rationale
- **Lessons**: what worked, what didn't, what to do differently next time

### Image handling

If the input contains image references (e.g., `![alt](path)` or `<img>` tags):
1. List the image references found and note what they appear to depict (from alt text or context)
2. If images are local files in `{INPUTS}/assets/` or elsewhere on disk, offer to read important ones via the Read tool to extract additional context
3. Note any image-derived insights in the episode summary under a "Figures" subsection

## Step 2: Discuss with User

**Skip this step entirely if `mode` is `auto` in `.memory-config.json`.**

Before writing anything, share a brief summary of what you found:
- 3-5 key takeaways from the input
- Which existing memory pages will be updated (if any)
- Which new pages you plan to create
- Any contradictions with existing memory content

Ask the user if they want to adjust emphasis or skip anything. Wait for confirmation before proceeding.

## Step 3: Create Episode Page

Create `memory/episodes/{{kebab-case-title}}.md`:

```markdown
---
title: "{{Episode Title}}"
type: episode
created: {{today}}
updated: {{today}}
sources:
  - {{original-filename}}
tags:
  - {{relevant tags}}
status: active
importance: {{high if critical event/decision, medium for typical, low for routine}}
confidence: high
last_accessed: {{today}}
access_count: 0
memory_type: episodic
validity_window: permanent
supersedes: []
---

# {{Episode Title}}

**Input**: `inputs/{{original-filename}}`
**Date of event**: {{if known, otherwise today}}
**Actors involved**: [[actor1]], [[actor2]]

## What Happened

{{Narrative account of the experience: what triggered it, what occurred, in what sequence}}

## Outcome

{{Success | Failure | Partial — with explanation}}

## Key Decisions

- {{Decision made and its rationale}}

## Lessons

- {{What worked, what didn't, what to do differently}}

## Actors Mentioned

- [[actor-name]] — {{role in this episode}}

## Schemas Relevant

- [[schema-name]] — {{how it applied or was discovered in this episode}}

## References

_Original input: `inputs/{{filename}}`_
```

## Step 4: Create or Update Actor Pages

For each significant actor identified:

**If the actor page already exists** (`memory/actors/{{name}}.md`):
- Read the existing page
- Add new information from this episode as a new section or integrate into existing sections
- Add the input to the frontmatter `sources` list
- Update the `updated` date
- Add any new `[[wikilinks]]` discovered
- If new info contradicts existing content, add a `> [!warning] Contradiction` callout and lower `confidence`

**If the actor page doesn't exist** and the actor is significant enough (mentioned substantively, not just in passing):
- Create `memory/actors/{{kebab-case-name}}.md` with full frontmatter
- Set `status: draft` if created from limited info in a single episode; `status: active` if substantial
- Set `importance` based on how central this actor is to the agent's domain
- Set `confidence: low` if single episode, `medium` if corroborated
- Set `memory_type: semantic`
- Write a description based on what this episode reveals about the actor
- Link to the episode page and any related actor/schema pages

## Step 5: Create or Update Schema Pages

Same logic as actors, but in `memory/schemas/`:

**If exists**: integrate new information, update sources, add cross-references
**If new and significant**: create `memory/schemas/{{kebab-case-name}}.md`.
- Set `status: draft` if derived from limited observation in one episode; `status: active` if the pattern is clear
- Set `confidence` based on corroboration (single episode = `low`, confirmed by multiple = `medium` or `high`)
- Set `memory_type: procedural` if it's a how-to strategy/procedure, `semantic` if it's factual knowledge about how something works

Schema pages should explain:
- What the pattern/strategy/heuristic is
- When to apply it (triggers, conditions)
- How to execute it (steps, if procedural)
- Why it works (rationale, evidence from episodes)
- Known limitations or failure modes

## Step 5.5: Confidence Assessment

After recording, assess the impact of this episode on existing memory:

1. **Corroboration check**: For each schema page touched or referenced by this episode, check if the episode confirms or contradicts the schema.
   - **Confirms**: If the schema's `confidence` is `low`, consider bumping to `medium`. If `medium` and now corroborated by 3+ episodes, consider `high`.
   - **Contradicts**: Add a `> [!warning] Contradiction` callout to the schema page. Lower `confidence` by one level (e.g., `high` -> `medium`). Note the specific conflicting claims.

2. **Staleness check**: If this episode reveals that an existing actor or schema page has outdated information, update it and set `validity_window` if the information is now time-bound.

## Step 6: Cross-Reference Pass

This is critical. After creating/updating pages:

1. **Forward links**: Scan every page you created or updated. Anywhere another memory page is mentioned by name, add a `[[wikilink]]` if not already present.

2. **Backlinks**: Scan OTHER existing memory pages (use Grep to find mentions of new actor/schema names). Add `[[wikilinks]]` in those pages pointing to the new pages you created.

3. **Episode links**: Ensure the episode page links to all actor and schema pages it references.

4. **Overview check**: Read `memory/overview.md`. If this episode significantly changes the big picture (new major pattern, shifts understanding, introduces important new area), update the overview.

## Step 7: Update Index

Read `memory/index.md` and add entries for every new page created. Update descriptions for any existing pages that were significantly modified.

Each entry format: `- [[page-name]] — One-line description`

Place entries under the correct category header (Actors, Schemas, Episodes, Evaluations, Reflections).

## Step 8: Update Log

Prepend a new entry to `memory/log.md` (after the header, before existing entries):

```markdown
## [{{today}}] record | {{Episode Title}}

Recorded `inputs/{{filename}}`. Pages created: [[list]]. Pages updated: [[list]]. Key takeaways: {{1-2 sentences}}.
```

## Step 9: Report

Tell the user:
- Pages created (with links)
- Pages updated (with what changed)
- Confidence changes (any schemas confirmed or contradicted)
- Any contradictions found
- Suggested follow-up: related experiences to record, patterns to consolidate, questions to explore
- If `auto_consolidate_threshold` is reached for any tag cluster, suggest running `/memory consolidate`
