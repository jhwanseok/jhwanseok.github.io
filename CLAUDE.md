# CLAUDE.md

# Project Overview

This repository is part of **Project HS**, a long-term initiative to build a trusted AI engineering brand through public engineering evidence.

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
- `docs/playbook/writing-rules.md` (execution rules and pre-publish checklist for every article/project page; read before writing or editing one)

These documents should guide implementation decisions.

## Decisions

Records the reasoning behind significant architectural and technology decisions, as ADRs (Architecture Decision Records).

- `docs/decisions/`

Read relevant ADRs before revisiting a decision that has already been made. If new information overturns a past decision, add a new ADR rather than silently deviating from it.

Not every implementation detail needs an ADR. Record one when a decision is significant, hard to reverse, or involved real alternatives — following the same `Observe → Establish → Document` workflow used for Project-Specific Conventions below.

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

## Review Article Tone

Established through the first review article (Sommelier, `src/pages/articles/sommelier-full-duplex-audio-preprocessing.md`) and encoded into `.claude/commands/review-article.md`. Revised 2026-08-30 after an audit found the 12 published articles had converged on one rigid skeleton (identical section count, repeated headings, a shared opening formula) that read as machine-generated; the user pointed at jiho-ml's weekly-nlp series and Daangn's engineering blog as the target feel. Sommelier and `skill-experiment-claude-md-management` were rewritten to the revised standard as the reference implementations.

- **The six roles are roles, not a heading template.** `docs/playbook/content.md` lists Summary → What Problem? → Engineering Decisions → Trade-offs → Production Perspective → My Takeaways. Do not turn these into exactly six `##` sections with a `---` between each. Fold a short "What Problem?" into the summary; merge "Trade-offs" and "Production Perspective" when they are one thought. The section count should differ per article. `---` dividers are for a genuine scene change, once or twice in a whole piece, not between every section.
- **Never reuse another review's heading text.** `## 남은 숙제` (was in 11 of 12 articles), `## 실제 서비스에 놓고 보면` (7 of 12), `## 공짜로 얻은 건 없다` / "공짜" in a trade-off heading (4 articles) — all banned. A heading is a sentence that states that section's actual conclusion, specific to this article.
- **Stock phrasings to avoid** (each was repeated across many articles and is what made them feel generated):
  - The opening's thesis-declaration sentence: "이 리뷰는 X가 무엇을 하는지 설명하는 데서 그치지 않고, …에 초점을 맞춘다." The opening closes on the *direction* of the result; what the review focuses on is shown by the body, not announced.
  - The empathy hook "…해본 사람이라면 (한 번쯤 부딪히는 벽 / 익숙한 불안)이 있다."
  - `#### 얻은 것: …` / `#### 잃은 것: …` as a matched heading pair. Write trade-offs as prose.
  - A section-closing blockquote that restates the section's lesson in one line. `blockquote` is for a real quote from the source or a figure caption only.
  - "진짜 질문은 A가 아니라 B다" / "X가 아니라 Y다" repeated as a rhetorical move.
- **`####` subheadings are rationed: at most 3 per section, each with 2–3+ paragraphs under it.** A section chopped into 10–12 one-paragraph `####` blocks reads as a bullet list, not an argument — this is the concrete cause of the "논리가 튄다" complaint. If paragraphs are only held together by "그런데 / 다만 / 즉 / 한편", the logic isn't actually connected; rewrite rather than paper over it. Default to flowing prose with no subheadings.
- **Voice is a warm 합니다체**, the register of jiho-ml's weekly-nlp: address the reader, pose questions and resolve them in the body, let first-person and honest reactions ("저는 이 대목에서 의아했습니다") show throughout — not only in the takeaways section. Subheadings state a conclusion, not a label ("오디오만으로 밀어붙이면 어디서 무너지는가", not "배경"). This is friendly, not casual — the `docs/playbook/content.md` bans on buzzwords/slang/clickbait still hold.
- **The opening section is a narrative hook, not a recap.** 기승전결: open with a situation or question the reader has met, build up why it is genuinely hard, turn to the reviewed work's core insight, close on the direction of the quantified result — but do not spend the conclusion in the opening. State a number, keep "how it got there" for the body.
- **Use an original diagram when a visual materially helps readers unfamiliar with the source.** Do not copy figures directly from the reviewed paper/blog (copyright risk, and it undercuts the "interpretation, not summary" goal). Redraw the core concept as an original SVG (see Diagram Palette below), store it under `public/images/articles/`, and place it in the opening section.

## Korean Prose Style

All Korean prose in this repo follows the `fluent-korean` style. Established 2026-08-30 by a full pass over every file in `src/pages/articles/` (the `23d845a` commit had already applied the em-dash part to `src/pages/projects/` skill series #0–3); the user asked for it to hold going forward on this project.

- **Register is a warm 합니다체**, not the `-다` declarative of a paper (decided 2026-08-30 alongside the Review Article Tone revision). Address the reader as "여러분", ask questions and answer them in the body, and let first-person perspective and honest reactions show. Friendly, not casual: buzzwords, slang, and clickbait still stay out. Reference tone: jiho-ml's weekly-nlp series. Applies to articles and project pages alike.
- **No em dashes (`—`) in body prose, headings, or `<abbr title="…">` text.** Replace each per context: a colon for an appositive/expansion, a connective for a logical link, or split into two sentences. When splitting, restore any subject or particle the dash was eliding — do not leave a bare fragment.
- **An inserted `A — B — C` aside becomes parentheses** (`A(B)C`) or a `, 즉 …` / `, 곧 …` clause.
- **No dashes in `title:` frontmatter or SVG text either.** Revised 2026-09-30: the user found the `—` in titles and diagram labels awkward, so the earlier exemption for a `[시리즈 라벨] 제목 — 부제: 세부` title shape was dropped. Titles now use `[시리즈 라벨] 주제: 핵심 문장, 보충구` with a single colon. See `docs/playbook/writing-rules.md` §3.
- **Sentences end on a 서술어 + 종결어미**, not a noun phrase or connective ending (headings and list items are exempt).
- **Prefer plain words over figurative ones in body prose** (e.g. 고정하다 over 못박다). Headings may stay creative per Review Article Tone. Keep metaphors already idiomatic in Korean technical writing (줄다리기, 디딤돌).
- Does not apply to code, code comments, or quoted source text.

## Article Reading Layout

`src/layouts/ContentLayout.astro` renders every article and project page. Adjusted 2026-08-30 in the same pass as the Review Article Tone revision, to move the reading experience away from "generated report" and toward "long-form blog post".

- **No automatic section numbering.** An earlier version prefixed every `##` with `01`–`06` via a CSS counter. Removed: on articles that all share a six-section skeleton, the leading-zero numbers amplified the "filled-in template" impression. Section headings are plain text now.
- **Body text is `slate-700`** (was `slate-600`), the lead paragraph after a heading `slate-800`. The mid-gray body over a white ground read as low-commitment and cold.
- **`####` is `17px` (matches body), not `15px`.** A subheading smaller than the body text it introduces gave the hierarchy no landmarks. Fewer, larger subheadings (see Review Article Tone's rationing rule) over many small ones.
- **Section separation is lighter**: `h2` uses `border-slate-100` with `mt-14`, `hr` uses `mt-12` (both were `mt-16`, `h2` border was `slate-200`). Combined with dropping the mandatory `---` between sections, this stops the page from reading as a stack of disconnected chapters.
- **Article `h1` is `text-3xl`** (was `text-2xl`) so the title clearly outranks the body on entry.

## Site Accent Color

The site's base palette is white + Tailwind `slate` (established before this convention existed — see `src/layouts/BaseLayout.astro`, `src/layouts/ContentLayout.astro`) and stays that way — this is about the one accent color layered on top of it, not a base-palette change.

- **Coral is the one accent color for the whole site**, registered as a custom Tailwind theme color in `src/styles/global.css` (`coral-50/100/300/500/600/700`, base `#e34a33`). Ramp: `coral-50`/`coral-100` (tint backgrounds), `coral-300` (borders, light accents), `coral-500`/`coral-600` (text, highlight strokes, left-accent bars), `coral-700` (darkest, for text on light coral fills).
- **Superseded indigo** (previously documented here). Indigo was reverted because it read as generic AI/SaaS blue-violet and didn't function as a real "point color" — it was too close in temperature to the slate base to actually pop. The user asked explicitly for the kind of single ownable brand color portals use (Kakao yellow, Naver green, Karrot orange): a color that contrasts in *temperature*, not just hue, against a cool gray base. Coral/orange was chosen for that warm-against-cool contrast. If indigo utility classes turn up anywhere in `src/`, that's leftover from before this change — replace with the coral equivalent.
- **Use it sparingly, as a "pay attention here" signal — not as decoration.** Current uses: (1) the hero node in an SVG pipeline/architecture diagram (see Diagram Palette), (2) the left border of a `blockquote` callout (`src/layouts/ContentLayout.astro`), (3) the translucent background on `<mark>` inline emphasis in article prose. Do not use it for body text color, links, or backgrounds outside a diagram's tint fill — the base palette stays monochrome slate/white per `docs/playbook/design.md`'s Visual Restraint principle.
- **A five-color warm/earthy palette (steel-blue, vanilla-custard, bone, faded-copper, rusty-spice) was proposed and rejected** for the base site: several swatches fail WCAG contrast against white (steel-blue 2.70:1, vanilla-custard ~1.1:1, bone ~1.3:1 — all below the 4.5:1 text / 3:1 non-text minimums), and a multi-hue/gradient palette for the *base site* contradicts the single-accent, Visual Restraint direction above. (Multiple pastel hues are fine in diagrams specifically — see below — the restriction is on the site's own chrome and prose.)
- **Inline highlight emphasis uses raw HTML.** Markdown has no native highlight syntax; write `<mark>...</mark>` directly in article `.md` files for the one claim per paragraph that most needs to stand out — it renders as a translucent coral wash behind the text, not an underline (an earlier version used `<u>` with a colored underline stroke; replaced because a full-text highlight reads more clearly than a thin colored line). Keep it rare: at most one per paragraph, at most one in the whole opening section, and most paragraphs should have none. The 2026-08-30 audit found articles with four `<mark>`s in the first four paragraphs and project pages with two in a single paragraph — that is the failure mode to avoid. If a passage feels like it needs several, the prose isn't doing the work.

### Diagram Palette

Reference: [Kakao Tech — "음성 AI 모델을 프로덕션에 올리기까지"](https://tech.kakao.com/posts/821), whose architecture diagrams are the model for this style — a warm cream canvas, soft rounded pastel boxes color-coded per component, thin warm-brown connector lines, bold/dark two-tier text (bold title + muted subtitle) per box. This replaced an earlier flat white-canvas/slate-only diagram style that read as generic and cold.

- **Canvas background is warm cream (`#fdf6ec`), not white.** This applies to the diagram image only — the site page background stays white.
- **Default/neutral steps** use a near-white warm fill (`#fffaf4`) with a soft warm-gray-tan border (`#e7dfd3`) and near-black warm text (`#292524`) — not slate. Cool grays clash visibly against the cream canvas.
- **All box subtitles share one muted warm brown (`#8a7f72`)** regardless of the box's own accent color, for a consistent "supporting text" voice across the whole diagram (matches the Kakao reference).
- **A small number of pastel accent colors mark specific component roles** — unlike site prose (coral-only), a diagram is allowed several hues at once, the way the Kakao reference gives Thinker/memory/Talker/Queue each their own color. Current semantic roles, reusing the same hue-per-meaning system from before (only the primary swapped from indigo to coral):

| Role | Color | Fill (tint) | Border | Text |
| --- | --- | --- | --- | --- |
| Default / neutral step | warm neutral | `#fffaf4` | `#e7dfd3` | `#292524` |
| Primary highlight — the one thing to notice | coral | `#e34a33` (solid, "hero" fill) or `#ffe4de` (pale lead-in tint) | `#c13a26` / `#ffab91` | white on solid; `#c13a26` on pale tint |
| Positive / improved outcome (e.g. a pipeline's destination, before→after gains) | emerald | `#10b981` (solid) or `#ecfdf5` (pale tint) | `#059669` / `#6ee7b7` | white on solid; `#059669` on pale tint |
| Trade-off / limitation / caution / processing-heavy step | amber | `#fef3c7` | `#fcd34d` | `#92400e` |
| Connector lines / arrows | warm brown | — | `#b3a08c` stroke | — |

Only use amber/emerald when a diagram actually needs that meaning (a comparison, an outcome, a caution) — don't add them decoratively to a diagram with nothing to compare. `sommelier-pipeline.svg` is the reference implementation: a pale-coral step leads into a solid-coral "hero" step (겹침 분리, the paper's key differentiator), an amber step marks the costliest stage (앙상블 ASR), and the pipeline's destination is solid emerald (the positive outcome of following the whole pipeline).

A five-color warm/earthy alternative (steel-blue, vanilla-custard, bone, faded-copper, rusty-spice) was considered and rejected for the *base site* — wrong temperature against slate/white there, and most swatches fail contrast against white. That rejection does not apply to diagrams, which now intentionally use a warm multi-pastel palette on a cream canvas.

### Animated Diagrams

A diagram may animate itself when the idea being explained *is* a progression over time — parallel streams advancing together, one stream leading another by a fixed offset, a quantity accumulating across layers. See ADR 0008 for why this is allowed and what the Visual Restraint section in `design.md` does and does not govern.

- **The default is still static.** Motion has to carry something the static frame cannot. A pipeline whose steps merely happen in order does not qualify — order is already legible from left-to-right arrows, and animating it just adds movement to a diagram that was already clear. When in doubt, ship static; a reader can re-read a static figure at their own pace, and cannot slow down an animated one.
- **One self-contained SVG under `public/images/articles/`, inserted with ordinary Markdown image syntax** — same as any other diagram. Per ADR 0007 articles are plain Markdown with no component imports, so the file renders through `<img>`. That blocks JavaScript but runs CSS keyframes and SMIL, so put the `<style>` block inside the SVG itself. Do not reach for a JS-driven stepper; that would mean reversing ADR 0007.
- **`@media (prefers-reduced-motion: reduce)` is mandatory, and its resting state must be authored deliberately.** Disabling the animation must leave a diagram that still reads — usually the final frame, or all states shown at once. Do not let it fall through to the 0% keyframe, which is often blank. `design.md`'s Accessibility section treats this as part of the engineering, not a nicety.
- **Loop slowly and completely — roughly 6–12s per cycle, repeating indefinitely.** A one-shot animation starts on page load, not on scroll, so a reader who arrives at the figure later sees only a frozen end state. Fast loops read as a busy GIF and pull the eye away from the prose beside them.
- **Animate at most four sequential states in one figure.** Beyond that the reader has to hold too much in memory between cycles — split into two diagrams, or fall back to a static filmstrip (several frames of the same flow stacked, each highlighting the step that changed). The filmstrip remains the right choice whenever sequence matters but continuity does not.
- **Animation changes nothing about the palette.** Same cream canvas, same role-per-hue system, same warm-brown connectors as above. Motion is an additional channel, not a reason to introduce new colors.

## Glossary Tooltips

Acronyms, dataset names, and model/tool names a general engineering reader won't know (e.g. DER, ROVER, Fisher, Switchboard, Sortformer) get a hover/focus definition instead of being left unexplained or breaking prose flow with a parenthetical every time.

- **Mechanism is pure CSS, no JS.** Write `<abbr title="짧은 한국어 설명" tabindex="0">TERM</abbr>` directly in article `.md` files. `src/layouts/ContentLayout.astro` renders the `title` as a small dark popover above the term on `:hover`/`:focus` via `content: attr(title)`; the native browser title tooltip is kept as a fallback (screen readers, no-CSS contexts), not suppressed.
- **Only tag a term's first mention in the article.** Repeat mentions later in the same piece stay plain text — tagging every occurrence would carpet the article in dotted underlines and defeat the "doesn't hurt readability" goal this was built for.
- **Never use `<abbr>` inside a `<table>` cell.** The table's own `overflow-x: auto` (see Diagram Palette's sibling rule in `ContentLayout.astro`) clips an absolutely-positioned popover that tries to render above/below a cell. Tag the term at its first mention in the surrounding prose instead — `sommelier-full-duplex-audio-preprocessing.md` does this for "DER": tagged with `<abbr>` in the sentence introducing the Pyannote/Sortformer comparison table, left as plain text inside the table's own header row. If a term only ever appears inside a table with no prose mention at all, expand it as a plain parenthetical in the sentence introducing the table instead of using `<abbr>`.
- **Keep definitions to one short phrase.** `attr()` renders plain text only (no line breaks, no formatting) into a `max-w-64` popover — write a single clause, not a sentence with its own sub-clauses.

## Commit Staging

Established when committing the tts-sentence-preprocessor Projects entry (2026-08-07): the working tree had pre-existing, unrelated uncommitted changes (a `docs/playbook/design.md` edit and a new `docs/decisions/0008-...` ADR, both from an earlier, separate piece of work) sitting alongside the actual task's changes.

- **Stage files explicitly by path, never `git add -A` / `git add .`.** Bundling unrelated uncommitted work into a commit makes that commit's diff misrepresent what it's actually about, and risks pushing changes the user hasn't reviewed as part of the current task.
- **When unrelated uncommitted changes exist in the working tree, leave them unstaged and tell the user explicitly what was excluded and why**, rather than silently including them or silently discarding them. The user commits those separately when ready.

This applies every time a commit is made in this repo, not just when something unrelated happens to be sitting in the working tree — check `git status` before staging and confirm every staged file is actually part of the current task.

## Publish-Day Dating

Established 2026-08-31 after the AudioLM (#3) and VALL-E (#4) reviews shipped carrying `2026-08-08` placeholder dates, which sorted them behind the already-published prologue and speech-tokens entries and scrambled the series order on the blog. `.github/workflows/check-dates.yml` enforces this on every push.

- **A page's `date:` frontmatter must equal the day it is first committed.** Drafts under `src/pages/articles/` and `src/pages/projects/` sit untracked with placeholder dates while being written, and those dates are almost always stale by the time the piece ships. In the same change that first adds a page to git (it shows as `??` in `git status`, not `M`), set its `date:` to today's date. This is a mandatory pre-commit step, not a nicety.
- **Keep the `Thh:mm:ss` time suffix and use it for ordering.** When several sibling pages publish together, give each a later time than the previous one (e.g. `T11:00:00`, `T12:00:00`) so the intended reading order survives the blog's date sort.
- **Editing an already-committed page does NOT change its `date:`.** Re-dating a live article re-sorts it to the top of the blog for what is only a copy edit. Leave the original publish date alone.
- When asked to "publish" or "commit" a batch of drafts, re-date every one of them in the working tree first, then commit — sequentially, one page per commit, if their relative order matters.

---

# Decision Hierarchy

When making decisions, follow this order:

1. Constitution
2. Playbook
3. Existing architecture, including recorded decisions in `docs/decisions/`
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