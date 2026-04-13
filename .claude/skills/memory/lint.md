# Memory Lint Operation

You are performing a health check on the memory store. Scan all pages and report issues.

## Pre-flight

0. Read `.memory-config.json` if it exists at the project root. Resolve `{MEMORY}` per the **Path Resolution** rules in SKILL.md. If no config, use `memory/` relative to project root. Always double-quote paths containing spaces in Bash commands. Note the `stale_days` and `access_count_prune_threshold` settings.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{MEMORY}/index.md`
3. Glob all markdown files in `{MEMORY}/**/*.md`

## Checks to Perform

### 1. Broken Wikilinks (Error)

For every `[[wikilink]]` found in memory pages:
- Resolve the link to a file: search for `{{link-name}}.md` anywhere under `memory/`
- If no matching file exists, report as a broken link

**How to scan**: Use Grep to find all `\[\[.*?\]\]` patterns across `memory/**/*.md`. For each unique link target, use Glob to check if the file exists.

### 2. Orphan Pages (Warning)

Pages with no inbound `[[wikilinks]]` from other pages. Exclude these from orphan detection:
- `memory/index.md`
- `memory/log.md`
- `memory/overview.md`

**How to scan**: For each memory page, Grep all other memory pages for `[[page-name]]`. If no other page links to it, it's an orphan.

### 3. Missing Pages (Suggestion)

Actors or schemas mentioned prominently in memory pages that don't have their own page yet. Look for:
- Repeated mentions of the same term across multiple pages without a corresponding `[[wikilink]]`
- `[[wikilinks]]` that point to non-existent pages (overlaps with broken links, but the suggestion here is to CREATE the page rather than fix the link)

### 4. Index Consistency (Error)

- Pages that exist in `memory/` subdirectories but are missing from `memory/index.md`
- Entries in `memory/index.md` that point to pages that don't exist
- Pages filed in the wrong category (e.g., an actor page listed under Schemas)

### 5. Frontmatter Validation (Warning)

For each memory page (excluding index.md and log.md), check:
- `title` field exists and is non-empty
- `type` field exists and is one of: episode, actor, schema, evaluation, reflection, overview
- `created` field exists and is a valid date
- `updated` field exists and is a valid date
- `sources` field exists (can be empty list for overview)
- `status` field exists and is one of: draft, active, consolidated, archived
- `importance` field exists and is one of: high, medium, low
- `confidence` field exists and is one of: high, medium, low, uncertain
- `last_accessed` field exists and is a valid date
- `access_count` field exists and is a non-negative integer
- `memory_type` field exists and is one of: episodic, semantic, procedural
- `validity_window` field exists and is either `permanent` or a valid date

### 6. Stale Content (Suggestion)

- Pages whose `updated` date is significantly older than the most recent record in `memory/log.md`, AND whose topic has been touched by newer episodes
- Episode pages that reference input files no longer in `inputs/`

### 6b. Unresolved Contradictions (Warning)

Scan all memory pages for `> [!warning] Contradiction` callouts. Report each one with:
- The page containing the contradiction
- A brief summary of the two conflicting claims
- Suggest resolution: which source is more recent, more corroborated, or more authoritative?

**How to scan**: Grep all `{MEMORY}/**/*.md` for the pattern `\[!warning\] Contradiction`.

### 7. Cross-Reference Gaps (Suggestion)

- Actor/schema pages that mention other actors/schemas by name without using `[[wikilinks]]`
- Pages that discuss related topics but don't link to each other

**How to scan**: For each actor and schema page name, Grep all other memory pages for that name (case-insensitive). Flag mentions that aren't wrapped in `[[...]]`.

### 8. Knowledge Gaps (Suggestion)

Identify areas where the memory store's coverage is thin:
- **Draft pages**: Pages with `status: draft` that have minimal content. Suggest what inputs could enrich them.
- **Single-source schemas**: Schema pages whose `sources` list has only one entry. Suggest recording more episodes for corroboration.
- **Mentioned but unexplored**: Topics that appear across multiple pages but have no dedicated page AND no episode directly covering them.

### 9. Stale Memories (Warning)

Pages where:
- `last_accessed` is more than `stale_days` days ago (default 30), AND
- `access_count` is below `access_count_prune_threshold` (default 2)

These are memories the agent recorded but never uses. Suggest archival or consolidation.

**How to scan**: Read frontmatter of all memory pages. Compare `last_accessed` against today's date. Check `access_count`.

### 10. Expired Validity (Error)

Pages where `validity_window` is a specific date that is in the past. These contain time-bound information that is no longer current.

**How to scan**: Read frontmatter of all memory pages. If `validity_window` is a date (not `permanent`), compare against today's date.

Suggest: update the page with current information, or archive it.

### 11. Low-Confidence Active Pages (Warning)

Pages with `status: active` but `confidence: low` or `confidence: uncertain`. These are being treated as reliable knowledge but lack corroboration.

Suggest: find more evidence (record more episodes), or downgrade `status` to `draft` until corroborated.

### 12. Unconsolidated Clusters (Suggestion)

Groups of 3+ episode pages that share similar tags and actors but haven't been consolidated into a schema. This nudges toward consolidation.

**How to scan**: Read tags and actor references from all episode pages with `status: active`. Group by tag overlap (2+ shared tags) and actor overlap (same actors involved). If a cluster of 3+ episodes exists without a common schema page linking them, suggest consolidation.

Suggest: run `/memory consolidate {{topic}}` for the identified cluster.

## Report Format

Group findings by severity:

```markdown
## Lint Report — {{today}}

### Errors (must fix)
- [ ] Broken link: `[[nonexistent-page]]` in memory/schemas/foo.md:15
- [ ] Index missing: memory/actors/bar.md not in index.md
- [ ] Expired validity: memory/schemas/api-v2-auth.md — validity_window 2026-03-01 has passed

### Warnings (should fix)
- [ ] Orphan page: memory/actors/baz.md (no inbound links)
- [ ] Missing frontmatter: memory/episodes/qux.md missing `confidence` field
- [ ] Stale memory: memory/episodes/old-task.md — last accessed 45 days ago, access_count: 0
- [ ] Low-confidence active: memory/schemas/retry-strategy.md — active but confidence: uncertain
- [ ] Unresolved contradiction: memory/actors/some-api.md — rate limit 100/min vs 60/min

### Suggestions (nice to have)
- [ ] Missing page: "deployment pipeline" mentioned in 3 pages but has no memory page
- [ ] Cross-ref gap: memory/actors/alice.md mentions "Bob" without [[wikilink]]
- [ ] Single source: [[retry-strategy]] could use more episodes — record more retry experiences
- [ ] Unconsolidated cluster: 4 episodes tagged "api-timeout" + actor [[external-api]] — run `/memory consolidate api-timeout`

### Health Summary

| Metric | Count |
|--------|-------|
| Total memory pages | {{N}} (excl. index, log, overview) |
| Episodes | {{N}} (active: {{N}}, consolidated: {{N}}, archived: {{N}}) |
| Actors | {{N}} |
| Schemas | {{N}} |
| Evaluations | {{N}} |
| Reflections | {{N}} |
| High confidence | {{N}} |
| Low/uncertain confidence | {{N}} |
| Avg access count | {{N}} |
```

## Auto-Fix

After presenting the report, ask the user:

> "Would you like me to auto-fix any of these? I can:
> 1. Fix all errors (broken links, index sync, expired validity archival)
> 2. Fix errors + warnings (add missing frontmatter, link orphans, archive stale memories)
> 3. Fix everything including suggestions (create missing pages, add cross-references, consolidate clusters)
> 4. Let me pick specific items"

For auto-fix:
- **Broken links**: If the target page clearly should exist, create a stub page. If it's a typo, fix the link.
- **Index sync**: Add missing pages to the index with a generated one-line description.
- **Orphan pages**: Add links from the most relevant related pages.
- **Missing frontmatter**: Generate reasonable defaults based on file location and content.
- **Expired validity**: Set `status: archived` on expired pages.
- **Stale memories**: Set `status: archived` on stale, low-access pages.
- **Missing pages**: Create stub pages with basic content derived from how the topic is discussed in existing pages.
- **Cross-ref gaps**: Add `[[wikilinks]]` around unlinked mentions.
- **Unconsolidated clusters**: Run the consolidate operation for each identified cluster.

## Log

After lint completes, append to `memory/log.md`:

```markdown
## [{{today}}] lint | Memory health check

Found: {{N}} errors, {{N}} warnings, {{N}} suggestions. {{Auto-fixed X items | No auto-fix applied.}}
```
