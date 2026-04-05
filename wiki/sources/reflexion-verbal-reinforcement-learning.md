---
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
type: source
created: 2026-04-05
updated: 2026-04-05
sources:
  - "Reflexion Shinn 2023 2303.11366.pdf"
tags:
  - reinforcement-learning
  - self-reflection
  - agents
  - code-generation
  - reasoning
status: complete
importance: high
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

**Source**: `sources/Reflexion Shinn 2023 2303.11366.pdf`
**Authors**: [[noah-shinn]], Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, [[shunyu-yao]]
**Affiliations**: Northeastern University, MIT, Princeton University
**Published**: arXiv 2303.11366 (2023)

## Summary

This paper introduces [[reflexion]], a framework for reinforcing language agents through **verbal self-reflection** rather than weight updates. When an agent fails a task, it generates a natural language reflection analyzing what went wrong, stores it in an episodic memory buffer, and uses that memory to improve on subsequent trials. This converts sparse scalar/binary feedback into rich "semantic gradients" — actionable verbal feedback that guides improvement.

The framework is modular with three components:
1. **Actor** ($M_a$): generates text and actions (can be [[chain-of-thought-prompting|CoT]], [[react]], etc.)
2. **Evaluator** ($M_e$): scores outputs (binary reward, heuristics, LLM-as-judge, or self-generated unit tests)
3. **Self-Reflection model** ($M_{sr}$): generates verbal feedback stored in long-term memory

The agent iterates: generate trajectory → evaluate → reflect → retry with memory of past reflections. Memory is bounded (usually 1-3 reflections) to fit context limits.

## Key Results

### Decision Making: ALFWorld (134 tasks)

| Method | Success Rate |
|--------|-------------|
| [[react|ReAct]] (baseline) | ~75% (converges trial 6-7) |
| **ReAct + Reflexion** | **97% (130/134)** |

- +22% absolute over ReAct baseline across 12 iterative trials
- Eliminates the common "phantom possession" error where agents think they hold items they don't
- Learning curve: immediate spike after first reflection, then steady improvement over 11 more trials
- ReAct-only converges at 22% hallucination rate with no recovery

### Reasoning: HotpotQA (100 questions)

| Method | Accuracy |
|--------|----------|
| CoT (baseline) | ~34% |
| ReAct (baseline) | ~30% |
| **Reflexion + CoT** | **~54%** |
| **Reflexion + ReAct** | **~50%** |

- +20% over baselines; baseline approaches show **zero** improvement on retry without reflection
- Ablation: episodic memory alone (just including last trajectory) helps some, but self-reflection adds 8% absolute on top

### Programming: Code Generation

| Benchmark | Previous SOTA | GPT-4 | Reflexion |
|-----------|--------------|-------|-----------|
| HumanEval (Python) | 65.8 (CodeT) | 80.1 | **91.0** |
| HumanEval (Rust) | — | 60.0 | **68.0** |
| MBPP (Python) | 67.7 (CodeT) | **80.1** | 77.1 |
| MBPP (Rust) | — | 70.9 | **75.4** |
| LeetCode Hard (Python) | — | 7.5 | **15.0** |

- 91% pass@1 on HumanEval — surpasses GPT-4's 80%
- Uses self-generated unit tests as the Evaluator
- Key limitation: false positive test suites (tests pass but code is wrong) cap performance — MBPP has 16% FP rate vs. 1.4% for HumanEval
- Language-agnostic: works for both Python (interpreted) and Rust (compiled)

## Key Claims

1. Verbal self-reflection is more effective than blind retry — agents without reflection show zero improvement across trials
2. Self-reflection acts as "semantic gradients" — richer than scalar rewards, enabling targeted improvement
3. The framework is modular — any Actor (CoT, ReAct), any Evaluator (binary, heuristic, LLM, unit tests), any reflection model
4. Episodic memory of reflections is key — bounded sliding window (1-3 entries) balances context length vs. learning
5. Self-generated unit tests enable pass@1-eligible code evaluation without ground truth test cases
6. Trial-and-error with reflection is a lightweight alternative to finetuning or RL with gradient descent

## Ablation Findings

- **Without self-reflection** (just retry): no improvement over baseline
- **Without test generation** (code tasks): performance drops below baseline (52% vs. 60%) — agent can't determine correctness
- **Without verbal explanation** (just test feedback): no improvement — error identification alone isn't enough without reflection bridging it to implementation fixes
- **Episodic memory vs. reflection**: reflection adds 8% absolute over just including the last trajectory

## Limitations (Acknowledged)

- May converge to local minima — verbal optimization is still optimization
- Memory limited to sliding window; future work could use vector DBs or SQL
- Code generation: non-deterministic functions, API-dependent functions, and concurrency are hard to test
- Self-generated test quality bounds overall performance (false positives are the bottleneck)

## Entities Mentioned

- [[noah-shinn]] — First author, Northeastern University
- [[shunyu-yao]] — Co-author, Princeton University (also first author of [[react]])
- Karthik Narasimhan — Co-author, Princeton (also on ReAct)

## Concepts Discussed

- [[reflexion]] — The core framework introduced in this paper
- [[react]] — Used as the Actor for decision-making tasks
- [[chain-of-thought-prompting]] — Used as the Actor for reasoning tasks
- [[tool-use-in-llms]] — Broader paradigm Reflexion contributes to
- Self-Refine (Madaan et al., 2023) — related iterative refinement work, but limited to single-generation tasks without memory

## Notable Quotes

> "Reflexion converts binary or scalar feedback from the environment into verbal feedback in the form of a textual summary, which is then added as additional context for the LLM agent in the next episode."

> "This self-reflective feedback acts as a 'semantic' gradient signal by providing the agent with a concrete direction to improve upon."

## References

_Original source: `sources/Reflexion Shinn 2023 2303.11366.pdf`_
