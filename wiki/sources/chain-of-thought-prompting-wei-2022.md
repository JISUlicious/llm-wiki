---
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
type: source
created: 2026-04-05
updated: 2026-04-05
sources:
  - "Chain-of-Thought Wei 2022 2201.11903.pdf"
tags:
  - reasoning
  - prompting
  - few-shot
  - emergent-abilities
  - arithmetic
  - commonsense
  - neurips-2022
status: complete
importance: high
---

# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

**Source**: `sources/Chain-of-Thought Wei 2022 2201.11903.pdf`
**Authors**: [[jason-wei]], Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, Denny Zhou
**Affiliation**: Google Research, Brain Team
**Published**: NeurIPS 2022 (arXiv: 2201.11903)

## Summary

This paper introduces [[chain-of-thought-prompting]] (CoT), a method for eliciting multi-step reasoning in LLMs by providing few-shot exemplars that include intermediate reasoning steps. The key finding is that CoT is an **emergent ability of model scale** — it only works at ~100B+ parameters and provides dramatic improvements on tasks where standard prompting has flat scaling curves.

The approach is remarkably simple: instead of `⟨input, output⟩` exemplars, use `⟨input, chain of thought, output⟩` triples. The model then generates similar reasoning chains for new problems.

## Key Results

### Arithmetic Reasoning (5 benchmarks)

| Benchmark | Standard Prompting (PaLM 540B) | CoT (PaLM 540B) | Prior Best (finetuned) |
|-----------|-------------------------------|-----------------|----------------------|
| **GSM8K** | 18% | **57%** | 55% (finetuned GPT-3 + verifier) |
| SVAMP | 79% | **86%** | 57% |
| MAWPS | 84% | **93%** | 84% |
| AQuA | 36% | **48%** | 37% |
| ASDiv | 74% | **74%** | 75% |

- GSM8K: **3x improvement** from standard to CoT prompting with PaLM 540B
- New SOTA on GSM8K, SVAMP, and MAWPS — a prompting-only approach competing with task-specific finetuned models

### Commonsense Reasoning (5 benchmarks)

| Benchmark | Standard (PaLM 540B) | CoT (PaLM 540B) | Prior Best |
|-----------|---------------------|-----------------|-----------|
| CSQA | 78% | 80% | 79% |
| **StrategyQA** | 75% | **76%** | 69% (SOTA) |
| Date Understanding | 62% | **77%** | — |
| **Sports Understanding** | 87% | **95%** | 84% (human) |
| SayCan (robot planning) | 82% | **91%** | — |

- StrategyQA: new SOTA (76% vs. 69%)
- Sports Understanding: surpasses unaided human sports enthusiast (95% vs. 84%)

### Symbolic Reasoning

- Last letter concatenation and coin flip tasks
- In-domain: near 100% solve rate with CoT at PaLM 540B scale
- **OOD generalization**: CoT facilitates length generalization to longer sequences than seen in exemplars (e.g., train on 2-word names, test on 4-word names)

### Scaling Properties

- **Small models (≤10B)**: CoT does not help or hurts — models produce fluent but illogical chains
- **Medium models (~60B)**: some improvement
- **Large models (≥100B)**: dramatic improvement — CoT is an **emergent ability**
- Models tested: GPT-3 (175B), LaMDA (137B), [[palm|PaLM]] (540B), UL2 (20B), Codex

## Ablation Study (Critical Findings)

| Variant | Effect | Implication |
|---------|--------|------------|
| **Equation only** | Minimal improvement on hard tasks | Natural language steps matter, not just math expressions |
| **Variable compute (dots)** | Same as baseline | Extra tokens alone don't help — content of reasoning matters |
| **Reasoning after answer** | Same as baseline | Model must reason BEFORE answering — it's not just knowledge activation |
| **Different annotators** | All outperform baseline | CoT is robust to linguistic style |
| **Different exemplars** | All outperform baseline | CoT is robust to specific choice of examples |

## Key Claims

1. CoT prompting is an **emergent ability of model scale** — only appears at ~100B parameters
2. Performance gains are largest for **harder problems** (multi-step > single-step)
3. The natural language reasoning is essential — not just more computation or equation extraction
4. The model must reason **before** answering (not after) — sequential reasoning is the mechanism
5. CoT is robust to annotator style, exemplar choice, and exemplar ordering
6. A prompting-only approach can match or exceed task-specific finetuned models
7. CoT expands the set of tasks that LLMs can perform — standard prompting is a **lower bound** on capability

## Error Analysis (GSM8K, LaMDA 137B)

Of 50 correct answers examined:
- 96% (48/50) had fully correct chains of thought
- 4% (2/50) had errors that coincidentally reached the right answer

Of 50 incorrect answers:
- **46%** were "almost correct" — minor mistakes (calculator error, symbol mapping, one step missing)
- **54%** had major errors in semantic understanding or coherence

Scaling from PaLM 62B → 540B fixes many one-step-missing and semantic understanding errors.

## Four Properties of CoT

1. **Decomposition** — allocates more computation to harder problems via intermediate steps
2. **Interpretability** — provides a window into the model's reasoning process
3. **Generality** — applicable to any task humans can solve via language
4. **Simplicity** — requires no finetuning; works with off-the-shelf models via prompting

## Limitations (Acknowledged)

- Does not prove the model is "actually reasoning" — open question
- Annotation costs could be prohibitive for finetuning (though few-shot is cheap)
- No guarantee of correct reasoning paths — can produce plausible but wrong chains
- Only works at large scale — costly to serve in real-world applications
- Small models produce "fluent but illogical" chains that actively hurt performance

## Entities Mentioned

- [[jason-wei]] — First author, Google Brain
- [[palm]] — Primary model used for strongest results (8B, 62B, 540B)
- Denny Zhou — Senior author, Google Brain

## Concepts Discussed

- [[chain-of-thought-prompting]] — The core method introduced in this paper
- Self-consistency (CoT-SC, Wang et al., 2022) — follow-up: sampling multiple CoT paths and majority voting
- Few-shot prompting (Brown et al., 2020) — the baseline approach CoT builds on

## Notable Quotes

> "Chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of ~100B parameters."

> "Standard prompting only provides a lower bound on the capabilities of large language models."

> "We qualitatively found that models of smaller scale produced fluent but illogical chains of thought, leading to lower performance than standard prompting."

## References

_Original source: `sources/Chain-of-Thought Wei 2022 2201.11903.pdf`_
