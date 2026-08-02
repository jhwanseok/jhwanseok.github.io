# 0003 — Defer Astro Content Collections Until Real Content Exists

## Status

Accepted

## Context

`roadmap.md` places the project in Phase 1 (Foundation); no Articles or
Projects content exists yet. `development.md` states: "Optimize for today's
clarity, not tomorrow's complexity," and "Do not abstract after the first
implementation. Wait until patterns naturally emerge." The initial plan for
this phase included Astro Content Collections with a zod-validated frontmatter
schema for Articles/Projects; this was removed after user feedback that it
would be built ahead of any real content to validate it against.

## Decision

Do not introduce Astro Content Collections, zod schemas, or frontmatter
conventions in Phase 1. `/projects` and `/articles` are plain static
placeholder pages ("coming soon") with no content-management infrastructure
behind them.

## Rationale

Designing a content schema — frontmatter fields, collection structure,
Markdown vs. MDX — without any real article or project to validate it
against is a speculative abstraction. The right shape for that
infrastructure should be discovered from actual writing, not guessed in
advance.

## Consequences

When the first real article or project is written (Phase 2/3 per
`roadmap.md`), this decision should be revisited: introduce Content
Collections (or an equivalent) based on what that first piece of content
actually needs, rather than a schema designed in the abstract.
