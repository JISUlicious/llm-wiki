---
title: Chain-of-Thought Prompting
type: concept
created: 2026-04-05
updated: 2026-04-05
sources:
  - "Chain-of-Thought Wei 2022 2201.11903.pdf"
  - "ReAct Yao 2022 2210.03629.pdf"
  - "Reflexion Shinn 2023 2303.11366.pdf"
tags:
  - reasoning
  - prompting
  - few-shot
  - emergent-abilities
  - arithmetic
  - commonsense
status: complete
importance: high
---

# Chain-of-Thought Prompting

**Chain-of-Thought (CoT) prompting** is a technique where LLMs generate intermediate reasoning steps before producing a final answer. Introduced by [[jason-wei]] et al. (NeurIPS 2022), it is one of the most influential discoveries about LLM capabilities: that reasoning can be **elicited** through prompting alone, without finetuning.

## Core Idea

Standard few-shot prompting uses `⟨input, output⟩` pairs. CoT augments these with intermediate reasoning: `⟨input, chain of thought, output⟩`. The model then generates similar reasoning chains for new problems.

```
Q: Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls.
   5 + 6 = 11. The answer is 11.
```

## Why It Works (Ablation Evidence)

The original paper tested several ablations to isolate why CoT helps:

| Variant | Result | What it rules out |
|---------|--------|------------------|
| **Equation only** (just math, no NL) | Minimal improvement | It's not just about extracting equations |
| **Variable compute** (output dots equal to answer length) | No improvement | It's not just about more tokens/computation |
| **Reasoning after answer** | No improvement | The model must reason BEFORE answering — it's not knowledge activation |
| **Different annotators** | All beat baseline | Not dependent on a specific writing style |

The natural language reasoning steps themselves are essential — not just extra computation, equation extraction, or knowledge retrieval.

## Four Properties

1. **Decomposition** — allocates additional computation to harder multi-step problems
2. **Interpretability** — provides a window into the model's reasoning process
3. **Generality** — applicable to any task humans can solve via language
4. **Simplicity** — no finetuning; works with off-the-shelf models

## Emergent Ability of Scale

CoT is a defining example of an **emergent ability** — it only appears at ~100B+ parameters:

- **Small models (≤10B)**: CoT hurts performance — models produce "fluent but illogical" chains
- **Medium models (~60B)**: modest improvement
- **Large models (≥100B)**: dramatic improvement, enabling SOTA results

This means standard prompting provides only a **lower bound** on LLM capabilities.

## Key Results

### Arithmetic (PaLM 540B)

| Benchmark | Standard | CoT | Improvement |
|-----------|----------|-----|-------------|
| **GSM8K** | 18% | **57%** | **3.2x** |
| SVAMP | 79% | 86% | +7% |
| MAWPS | 84% | 93% | +9% |

GSM8K result surpassed finetuned GPT-3 with a verifier (55%).

### Commonsense

- **StrategyQA**: 76% (new SOTA, surpassing 69% prior best)
- **Sports Understanding**: 95% (surpassing human baseline of 84%)

### Symbolic Reasoning

- Near 100% on in-domain tasks at scale
- Enables **OOD length generalization** (train on 2-word, test on 4-word)

## Variants

- **CoT-SC (Self-Consistency)** (Wang et al., 2022): sample multiple CoT paths with temperature, take majority vote. Consistently boosts over single CoT.
- **Zero-shot CoT** (Kojima et al., 2022): append "Let's think step by step" without few-shot examples.
- **Least-to-Most Prompting** (Zhou et al., 2022): decompose complex tasks into simpler subproblems.

## Limitations

- **Hallucination-prone** — reasoning is a "static black box" with no external grounding. On HotpotQA, 56% of CoT failures were due to hallucinated facts (per [[react-synergizing-reasoning-and-acting]])
- **No external knowledge access** — relies entirely on parametric knowledge
- **No guarantee of correct reasoning** — can produce plausible but wrong chains
- **Scale-dependent** — only works at ~100B+ parameters, costly to serve
- **Error analysis** (GSM8K): 46% of errors are near-misses (minor arithmetic/symbol errors), 54% are major semantic errors

## Relationship to ReAct and Reflexion

CoT is the foundation that [[react]] and [[reflexion]] build upon:

- **[[react]]** adds actions to CoT, grounding reasoning in external knowledge. CoT is better for flexible reasoning (16% reasoning errors vs. 47%), but ReAct eliminates hallucination (0% vs. 56%). Best combined: ReAct + CoT-SC.
- **[[reflexion]]** uses CoT (or ReAct) as its Actor, adding self-reflection and episodic memory. With Reflexion, CoT agents improve 20% on HotpotQA across trials — without Reflexion, baseline CoT shows **zero** improvement on retry.

> CoT is "reasoning only," ReAct is "reasoning + acting," Reflexion is "reasoning + acting + learning." They form a progression, not competing alternatives.

## Impact

CoT prompting transformed how the field thinks about LLM capabilities. It showed that reasoning is not a matter of model architecture but of **how you prompt** — and that capabilities can be latent until the right elicitation method is found. This insight catalyzed an explosion of work on prompting strategies, agent architectures, and emergent abilities.

## References

- [[chain-of-thought-prompting-wei-2022]]
- [[react-synergizing-reasoning-and-acting]]
- [[reflexion-verbal-reinforcement-learning]]
