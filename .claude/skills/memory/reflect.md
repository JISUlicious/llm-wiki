# Memory Reflect Operation

You are generating meta-observations by synthesizing across the memory store. Unlike `query` (which answers a specific question), `reflect` is open-ended: "what patterns do I notice? what have I learned? what am I uncertain about?"

The argument is an optional topic or `--global`:
- `/memory reflect api-reliability` — focus on a specific topic
- `/memory reflect --global` — reflect across the entire memory store
- `/memory reflect` (no argument) — same as `--global`

## Pre-flight

0. Read `.memory-config.json` if it exists at the project root. Resolve `{MEMORY}` per the **Path Resolution** rules in SKILL.md. If no config, use `memory/` relative to project root. Always double-quote paths containing spaces in Bash commands. Note the `mode` setting.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{MEMORY}/index.md` to understand the full scope of the memory store
3. Read `{MEMORY}/overview.md` for the current high-level synthesis

## Step 1: Scope the Reflection

### Topic-focused reflection:
1. Search for pages matching the topic — Grep across all `{MEMORY}/` subdirectories
2. Read all matching episodes, schemas, actors, and evaluations
3. Also read any reflections previously filed on this or related topics

### Global reflection (`--global` or no argument):
1. Read `{MEMORY}/log.md` (last 20-30 entries) to understand recent activity trajectory
2. Read all schema pages (these are the distilled knowledge — most informative for global reflection)
3. Sample high-importance and high-access-count pages across all categories
4. Read any existing reflection pages to avoid repeating prior observations

### Access Tracking (Side-Effect)

**For every page you read during reflection**, update its frontmatter:
- Set `last_accessed` to today's date
- Increment `access_count` by 1

## Step 2: Pattern Detection

Analyze the pages you've read. Look for:

### Recurring Successes
- What strategies or approaches have worked consistently across episodes?
- Are there schemas with `confidence: high` that represent well-established knowledge?
- What actors/tools have been reliably effective?

### Recurring Failures
- What failure modes keep appearing?
- Are there schemas that episodes frequently contradict?
- What approaches have been tried and abandoned?

### Unstable Knowledge
- Schemas that have been updated frequently (many episodes, changing conclusions)
- Pages with `confidence: uncertain` or unresolved contradictions
- Actor pages where behavior seems to have changed over time

### Knowledge Gaps
- Areas with many episodes but no schemas (unprocessed experience — needs consolidation)
- Topics mentioned across multiple pages but never given their own page
- Schemas with `confidence: low` that lack corroboration
- Actors the agent interacts with often but knows little about

### Strengths
- Areas with high-confidence, frequently-accessed schemas (well-understood domains)
- Topics where episodes consistently confirm existing schemas
- Well-connected areas of the memory graph (lots of cross-references)

### Temporal Patterns
- Has the agent's knowledge shifted over time? (early episodes say X, later ones say Y)
- Are there seasonal or cyclical patterns?
- Is the rate of new learning accelerating or plateauing?

## Step 3: Generate Reflection Page

Create `memory/reflections/{{kebab-case-topic-or-date}}.md`:

For topic-focused: `memory/reflections/reflection-{{topic}}-{{today}}.md`
For global: `memory/reflections/reflection-global-{{today}}.md`

```markdown
---
title: "{{Reflection Title}}"
type: reflection
created: {{today}}
updated: {{today}}
sources: []
tags:
  - reflection
  - {{topic tags if topic-focused}}
status: active
importance: {{high for global reflections, medium for topic-focused}}
confidence: medium
last_accessed: {{today}}
access_count: 0
memory_type: semantic
validity_window: permanent
supersedes: []
---

# {{Reflection Title}}

_Reflection generated on {{today}}. Scope: {{topic or "global"}}._

## Patterns Observed

{{What recurs across the memory store? What themes emerge?}}

- **Pattern 1**: {{description with [[wikilinks]] to supporting pages}}
- **Pattern 2**: {{description}}

## Strengths

{{What does the agent know well? Where is confidence high?}}

- {{Well-understood area with [[wikilinks]]}}

## Uncertainties

{{What is the agent not sure about? Where are contradictions or low confidence?}}

- {{Uncertain area — why, and what would resolve it}}

## Knowledge Gaps

{{What should the agent learn more about? What's missing?}}

- {{Gap — what inputs would fill it}}

## Recommendations

{{Concrete next steps the agent or user should take}}

- [ ] Record more episodes about {{topic}} to strengthen [[schema-name]]
- [ ] Run `/memory consolidate {{topic}}` — {{N}} episodes ready for consolidation
- [ ] Archive [[stale-page]] — not accessed in {{N}} days, low relevance
- [ ] Investigate contradiction in [[page-name]] — {{brief description}}
- [ ] Create missing page for "{{topic}}" — mentioned in {{N}} pages

## Memory Store Health

| Metric | Value |
|--------|-------|
| Pages consulted | {{N}} |
| Active schemas | {{N}} |
| High-confidence schemas | {{N}} |
| Unconsolidated episode clusters | {{N}} |
| Unresolved contradictions | {{N}} |
| Stale pages (>{{stale_days}} days) | {{N}} |
```

## Step 4: Update Overview (if warranted)

For **global reflections**, or topic reflections that reveal significant new patterns:

1. Read `memory/overview.md`
2. If the reflection reveals patterns not captured in the overview, update it:
   - Add new themes to "Key Patterns"
   - Update "Open Questions" based on identified gaps
   - Revise the Summary if the big picture has shifted
3. Update the `updated` date on overview.md

For minor topic-focused reflections, skip this step.

## Step 5: Update Index and Log

1. Add the reflection to `memory/index.md` under Reflections
2. Prepend to `memory/log.md`:

```markdown
## [{{today}}] reflect | {{Topic or "Global reflection"}}

Generated reflection: [[reflection-page-name]]. Key findings: {{1-2 sentences summarizing the most important observations}}. Pages consulted: {{N}}. Recommendations: {{N}} action items.
```

## Step 6: Report

Tell the user:
- Reflection page created (with link)
- Top 3 most important findings
- Specific actionable recommendations
- Whether the overview was updated
- Suggested next operations:
  - `/memory consolidate {{topic}}` if clusters were identified
  - `/memory record {{suggested-input}}` if knowledge gaps were found
  - `/memory lint` if structural issues were noticed
  - `/memory query {{question}}` for follow-up questions raised by the reflection
