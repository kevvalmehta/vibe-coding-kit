# DESIGN-SPEC — <project name>

> The binding design contract for this build. Written by `/design-craft` BEFORE any markup,
> updated only with the owner's knowledge, read on every page/screen built, and re-checked by
> the tell scan + self-critique gate. If a design decision isn't in here, it isn't a decision —
> it's a default, and defaults are tells.
>
> Lives at `DESIGN-SPEC.md` in the project root (this is the quality-charter's
> "contract-before-work" pattern, applied to design).

## 1. Design read (3 sentences max)

Who this site must convince, of what, and the ONE feeling the design should leave.
Reference: <one real site/brand whose feel we follow, or a named direction — never "modern and clean">.

## 2. Dials

(From taste-skill §1 — 0–10.) VARIANCE: n · MOTION: n · DENSITY: n — with a one-line reason.

## 3. Machine block (keep valid JSON, so a script or a later QA step can parse it)

```json design-spec
{
  "palette": {
    "bg": "#F0EBE7",
    "ink": "#1E2A38",
    "brand": "#2A3E51",
    "accent": "#913314",
    "accent_rule": "CTA + hover + active folio only",
    "max_distinct_colors": 8
  },
  "fonts": {
    "display": "Figtree",
    "body": "Figtree",
    "mono": "IBM Plex Mono",
    "loading": "google-fonts",
    "banned_fallback_only": ["Inter", "system-ui", "Arial"]
  },
  "type_scale": { "display_max_px": 76, "display_min_px": 48, "body_px": 17 },
  "grid": { "columns": 12, "max_width_px": 1200, "baseline_px": 8 },
  "motion": {
    "budget": 3,
    "moves": [
      { "name": "hero-stagger-reveal", "why": "establishes reading order on the one key sequence" },
      { "name": "count-up-proof", "why": "the stats are the argument" },
      { "name": "condensing-header", "why": "orientation after leaving the top" }
    ],
    "reduced_motion": true
  },
  "skeletons": {
    "index": { "hero": "H1", "proof": "B3", "services": "B1", "about-teaser": "B2", "cta": "B7", "footer": "F1" }
  }
}
```

Skeleton IDs come from `references/layout-skeletons.md`; motion moves from
`references/premium-motion.md` (both inside the `design-craft` skill). Add one `skeletons.<page>`
entry per page/screen as it is designed.

## 4. Hero composition (the money shot, in words)

Which skeleton, which REAL photo or screenshot (file name from `assets/`), where the headline
sits, what the CTA says, what the one motion move is. Specific enough that a different model
could rebuild it. (For an app: the first screen a new user sees, described the same way.)

## 5. Photo treatment

The single treatment all photos/screenshots share (frame / duotone / crop style), and the list of
real assets available. Missing-asset plan: which sections get labelled placeholders, composed
inside the skeleton frame — never a fabricated person, never an unlabelled stock stand-in.

## 6. Deviations log

| date | what changed | why | approved by |
|------|--------------|-----|-------------|
