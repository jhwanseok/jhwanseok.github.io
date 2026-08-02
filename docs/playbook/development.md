# Development Playbook

> Build software that is easy to understand, maintain, and evolve.

---

# Purpose

This document defines how software should be developed within this project.

It provides implementation guidelines to ensure consistency, maintainability, and long-term quality.

When implementation choices are unclear, prefer the simplest solution that aligns with the project's vision and product goals.

---

# Development Principles

## Optimize for today's clarity, not tomorrow's complexity.

Design for current requirements.

Avoid speculative abstractions.

Introduce complexity only when it solves an existing problem.

---

## Simplicity over cleverness

Prefer code that is easy to understand over code that is technically impressive.

Future maintainability is more valuable than short-term optimization.

---

## Components over duplication

Extract reusable components only when reuse is proven.

Do not abstract after the first implementation.

Wait until patterns naturally emerge.

---

## Readability first

Code is read far more often than it is written.

Optimize for readability.

Choose descriptive names.

Keep functions focused.

Reduce unnecessary nesting.

---

## Incremental improvement

Prefer small improvements over large rewrites.

Each commit should leave the project in a better state.

---

# Architecture Guidelines

- Keep components small and focused.
- Separate presentation from business logic.
- Avoid unnecessary dependencies.
- Prefer composition over inheritance.
- Keep the folder structure intuitive.

---

# Technology Principles

Frameworks are tools.

The architecture should remain understandable even if the framework changes.

Avoid framework-specific solutions unless they provide significant value.

---

# Performance

Optimize only after identifying real bottlenecks.

Prioritize:

1. Correctness
2. Readability
3. Maintainability
4. Performance

Premature optimization should be avoided.

---

# Git Workflow

Prefer small, focused commits.

Each commit should represent a logical unit of work.

Commit messages should clearly describe intent rather than implementation details.

---

# Documentation

Documentation is part of development.

When adding a feature, consider whether its behavior, architecture, or rationale should also be documented.

Engineering decisions should leave evidence.

---

# Decision Checklist

Before implementing a feature, ask:

- Does this solve a real problem?
- Is this the simplest solution?
- Will another engineer understand this in six months?
- Does this align with the project vision?
- Does this introduce unnecessary complexity?

If any answer is "no", reconsider the implementation.

---

# Evolution

This playbook should evolve alongside the project.

Development practices may change as experience grows, but simplicity, clarity, and maintainability should remain the foundation.