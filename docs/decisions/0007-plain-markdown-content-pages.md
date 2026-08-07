# 0007 — Plain Markdown Pages for Articles and Projects

## Status

Accepted

## Context

ADR 0003 deferred Astro Content Collections because no real Articles or
Projects content existed yet, and designing a frontmatter schema without
real content to validate it against would have been speculative. It also
stated the decision should be revisited "when the first real article or
project is written."

That trigger has arrived: a slash command is being introduced to author
review articles (reviews of external blog posts, papers, or talks) directly
into `/articles`. `/articles` and `/projects` are still plain static
placeholder pages with no listing or rendering logic behind them.

The frontmatter each content type actually needs turned out to be small and
different per type: Articles need `title`, `date`, `category` (from the
Content Categories in `content.md`); Projects need `title`, `date`,
`description`. Neither needs a zod-validated schema, MDX, or a query API —
just enough structure to list and render Markdown files that already exist
as plain files under `src/pages/`.

## Decision

Introduce a shared, minimal rendering layer instead of Astro Content
Collections:

- Plain `.md` files placed directly in `src/pages/articles/` and
  `src/pages/projects/` — Astro 7 routes these automatically with no
  additional integration.
- A single `ContentLayout.astro` used by both content types, which reads
  `Astro.props.frontmatter` and renders `category` (Articles) or
  `description` (Projects) as whichever is present.
- A shared `sortByDateDesc` utility and `ContentList.astro` component, used
  by both `articles/index.astro` and `projects/index.astro` to list and sort
  entries collected via `import.meta.glob`.

## Rationale

The frontmatter needs observed from real content are simple enough that a
zod schema and Content Collections query API would add structure the
project doesn't yet benefit from. A shared layout and listing component
give Articles and Projects consistent behavior without duplicating markup,
while staying at the complexity level the current content actually
requires.

## Consequences

If the number of articles/projects grows large enough that manual
`import.meta.glob` listing and lookup become unwieldy, or if frontmatter
requirements grow more complex (e.g., tags, related content, draft status),
this decision should be revisited in favor of Astro Content Collections —
at that point with real schema requirements to design against.
