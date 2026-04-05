---
title: ReAct
type: concept
created: 2026-04-05
updated: 2026-04-05
sources:
  - "ReAct Yao 2022 2210.03629.pdf"
  - "Reflexion Shinn 2023 2303.11366.pdf"
tags:
  - reasoning
  - acting
  - prompting
  - agents
  - tool-use
status: complete
importance: high
---

# ReAct

**ReAct** (Reason + Act) is a prompting paradigm that interleaves **reasoning traces** and **task-specific actions** in LLM outputs. Introduced by [[shunyu-yao]] et al. (2022), it is one of the foundational approaches to [[tool-use-in-llms]] and LLM-based agents.

## Core Idea

Standard LLM prompting separates reasoning ([[chain-of-thought-prompting]]) from acting (action generation). ReAct unifies them: the model alternates between generating a **Thought** (free-form language reasoning that doesn't affect the environment) and an **Action** (a concrete step that produces an **Observation** from the environment).

The action space is formally augmented:

$$\hat{A} = A \cup L$$

where $A$ is the task-specific action space and $L$ is the space of natural language thoughts. A thought $\hat{a}_t \in L$ updates the agent's context without affecting the environment: $c_{t+1} = (c_t, \hat{a}_t)$.

## How It Works

A typical ReAct trajectory looks like:

```
Question: What is the elevation of the birthplace of the inventor of the telephone?

Thought 1: I need to find the inventor of the telephone, then find their birthplace,
            then find the elevation of that place.
Action 1:  Search[inventor of the telephone]
Obs 1:     Alexander Graham Bell invented the telephone...born in Edinburgh, Scotland.
Thought 2: The inventor is Alexander Graham Bell, born in Edinburgh. I need to find
            the elevation of Edinburgh.
Action 2:  Search[Edinburgh elevation]
Obs 2:     Edinburgh has an elevation of 47 metres (154 ft).
Thought 3: The elevation of Edinburgh is 47 metres. That's my answer.
Action 3:  Finish[47 metres]
```

## Types of Useful Thoughts

The paper identifies several types of reasoning that emerge in ReAct traces:

1. **Goal decomposition** — breaking tasks into subgoals
2. **Progress tracking** — noting what's been accomplished
3. **Exception handling** — adjusting plans when things go wrong
4. **Commonsense injection** — applying world knowledge to guide actions
5. **Information extraction** — pulling key facts from observations
6. **Search reformulation** — trying different queries when search fails
7. **Answer synthesis** — combining gathered information into a final answer

## Strengths

- **Reduces hallucination** — actions ground reasoning in external knowledge; ReAct had 0% hallucination failures vs. 56% for [[chain-of-thought-prompting|CoT]] on HotpotQA
- **Few-shot effective** — 1-6 in-context examples outperform methods trained on 10³-10⁵ examples
- **Interpretable** — humans can trace the reasoning and see which information came from where
- **General** — works across QA, fact verification, text games, web navigation
- **Controllable** — humans can edit thoughts mid-trajectory to correct the agent

## Limitations

- **Reasoning inflexibility** — the alternating structure constrains reasoning steps, leading to more reasoning errors than free-form CoT (47% vs. 16% on HotpotQA)
- **Repetitive loops** — the model sometimes gets stuck regenerating the same thought-action pairs
- **Search dependency** — 23% of failures come from uninformative search results
- **Prompt length** — complex tasks need more demonstrations, which can exceed context limits

## Best Practice: ReAct + CoT-SC

The paper's best results combine ReAct with CoT self-consistency:

- **ReAct → CoT-SC**: when ReAct fails to answer within N steps, fall back to CoT-SC
- **CoT-SC → ReAct**: when CoT-SC majority vote is low-confidence, fall back to ReAct

This uses internal knowledge when confident, external retrieval when not.

## Extensions

### Reflexion

[[reflexion]] (Shinn et al., 2023) uses ReAct as its Actor component and adds a **trial-and-error learning loop** with verbal self-reflection. When a ReAct agent fails, a self-reflection model analyzes the failure, stores the reflection in episodic memory, and the agent retries with that memory as context. This addresses ReAct's key limitations:

- **Repetitive loops**: Reflexion helps agents escape by reflecting on what went wrong
- **Search dependency**: agents learn from failed searches to reformulate queries in subsequent trials
- **Result**: ReAct + Reflexion achieves 97% (130/134) on ALFWorld, up from ~75% for ReAct alone

## Impact

ReAct is a foundational paper for the LLM agent ecosystem. It directly influenced frameworks like LangChain, AutoGPT, and subsequent work on [[tool-use-in-llms]]. The thought-action-observation loop became the standard pattern for LLM agents interacting with external tools and environments. [[reflexion]] further extended this by adding learning from failure.

## References

- [[react-synergizing-reasoning-and-acting]]
- [[reflexion-verbal-reinforcement-learning]]
