# 0005 — Deploy via GitHub Actions to GitHub Pages

## Status

Accepted

## Context

The repository is named `jhwanseok.github.io`, which is the naming
convention GitHub requires for a User/Organization Pages site. The site is
fully static (no backend), which GitHub Pages serves natively.

## Decision

Build the Astro static output with GitHub Actions using the official
`withastro/action`, and deploy it to GitHub Pages using
`actions/deploy-pages`, triggered on every push to `main`.

## Rationale

The repository name already commits this project to GitHub Pages hosting.
Using the official Astro GitHub Action keeps the workflow minimal and
framework-maintained rather than hand-rolling a build/deploy script.

## Alternatives Considered

- **Netlify / Vercel** — offer more hosting features (deploy previews,
  serverless functions), but add an external hosting dependency that isn't
  needed for a static site and doesn't match the `<user>.github.io` hosting
  already committed to by the repository name.

## Consequences

The site can only serve static assets. Any future feature that needs a
server (e.g., a contact form backend) will require a separate service
outside this deployment pipeline — see `0003-defer-content-collections.md`
and the Contact page decision to use `mailto:`/profile links instead of a
form, for the same reason.
