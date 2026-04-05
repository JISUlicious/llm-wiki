---
title: Activity Log
type: log
created: 2026-04-05
updated: 2026-04-05
---

# Activity Log

Chronological record of wiki operations. Newest entries first.

---

## [2026-04-05] ingest | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

Ingested `sources/Chain-of-Thought Wei 2022 2201.11903.pdf` (downloaded from arxiv.org/pdf/2201.11903). Pages created: [[chain-of-thought-prompting-wei-2022]], [[jason-wei]]. Pages updated: [[chain-of-thought-prompting]] (major — promoted from draft to complete with primary source), [[palm]]. Key takeaways: CoT is an emergent ability of scale (~100B+); 3x improvement on GSM8K; ablations prove natural language steps are essential, not just more computation; standard prompting is a lower bound on LLM capabilities.

## [2026-04-05] ingest | Reflexion: Language Agents with Verbal Reinforcement Learning

Ingested `sources/Reflexion Shinn 2023 2303.11366.pdf`. Pages created: [[reflexion-verbal-reinforcement-learning]], [[reflexion]], [[noah-shinn]]. Pages updated: [[react]], [[tool-use-in-llms]], [[shunyu-yao]]. Key takeaways: verbal self-reflection enables LLM agents to learn from failure without weight updates; achieves 91% HumanEval, 97% ALFWorld; retry without reflection shows zero improvement.

## [2026-04-05] ingest | ReAct: Synergizing Reasoning and Acting in Language Models

Ingested `sources/ReAct Yao 2022 2210.03629.pdf`. Pages created: [[react-synergizing-reasoning-and-acting]], [[react]], [[chain-of-thought-prompting]], [[tool-use-in-llms]], [[shunyu-yao]], [[palm]]. Key takeaways: ReAct interleaves reasoning and actions for grounded, interpretable LLM agents; eliminates hallucination vs CoT; few-shot prompting outperforms methods trained on orders of magnitude more data.

## [2026-04-05] init | Wiki initialized

Wiki created for: AI / Machine Learning. Covers models, architectures, training techniques, scaling laws, benchmarks, research labs, and key researchers.
Directories created: sources/, wiki/entities/, wiki/concepts/, wiki/sources/, wiki/comparisons/, wiki/queries/.
Schema generated: CLAUDE.md with Dataview-friendly frontmatter (status, importance fields).
