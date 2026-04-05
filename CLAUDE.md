# LLM Wiki Schema

## Domain

This wiki covers **Artificial Intelligence and Machine Learning** — models, architectures, training techniques, scaling laws, benchmarks, research labs, key researchers, and the evolving landscape of AI capabilities. Scope includes deep learning, NLP, computer vision, reinforcement learning, AI safety, and adjacent topics like MLOps and deployment.

## Source Types

- **Web articles & blog posts**: Tech blog posts, news articles, opinion pieces. Clipped via Obsidian Web Clipper or saved as markdown. Focus on extracting claims, key insights, and who said what.
- **Research papers**: Academic papers, technical reports, whitepapers (arXiv, conference proceedings). Extract: problem statement, method, key results, ablations, limitations. Note citation counts and venue if available.
- **Books & transcripts**: Book chapters, podcast transcripts, lecture notes, interview transcripts. Extract key arguments, notable quotes, and speaker attributions.
- **Mixed**: Any other format — treat as general markdown and extract what's valuable.

## Page Types

### Entities
Pages for distinct things: researchers, labs, companies, models, datasets, benchmarks, conferences.
- Directory: `wiki/entities/`
- Naming: `kebab-case-name.md`
- For AI models: include parameter count, training data, release date, key capabilities
- For researchers: include affiliation, key contributions, notable papers
- For labs/companies: include focus area, notable releases, key personnel

### Concepts
Pages for ideas, techniques, architectures, training methods, theoretical frameworks.
- Directory: `wiki/concepts/`
- Naming: `kebab-case-name.md`
- Include: intuition/explanation, mathematical formulation (if applicable), history, key papers, relationship to other concepts
- Examples: attention mechanism, RLHF, mixture of experts, scaling laws, chain-of-thought

### Source Summaries
One page per ingested source document. Captures key claims, data, and takeaways.
- Directory: `wiki/sources/`
- Naming: `kebab-case-short-title.md`

### Comparisons
Side-by-side analyses, comparison tables, tradeoff discussions.
- Directory: `wiki/comparisons/`
- Naming: `kebab-case-comparison-title.md`
- Use markdown tables for structured comparisons (e.g., model benchmarks)

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
- Use LaTeX notation (`$...$`) for inline math, (`$$...$$`) for display math when describing formulas
- When referencing papers, use format: "Author et al. (Year)" with a link to the source summary page

## Frontmatter Schema

```yaml
title: string (required)
type: entity | concept | source | comparison | query (required)
created: YYYY-MM-DD (required)
updated: YYYY-MM-DD (required)
sources: list of source filenames (required for all except overview/index)
tags: list of strings (required — for Dataview queries)
status: draft | complete | needs-update (for Dataview filtering)
importance: high | medium | low (for Dataview sorting)
```

### Dataview Examples

With this frontmatter, you can run Dataview queries in Obsidian like:

```dataview
TABLE tags, updated, importance
FROM "wiki/concepts"
WHERE status = "complete"
SORT importance ASC
```

```dataview
LIST
FROM "wiki/entities"
WHERE contains(tags, "model")
SORT updated DESC
```

## Maintenance Notes

This file is co-evolved between you and the LLM. As you work with the wiki, update this schema to reflect new conventions, page types, or workflows that emerge.
