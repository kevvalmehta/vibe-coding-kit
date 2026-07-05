# Layout Skeletons — a bank of section shapes that don't read as AI

The single strongest AI tell is the **skeleton**: centered hero → three feature cards → centered
CTA, every section a centered stack. No scanner catches it reliably, so we prevent it at
composition time: **every section in DESIGN-SPEC.md must name a skeleton from this bank** (or a
deliberate custom one, described). Two adjacent sections may not use the same skeleton.

Grid ground rules (from `swiss-grid-and-vignelli.md`): 12-col grid, flush-left type, scale-driven
hierarchy, white space as protagonist, mono register for eyebrows/folios/captions, data as large
numerals. All skeletons below assume those.

Column notation: `[7|5]` = 12-col split, 7 columns + 5 columns.

## Heroes (pick ONE)

### H1 — Editorial split hero `[7|5]` or `[8|4]`
Left: mono eyebrow → display headline (clamp 3.2–5.5rem) → one-sentence dek → left-aligned CTA
pair (solid + text-arrow). Right: the owner's real photo in a composed frame, slightly
overlapping the section boundary below. Asymmetry is the point.

### H2 — Full-bleed cinematic
Real photo full-bleed with a single-direction gradient scrim (one direction only, to ink — never
purple, never radial). Text block pinned to a grid column, NOT centered. Mono kicker + display
line + CTA. Best for stage/performance shots.

### H3 — Type-led hero (no image)
Display headline spanning 10–12 cols at very large scale, dek on cols 7–11 (offset, not under it),
thin rule, mono meta-line (city · role · availability). For when no strong hero photo exists —
type IS the image. Never fill the gap with a fake person or stock.

### H4 — Split with proof rail
`[7|5]` hero where the right column is a vertical rail of 2–3 large numerals with mono labels
(count-up motion candidate). The proof is the hero.

## Body sections (assign one per section of the agreed copy/content)

### B1 — Numbered editorial index (replaces "3 feature cards")
Services/offers as a numbered list: `01` mono folio → service name at display size → 1-line
description right-aligned on its own column → hairline rule between rows. Row hover: arrow slides,
background tints 3%. Feels like a studio's index page, scales 2–6 items.

### B2 — Alternating photo rows
Real photo `[6]` + text `[5]` (1-col gutter), alternating sides each row. Photos share ONE
treatment (frame/duotone). Text: mono eyebrow → h3 → short body → text-arrow link. Never more
than 3 rows.

### B3 — Stat band (data-large)
Full-width band (ink or brand-dark background): 3–4 numerals at 4–6rem with mono labels beneath,
flush-left within their columns, generous vertical padding. The ONLY safe dark-band section; use
once.

### B4 — Quote spread
One testimonial as a spread: oversized quotation mark or 2px accent rule → quote at 1.6–2.2rem on
cols 2–9 → attribution as mono line with a small real photo. One strong quote beats a 3-card
testimonial carousel every time.

### B5 — Sticky-rail chapter
Long content (about, process): left rail (cols 1–4) sticky with mono chapter label + h2; right
(cols 5–12) scrolls through the body. Editorial-magazine feel; use for ONE long section max.

### B6 — Logo/credibility strip
Single row of grey-scaled logos or a mono text-line of credentials ("Keynotes: Optica · SXSW ·
TEDx") between hero and first body section. Height ≤ 120px; optional marquee if > 6 items.

### B7 — Offset CTA block
Final CTA as `[8|4]`: statement headline left, CTA button + mono contact details right, top
hairline rule. NOT a centered "Ready to get started?" box. May sit on a 4–6% accent-tinted
background.

### B8 — FAQ / detail accordion
Flush-left rows, mono numbering, hairline rules, plus/minus rotates 45° on open (`--ease-out`).
No card borders, no shadow boxes.

## Footers

### F1 — Designed-object footer
Footer as a real composition: display-size wordmark or invitation line spanning the grid, columns
of mono links below, bottom line with © + mono folio. The footer is the last impression — a
3-link centered footer reads abandoned.

## Banned skeletons (auto-reject at self-critique)

- Centered hero + 3 icon-cards + centered CTA (in any order).
- Any grid of ≥ 3 identical cards with icon-top, title, text (use B1 or B2).
- Carousel/slider for testimonials (use B4).
- Two or more consecutive centered-stack sections.
- Full-width centered text sections repeated down the page ("wall of centers").

## How to use this file

1. In DESIGN-SPEC.md, map every page section from the agreed copy/content to a skeleton ID
   (`hero: H1`, `services: B1`, …) with a one-line reason.
2. Vary: adjacent sections must differ; a page should use ≥ 3 distinct body skeletons.
3. Real photos beat icons in every skeleton. Missing photo → labelled placeholder composed
   INSIDE the skeleton's frame (keep the composition; label the gap).
