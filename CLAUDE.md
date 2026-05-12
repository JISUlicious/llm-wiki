# AI/ML Wiki — Project Schema

This file is project-specific guidance for the wiki. It defines what this wiki covers and any domain conventions. Skill mechanics (directory layout, frontmatter shape, ingest steps, link format, etc.) live in `.claude/skills/wiki/SKILL.md`.

## Domain

This wiki covers **Artificial Intelligence and Machine Learning** — models, architectures, training techniques, scaling laws, benchmarks, research labs, key researchers, and the evolving landscape of AI capabilities. Scope includes deep learning, NLP, computer vision, reinforcement learning, AI safety, and adjacent topics like MLOps and deployment.

## Source Types

- **Web articles & blog posts**: Tech blog posts, news articles, opinion pieces. Clipped via Obsidian Web Clipper or saved as markdown. Focus on extracting claims, key insights, and who said what.
- **Research papers**: Academic papers, technical reports, whitepapers (arXiv, conference proceedings). Extract: problem statement, method, key results, ablations, limitations. Note citation counts and venue if available.
- **Books & transcripts**: Book chapters, podcast transcripts, lecture notes, interview transcripts. Extract key arguments, notable quotes, and speaker attributions.
- **Mixed**: Any other format — treat as general markdown and extract what's valuable.

## Domain-Specific Page Guidance

Augments the skill's generic page-type definitions:

- **AI models** (entity pages): include parameter count, training data, release date, key capabilities.
- **Researchers** (entity pages): include affiliation, key contributions, notable papers.
- **Labs / companies** (entity pages): include focus area, notable releases, key personnel.
- **Concepts**: include intuition/explanation, mathematical formulation (if applicable), history, key papers, relationship to other concepts. Examples in this domain: attention mechanism, RLHF, mixture of experts, scaling laws, chain-of-thought.

## Domain Conventions

- Use LaTeX notation (`$...$`) for inline math, (`$$...$$`) for display math when describing formulas.
- When referencing papers, use the format: "Author et al. (Year)" with a link to the source summary page.

## Maintenance Notes

This file is co-evolved between you and the LLM. As you work with the wiki, update this schema to reflect new domain conventions, important entity types, or workflows that emerge. Skill-level mechanics (link format, frontmatter shape, directory layout) belong in `.claude/skills/wiki/`, not here.
