---
title: Overview
type: overview
created: 2026-04-05
updated: 2026-04-05
tags:
  - agents
  - reasoning
  - tool-use
  - self-reflection
  - emergent-abilities
---

# Overview

This wiki covers **Artificial Intelligence and Machine Learning** — models, architectures, techniques, researchers, and the evolving landscape of AI capabilities.

## Summary

The wiki traces the **reasoning and agency lineage** in LLMs through three foundational papers:

1. **[[chain-of-thought-prompting]]** (Wei et al., NeurIPS 2022) — discovered that step-by-step reasoning is an emergent ability of model scale. Including reasoning demonstrations in prompts unlocks dramatic improvements on math, commonsense, and symbolic reasoning tasks. The key insight: standard prompting is a **lower bound** on LLM capabilities.

2. **[[react]]** (Yao et al., ICLR 2023) — extended CoT by interleaving reasoning traces with task-specific **actions**. This grounds reasoning in external knowledge (e.g., Wikipedia), eliminating the hallucination problem that plagues pure CoT (0% vs. 56% hallucination failures on HotpotQA).

3. **[[reflexion]]** (Shinn et al., 2023) — extended ReAct with **verbal self-reflection** and episodic memory. Agents learn from failure across trials without weight updates, achieving 91% on HumanEval and 97% on ALFWorld.

**The progression**: reasoning → reasoning + acting → reasoning + acting + learning from failure.

## Key Themes

### Emergent Abilities and Scale

[[chain-of-thought-prompting]] is a defining example of an **emergent ability** — it only works at ~100B+ parameters. Smaller models produce "fluent but illogical" reasoning that hurts performance. This raises fundamental questions about what other latent capabilities exist in large models, waiting for the right elicitation.

### Reasoning + Acting Synergy

Pure reasoning (CoT) is flexible but hallucination-prone. Pure acting is grounded but lacks planning. [[react]] showed that interleaving them yields more accurate, interpretable, and trustworthy agents. The thought-action-observation loop became the standard architecture for LLM agents.

### Learning Without Weight Updates

[[reflexion]] demonstrated that verbal self-reflection is a viable alternative to gradient-based RL. Agents improve through "semantic gradients" — natural language explanations of what went wrong. Critically, retry without reflection shows **zero improvement**, proving that explicit verbal reasoning about failure (not just repeated sampling) is the mechanism.

### Tool Use as a Paradigm

[[tool-use-in-llms]] transforms LLMs from generators into agents. The progression from CoT (internal reasoning) to ReAct (external actions) to Reflexion (learning from failed actions) maps the evolution of the agent paradigm.

## Key Connections

- **[[jason-wei]]** (Google Brain) → [[chain-of-thought-prompting]] → foundation for all reasoning work
- **[[shunyu-yao]]** (Princeton) → [[react]] + [[reflexion]] → the agent paradigm
- **[[palm]]** → primary model for both CoT and ReAct experiments; the scaling evidence
- Karthik Narasimhan (Princeton) → advisor/co-author on both ReAct and Reflexion
- All three papers evaluate on overlapping benchmarks (HotpotQA, ALFWorld), enabling direct comparison

## Open Questions

- What other emergent abilities are latent in large models, waiting for the right prompting method?
- How do CoT/ReAct/Reflexion interact with RLHF-trained models vs. base models?
- What are the limits of verbal self-reflection? When does it hit a ceiling?
- How do newer approaches (Tree of Thoughts, LATS, etc.) extend this lineage?
- What are the safety implications of self-improving agents acting in real environments?
- Can these techniques work with smaller models through finetuning or distillation?
