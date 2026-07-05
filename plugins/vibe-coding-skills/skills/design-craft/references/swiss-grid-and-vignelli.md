# Swiss grid + Vignelli craft

Original notes (authored for this kit) distilling the public design principles of **Josef
Müller-Brockmann** (*Grid Systems in Graphic Design*, 1981) and **Massimo Vignelli** (*The Vignelli
Canon*). These are widely-taught principles, restated here in web terms. No third-party skill files
are reproduced — this is our own working summary.

> The single move that most separates "a studio designed this" from generic-sans slop: **a sans
> display + a mono annotation register**, on a real grid, with **data set large**.

## 1. Grid + rhythm
- **Modular grid.** 12 columns + an **8px baseline** is a robust web default. Place elements by
  column *line* (e.g. `1 / 6`, `6 / 13`), don't eyeball spans. Text and media occupy whole modules.
- **Baseline rhythm is sacred.** Line-heights and vertical spacing are whole multiples of the baseline
  (px for display type, so large glyphs stay on the line). Media heights = multiples of the leading so
  top and bottom both land on lines.
- **Tight outside margins create tension; wider margins create calm.** Gutters ~one line of type.
- **Asymmetry held by the grid.** Generous white space — "it is the white that makes the black sing."

## 2. Typography
- **Two type sizes per page, big jumps.** Hierarchy through **scale + weight + space**, not color or
  novelty faces. Heading ≈ 2× body minimum; push the display size for power.
- **Flush-left, ragged-right.** Justified is contrived; centered only for lapidary text.
- **Display sans + mono register.** A grotesque/humanist sans for headlines and body; a **monospace
  (IBM Plex Mono, Space Mono) for kicker labels, section folios (01/02/03), captions, stat labels,
  and the footer.** The mono caps reinforce a technical, editorial register and instantly de-default
  the page.
- **Data set large.** Key numbers/stats are a signature move — set them big as the visual event, with
  a small mono label beneath. (Count them up on reveal for motivated motion.)
- **Optical alignment.** A large headline's *box* on the grid line still looks off because the
  glyph's ink is inset by its side-bearing. For hero/display type, nudge the box left by the measured
  side-bearing so the **ink**, not the box, lands on the line. (Box-on-grid ≠ ink-on-grid.)

## 3. Color
- One accent, used as a **signifier** (CTA, emphasis), not decoration. Source the palette from
  something concrete (the brand, a logo, a photo) so it has a reason. Primary/structural neutrals you
  actually chose — never stock slate or stock cream-by-default.

## 4. Discipline (the intangibles)
- **Semantics first** — find the essence before drawing. **Appropriateness** — "listen to what the
  thing wants to be." **Visual power through contrast of scale**, never loudness. **Timelessness** over
  trend. "If you see the layout, it is probably a bad layout."
- No sloppiness: one spacing scale, one radius scale, aligned edges, real content lengths tested.

## 5. Motion (motivated only)
- Motion communicates state or guides attention: count-ups on real data, a single staggered reveal,
  a condensing sticky header, hover that signals interactivity. Never the same fade bolted on every
  section (that's an AI tell). Always honor `prefers-reduced-motion`.

## Quick checklist
- [ ] Real grid + baseline rhythm (not arbitrary margins)
- [ ] Sans display + **mono** kicker/folio/caption register
- [ ] Stats/data set **large** with small mono labels
- [ ] Flush-left, two sizes, big scale jump
- [ ] One sourced accent; chosen neutrals
- [ ] White space generous; layout invisible
- [ ] Motion motivated + reduced-motion safe
