# Wiki Lint Operation

You are performing a health check on the wiki. Scan all pages and report issues.

## Pre-flight

0. Read `.wiki-config.json` if it exists at the project root. Resolve `{WIKI}` per the **Path Resolution** rules in SKILL.md. If no config, use `wiki/` relative to project root. Always double-quote paths containing spaces in Bash commands.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{WIKI}/index.md`
3. Glob all markdown files in `{WIKI}/**/*.md`

## Checks to Perform

### 1. Broken Wikilinks (Error)

For every `[[wikilink]]` found in wiki pages:
- Resolve the link to a file: search for `{{link-name}}.md` anywhere under `wiki/`
- If no matching file exists, report as a broken link

**How to scan**: Use Grep to find all `\[\[.*?\]\]` patterns across `wiki/**/*.md`. For each unique link target, use Glob to check if the file exists.

### 2. Orphan Pages (Warning)

Pages with no inbound `[[wikilinks]]` from other pages. Exclude these from orphan detection:
- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview.md`

**How to scan**: For each wiki page, Grep all other wiki pages for `[[page-name]]`. If no other page links to it, it's an orphan.

### 3. Missing Pages (Suggestion)

Concepts or entities mentioned prominently in wiki pages that don't have their own page yet. Look for:
- Repeated mentions of the same term across multiple pages without a corresponding `[[wikilink]]`
- `[[wikilinks]]` that point to non-existent pages (overlaps with broken links, but the suggestion here is to CREATE the page rather than fix the link)

### 4. Index Consistency (Error)

- Pages that exist in `wiki/` subdirectories but are missing from `wiki/index.md`
- Entries in `wiki/index.md` that point to pages that don't exist
- Pages filed in the wrong category (e.g., an entity page listed under Concepts)

### 5. Frontmatter Validation (Warning)

For each wiki page (excluding index.md and log.md), check:
- `title` field exists and is non-empty
- `type` field exists and is one of: entity, concept, source, comparison, query, overview
- `created` field exists and is a valid date
- `updated` field exists and is a valid date
- `sources` field exists (can be empty list for overview)
- `status` field exists and is one of: draft, complete, needs-update
- `importance` field exists and is one of: high, medium, low

### 6. Stale Content (Suggestion)

- Pages whose `updated` date is significantly older than the most recent ingest in `wiki/log.md`, AND whose topic has been touched by newer sources
- Source summary pages that reference source files no longer in `sources/`

### 6b. Unresolved Contradictions (Warning)

Scan all wiki pages for `> [!warning] Contradiction` callouts. These are added during ingest when new information conflicts with existing content. Report each one with:
- The page containing the contradiction
- A brief summary of the two conflicting claims
- Suggest resolution: which source is more authoritative, more recent, or more widely cited?

**How to scan**: Grep all `{WIKI}/**/*.md` for the pattern `\[!warning\] Contradiction`.

### 7. Cross-Reference Gaps (Suggestion)

- Entity/concept pages that mention other entities/concepts by name without using `[[wikilinks]]`
- Pages that discuss related topics but don't link to each other

**How to scan**: For each entity and concept page name, Grep all other wiki pages for that name (case-insensitive). Flag mentions that aren't wrapped in `[[...]]`.

### 8. Knowledge Gaps (Suggestion)

Identify areas where the wiki's coverage is thin and suggest external sources to look for:

- **Draft pages**: Pages with `status: draft` that have minimal content. Suggest a specific search query to enrich them (e.g., `search "PaLM 2 technical report Google 2023"` to fill out [[palm]]).
- **Single-source concepts**: Concept pages whose `sources` list has only one entry. Suggest finding additional sources for triangulation and broader perspective.
- **Stale topics**: Pages where the most recent source is significantly older than the current date. Suggest searching for recent developments.
- **Mentioned but unexplored**: Topics that appear across multiple pages but have no dedicated page AND no source directly covering them. Suggest a search query.

**How to scan**: Read frontmatter of all wiki pages. For draft pages and single-source pages, generate a concrete search query string the user could paste into Google Scholar, Semantic Scholar, or a search engine.

## Report Format

Group findings by severity:

```markdown
## Lint Report — {{today}}

### Errors (must fix)
- [ ] Broken link: `[[nonexistent-page]]` in wiki/concepts/foo.md:15
- [ ] Index missing: wiki/entities/bar.md not in index.md

### Warnings (should fix)
- [ ] Orphan page: wiki/entities/baz.md (no inbound links)
- [ ] Missing frontmatter: wiki/sources/qux.md missing `type` field

### Suggestions (nice to have)
- [ ] Missing page: "reinforcement learning" mentioned in 3 pages but has no wiki page
- [ ] Cross-ref gap: wiki/entities/alice.md mentions "Bob" without [[wikilink]]
- [ ] Stale content: wiki/concepts/old-topic.md not updated since 2 new sources ingested
- [ ] Knowledge gap: [[palm]] is status:draft with 1 source — search "PaLM 2 technical report Google 2023"
- [ ] Single source: [[some-concept]] could use more perspectives — search "concept name survey 2024"
```

## Auto-Fix

After presenting the report, ask the user:

> "Would you like me to auto-fix any of these? I can:
> 1. Fix all errors (broken links, index sync)
> 2. Fix errors + warnings (add missing frontmatter, link orphans)
> 3. Fix everything including suggestions (create missing pages, add cross-references)
> 4. Let me pick specific items"

For auto-fix:
- **Broken links**: If the target page clearly should exist, create a stub page. If it's a typo, fix the link.
- **Index sync**: Add missing pages to the index with a generated one-line description.
- **Orphan pages**: Add links from the most relevant related pages.
- **Missing frontmatter**: Generate reasonable defaults based on file location and content.
- **Missing pages**: Create stub pages with basic content derived from how the concept is discussed in existing pages.
- **Cross-ref gaps**: Add `[[wikilinks]]` around unlinked mentions.

## Log

After lint completes, append to `wiki/log.md`:

```markdown
## [{{today}}] lint | Wiki health check

Found: {{N}} errors, {{N}} warnings, {{N}} suggestions. {{Auto-fixed X items | No auto-fix applied.}}
```
