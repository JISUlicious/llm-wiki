---
title: Activity Log
type: log
created: 2026-04-05
updated: 2026-04-12
---

# Activity Log

Chronological record of wiki operations. Newest entries first.

---

## [2026-04-12] ingest | Dense Passage Retrieval for Open-Domain Question Answering

Ingested `sources/DPR Karpuhkin 2020 2004.04906.pdf`. Pages created: [[dense-passage-retrieval-for-open-domain-question-answering]], [[dense-passage-retrieval]]. Pages updated: none. Key takeaways: DPR shows that a simple BERT dual-encoder with strong negatives can beat BM25 on open-domain QA retrieval and materially improve end-to-end QA accuracy.

## [2026-04-12] ingest | GPT-4 Technical Report

Ingested `sources/GPT-4 Tech report 2303.08774.pdf`. Pages created: [[gpt-4-technical-report]], [[gpt-4]]. Pages updated: [[overview]]. Key takeaways: GPT-4 extends the GPT line to multimodal input, emphasizes predictable scaling and RLHF-based safety work, and withholds core architecture details while reporting strong benchmark performance.

## [2026-04-12] ingest | Language Models are Few-Shot Learners

Ingested `sources/GPT-3 Brown 2020.pdf`. Pages created: [[language-models-are-few-shot-learners]], [[gpt-3]], [[in-context-learning]]. Pages updated: [[gpt-1]], [[gpt-2]], [[generative-pretraining]], [[overview]]. Key takeaways: GPT-3 shows that very large autoregressive models can adapt from prompt context alone across zero-, one-, and few-shot regimes; the paper also foregrounds contamination and misuse risks.

## [2026-04-12] ingest | Language Models are Unsupervised Multitask Learners

Ingested `sources/GPT-2 2019 language_models_are_unsupervised_multitask_learners.pdf`. Pages created: [[language-models-are-unsupervised-multitask-learners]], [[gpt-2]]. Pages updated: [[generative-pretraining]], [[gpt-1]], [[overview]]. Key takeaways: GPT-2 shows that scaling decoder-only language models yields strong zero-shot transfer across many tasks; the model still underfits WebText, pointing to further gains from scale.

## [2026-04-12] ingest | Improving Language Understanding by Generative Pre-Training

Ingested `sources/GPT_1_OpenAI_2018.pdf.pdf`. Pages created: [[improving-language-understanding-by-generative-pre-training]], [[gpt-1]], [[generative-pretraining]]. Pages updated: [[bert]], [[overview]]. Key takeaways: GPT-1 establishes decoder-only autoregressive pre-training plus discriminative fine-tuning as a strong transfer recipe; task-aware input transformations let one model compete across many NLP tasks.

## [2026-04-12] ingest | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

Ingested `sources/BERT Devlin 1810.04805.pdf`. Pages created: [[bert-pre-training-of-deep-bidirectional-transformers]], [[bert]], [[masked-language-modeling]]. Pages updated: [[overview]]. Key takeaways: BERT makes bidirectional Transformer pre-training practical through masked language modeling and next sentence prediction; a single fine-tuned model then reaches state of the art across a wide range of NLP tasks.

## [2026-04-12] ingest | Attention Is All You Need

Ingested `sources/Transformar Vaswani 1706.03762.pdf`. Pages created: [[attention-is-all-you-need]], [[transformer-architecture]], [[self-attention]]. Pages updated: [[overview]], [[palm]], [[functional-emotions]], [[activation-steering]]. Key takeaways: the paper replaces recurrence with attention-only encoder/decoder stacks; self-attention yields short dependency paths, much better parallelization, and state-of-the-art translation performance at lower training cost.

## [2026-04-12] ingest | Agentic AI and the next intelligence explosion

Ingested `sources/Agentic AI and the next intelligence explosion.md`. Pages created: [[agentic-ai-and-the-next-intelligence-explosion]], [[agentic-ai]], [[society-of-thought]]. Pages updated: [[reflexion]], [[tool-use-in-llms]], [[overview]]. Key takeaways: the essay argues that the next intelligence explosion will be plural and social rather than monolithic; future capability and alignment hinge on recursive delegation, human-AI institutions, and internal/external collective reasoning.

## [2026-04-05] ingest | Emotion Concepts and their Function in a Large Language Model

Ingested `sources/emotion-concepts-anthropic-2026.md` (fetched from https://transformer-circuits.pub/2026/emotions/index.html). Pages created: [[emotion-concepts-anthropic-2026]], [[functional-emotions]], [[emotion-vectors]], [[activation-steering]], [[anthropic]], [[claude-sonnet]], [[chris-olah]]. Pages updated: [[overview]] (added interpretability/alignment theme). Key takeaways: LLMs form internal linear representations of emotion concepts that causally influence alignment-relevant behavior; desperation drives misalignment while calm suppresses it; post-training shifts emotional profiles toward low-arousal, introspective states.

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
