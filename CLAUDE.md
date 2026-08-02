# CLAUDE.md

# Project Overview

This repository is part of **Project JH**, a long-term initiative to build a trusted AI engineering brand through public engineering evidence.

The goal of this repository is not simply to build software, but to create maintainable engineering work that demonstrates real-world engineering capability.

Before making implementation decisions, understand both the project's identity and its execution principles.

---

# Read Before Coding

Read these documents in order before making significant changes.

## Constitution

Defines the project's identity and long-term direction.

- `docs/constitution/vision.md`
- `docs/constitution/brand.md`
- `docs/constitution/product.md`

## Playbook

Defines how this project is implemented.

- `docs/playbook/development.md`
- `docs/playbook/design.md`
- `docs/playbook/content.md`
- `docs/playbook/roadmap.md`

These documents should guide implementation decisions.

---

# Working Principles

## Optimize for Today's Clarity

Always prefer solutions that are clear, understandable, and maintainable today.

Avoid introducing complexity for problems that do not yet exist.

Design for current requirements first.

---

## Build Only What Is Needed

Introduce infrastructure, abstractions, libraries, or technologies only when they solve an existing problem.

Do not prepare for hypothetical future requirements.

Let the architecture evolve through real implementation rather than anticipation.

When uncertain, choose the simpler solution.

---

## Respect the Existing Architecture

Before making changes:

- Understand the current implementation.
- Preserve consistency across the project.
- Prefer small, incremental improvements.
- Avoid unnecessary rewrites.

Architecture should evolve, not be replaced.

---

## Documentation Is Engineering

Documentation is part of the implementation.

When introducing meaningful changes, consider whether the related documentation should also evolve.

Engineering decisions should leave evidence.

---

## Explain Important Decisions

When introducing architectural or technical changes:

- Explain why the change is necessary.
- Describe important trade-offs.
- State assumptions when appropriate.

Implementation should remain understandable by future contributors.

---

# Working Workflow

For every non-trivial task:

1. Understand the request.
2. Read the relevant documentation.
3. Review the existing implementation.
4. Present an implementation plan.
5. Explain important trade-offs and assumptions.
6. Wait for confirmation when architectural decisions are involved.
7. Implement the approved solution.
8. Summarize the completed work.
9. Suggest documentation updates if new conventions have emerged.

---

# Planning Before Coding

Do not immediately begin implementation.

First:

- Understand the problem.
- Explain the proposed approach.
- Identify trade-offs.
- Highlight assumptions.

Implementation begins only after the approach is understood.

---

# Project-Specific Conventions

This section intentionally starts small.

Implementation-specific conventions should only be added after they become established through actual development.

Examples include:

- Directory structure
- Astro conventions
- Component organization
- Naming conventions
- Styling rules
- Testing strategy
- Deployment workflow

Do not define speculative conventions.

Follow this workflow:

> Observe → Establish → Document

---

# Decision Hierarchy

When making decisions, follow this order:

1. Constitution
2. Playbook
3. Existing architecture
4. Project-specific conventions in this document

Higher levels always take precedence.

---

# Collaboration

Treat the user as the technical lead.

Do not make significant architectural decisions independently.

Provide recommendations.

Explain trade-offs.

Ask questions when requirements are unclear.

Prefer discussion over assumptions.

---

# Final Principle

This project values thoughtful engineering over rapid implementation.

Take time to understand before making changes.

Prioritize understanding over assumptions.

Prefer thoughtful decisions over quick solutions.

Leave the project in a better state than you found it.