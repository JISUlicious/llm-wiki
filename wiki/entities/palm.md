---
title: PaLM
type: entity
created: 2026-04-05
updated: 2026-04-12
sources:
  - "ReAct Yao 2022 2210.03629.pdf"
  - "Chain-of-Thought Wei 2022 2201.11903.pdf"
  - "Transformar Vaswani 1706.03762.pdf"
tags:
  - model
  - google
  - large-language-model
status: draft
importance: medium
---

# PaLM

**PaLM** (Pathways Language Model) is a large language model developed by Google, introduced by Chowdhery et al. (2022). The largest variant has **540 billion parameters**.

## Key Details

- **Developer**: Google Research
- **Parameters**: 8B, 62B, 540B variants
- **Architecture**: Dense [[transformer-architecture|Transformer]]
- **Training**: Trained using the Pathways system for efficient distributed training

## Role in Chain-of-Thought Prompting

PaLM is the primary model demonstrating [[chain-of-thought-prompting]]'s effectiveness. The scaling across 8B → 62B → 540B is the canonical evidence for CoT as an **emergent ability**:

- **PaLM 8B/62B**: CoT provides minimal or no improvement
- **PaLM 540B + CoT**: dramatic improvements — 3.2x on GSM8K (18% → 57%), SOTA on StrategyQA (76%), surpasses human on Sports Understanding (95%)
- CoT + PaLM 540B surpassed finetuned GPT-3 with verifier on GSM8K

## Role in ReAct

[[react]] uses PaLM-540B as the primary base model:

- Few-shot ReAct prompting achieves strong results across all four benchmarks
- **Finetuning scaling**: PaLM-8B finetuned on 3K ReAct trajectories outperforms all PaLM-62B prompting methods; PaLM-62B finetuned outperforms all PaLM-540B prompting methods
- Appendix results show GPT-3 outperforms PaLM-540B on some ReAct tasks

## References

- [[chain-of-thought-prompting-wei-2022]]
- [[react-synergizing-reasoning-and-acting]]
- Chowdhery et al., 2022 — original PaLM paper (not yet in sources)
