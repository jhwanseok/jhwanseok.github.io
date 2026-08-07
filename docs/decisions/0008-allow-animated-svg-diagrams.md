# 0008 — Allow Self-Animating SVG Diagrams in Articles

## Status

Accepted

## Context

A planned article series on Speech Language Models needs to explain concepts
whose subject matter *is* a time axis — parallel speech/text streams in a
full-duplex model, the alignment offset between a text stream and the audio
stream it precedes, residual quantization accumulating across codebook
layers. A static diagram can show the end state of these, but not the
progression that is the actual point being explained.

This surfaced an apparent conflict inside `docs/playbook/design.md`:

- **"Motion has purpose"** permits animation that communicates state
  changes, and forbids only animation whose purpose is visual novelty.
- **"Visual Restraint"** lists "Excessive animations" and "Auto-playing
  visual effects" among visual elements to avoid.

Two facts resolved the conflict rather than deepening it.

**First, the prohibition was never an observed decision.** `git log -S "Auto-playing
visual effects"` returns exactly one commit — `94f7490 docs: establish
project foundation`, the initial bootstrap that created all eight
constitution and playbook documents at once, before any page, article, or
diagram existed. No incident, discussion, or ADR sits behind it. It is a
generic default carried in with the scaffolding. `CLAUDE.md` explicitly
warns against exactly this class of rule: "Do not define speculative
conventions", to be replaced through `Observe → Establish → Document`.

**Second, the two rules address different scopes.** The Visual Restraint
list sits alongside "decorative 3D effects", "unnecessary glassmorphism",
and "busy backgrounds" — all properties of *interface chrome*. The same
document's Design Philosophy names the other scope directly: "Design exists
to support the content. Projects, technical writing, **architecture
diagrams**, and documentation should always remain the primary focus." A
diagram is not chrome competing with the content; it is the content. Visual
Restraint governs the interface around the article, and "Motion has purpose"
governs the figures inside it.

There is also a technical constraint worth recording. ADR 0007 keeps
articles as plain Markdown with no component imports, so a diagram is
inserted as `![alt](/images/articles/{slug}.svg)`, which renders through an
`<img>` element. An SVG referenced by `<img>` runs no JavaScript, but does
run CSS keyframes and SMIL, and does evaluate `prefers-reduced-motion`
against the user's system setting. Animation is therefore available with no
new infrastructure and no change to ADR 0007.

## Decision

Allow article diagrams to animate themselves, as a single self-contained SVG
file under `public/images/articles/`, inserted with ordinary Markdown image
syntax.

Constraints, recorded in full in `CLAUDE.md` under "Diagram Palette":

- Motion must carry meaning the static frame cannot. A diagram whose
  animation only draws attention to an otherwise static structure should
  stay static.
- CSS keyframes or SMIL only — no JavaScript, which `<img>` blocks anyway.
- A `@media (prefers-reduced-motion: reduce)` block is mandatory, and must
  leave the diagram readable in a meaningful resting state rather than
  blank.
- The loop must be slow and complete (roughly 6–12s), and must not rely on
  the reader catching a one-shot animation they may have scrolled past.

Also amend `docs/playbook/design.md` so the Visual Restraint list states the
scope it actually governs, and stop the two sections from reading as a
contradiction for the next person.

## Rationale

The alternative — keeping the prohibition — would preserve a rule nobody
chose in order to avoid a problem nobody has had, at the cost of the one
capability the planned series most needs. `CLAUDE.md`'s "Build Only What Is
Needed" argues against speculative infrastructure; the same reasoning argues
against speculative prohibitions.

Clarifying the scope is preferable to deleting the Visual Restraint bullets.
The concern behind them is real for interface chrome, where auto-playing
motion genuinely does compete with reading. Narrowing the rule keeps that
protection while removing a restriction it was never meant to impose.

## Alternatives Considered

- **Static filmstrip — one SVG containing several frames of the same flow,
  each with the changed element highlighted.** Rejected as the *default*,
  not as a technique: it requires no rule change and remains the right
  choice for most pipeline diagrams, but it consumes vertical space in
  proportion to the number of steps and communicates sequence rather than
  continuity. Still expected to be the common case; this ADR only removes
  the prohibition on the other case.
- **JavaScript stepper component with reader-controlled playback.** Best
  reader experience — explicit play/pause, no motion until requested. Rejected
  because it requires importing a component into Markdown, which ADR 0007
  rules out, and would mean reversing that decision for a need that a
  self-contained SVG already meets.

## Consequences

Diagrams gain a failure mode static images do not have: a broken keyframe or
a missing reduced-motion fallback degrades to a blank or frozen figure
rather than a wrong one. The reduced-motion resting state must therefore be
authored deliberately, not left to whatever the animation's 0% frame happens
to be.

Readers get no playback control. If a future diagram genuinely needs
play/pause or step-through — likely if a single figure ever has to carry
more than about four sequential states — that is the trigger to revisit
ADR 0007, since the constraint would then be the no-components rule rather
than this one.
