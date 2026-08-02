# 0002 — Choose Tailwind CSS for Styling

## Status

Accepted

## Context

`design.md` states that "consistency builds trust" and calls for consistent
layouts, spacing, and typography throughout the site. Without some form of
centralized design tokens, that consistency depends entirely on manual
discipline across every page and component. Two options were discussed with
the user: Tailwind CSS, or plain CSS with custom properties.

## Decision

Adopt Tailwind CSS (v4) for styling, integrated via `@tailwindcss/vite`. Tailwind
v4 is configured CSS-first — there is no `tailwind.config.mjs`; utilities are
enabled via `@import "tailwindcss";` in `src/styles/global.css`.

## Rationale

- Utility classes make consistent spacing/typography/color trivial to apply
  and enforce across pages, without hand-rolling and maintaining a custom
  design-token system.
- Integration with Astro is minimal (`astro add tailwind`), and Tailwind's
  JIT compiler only ships the CSS actually used, keeping output small.

## Alternatives Considered

- **Plain CSS with custom properties** — zero additional dependency, which
  would have aligned more directly with `development.md`'s "avoid unnecessary
  dependencies." Rejected because consistency would then rely purely on
  manual discipline rather than being enforced by tooling, which is a higher
  long-term maintenance risk for a project expected to grow.

## Consequences

- Adds two dependencies: `tailwindcss` and `@tailwindcss/vite`.
- Future styling should use Tailwind utility classes rather than new
  hand-written CSS files, unless a specific case can't be expressed with
  utilities.
