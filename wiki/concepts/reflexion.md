---
title: Reflexion
type: concept
created: 2026-04-05
updated: 2026-04-12
sources:
  - "Reflexion Shinn 2023 2303.11366.pdf"
  - "Agentic AI and the next intelligence explosion.md"
tags:
  - reinforcement-learning
  - self-reflection
  - agents
  - memory
  - learning
status: complete
importance: high
---

# Reflexion

**Reflexion** is a framework for teaching LLM agents to learn from their mistakes through **verbal self-reflection** rather than weight updates. Introduced by [[noah-shinn]] et al. (2023), it extends agent paradigms like [[react]] by adding a trial-and-error learning loop with episodic memory.

## Core Idea

Traditional RL requires expensive finetuning. Reflexion instead uses natural language as the medium for reinforcement:

1. Agent attempts a task and fails
2. A self-reflection model analyzes the failure in natural language
3. The reflection is stored in an episodic memory buffer
4. On the next trial, the agent conditions on its past reflections

The reflections act as **"semantic gradients"** — richer than scalar rewards, providing concrete, actionable directions for improvement.

## Architecture

```
┌─────────────┐
│   Actor      │ ← CoT, ReAct, or other action generator
│   (Mₐ)       │
└──────┬───────┘
       │ actions
       ▼
┌─────────────┐      ┌──────────────────┐
│ Environment  │─────▶│   Evaluator      │
│              │ obs  │   (Mₑ)           │
└─────────────┘      │ binary/scalar/LLM │
                     └──────┬───────────┘
                            │ reward signal
                            ▼
                     ┌──────────────────┐
                     │ Self-Reflection   │
                     │   (Mₛᵣ)          │
                     │ "I failed because │
                     │  I searched for X │
                     │  instead of Y..." │
                     └──────┬───────────┘
                            │ verbal reflection
                            ▼
                     ┌──────────────────┐
                     │ Episodic Memory   │
                     │ [sr₀, sr₁, sr₂]  │
                     │ (sliding window)  │
                     └──────────────────┘
                            │ context for next trial
                            ▼
                     ┌─────────────┐
                     │   Actor      │ (next trial)
                     └─────────────┘
```

### Three Components

| Component | Role | Implementations |
|-----------|------|----------------|
| **Actor** ($M_a$) | Generates text and actions | [[react]], [[chain-of-thought-prompting\|CoT]], direct generation |
| **Evaluator** ($M_e$) | Scores outputs | Binary reward, heuristics, LLM-as-judge, self-generated unit tests |
| **Self-Reflection** ($M_{sr}$) | Generates verbal feedback | LLM prompted with trajectory + reward |

### Memory

- **Short-term**: current trajectory (actions, observations)
- **Long-term**: episodic buffer of past reflections (bounded, usually 1-3 entries)
- The Actor conditions on both at inference time

## Key Results

| Task | Baseline | Reflexion | Improvement |
|------|----------|-----------|-------------|
| ALFWorld (decision making) | ~75% (ReAct) | 97% (130/134) | +22% |
| HotpotQA (reasoning) | ~34% (CoT) | ~54% | +20% |
| HumanEval Python (coding) | 80.1% (GPT-4) | 91.0% | +11% |
| LeetCode Hard Python | 7.5% (GPT-4) | 15.0% | +7.5% |

## Why It Works

The critical finding: **retry without reflection doesn't help**. Baseline approaches (ReAct, CoT) show zero improvement across trials with temperature sampling alone. The verbal reflection step is what bridges error identification to actionable improvement.

Two types of learning observed in ALFWorld:
1. **Immediate correction** — early mistakes in long trajectories are easily identified; agent suggests a new action
2. **Systematic exploration** — agent exploits memory over several trials to methodically search rooms it hasn't fully explored

## Relationship to Other Concepts

- **Extends [[react]]** — uses ReAct as the Actor, adds learning-from-failure on top
- **Contrasts with Self-Refine** (Madaan et al., 2023) — Self-Refine does single-pass iterative refinement without episodic memory; Reflexion maintains memory across trials
- **Verbal RL** — positions itself as an alternative to gradient-based RL: lighter weight, more interpretable, no finetuning needed
- **Credit assignment via language** — LLMs can do credit assignment ("action 3 was wrong because...") that scalar rewards cannot

## Limitations

- May converge to local minima — verbal optimization is still optimization
- Self-generated test quality bounds coding performance (false positive tests → premature termination)
- Memory bounded by context window — sliding window of 1-3 reflections
- Relies on LLM self-evaluation capability — no formal guarantee of success

## Impact

Reflexion demonstrated that LLM agents can learn from experience without any weight updates, making it a key paper in the [[agentic-ai]] paradigm. The trial-reflect-retry loop has been adopted widely in agent frameworks and influenced subsequent work on self-improving systems.

Later synthesis work such as [[agentic-ai-and-the-next-intelligence-explosion]] frames this kind of memory-enabled retry loop as a building block for larger agent ecologies, where performance depends not only on single-agent competence but also on delegation, role structure, and coordination.

## References

- [[reflexion-verbal-reinforcement-learning]]
- [[react-synergizing-reasoning-and-acting]]
