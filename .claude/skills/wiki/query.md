# Wiki Query Operation

You are answering a question using the wiki as your knowledge base. The question is provided as an argument.

## Pre-flight

0. Read `.wiki-config.json` if it exists at the project root. Resolve `{WIKI}` per the **Path Resolution** rules in SKILL.md. If no config, use `wiki/` relative to project root. Always double-quote paths containing spaces in Bash commands.
1. Read `CLAUDE.md` (at project root) for domain-specific conventions
2. Read `{WIKI}/index.md` to understand the full scope of the wiki

## Step 1: Find Relevant Pages

Based on the question and the index, identify which wiki pages are likely relevant. Consider:
- Entity pages that match people/things mentioned in the question
- Concept pages that match topics in the question
- Source summary pages that might have relevant detail
- Comparison pages if the question involves comparing things
- Previous query pages if a similar question was asked before

Use Grep to search wiki pages for keywords if the index alone isn't sufficient.

## Step 2: Read and Synthesize

Read the relevant wiki pages. Follow `[[wikilinks]]` to gather additional context — if a page references another page that seems relevant, read that too. Build up a comprehensive understanding before answering.

## Step 3: Answer the Question

Provide a thorough answer that:

- **Cites wiki pages** using `[[wikilinks]]`: "According to [[transformer-architecture]], the key innovation was..."
- **Cites original sources** when precision matters: "As noted in `sources/attention-paper.md`..."
- **Synthesizes across multiple pages** — don't just summarize one page, connect information from several
- **Acknowledges gaps**: if the wiki doesn't have enough information to fully answer, say so and suggest what sources might help
- **Notes contradictions**: if different wiki pages disagree on something relevant, surface the tension

Match the answer format to the question:
- Factual question → concise answer with citations
- Comparison question → table or structured comparison
- Exploratory question → longer synthesis with connections
- "What do we know about X?" → comprehensive overview drawing from all relevant pages

### Output format options

Choose the best format for the question. Combine multiple formats when useful.

- **Prose** — default for factual or exploratory questions
- **Comparison table** — for "X vs Y" questions. Use markdown tables with clear column headers and `[[wikilinks]]` in cells.
- **Mermaid diagram** — for relationships, timelines, flowcharts, or architecture. Obsidian renders Mermaid natively:
  ```mermaid
  graph LR
    A[["Concept A"]] --> B[["Concept B"]]
    A --> C[["Concept C"]]
  ```
  Use `graph` for relationships, `timeline` for chronology, `flowchart` for processes.
- **Dataview snippet** — when the answer is "list all X with property Y," generate a Dataview query the user can paste into Obsidian:
  ```dataview
  TABLE tags, updated, importance
  FROM "wiki/concepts"
  WHERE contains(tags, "reasoning")
  SORT updated DESC
  ```
- **Marp slide deck** — for presentation-style output. Use Marp markdown syntax (Obsidian has a Marp plugin). Separate slides with `---` and use front matter `marp: true`:
  ```markdown
  ---
  marp: true
  ---
  # Slide Title
  - Key point 1
  - Key point 2
  ---
  # Next Slide
  ```
  Best for "summarize X for a presentation" or "give me an overview I can present."
- **Combination** — prose with an embedded table or diagram is often the best format for complex answers

## Step 4: Offer to File

After answering, ask the user:

> "Would you like me to file this answer as a wiki page? This would preserve the synthesis for future reference."

If yes:
1. Create `wiki/queries/{{kebab-case-question-slug}}.md` with frontmatter:
   ```yaml
   title: "{{Question as title}}"
   type: query
   created: {{today}}
   updated: {{today}}
   sources: [{{list of source files that contributed}}]
   tags: [{{relevant tags}}]
   status: complete
   importance: medium
   ```
2. Add `[[wikilinks]]` throughout the filed answer
3. Update `wiki/index.md` — add entry under Queries
4. Update `wiki/log.md`

## Step 5: Log the Query

Regardless of whether the answer was filed, append to `wiki/log.md`:

```markdown
## [{{today}}] query | {{Short question summary}}

Question: "{{full question}}". {{Filed as [[query-page-name]] | Not filed.}} Key pages consulted: [[page1]], [[page2]].
```

## Step 6: Suggest Follow-ups

Based on what you learned while answering, suggest:
- Related questions the user might want to explore
- Gaps in the wiki that new sources could fill
- Connections or patterns you noticed that might be worth investigating
