# Memory Query Operation

You are recalling information from the agent's memory store. The question is provided as an argument.

## Pre-flight

0. Read `.memory-config.json` if it exists at the project root. Resolve `{MEMORY}` per the **Path Resolution** rules in SKILL.md. If no config, use `memory/` relative to project root. Always double-quote paths containing spaces in Bash commands. Note the `mode` setting.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{MEMORY}/index.md` to understand the full scope of the memory store

## Step 1: Find Relevant Pages

Based on the question and the index, identify which memory pages are likely relevant. Consider:
- Actor pages that match agents/tools/systems mentioned in the question
- Schema pages that match strategies/patterns/procedures in the question
- Episode pages that might have relevant experiential detail
- Evaluation pages if the question involves comparing approaches
- Previous reflection pages if a similar question was explored before

Use Grep to search memory pages for keywords if the index alone isn't sufficient.

### Recency Weighting

When multiple pages are relevant, prefer pages with:
1. More recent `updated` dates
2. Higher `access_count` (frequently useful memories)
3. Higher `confidence` levels
4. `status: active` over `draft`

This is a soft preference — old high-importance pages still surface. But between two equally relevant pages, the more recent and more accessed one wins.

### Status Filtering

By default, **exclude** pages with `status: archived` or `status: consolidated` from results. Only include them if the initial active set is insufficient to answer the question. If you do include consolidated/archived pages, note this to the user.

## Step 2: Read and Synthesize

Read the relevant memory pages. Follow `[[wikilinks]]` to gather additional context — if a page references another page that seems relevant, read that too. Build up a comprehensive understanding before answering.

### Access Tracking (Side-Effect)

**For every page you read during this query**, update its frontmatter:
- Set `last_accessed` to today's date
- Increment `access_count` by 1

This creates a reinforcement signal — frequently useful memories stay accessible while rarely accessed ones decay toward archival.

## Step 3: Answer the Question

Provide a thorough answer that:

- **Cites memory pages** using `[[wikilinks]]`: "According to [[api-timeout-debugging]], the root cause was..."
- **Cites original inputs** when precision matters: "As recorded in `inputs/conversation-2026-04-10.md`..."
- **Synthesizes across multiple pages** — don't just summarize one page, connect information from several
- **Reports confidence**: if the answer draws from low-confidence or single-episode memories, say so
- **Acknowledges gaps**: if the memory store doesn't have enough information to fully answer, say so and suggest what inputs might help
- **Notes contradictions**: if different memory pages disagree on something relevant, surface the tension

Match the answer format to the question:
- Factual question -> concise answer with citations
- Comparison question -> table or structured comparison
- "What have I learned about X?" -> comprehensive overview drawing from all relevant pages
- "How do I do X?" -> procedural answer drawing from schema pages
- "What happened when X?" -> episodic answer drawing from episode pages

### Output format options

Choose the best format for the question. Combine multiple formats when useful.

- **Prose** — default for factual or exploratory questions
- **Comparison table** — for "X vs Y" questions. Use markdown tables with clear column headers and `[[wikilinks]]` in cells.
- **Mermaid diagram** — for relationships, timelines, flowcharts, or processes. Obsidian renders Mermaid natively:
  ```mermaid
  graph LR
    A[["Actor A"]] --> B[["Schema B"]]
    A --> C[["Actor C"]]
  ```
  Use `graph` for relationships, `timeline` for chronology, `flowchart` for processes.
- **Dataview snippet** — when the answer is "list all X with property Y," generate a Dataview query the user can paste into Obsidian:
  ```dataview
  TABLE tags, updated, confidence, access_count
  FROM "memory/schemas"
  WHERE status = "active"
  SORT access_count DESC
  ```
- **Combination** — prose with an embedded table or diagram is often the best format for complex answers

### Auto Mode Output

If `mode` is `auto`, skip prose formatting and return a structured markdown block that the calling agent can parse:

```markdown
## Answer
{{concise answer}}

## Confidence
{{high | medium | low | uncertain}}

## Sources
- [[page1]] — relevance
- [[page2]] — relevance

## Gaps
- {{what's missing}}
```

## Step 4: Offer to File

**Skip this step if `mode` is `auto`.**

After answering, ask the user:

> "Would you like me to file this answer as a reflection? This would preserve the synthesis for future recall."

If yes:
1. Create `memory/reflections/{{kebab-case-question-slug}}.md` with frontmatter:
   ```yaml
   title: "{{Question as title}}"
   type: reflection
   created: {{today}}
   updated: {{today}}
   sources: [{{list of input files that contributed}}]
   tags: [{{relevant tags}}]
   status: active
   importance: medium
   confidence: {{derived from the confidence of source pages}}
   last_accessed: {{today}}
   access_count: 0
   memory_type: semantic
   validity_window: permanent
   supersedes: []
   ```
2. Add `[[wikilinks]]` throughout the filed answer
3. Update `memory/index.md` — add entry under Reflections
4. Update `memory/log.md`

## Step 5: Log the Query

Regardless of whether the answer was filed, append to `memory/log.md`:

```markdown
## [{{today}}] query | {{Short question summary}}

Question: "{{full question}}". {{Filed as [[reflection-page-name]] | Not filed.}} Key pages consulted: [[page1]], [[page2]].
```

## Step 6: Suggest Follow-ups

Based on what you learned while answering, suggest:
- Related questions the user might want to explore
- Gaps in memory that new inputs could fill
- Patterns noticed that might be worth consolidating
- Schemas with low confidence that more episodes could strengthen
