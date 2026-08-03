# 0006 — Korean as the Default Website Content Language

## Status

Accepted

## Context

The site's audience (`brand.md`) includes AI/software engineers and technical
recruiters, without an explicit language requirement. So far, all pages
(Home, About, Projects, Articles, Resume, Contact) were written in English.
The user decided that the website itself should default to Korean, while
everything else about the repository — the repo itself, `docs/constitution/`,
`docs/playbook/`, `CLAUDE.md`, code, and commit messages — stays in English.

## Decision

Prose content — body copy, descriptions, and headings that introduce that
prose — across Home, About, Projects, Articles, Resume, and Contact is
written in Korean by default.

Global navigation labels, and the page-level labels that mirror them
one-to-one (`Home` / `About` / `Projects` / `Articles` / `Resume` /
`Contact`, used as both the `<Header>` nav items and each page's `<title>`),
stay in English. These function as wayfinding/category labels rather than
prose, and already match the English URL paths (`/about`, `/projects`,
etc.), so translating them would create a mismatch between what the label
says and what the URL/nav says.

Internationalization (i18n) is **not** introduced at this stage; an English
version of the prose content, if ever needed, will be added later as a
separate, explicit feature rather than built in now.

Repository-level material — this repo's own documentation
(`docs/constitution/`, `docs/playbook/`, `docs/decisions/`), `CLAUDE.md`,
source code (including comments/identifiers), and commit messages — remains
in English.

`<html lang="...">` in `BaseLayout.astro` is set to `ko` to match the
rendered content.

## Rationale

Splitting "engineering evidence infrastructure" (English, for the
engineering-artifact audience of this repo itself — other engineers reading
the code/docs) from "site content" (Korean, for the actual audience reading
the published pages) lets each side use its natural language without forcing
a premature i18n system before there's a second language to actually serve.

## Alternatives Considered

- **Build i18n now with English as primary** — rejected: no second-language
  content exists yet, so a routing/translation-key system would be
  speculative infrastructure (see `0003-defer-content-collections.md` for the
  same reasoning applied to content structure).
- **Bilingual single-page content** — rejected as unnecessarily complex for
  Phase 1 and inconsistent with `design.md`'s preference for clarity over
  completeness.

## Consequences

- All new prose copy going forward is written in Korean first.
- The six wayfinding labels (Home/About/Projects/Articles/Resume/Contact)
  stay in English everywhere they appear — nav, `<title>`, and the Home
  page's "What You'll Find Here"-style section links — even though the
  content beneath them is Korean.
- Proper nouns, URLs, and technical identifiers (e.g., "GitHub",
  email addresses, `/about`-style paths) remain unlocalized, which is
  standard practice in Korean technical writing.
- If an English version is added later, it will need an explicit i18n
  decision (routing strategy, content duplication approach) — not covered by
  this ADR.
