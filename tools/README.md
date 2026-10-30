# Regenerating the isometric art

The three SVGs in `assets/` are generated, not drawn by hand. Isometric
coordinates are unforgiving, and one wrong number shows up as a crooked box.

```bash
python tools/scenes.py
```

That rewrites `assets/hero.svg`, `assets/stack.svg` and `assets/shipped.svg`
in place. Output is deterministic, so running it without changing anything
leaves the files byte-identical.

| File | What it holds |
|------|---------------|
| `iso.py` | The projection, the box and text primitives, the palette, the stylesheet |
| `scenes.py` | The three scenes and the content that goes in them |

## Where the numbers live

`scenes.py` holds the facts, so edit it there rather than the SVGs:

- **`LAYERS`** — the six rows of the stack diagram, bottom to top.
- **`shipped()`** — `NX, NY` is the tile grid, and `stores`, `repos` and
  `folio` name the cells that get a height of their own. Everything else is a
  blog-network tile. The grid is 11 x 5 so the tiles come to exactly 55, which
  is what the caption claims; if the count changes, change the grid with it.

## Things that will bite

- **No external fonts.** GitHub serves these as standalone images, so a
  Google Fonts link does nothing. Every typeface is a system stack.
- **No scripts.** All motion is CSS keyframes inside each file.
- **`<h1>` and `<h2>` draw a full-width rule** in GitHub's markdown. The
  README uses `<h3>` and below for that reason.
- **Retired icon slugs.** shields.io answers `200` for a logo that no longer
  exists and silently leaves the icon out, so a status code proves nothing.
  `linkedin` and `codepen` are both retired. Compare the response size against
  the same badge with a nonsense slug: identical bytes means no icon.
- **Camo caches.** The `?v=1` on each asset URL is there to be bumped when a
  scene changes and the old one sticks around.
