# Premium Motion & Polish

Motion is where "AI-built" is most visible. Slop motion = the same `fade-in` wrapper on every
section, linear easing, and animation for its own sake. Premium motion = few moves, each one
*motivated* (it communicates something), physical easing, and restraint everywhere else.

This file is **copy-paste grade on purpose**: do not invent easing curves or observer boilerplate
from scratch — adapt these. They work in plain HTML/CSS/JS, Astro, and Next.js alike.

## The motion budget (hard rules)

1. **Max 3 named moves per site.** Every move gets a name and a reason in DESIGN-SPEC.md
   (e.g. "count-up on proof numerals — the stats ARE the argument"). No name+reason → cut it.
2. **Never the same entrance on every section.** One reveal system applied uniformly is the #1
   motion tell. Reveal *key* moments; let ordinary sections just be there.
3. **Always honor `prefers-reduced-motion`.** Non-negotiable — self-critique Q12 fails without it.
4. **Nothing moves that the user didn't cause or that doesn't inform.** Scroll and hover are
   causes. A hero that animates itself apart on load informs nothing.
5. **Durations:** micro-interactions 120–250ms; reveals 400–700ms; never > 900ms. Delays for
   stagger: 60–90ms steps, max ~5 steps.

## Easing tokens (put these in `:root`, use nothing else)

```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* expo-out: fast start, soft landing — reveals */
  --ease-inout: cubic-bezier(0.65, 0, 0.35, 1);   /* symmetric — position/layout shifts */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* slight overshoot — small UI only, never text */
  --dur-fast: 180ms;
  --dur-reveal: 600ms;
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

`ease`, `linear`, and `ease-in-out` keywords read as defaults. Only animate `transform` and
`opacity` (compositor-friendly); animating `top/left/width/height/margin` causes jank.

## The move library (pick ≤ 3, adapt, name them in the spec)

### 1. Staggered reveal — for ONE key sequence, not every section
Reveal the hero's elements in reading order, or the items of one editorial list. Nothing else.

```html
<section data-reveal-group>
  <p class="eyebrow" data-reveal>Keynote speaker</p>
  <h1 data-reveal>The line that earns the fee.</h1>
  <div class="hero-media" data-reveal>…</div>
</section>
```
```css
[data-reveal] { opacity: 0; transform: translateY(14px); }
.no-js [data-reveal], [data-reveal].is-in {
  opacity: 1; transform: none;
  transition: opacity var(--dur-reveal) var(--ease-out), transform var(--dur-reveal) var(--ease-out);
}
```
```js
document.documentElement.classList.remove('no-js');
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (!e.isIntersecting) continue;
    const items = e.target.matches('[data-reveal]') ? [e.target]
      : [...e.target.querySelectorAll('[data-reveal]')];
    items.forEach((el, i) => setTimeout(() => el.classList.add('is-in'), i * 80));
    io.unobserve(e.target);
  }
}, { threshold: 0.25 });
document.querySelectorAll('[data-reveal-group], [data-reveal]:not([data-reveal-group] [data-reveal])')
  .forEach((el) => io.observe(el));
```
Add `class="no-js"` to `<html>` so content is never invisible without JS.

### 2. Count-up numerals — when the data is the argument
Only on real stats (talks given, audiences reached, years). Fake stats are a copy crime, not a
motion choice.

```js
function countUp(el) {
  const target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || '';
  const t0 = performance.now(), dur = 900;
  (function tick(t) {
    const p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
    el.textContent = Math.round(target * eased).toLocaleString() + suffix;
    if (p < 1) requestAnimationFrame(tick);
  })(t0);
}
```
Trigger from the same IntersectionObserver. With reduced motion, set the final value immediately.

### 3. Condensing sticky header
The header shrinks (padding + logo scale) after ~80px of scroll. Communicates "you've left the
top; nav stays with you."

```js
const header = document.querySelector('header');
addEventListener('scroll', () => header.classList.toggle('is-condensed', scrollY > 80), { passive: true });
```
```css
header { transition: padding var(--dur-fast) var(--ease-inout), background var(--dur-fast) var(--ease-inout); }
header.is-condensed { padding-block: 0.6rem; background: color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter: blur(8px); }
```

### 4. Hover that communicates (micro-interactions — these are free, use everywhere)
Hover states are polish, not "moves" — they don't count against the budget, but they must be
consistent and instant-feeling (≤ 200ms).

```css
.link-arrow .arrow { display: inline-block; transition: transform var(--dur-fast) var(--ease-out); }
.link-arrow:hover .arrow { transform: translateX(4px); }

.card-photo img { transition: transform 500ms var(--ease-out); }
.card-photo:hover img { transform: scale(1.03); }   /* wrap img in overflow:hidden frame */

.btn { transition: transform var(--dur-fast) var(--ease-out), box-shadow var(--dur-fast) var(--ease-out); }
.btn:hover { transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
```
Every interactive element needs a hover AND a `:focus-visible` state. A site with zero hover
transitions feels dead ("rusted"); a site where cards lift 12px with glowing shadows feels AI.
The premium band is narrow: 1–4px movement, subtle, fast.

### 5. Image treatment as polish (zero-JS)
Premium feel is mostly *material*, not movement: give photos a consistent treatment — a frame,
a single-color duotone wash, a hard-edged crop with a mono caption — so they look art-directed.

```css
.frame { position: relative; overflow: hidden; }
.frame::after { content: ''; position: absolute; inset: 0; box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--ink) 14%, transparent); pointer-events: none; }
.frame img { display: block; width: 100%; height: 100%; object-fit: cover; }
```

### 6. Marquee / ticker strip — logos or credibility line (optional, counts as a move)
```css
.marquee { overflow: hidden; white-space: nowrap; }
.marquee-track { display: inline-block; animation: marquee 28s linear infinite; }
@keyframes marquee { to { transform: translateX(-50%); } }
.marquee:hover .marquee-track { animation-play-state: paused; }
```
Duplicate the content once inside the track for a seamless loop. Linear easing is correct here
(constant conveyor) — the one exception to the easing rule.

## Banned motion (auto-flagged or eyeballed in QA)

- The same fade/slide entrance on every section.
- Anything animating on page load before the user does anything (except the ONE hero reveal).
- Parallax backgrounds; scroll-jacking; tilt-on-hover cards.
- Spinning/pulsing icons; gradient shimmer text; typing-effect headlines.
- Animated blob/particle backgrounds.
- More than one thing moving at once in the viewport at rest.

## Pre-ship motion check (answer in the self-critique)

1. Can you name each move and what it communicates? (If not: cut.)
2. Scroll the whole page fast — does anything feel like a slideshow of fade-ins?
3. Toggle `prefers-reduced-motion` — is the site fully usable and complete?
4. Hover every link, button, card — does each respond within 200ms, subtly?
5. At rest (no input), is the page completely still (marquee excepted)?
