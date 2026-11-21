# Profile README redesign: animated SVG cards

**Date:** 2026-11-21 · **Status:** approved and built

## Intent

Rebuild the profile README as a stack of animated SVG cards, in the manner of
[Avi Vashishta's profile](https://github.com/AviVashishta29) and
[his write-up](https://www.avivashishta.com/blog/github-profile-readme-animated-svg-cards).
Take his card architecture, animation grammar and font-embedding technique.
Do not take his content model.

## Why not a straight copy

Three of the five cards on that profile are GitHub activity metrics: a contribution
heatmap, a headline contribution count, and a streak column. Measured today this
account has **327 contributions, 0 stars across 9 repos, and 11 months of history**.
Rendered literally, those cards would publish a sparse heatmap, no streak worth
printing, and three repo cards reading zero stars. That is weaker than the README
being replaced, which leads with shipped client work GitHub does not measure.

So every card keeps its form and changes its input.

| Reference card | This profile |
|---|---|
| "8,398 contributions" | "50+ sites, live" |
| Blue contribution heatmap | existing `shipped.svg`, already 56 tiles of real shipped work |
| BUILD / BRAND / LEARN tiles | SHIPPED / RUNNING / LEARNING |
| Repo cards with star counts | same cards, star counts dropped |

## Approaches considered

1. **Full paper re-skin.** Cream cards and serif display type, closest to the
   reference. Rejected: `hero.svg`, `stack.svg` and `shipped.svg` would all be
   redrawn, discarding the isometric work that is the most distinctive thing here.
2. **Fix and animate only.** Embed fonts, enrich the existing three scenes, change
   nothing structurally. Rejected: does not deliver the card stack that was asked for.
3. **Existing palette, reference architecture.** *Chosen.* Keep indigo-on-dark and
   both isometric scenes; rebuild the page around them as an animated card stack.

## The page

```
+------------------------------------------------------+
|  HERO            name, kicker, one line, site link    |  rebuilt
+------------------------------------------------------+
|  SHIPPED FIELD   56 isometric tiles                   |  kept, retitled
+------------------------------------------------------+
|  NUMBERS         "50+ sites, live" + stat column      |  new
+------------------------------------------------------+
| SHIPPED  |  RUNNING  |  LEARNING   three linked tiles |  new, 32.5% each
+------------------------------------------------------+
|  STACK           six exploded layers                  |  kept
+------------------------------------------------------+
| roadmap  |  vincent  |  ipl        three repo cards   |  new, 32.5% each
+------------------------------------------------------+
|  link chips, unchanged                                |  kept
+------------------------------------------------------+
```

## Cards

| File | Content |
|---|---|
| `hero.svg` | Name in display serif. Kicker `WEB DEVELOPER @ VOCSY INFOTECH`. One line. Portfolio link with arrow. |
| `numbers.svg` | Headline `56 shipped`, captioning the field above it. Column: 2 live client stores · 26 months at Vocsy, intern to developer · about a day per build. |
| `tile-shipped.svg` | `50+ sites`. Blog network, WordPress, standardised base, every generated change reviewed. |
| `tile-running.svg` | `2 stores`. heliosexport.com and shop.sanmarfoods.com, live in production. |
| `tile-learning.svg` | `314 resources`. AI engineering curriculum rebuilt as a site you can work through. |
| `repo-*.svg` (3) | Language dot, repo name, one line, language label. No star counts. |

## Technical calls

These are mine unless corrected.

- **Fonts embedded, not referenced.** The current SVGs declare `ui-monospace, ...`,
  a system stack. GitHub serves SVG through `<img>`, which is sandboxed and cannot
  fetch fonts, so text renders in whatever the viewer has. `hero.svg` positions text
  by hand at 7.90px per character cell, so any viewer whose monospace differs sees
  it drift. Fixing this is the main correctness win of the whole job.
- **Two faces:** Instrument Serif for display numbers and the name, JetBrains Mono
  for labels. Both OFL. Embedded as base64 WOFF2 data URIs.
- **Subset per card, not once globally.** The reference subsets to printable ASCII,
  about 18 KB per face per file. Card text is known at render time, so each card
  embeds only the glyphs it actually draws, which is nearer 2 to 4 KB. Matters
  because the page loads eight images.
- **Animation:** CSS keyframes for entrances and shines, SMIL for anything CSS
  cannot do in SVG (number count-ups, gradient sweeps on text). Delays staggered so
  the page plays top to bottom. All of it inside `@media (prefers-reduced-motion:
  reduce)` escape hatches.
- **One new generator,** `tools/cards.py`, reusing the palette and `write()` from
  `tools/iso.py`. `STATIC=1` renders the final frame for screenshotting.
- **Cache busting:** planned as a `?v=` bump per changed asset. Measured after
  the merge, this turns out not to work and not to be needed. Relative paths
  resolve to `/raw/<ref>/...`, GitHub's own route rather than the camo proxy,
  and it caches by path with `max-age=300`, ignoring the query. A changed card
  serves stale for up to five minutes and then corrects itself. The params are
  left in place because they cost nothing, with the correction recorded in the
  README's own comment so nobody bumps one expecting it to help.

## Non-goals

- No contribution counts, streaks, commit calendars or star counts anywhere.
- No claim that AI engineering is the current job. The kicker says web developer;
  Claude Code appears as pipeline tooling, which is what it is.
- No em dashes in any copy.
- No GitHub Action yet. The headline numbers are not GitHub-derived, so a daily
  refresh would only churn. Worth adding later if a card starts showing live data.

## Settled during the build

- **The headline number moved.** `50+ sites, live` was the approved headline, but
  the SHIPPED tile repeats it word for word two rows down, and on screen that read
  as a mistake rather than as emphasis. The headline is the total now, `56 shipped`,
  which captions the 56-tile field directly above it and leaves the tiles to break
  it down into 50+, 2 and 314. One number, one place.
- **Prose kept.** The card stack is the scan layer; the two tables and the two
  bullet sections carry detail no 10.5px card line can (the Socket.io sweeper, the
  50.7% coin flip, the 314 counted against printed arrow glyphs). They also survive
  on a phone, where an 860px card does not.
- **Dropped:** the `readme-typing-svg` banner, whose four lines the hero tagline and
  the three tiles now say in type that cannot drift, and the `top-langs` card, an
  external service in a foreign style whose languages are now dots on the repo cards.
- **Repo card languages** come from the GitHub languages API, not from memory:
  HTML, JavaScript, Python. Dots use Linguist's own colours.
- **Relative image paths** confirmed against the reference profile, which uses
  `./cards/*.svg` and renders. Lets any branch preview its own assets.
- **Fonts:** `monob.ttf` was unused and is gone. Subsets keep name IDs 0, 13 and 14
  so the copyright and licence travel with every embedded copy, which costs 1.5 KB
  across the sixteen faces. `tools/fonts/README.md` carries the notice.
