---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
type: source
created: 2026-04-05
updated: 2026-04-05
sources:
  - "ReAct Yao 2022 2210.03629.pdf"
tags:
  - reasoning
  - acting
  - prompting
  - tool-use
  - few-shot
  - iclr-2023
status: complete
importance: high
---

# ReAct: Synergizing Reasoning and Acting in Language Models

**Source**: `sources/ReAct Yao 2022 2210.03629.pdf`
**Authors**: [[shunyu-yao]], Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**Affiliations**: Princeton University, Google Research (Brain team)
**Published**: ICLR 2023 (arXiv: 2210.03629)

## Summary

This paper introduces [[react]], a paradigm for prompting LLMs to generate interleaved **reasoning traces** (thoughts) and **task-specific actions**. The key insight is that reasoning and acting are synergistic: reasoning traces help the model plan, track progress, handle exceptions, and synthesize answers, while actions allow the model to interface with external environments (e.g., Wikipedia APIs) to gather information that grounds the reasoning.

ReAct augments the agent's action space from $A$ to $\hat{A} = A \cup L$, where $L$ is the space of natural language "thoughts." Thoughts do not affect the external environment but update the agent's internal context to support future reasoning and acting.

The approach is evaluated on four benchmarks spanning knowledge-intensive reasoning and interactive decision making, using [[palm]] (540B) with few-shot prompting.

## Key Results

### Knowledge-Intensive Reasoning (HotpotQA, FEVER)

| Method | HotpotQA (EM) | FEVER (Acc) |
|--------|--------------|-------------|
| Standard | 28.7 | 57.1 |
| [[chain-of-thought-prompting|CoT]] | 29.4 | 56.3 |
| CoT-SC (21 samples) | 33.4 | 60.4 |
| Act-only | 25.7 | 58.9 |
| **ReAct** | **27.4** | **60.9** |
| ReAct → CoT-SC | 34.2 | 64.6 |
| CoT-SC → ReAct | 35.1 | 62.0 |

- ReAct outperforms Act-only consistently, showing reasoning guides better action selection
- ReAct beats CoT on FEVER (60.9 vs 56.3) where factual retrieval matters most
- CoT slightly beats ReAct on HotpotQA (29.4 vs 27.4) where flexible reasoning matters more
- **Best overall**: combining ReAct + CoT-SC, reaching 21-sample CoT-SC performance with only 3-5 samples

### Interactive Decision Making (ALFWorld, WebShop)

| Method | ALFWorld (SR%) | WebShop (SR%) |
|--------|---------------|---------------|
| Act-only | 45 | 30.1 |
| **ReAct** | **71** | **40.0** |
| BUTLER (imitation learning, 10⁵ examples) | 37 | — |
| IL + RL | — | 28.7 |
| Human expert | — | 59.6 |

- ReAct outperforms Act by +26% absolute on ALFWorld and +10% on WebShop
- Beats imitation/RL methods trained on 10³–10⁵ examples using only 1-2 in-context examples

### Failure Analysis (HotpotQA, 200 examples)

| Mode | ReAct | CoT |
|------|-------|-----|
| True positive (correct reasoning) | 94% | 86% |
| False positive (hallucinated success) | 6% | 14% |
| Hallucination (failure mode) | 0% | 56% |
| Reasoning error | 47% | 16% |
| Search result error | 23% | — |

- CoT's dominant failure: hallucination (56% of errors)
- ReAct's dominant failure: reasoning errors, often repetitive loops (47%)
- ReAct has **zero** hallucination failures due to external grounding

### Finetuning

- PaLM-8B finetuned on 3K ReAct trajectories outperforms all PaLM-62B prompting methods
- PaLM-62B finetuned ReAct outperforms all PaLM-540B prompting methods
- Finetuning ReAct/Act teaches generalizable information retrieval skills; finetuning Standard/CoT teaches memorization

## Key Claims

1. Interleaving reasoning and acting is more effective than either in isolation
2. External grounding via actions dramatically reduces hallucination compared to pure reasoning
3. The structural constraint of alternating thought-action-observation reduces reasoning flexibility (tradeoff)
4. Combining internal knowledge (CoT-SC) with external retrieval (ReAct) yields the best results
5. Few-shot ReAct prompting can outperform methods trained on orders of magnitude more data
6. The approach is general — works across QA, fact verification, text games, and web navigation

## Entities Mentioned

- [[shunyu-yao]] — First author, Princeton University
- [[palm]] — PaLM-540B, the base model used for experiments
- Karthik Narasimhan — Co-author, Princeton University

## Concepts Discussed

- [[react]] — The core paradigm introduced in this paper
- [[chain-of-thought-prompting]] — Key baseline and complementary method
- [[tool-use-in-llms]] — Broader paradigm that ReAct contributes to
- Self-consistency (CoT-SC) — Sampling multiple CoT paths and taking majority vote
- Inner Monologue — Prior work on embodied reasoning; ReAct argues it lacks true "inner thought"

## Notable Quotes

> "A unique feature of human intelligence is the ability to seamlessly combine task-oriented actions with verbal reasoning (or inner speech), which has been theorized to play an important role in human cognition for enabling self-regulation or strategization."

> "The idea of ReAct is simple: we augment the agent's action space to $\hat{A} = A \cup L$, where $L$ is the space of language."

## References

_Original source: `sources/ReAct Yao 2022 2210.03629.pdf`_
