# 0004 — Defer Dark Mode Support

## Status

Accepted

## Context

`design.md` does not require dark mode; `roadmap.md`'s Phase 4 (Refinement)
is the intended home for improvements like this once the core design
language is stable. This was explicitly discussed with the user during
planning as one of two confirmed Phase 1 scope decisions.

## Decision

Ship Phase 1 with a single light theme only. No dark mode toggle, no
`prefers-color-scheme` handling.

## Rationale

The design language (typography, spacing, color) has not yet been validated
through real use. Supporting a second theme now would double the design-token
and contrast-testing surface before the primary (light) direction is settled
— working against "optimize for today's clarity, not tomorrow's complexity"
(`development.md`).

## Alternatives Considered

- **Build dark mode from day one** — rejected because it adds design and
  testing surface without a demonstrated need, before the light theme itself
  has been validated.

## Consequences

If dark mode is requested later, color usage will need to be revisited —
e.g., introducing CSS custom properties or Tailwind's `dark:` variant for
the colors currently hard-coded as Tailwind slate utilities. Not a breaking
change, but not yet designed for.
