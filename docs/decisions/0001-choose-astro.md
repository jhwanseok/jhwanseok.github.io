# 0001 — Choose Astro as the Web Framework

## Status

Accepted

## Context

Phase 1 (Foundation) needed a framework for a content-first personal engineering
portfolio (Home / About / Projects / Articles / Resume / Contact), deployed as a
static site on GitHub Pages. `development.md` states that "frameworks are tools"
and that the architecture should remain understandable even if the framework
changes. `CLAUDE.md`'s Project-Specific Conventions section already listed
"Astro conventions" as an example category, signaling that this project was
expected to build on Astro.

## Decision

Adopt Astro, with TypeScript in strict mode, as the site framework.

## Rationale

- The site is overwhelmingly static, long-form content (articles, project
  write-ups) rather than an interactive application. Astro's island
  architecture ships zero JavaScript by default, which keeps the site fast
  and accessible without extra effort.
- Astro components, file-based routing, and content collections map directly
  onto the site's information architecture without requiring a client-side
  framework runtime.
- TypeScript strict mode supports "keep the project maintainable"
  (`development.md`) by catching type errors in component props and (later)
  content schemas at build time.

## Alternatives Considered

- **Next.js / React** — more capable than needed for a mostly-static site;
  ships a React runtime by default and encourages patterns (client components,
  hooks) that this project doesn't need yet.
- **Plain static HTML / Eleventy** — simpler and dependency-light, but weaker
  TypeScript and component-reuse ergonomics as the site grows.

## Consequences

- Pages and components follow Astro's `.astro` file model and file-based
  routing (`src/pages/`).
- Any future use of interactive UI (if ever needed) should go through Astro's
  islands rather than converting the whole site to a client-rendered app.
