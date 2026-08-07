# 0009 — Multi-Value Tags Replace Single Category, Shared by Articles and Projects

## Status

Accepted

## Context

ADR 0007 gave Articles a single `category: string` frontmatter field, drawn
from the Content Categories list in `docs/playbook/content.md`, rendered as
one pill in `ContentLayout.astro` and `ContentList.astro`. Projects received
no equivalent field — only `description`, per that ADR's stated schema
(`title`, `date`, `description`).

With the second real article written — a Projects entry for
`tts-sentence-preprocessor` — two things became clear. First, real content
does not sit neatly under one Content Category: the Sommelier review is
about Voice AI, but its "Engineering Decisions" and "Production Perspective"
sections are just as much about System Architecture and Production
Engineering, and picking only one undersold how the site's own taxonomy is
meant to describe a piece of writing. Second, because Projects never had a
category-equivalent field at all, the first Projects entry had no topical
tag whatsoever, while the one Articles entry had exactly one.

## Decision

Replace `category?: string` with `tags?: string[]` in `ContentFrontmatter`
(`src/utils/content.ts`), and make the field common to both Articles and
Projects — previously only Articles had it.

- `ContentLayout.astro` (article/project page header) and `ContentList.astro`
  (`/articles`, `/projects` listings) map over `tags` and render one pill per
  entry instead of a single conditional pill.
- Values still come from the fixed Content Categories list in
  `docs/playbook/content.md` (AI Engineering, Voice AI, LLM Applications,
  System Architecture, Production Engineering, AI Evaluation, Observability,
  Engineering Experiments, Engineering Notes). An entry may now cite more
  than one, but not introduce ad hoc terms outside that list.
- `description` is unchanged and stays independent of `tags` — Projects keep
  it as their listing blurb; Articles may or may not use it.

## Rationale

A shared, plural field keeps Articles and Projects on one schema rather than
two diverging ones, consistent with ADR 0007's original intent of a single
`ContentLayout` with minimal per-type differences. The change itself is
small — widening an existing string field to a string array and mapping over
it instead of a single conditional render — so it doesn't warrant a new
component or a Content Collections schema.

Keeping values constrained to the documented Content Categories list, rather
than opening the field to freeform keywords, avoids a set of near-duplicate
tags accumulating across pages (e.g. "Voice AI" vs "voice-ai" vs "TTS"). This
mirrors the controlled-vocabulary approach the project already takes
elsewhere (e.g. the Diagram Palette's fixed semantic roles in `CLAUDE.md`).

## Alternatives Considered

- **Free-form per-article keywords** (e.g. "IPA", "G2P", "Diarization") were
  considered. They would make each piece of content searchable by more
  specific implementation terms, but risk drifting apart in phrasing over
  time and duplicate what the Content Categories taxonomy already covers at
  a coarser grain. Rejected in favor of the constrained list; revisit if the
  fixed taxonomy proves too coarse once there is more content to organize.
- **Adding a new `keywords` field alongside the existing `category`**,
  rather than replacing it, was also considered. Two overlapping fields —
  one singular, one plural, both drawn from the same taxonomy — would be
  redundant and require keeping both in sync on every entry. Rejected.

## Consequences

Any future Content Category should still be added to the list in
`docs/playbook/content.md` first, per existing convention, and may now be
attached to more than one Article or Project. If tag values start drifting
from the fixed list in practice, or the site needs user-facing tag
filtering/browsing, that is the trigger to revisit ADR 0007's original
consequences note and move to Content Collections with a zod-validated
schema, enforcing the taxonomy at build time instead of by convention.
