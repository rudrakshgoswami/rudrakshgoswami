# Profile README v2: flat card system

**Date:** 2026-11-24 · **Status:** awaiting approval · Supersedes the layout in
[readme-redesign.md](readme-redesign.md), which stays as the record of v1.

## Intent

Rebuild the page as a single flat card system in the manner of
[ronartz/ronartz](https://github.com/ronartz/ronartz): numbered section title
cards, uniform card rows, anchor navigation, no visual exceptions. Keep the
indigo. Beat the reference on the things it gets wrong rather than on styling.

## Decided with Rudraksh, 2026-11-24

| Question | Answer |
|---|---|
| Keep the isometric scenes? | **No.** All flat. I argued to keep them; overruled. |
| Palette | **Indigo**, not the reference's orange |
| Prose | **Cards lead, a thin text layer survives** for the repo detail |

## Where the reference is beatable

Measured, not assumed, on 2026-11-24:

- **It embeds no fonts.** Every card declares `Arial,Helvetica,sans-serif` and
  `Consolas,Menlo,monospace`. On any machine without Consolas the metrics shift
  and the hand-positioned layout drifts. Ours embeds a per-card subset already.
- **It breaks on phones.** `width="33.33%"` puts its tiles and repo cards at
  103px wide in a 309px column. Ours uses fixed widths and wraps instead.
- **It publishes its own weakest numbers:** 62 contributions in twelve months,
  a 4-day streak, 17 active days, and a monthly chart flat for eleven months.
  No contribution metric appears anywhere here. That rule is unchanged from v1.
- Its repo carries no description and no topics. Ours carries both.

So "enhanced" is mostly a matter of not copying its mistakes, plus having real
client work underneath.

## What the dropped scenes were carrying

Dropping `shipped.svg` and `stack.svg` loses two things that have to land
somewhere, or the redesign is a downgrade:

| Was in | Content | Now in |
|---|---|---|
| `shipped.svg` | 56 tiles, and the legend splitting them into 50 network sites, 2 stores, 1 portfolio, 3 repos | `record.svg`, as a flat 56-square grid with the same legend |
| `stack.svg` | every technology named, across six layers from DNS to the AI layer | `toolkit.svg`, as labelled chips grouped by the same six layers |

The chip grid is the one place the flat version genuinely beats the isometric
one: a recruiter scanning for "Docker" or "MySQL" finds it faster in a grid of
labels than in an exploded diagram.

Both SVGs stay in `assets/`. They leave the README, not the repository.

## The page

```
  hero.svg                                     860   name, kicker, one line, link
  site | linkedin | email | views              chips

  01 / THE RECORD                              860   title card
  record.svg                                   860   56 grid + legend + 3 stats
  SHIPPED | RUNNING | LEARNING                 3 x 272

  02 / SELECTED WORK                           860   title card
  heliosexport | shop.sanmarfoods              2 x 416

  03 / OPEN SOURCE                             860   title card
  roadmap | vincent | ipl                      3 x 272
  repo detail table                            markdown, the thin text layer

  04 / TOOLKIT                                 860   header baked in
  05 / RIGHT NOW                               860   header baked in
  contact                                      860   header baked in
  portfolio | email | linkedin | fiverr | freelancer   chips
```

Sections 04, 05 and the contact card are single cards, so their heading is
drawn inside them rather than given a title card of its own. Only a section
with a multi-card row gets a separate title bar.

## Cards to build

| File | Size | Content |
|---|---|---|
| `hero.svg` | 860x200 | rebuilt without the isometric mark |
| `t-record.svg`, `t-work.svg`, `t-source.svg` | 860x56 | numbered title bars |
| `record.svg` | 860x300 | `56 shipped`, the 56-square grid, the four-way legend, and 2 stores / 26 months / ~1 day per build |
| `tile-*.svg` x3 | 272x190 | existing three, restyled to the flat system |
| `store-helios.svg`, `store-sanmar.svg` | 416x210 | replace the two-row markdown table |
| `repo-*.svg` x3 | 272x190 | existing three, restyled |
| `toolkit.svg` | 860x280 | technology chips grouped by the six stack layers |
| `now.svg` | 860x200 | replaces the Right now bullets |
| `contact.svg` | 860x140 | closing card |

Reused unchanged: the link chips in `assets/links/`, minus the eight social
chips already cut.

## Technical calls

Mine unless corrected.

- **One generator.** Extend `tools/cards.py`. The shell, the embedded-font
  subsetting, the count-up and the fit asserts all exist and are reused.
- **Fixed pixel widths, never percentages**, for the reasons measured in v1.
  272 x 3 and 416 x 2 both fit the 846px column and wrap cleanly below it.
- **Anchor navigation**, as the reference does it: the title cards get `id`
  anchors so the hero can link down to a section.
- **Fit asserts on every new card**, so copy that outgrows its box fails the
  render rather than shipping clipped.
- **Deterministic output** stays: no card may change bytes unless its content
  changed.

## Non-goals

- No contribution counts, streaks, commit calendars or star counts. Unchanged.
- No GitHub Action. The numbers here are not GitHub-derived, so a daily refresh
  would only churn.
- ~~No claim that AI engineering is the current job.~~ **Reversed 2026-11-24.**
  The hero kicker read `WEB DEVELOPER @ VOCSY INFOTECH` on my advice. Rudraksh
  uses `WordPress Developer → AI Engineer` on his LinkedIn and his resume, told
  me that version is the one he wants, and asked for everything else to match
  it. The kicker and the GitHub bio now do. My argument against it is recorded
  in `11-resume-linkedin-applications.md`; the decision is his.
- No em dashes.
- No orange.

## Risk

This replaces a working page with a bigger one. The three isometric scenes are
the only assets here that cannot be produced from a template, and two of them
are being retired on purpose. If the flat version lands worse, v1 is one
`git revert` away and both SVGs are still in `assets/`.
