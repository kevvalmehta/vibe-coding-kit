# Self-Critique — the gate you run on YOURSELF before anyone else sees the page

Run this after composing the first screen/homepage concept and after building each page or
screen. It is mandatory. Look at the actual rendered page (screenshot or browser — not the
code) and answer every question honestly. **Score < 12/14 → fix and re-run. Never present a
failing page.** Record the final score + one-line answers (e.g. in `qa/self-critique-<page>.md`).

Before eyeballing, run the mechanical half (no judgment required, works on any model):

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/devibe_scan.py" <path-to-the-built-pages>
```

(The script lives at `plugins/vibe-coding-skills/scripts/devibe_scan.py` wherever this kit is
installed.) Fix every high-severity tell it reports first. Then score the 14 questions:

## Composition (look at the whole page zoomed out)

1. **Skeleton variety** — does the page match the skeleton map in DESIGN-SPEC.md, with no two
   adjacent sections shaped the same, and NO banned skeleton (centered hero + 3 cards, wall of
   centered stacks)?
2. **Asymmetry** — is there at least one strong asymmetric composition above the fold?
3. **Scale drama** — is the biggest type at least 3× the body size? Do numerals/data appear LARGE?
4. **White space** — is there at least one generous breathing area, or is everything evenly packed?

## Identity (would a stranger know whose site this is?)

5. **Not the median** — cover the logo: does anything remain that couldn't be any company's site?
6. **Locked accent** — is the accent used ONLY where the spec allows (CTA/hover/folio), with the
   brand anchor color doing the identity work?
7. **Type system** — are the spec's real fonts actually loading (check the network tab / @font-face),
   with the mono register present on eyebrows/folios/captions?
8. **Real photos** — are the owner's real photos placed and treated consistently? Are missing-asset
   placeholders composed inside the layout (labelled, but not wrecking the composition)?

## Motion & feel (interact with it)

9. **Named moves only** — can you name every motion on the page and its reason from the spec?
   Is anything moving that you can't name?
10. **No slideshow effect** — scroll fast top to bottom: does it feel composed, or like a sequence
    of fade-ins?
11. **Alive under the cursor** — hover every link/button/card: subtle, fast (≤200ms) response on
    all of them?
12. **Reduced motion** — with `prefers-reduced-motion`, is the page complete and still?

## Fidelity

13. **Copy 1:1** — does every section of the agreed copy/content (if one exists) appear, with no invented text, no
    dropped sections, headings verbatim?
14. **Nothing broken** — all images load, no placeholder strings (`PLACEHOLDER`, `lorem`,
    `example.com`) anywhere, form action is real or explicitly flagged?

## Scoring

- 14/14 → present it.
- 12–13 → fix the misses if fixable in this round, note the rest honestly, present.
- < 12 → do NOT present. Fix, re-render, re-run. If the same question fails twice, the design
  approach is wrong — go back to the skeleton map / spec, don't patch symptoms.

A model with weaker taste should trust the checklist MORE, not less: the questions encode the
judgment so you don't have to have it.
