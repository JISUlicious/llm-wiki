---
title: Tool Use in LLMs
type: concept
created: 2026-04-05
updated: 2026-04-05
sources:
  - "ReAct Yao 2022 2210.03629.pdf"
  - "Reflexion Shinn 2023 2303.11366.pdf"
tags:
  - tool-use
  - agents
  - acting
  - grounding
status: draft
importance: high
---

# Tool Use in LLMs

**Tool use** refers to the ability of LLMs to interface with external tools, APIs, and environments to perform actions beyond pure text generation. This is one of the key capabilities that transforms LLMs from language generators into **agents**.

## Core Idea

LLMs have vast parametric knowledge but it is static, potentially outdated, and prone to hallucination. Tool use addresses this by letting the model:

1. **Retrieve** information from external sources (search engines, databases, APIs)
2. **Compute** using external tools (calculators, code interpreters)
3. **Act** in environments (web browsers, file systems, robotics)

The model generates structured calls to tools, receives observations, and incorporates them into its reasoning.

## Approaches

### Prompting-Based

- [[react]] — interleaves reasoning traces with tool-calling actions. Foundational approach showing that reasoning + acting > either alone.
- [[reflexion]] — extends ReAct with verbal self-reflection and episodic memory, enabling agents to learn from failed tool interactions across trials. Achieves 97% on ALFWorld and 91% on HumanEval.
- **WebGPT** (Nakano et al., 2021) — LLM interacts with web browsers to answer questions. Uses reinforcement learning from human feedback rather than few-shot prompting.
- **Toolformer** (Schick et al., 2023) — LM learns to insert API calls into text during generation, trained via self-supervision.

### Embodied / Robotics

- **SayCan** (Ahn et al., 2022) — LLM proposes actions, affordance model reranks based on visual environment
- **Inner Monologue** (Huang et al., 2022) — adds environment feedback to action planning, but [[react]] argues it lacks true "inner reasoning"

### Conversational

- **BlenderBot**, **Sparrow** — chatbots that make API calls as part of dialogue
- **SimpleTOD** — task-oriented dialogue with API integration

## The Thought-Action-Observation Loop

The pattern introduced by [[react]] has become the standard architecture for tool-using agents:

```
Thought → Action → Observation → Thought → Action → Observation → ...
```

This loop is the foundation of agent frameworks like LangChain, AutoGPT, and similar systems. The key insight: **reasoning guides tool selection, and tool outputs ground reasoning**.

## Key Tradeoffs

| Aspect | Pure Reasoning (CoT) | Pure Acting | Reasoning + Acting (ReAct) |
|--------|---------------------|-------------|---------------------------|
| Hallucination | High | Medium | Low |
| Reasoning flexibility | High | Low | Medium |
| External grounding | None | Yes | Yes |
| Interpretability | Medium | Low | High |

## Learning from Tool Use

A key development is agents that **learn from failed tool interactions**. [[reflexion]] showed that verbal self-reflection after failures enables agents to improve across trials without any weight updates. This addresses the "error recovery" challenge by converting failures into episodic memory that guides future attempts.

## Open Challenges

- **Tool selection at scale** — choosing the right tool from a large toolbox
- **Error recovery** — handling failed tool calls gracefully (partially addressed by [[reflexion]])
- **Multi-step planning** — complex tasks requiring long chains of tool use
- **Cost/latency** — each tool call adds latency and token cost
- **Safety** — preventing harmful actions in real environments

## References

- [[react-synergizing-reasoning-and-acting]]
- [[reflexion-verbal-reinforcement-learning]]
