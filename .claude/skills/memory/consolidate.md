# Memory Consolidate Operation

You are consolidating related episodes into reusable schema pages. This is the episodic-to-semantic memory transition — extracting general patterns from specific experiences.

The argument is an optional topic (e.g., `/memory consolidate api-timeouts`). If no topic is given, scan for consolidation candidates automatically.

## Pre-flight

0. Read `.memory-config.json` if it exists at the project root. Resolve `{MEMORY}` per the **Path Resolution** rules in SKILL.md. If no config, use `memory/` relative to project root. Always double-quote paths containing spaces in Bash commands. Note the `mode` and `auto_consolidate_threshold` settings.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{MEMORY}/index.md` to understand existing memory content
3. Read `{MEMORY}/log.md` (last 5-10 entries) to understand recent activity

## Step 1: Identify Consolidation Candidates

### If a topic is given:
1. Search for episode and schema pages matching the topic — use Grep across `{MEMORY}/episodes/` and `{MEMORY}/schemas/` for the topic keywords
2. Also search by tags: read frontmatter of episode pages and find those with matching tags
3. Collect all matching episodes with `status: active` (skip `consolidated` and `archived`)

### If no topic is given:
1. Read frontmatter (tags, sources, status) from all episode pages with `status: active`
2. Group episodes by tag overlap (2+ shared tags) and actor overlap (same `[[actor]]` links)
3. Identify clusters of 3+ episodes that share a common theme but have no existing schema page that links them all
4. Present the candidate clusters to the user and ask which to consolidate (skip prompt in `auto` mode — consolidate the largest cluster)

If no candidates are found, report "No consolidation candidates found" and suggest recording more episodes.

## Step 2: Read the Cluster

For each episode in the consolidation cluster:
1. Read the full episode page
2. Note: What Happened, Outcome, Key Decisions, Lessons sections
3. Track which actors and schemas are referenced

Also read any existing schema pages that the episodes link to — the consolidation might update an existing schema rather than create a new one.

## Step 3: Synthesize

Extract from the episode cluster:

- **Common patterns**: What recurs across episodes? What triggers appear repeatedly?
- **Effective strategies**: What approaches worked? Under what conditions?
- **Failure modes**: What went wrong? Are there recurring failure patterns?
- **General rules**: What principles can be extracted that would apply to future similar situations?
- **Conditions and exceptions**: When does the pattern apply? When does it break down?

Distinguish between:
- **Procedural knowledge** (how to do something — steps, sequence, tools): set `memory_type: procedural`
- **Semantic knowledge** (facts about how something works — properties, relationships): set `memory_type: semantic`

## Step 4: Create or Update Schema Page

### If no existing schema covers this topic:

Create `memory/schemas/{{kebab-case-topic}}.md`:

```markdown
---
title: "{{Schema Title}}"
type: schema
created: {{today}}
updated: {{today}}
sources:
  - {{list of input files from all source episodes}}
tags:
  - {{relevant tags}}
status: active
importance: {{high if widely applicable, medium default, low if narrow}}
confidence: {{derived from episode count and consistency — see below}}
last_accessed: {{today}}
access_count: 0
memory_type: {{procedural | semantic}}
validity_window: permanent
supersedes: []
---

# {{Schema Title}}

{{One-paragraph summary of the pattern/strategy/heuristic}}

## When to Apply

- {{Trigger conditions — when should the agent use this schema?}}
- {{Context requirements — what needs to be true?}}

## How It Works

{{For procedural schemas: step-by-step procedure}}
{{For semantic schemas: explanation of the pattern/mechanism}}

## Evidence

| Episode | Outcome | Key Observation |
|---------|---------|-----------------|
| [[episode-1]] | Success | {{what confirmed the pattern}} |
| [[episode-2]] | Failure | {{what went wrong}} |
| [[episode-3]] | Success | {{additional confirmation}} |

## Known Limitations

- {{When this pattern doesn't apply}}
- {{Failure modes observed}}
- {{Edge cases}}

## Derived From

This schema was consolidated from {{N}} episodes on {{today}}:
{{list of episode wikilinks}}

## References

- [[episode-1]]
- [[episode-2]]
- [[episode-3]]
```

### If an existing schema covers this topic:

1. Read the existing schema page
2. Integrate new evidence from the additional episodes
3. Update the Evidence table
4. Revise the pattern description if the new episodes refine understanding
5. Update `confidence` based on the expanded evidence base
6. Add new episodes to the Derived From section and References
7. Update `updated` date and `sources` list

## Step 5: Confidence Propagation

Derive the schema's confidence from its evidence base:

| Episodes | Consistency | Confidence |
|----------|-------------|------------|
| 5+ episodes | All consistent | `high` |
| 3-4 episodes | Mostly consistent | `medium` |
| 3+ episodes | Mixed outcomes | `low` |
| 1-2 episodes | Any | `low` |
| Any | Contains contradictions | `uncertain` |

If episodes contradict each other, add a `> [!warning] Contradiction` callout to the schema page noting the specific disagreement, and set `confidence: uncertain`.

## Step 6: Mark Episodes as Consolidated

For each source episode:
1. Set `status: consolidated` in the episode's frontmatter
2. Add `superseded_by: {{schema-page-name}}.md` to the episode's frontmatter (add this field if it doesn't exist)
3. Do NOT delete the episode — it remains as an audit trail
4. The episode's content stays intact; only status changes

Consolidated episodes are deprioritized in future queries (status filtering) but remain accessible if needed.

## Step 7: Cross-Reference Pass

1. Ensure the new/updated schema page links to all relevant actors and other schemas
2. Update actor pages that are referenced — add a link to the new schema under a "Related Schemas" or similar section
3. Update other schema pages if the new schema relates to them
4. Check `memory/overview.md` — if this consolidation reveals a significant pattern, update the overview

## Step 8: Update Index and Log

1. Add the new schema to `memory/index.md` under Schemas (or update the description if the schema already existed)
2. Prepend to `memory/log.md`:

```markdown
## [{{today}}] consolidate | {{Schema Title}}

Consolidated {{N}} episodes into [[schema-page-name]]. Episodes consolidated: [[ep1]], [[ep2]], [[ep3]]. Confidence: {{level}}. Key pattern: {{1 sentence summary}}.
```

## Step 9: Report

Tell the user:
- Schema page created or updated (with link)
- Number of episodes consolidated
- Confidence level and why
- Any contradictions found across episodes
- Suggested follow-ups:
  - Other clusters that could be consolidated
  - Low-confidence schemas that need more episodes
  - Related topics worth exploring via `/memory reflect`
