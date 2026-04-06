# LLM Wiki for Claude Code

A Claude Code agent skill that builds and maintains a personal knowledge base from raw source documents. Based on [Karpathy's LLM Wiki](https://github.com/karpathy/llm-wiki) pattern.

Instead of RAG — where the LLM re-derives answers from raw chunks on every query — this approach has the LLM **incrementally compile** knowledge into persistent, interlinked markdown pages. Every source you add makes the wiki richer. The knowledge compounds.

You curate sources and ask questions. The LLM does the summarizing, cross-referencing, and bookkeeping.

## How It Works

```
sources/          You drop documents here (articles, papers, notes)
    ↓ /wiki ingest
wiki/             The LLM builds interlinked markdown pages
    ↓ browse
Obsidian          You read the wiki in real time via graph view
```

Three layers:

| Layer | What | Who owns it |
|-------|------|-------------|
| `sources/` | Raw documents — articles, papers, notes, images | You (immutable) |
| `wiki/` | Generated markdown pages — entities, concepts, summaries | The LLM |
| `CLAUDE.md` | Schema — conventions, page types, domain rules | You + the LLM |

## Commands

| Command | What it does |
|---------|-------------|
| `/wiki init` | Bootstrap a new wiki — creates directories, generates a domain-tailored schema |
| `/wiki ingest <source>` | Process a source (local file, URL, or directory for batch) into wiki pages |
| `/wiki query "your question"` | Answer a question with tables, Mermaid diagrams, Dataview snippets |
| `/wiki lint` | Health-check: broken links, orphans, cross-refs, knowledge gaps with search suggestions |

## Quick Start

1. **Install** — clone this repo (or copy `.claude/skills/wiki/` into your project)

2. **Initialize** — run `/wiki init` in Claude Code. It will ask about your domain and set everything up:
   ```
   /wiki init
   ```

3. **Add sources** — drop markdown files into `sources/`. Use [Obsidian Web Clipper](https://obsidian.md/clipper) to convert web articles, or just write plain markdown.

4. **Ingest** — tell Claude to process each source:
   ```
   /wiki ingest sources/my-article.md
   /wiki ingest https://arxiv.org/pdf/2201.11903
   /wiki ingest https://blog.example.com/interesting-post
   /wiki ingest https://raw.githubusercontent.com/user/repo/main/notes.md
   ```
   Accepts local files and URLs. All URL types follow the same pattern — download the raw file, convert to markdown if needed, keep both in `sources/`:

   | Input | Pipeline |
   |-------|----------|
   | Local `.md` file | Read directly |
   | PDF URL | `curl → .pdf` + `pdftotext → .md` |
   | Plain-text URL (`.md`, `.txt`) | `curl → .md` (no conversion) |
   | HTML web page | `curl → .html` + `pandoc`/Python → `.md` |

   For best quality on web pages, use [Obsidian Web Clipper](https://obsidian.md/clipper) to save as markdown first.

5. **Explore** — open the project folder in [Obsidian](https://obsidian.md). Browse pages, follow links, check the graph view.

6. **Query** — ask questions against the accumulated knowledge:
   ```
   /wiki query "How does X compare to Y?"
   ```

7. **Maintain** — periodically lint the wiki:
   ```
   /wiki lint
   ```

## What Gets Generated

After ingesting a few sources, your wiki might look like this:

```
wiki/
├── index.md                        # Catalog of all pages
├── log.md                          # Timeline of all operations
├── overview.md                     # High-level synthesis
├── entities/
│   ├── andrej-karpathy.md
│   └── openai.md
├── concepts/
│   ├── transformer-architecture.md
│   └── attention-mechanism.md
├── sources/
│   ├── attention-is-all-you-need.md
│   └── scaling-laws-for-llms.md
├── comparisons/
│   └── gpt4-vs-claude.md
└── queries/
    └── how-does-scaling-affect-performance.md
```

Every page has YAML frontmatter, `[[wikilinks]]` to related pages, and references back to the original sources. Obsidian renders it all as a navigable, graph-connected knowledge base.

## Page Format

All wiki pages follow the same structure:

```markdown
---
title: Transformer Architecture
type: concept
created: 2026-04-05
updated: 2026-04-05
sources:
  - attention-is-all-you-need.md
tags:
  - deep-learning
  - architecture
---

# Transformer Architecture

The transformer is a neural network architecture based on
[[attention-mechanism]]...

## References

- [[attention-is-all-you-need]]
```

## Obsidian Vault Integration

By default, the wiki lives locally in the project directory. You can point it at an existing Obsidian vault instead — great for iCloud-synced vaults that you browse on your phone/tablet.

During `/wiki init`, answer "yes" to the vault question and provide the path:

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault
```

This creates a `.wiki-config.json` at the project root:

```json
{
  "vault_path": "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault",
  "sources_dir": "sources",
  "wiki_dir": "wiki"
}
```

When `vault_path` is set, all `sources/` and `wiki/` operations read from and write to that vault. When `null` (or the file doesn't exist), everything stays local — fully backward compatible.

- `CLAUDE.md` always stays at the project root (it's Claude Code-specific, not wiki content)
- No symlinks, no MCP servers, no external tools — just a config file the skill reads

## Design Choices

- **No external dependencies** — pure Claude Code tools (Read, Write, Edit, Glob, Grep). No Python, no vector DB, no search server.
- **Obsidian-compatible** — `[[wikilinks]]`, YAML frontmatter, folder structure. Open the directory in Obsidian and it just works.
- **Vault-aware** — optionally read/write to an existing Obsidian vault (including iCloud-synced vaults) via `.wiki-config.json`.
- **Index-driven navigation** — the LLM reads `wiki/index.md` to find relevant pages. Works well up to hundreds of pages without embedding infrastructure.
- **Human-in-the-loop** — ingest discusses findings before writing; lint asks before auto-fixing. You stay in control.
- **Schema is co-evolved** — `CLAUDE.md` starts with sensible defaults and adapts to your domain over time.

## Use Cases

- **Research** — read papers over weeks, build a comprehensive wiki with evolving thesis
- **Book companion** — file chapters, track characters/themes/plot threads as you read
- **Personal knowledge** — journal entries, articles, podcast notes, structured over time
- **Competitive analysis** — accumulate intel from multiple sources into a coherent picture
- **Course notes** — lectures, readings, assignments woven into an interlinked knowledge graph

## Tips

- **One source at a time** is the recommended workflow. Stay involved — read the summaries, guide emphasis, check the updates.
- **Batch ingest** works too — `/wiki ingest sources/` processes all files with less supervision. Good for ingesting a backlog.
- **File good answers** — when `/wiki query` gives a useful synthesis, say yes to filing it. Your explorations compound just like ingested sources.
- **Use Obsidian graph view** to see the shape of your wiki — what's connected, what's a hub, what's orphaned.
- **Lint regularly** as the wiki grows. It catches drift, broken links, gaps, and suggests search queries to fill knowledge holes.
- **Commit often** — after each operation, the skill offers to git commit. Accept to get free version history of your wiki's evolution.
- **Rich query outputs** — queries can produce comparison tables, Mermaid diagrams, and Dataview snippets, not just prose.

## Project Structure

```
.claude/skills/wiki/
├── SKILL.md       # Main skill — router + shared conventions
├── init.md        # Initialize a new wiki
├── ingest.md      # Process a source document
├── query.md       # Answer questions from the wiki
└── lint.md        # Health-check the wiki
```

## Credits

Based on [llm-wiki](https://github.com/karpathy/llm-wiki) by Andrej Karpathy. This implementation adapts the pattern as a Claude Code agent skill.
