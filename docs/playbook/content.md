# Content Playbook

> Write to contribute, not to impress.

---

# Purpose

This document defines how technical content should be written and published within this project.

The goal is to create engineering content that is practical, trustworthy, and valuable to other engineers.

Content should prioritize knowledge sharing over personal promotion.

---

# Content Philosophy

Every article should help readers better understand an engineering problem, an implementation approach, or a technical decision.

The purpose of writing is to contribute useful engineering knowledge, not to demonstrate expertise.

If readers learn something practical, the content has achieved its purpose.

---

# Writing Principles

## Evidence over opinion

Support technical decisions with reasoning, experiments, benchmarks, or practical experience whenever possible.

Avoid making claims without explanation.

---

## Explain the "why"

Do not only describe what was built.

Explain:

- Why the problem matters.
- Why this solution was chosen.
- What alternatives were considered.
- What trade-offs were accepted.
- What was learned.

Engineering decisions are often more valuable than implementation details.

---

## Be practical

Prioritize content that readers can apply in their own work.

Whenever appropriate, include:

- Code examples
- Architecture diagrams
- Configuration examples
- References
- Lessons learned

---

## Be honest

Document both successes and failures.

If something did not work, explain why.

Engineering credibility comes from transparency rather than perfection.

---

## Prefer clarity over completeness

A clear explanation of one important idea is more valuable than a comprehensive explanation that is difficult to follow.

Avoid unnecessary complexity.

---

# Content Categories

The primary content categories include:

- AI Engineering
- Voice AI
- LLM Applications
- System Architecture
- Production Engineering
- AI Evaluation
- Observability
- Engineering Experiments
- Engineering Notes

These categories may evolve alongside the project.

An article or project may cite more than one category as tags, when its content genuinely spans them — see ADR 0009. Tag values should still come from this list rather than ad hoc terms, so the vocabulary stays controlled.

---

# Article Structure

While not every article must follow the same structure, most technical articles should include:

1. Problem
2. Context
3. Solution
4. Trade-offs
5. Results
6. Lessons Learned

The structure should make it easy for readers to understand both the implementation and the reasoning.

---

# Review Article Structure

Some articles review external technical material — a blog post, a paper, or a conference talk — rather than describing original work. These articles should still interpret, not introduce.

The goal is to explain how the reviewed material's engineering decisions apply to real systems, not to summarize what it says.

Review articles should cover these six roles, usually in this order:

1. Summary
2. What Problem?
3. Engineering Decisions
4. Trade-offs
5. Production Perspective
6. My Takeaways

These are roles, not a heading template. Do not map them one-to-one onto six `##` sections: a short "What Problem?" can fold into the summary, and "Trade-offs" and "Production Perspective" can share a section when they are one line of thought. The number of sections should vary from article to article. Reusing another review's heading text (`## 남은 숙제`, `## 실제 서비스에 놓고 보면`, `## 공짜로 얻은 건 없다`) is a form of the Unnecessary repetition the Writing Style section rules out — see `.claude/commands/review-article.md` for the concrete list of stock phrasings to avoid.

This structure differs from the general Article Structure above because the source material already documents the problem and solution. The value of a review article is in the interpretation layered on top of it: what was gained and lost by the reviewed design, what it means for a production system, and what the author would carry forward into their own work.

Every review article must cite what it reviews. Link back to the original source(s) — paper, blog post, repository, talk — so the reader can always find and verify what is being interpreted. Place these links near the top of the article, before the interpretation begins.

---

# Writing Style

The writing style should be:

- Professional
- Technical
- Direct
- Clear
- Evidence-based

Avoid:

- Clickbait titles
- Marketing language
- Buzzwords without explanation
- Overly casual writing
- Unnecessary repetition — within an article, and also *across* articles. Reusing the same section headings, the same opening sentence pattern, or the same "gained / lost" sub-structure from one piece to the next makes the whole body of work read as machine-generated. Each article's structure should follow that article's actual content.

Write with the assumption that the audience consists of fellow engineers.

## Korean prose

Korean prose in this repo uses a warm 합니다체 — the register of an experienced engineer explaining something to a peer, not a paper's `-다` declarative. Address the reader ("여러분"), ask questions and answer them in the body, and let first-person perspective and honest reactions show. This is "friendly", not "casual": buzzwords, slang, and clickbait stay out. The reference tone is jiho-ml's weekly-nlp series. See `CLAUDE.md`'s "Korean Prose Style" section for the mechanical rules (no em dashes, sentences end on a 서술어, etc.).

---

# Publishing Checklist

Before publishing, ask:

- Is the problem clearly explained?
- Is the reasoning behind decisions documented?
- Does the article provide practical value?
- Is the content technically accurate?
- Would another engineer find this useful in six months?

If the answer is "no" to any question, revise the article.

---

# Evolution

Writing quality improves through continuous practice.

This playbook should evolve as new writing patterns emerge, but the focus should remain on clarity, practicality, and engineering value.