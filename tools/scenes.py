# -*- coding: utf-8 -*-
"""Build the three isometric scenes for the profile README."""
import contextlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso import (ACCENT, DIM, FACES, FAINT, INK, MONO, MUTED, SLAB, VIOLET,
                 Scene, adv, fits, write)

BOLD, BOOK = FACES["700"], FACES["400"]


@contextlib.contextmanager
def at(scene, ox, oy, scale):
    """Temporarily move the projector, for insets and legends."""
    keep = (scene.ox, scene.oy, scene.s)
    scene.ox, scene.oy, scene.s = ox, oy, scale
    try:
        yield
    finally:
        scene.ox, scene.oy, scene.s = keep


def prompt(sc, x, y, path, cmd):
    """A fake shell prompt, the one bit of chrome every section shares."""
    rest = " $ " + cmd
    sc.text(x, y, path, size=12.5, fill="#818CF8", weight="600", cls="fade")
    sc.text(x + adv(BOLD, path, 12.5), y, rest, size=12.5, fill=FAINT, cls="fade")
    sc.add('<rect x="%.1f" y="%.1f" width="7" height="14" fill="#818CF8" '
           'opacity="0.75" class="blink"/>'
           % (x + adv(BOLD, path, 12.5) + adv(BOOK, rest, 12.5) + 3, y - 10.5))


# The hero lived here until the card redesign. It drew its own letterforms as
# extruded slabs and read "WordPress Developer -> AI Engineer", which is not the
# current job. tools/cards.py owns assets/hero.svg now; git has the old one.


# -------------------------------------------------------------------- stack
LAYERS = [
    ("DNS & EDGE", "Cloudflare \u00b7 Namecheap \u00b7 SSL", MUTED, False),
    ("SERVER", "DigitalOcean \u00b7 Hostinger \u00b7 cPanel \u00b7 Cloudways", MUTED, False),
    ("DATABASE", "MySQL", SLAB, False),
    ("PLATFORM", "WordPress \u00b7 WooCommerce \u00b7 Shopify", SLAB, False),
    ("CODE", "PHP \u00b7 JavaScript \u00b7 Liquid \u00b7 Python", VIOLET, False),
    ("AI LAYER", "Claude Code \u00b7 agents \u00b7 automation", ACCENT, True),
]


def stack():
    sc = Scene(860, 492, 0, 0)
    prompt(sc, 36, 44, "~/stack", "tree -L 1")

    SCALE, W, D, TH, STEP = 37, 5.0, 3.0, 0.62, 1.34
    with at(sc, 258, 300, SCALE):
        for i, (name, techs, pal, glow) in enumerate(LAYERS):
            z = i * STEP
            delay = 0.2 + i * 0.11
            sc.open_group("rise", delay)
            sc.slab(0, 0, W, D, z, z + TH, pal, glow=glow)
            sc.close_group()

            # leader line out to the label, from the slab's right-hand corner
            ex, ey = sc.p(W, 0, z + TH)
            lx = 512
            sc.add('<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f" fill="none" stroke="%s" '
                   'stroke-width="1" opacity="0.5" class="line %s"/>'
                   % (ex, ey, ex + 26, ey - 13, lx - 12, ey - 13,
                      pal["edge"], sc.delay(delay + 0.3)))
            sc.add('<circle cx="%.2f" cy="%.2f" r="2.4" fill="%s" class="fade %s"/>'
                   % (ex, ey, pal["edge"], sc.delay(delay + 0.3)))

            sc.open_group("fade", delay + 0.38)
            # The tech lists are the widest copy on this card; with a real font
            # the render should fail rather than let one run off the edge.
            fits(BOLD, name, 13, sc.w - 36 - lx, "stack layer name", 1.6)
            fits(BOOK, techs, 11, sc.w - 36 - lx, "stack techs " + name)
            sc.text(lx, ey - 16, name, size=13, fill=INK, weight="700", ls="1.6")
            sc.text(lx, ey - 1, techs, size=11, fill=DIM)
            sc.close_group()

    sc.open_group("fade", 1.5)
    sc.text(36, 462, "I run the servers and the domains, not just the code.",
            size=12, fill="#A5B4FC", weight="600")
    sc.text(36, 478, "bottom to top, every layer I have shipped on and still maintain",
            size=10.5, fill=FAINT)
    sc.close_group()
    return sc.render("The full stack Rudraksh works across, from DNS up to the AI layer")


# ------------------------------------------------------------------ shipped
def shipped():
    sc = Scene(860, 470, 0, 0)
    prompt(sc, 36, 44, "~/shipped", "ls -l")

    # 8x7 = 56 tiles: two client stores, the portfolio, three repos and the
    # 50 blog-network sites. 56 has no 11x5-shaped rectangle, which is why the
    # field is squarer than it used to be.
    NX, NY, SCALE = 8, 7, 32
    GAP, H_NET, H_FOLIO, H_REPO, H_TALL = 0.08, 0.22, 1.0, 0.7, 1.45

    stores = {(1, 0): "heliosexport.com", (6, 0): "shop.sanmarfoods.com"}
    repos = {(1, 3), (4, 3), (7, 3)}
    folio = {(3, 1)}

    def kind(cell):
        if cell in stores:
            return H_TALL, ACCENT, True
        if cell in repos:
            return H_REPO, VIOLET, False
        if cell in folio:
            return H_FOLIO, SLAB, False
        return H_NET, MUTED, False

    # 8x7 projects 27px narrower than 11x5 did, so the field shifts right to
    # keep an even gap on both sides of it.
    with at(sc, 290, 172, SCALE):
        cells = [(x, y) for x in range(NX) for y in range(NY)]
        cells.sort(key=lambda c: c[0] + c[1])          # far tiles first
        for x, y in cells:
            h, pal, glow = kind((x, y))
            delay = 0.22 + (x + y) * 0.045 + x * 0.004
            sc.open_group("rise", delay)
            sc.slab(x + GAP, y + GAP, x + 1 - GAP, y + 1 - GAP, 0, h, pal,
                    edge=(h > H_NET), glow=glow)
            sc.close_group()

        # the two stores earn a name
        for (x, y), label in sorted(stores.items()):
            tx, ty = sc.p(x + 0.5, y + 0.5, H_TALL)
            up = 34
            sc.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                   'stroke-width="1" opacity="0.55" class="line %s"/>'
                   % (tx, ty, tx, ty - up, ACCENT["edge"], sc.delay(1.0)))
            sc.open_group("fade", 1.1)
            sc.text(tx, ty - up - 6, label, size=11, fill="#BAE6FD", weight="600",
                    anchor="middle")
            sc.close_group()

    legend = [
        (ACCENT, H_TALL, "Live client stores", "2", "WooCommerce \u00b7 Shopify"),
        (SLAB, H_FOLIO, "Portfolio site", "1", "rudrakshgoswami.vercel.app"),
        (VIOLET, H_REPO, "Open-source repos", "3",
         "vincent-app · ipl-data-analysis", "ai-engineer-roadmap"),
        (MUTED, H_NET, "Blog network", "50", "WordPress, built with Claude Code"),
    ]
    head = "56 TILES, 56 THINGS THAT ARE LIVE"
    # JetBrains Mono sets about 9% wider than the system monospace this was
    # drawn against, which ran the legend off the card. The column now starts
    # wherever its widest line still finishes RM short of the edge, so the copy
    # decides the position instead of a number tuned to the old font. The
    # isometric field ends near x=512, which is the floor on how far left it
    # can go.
    RM = 36
    notes = [n for row in legend for n in row[4:]]
    LX = int(min(sc.w - RM - adv(BOLD, head, 11, 1.2),
                 sc.w - RM - 52 - max(adv(BOOK, n, 10.5) for n in notes)))
    assert LX > 540, "legend column would collide with the field at x=%d" % LX
    sc.open_group("fade", 1.25)
    sc.text(LX, 118, head, size=11, fill=INK, weight="700", ls="1.2")
    sc.close_group()
    for i, row in enumerate(legend):
        pal, h, title, count = row[:4]
        notes = row[4:]
        y = 150 + i * 64
        with at(sc, LX + 16, y, 22):
            sc.open_group("rise", 1.35 + i * 0.1)
            sc.slab(0, 0, 1, 1, 0, max(h, 0.3), pal)
            sc.close_group()
        sc.open_group("fade", 1.42 + i * 0.1)
        tx = LX + 52 + adv(BOLD, count, 15) + 6
        fits(BOLD, title, 12, sc.w - RM - tx, "shipped legend " + count)
        sc.text(LX + 52, y - 4, count, size=15, fill=pal["edge"], weight="800")
        sc.text(tx, y - 4, title, size=12, fill=INK, weight="600")
        for k, note in enumerate(notes):
            sc.text(LX + 52, y + 12 + k * 13, note, size=10.5, fill=FAINT)
        sc.close_group()

    sc.open_group("fade", 1.9)
    sc.text(36, 452, "each tile is one site that is live, not one commit",
            size=11, fill=FAINT)
    sc.close_group()
    return sc.render("Fifty-six live sites, two client stores and three open-source repositories")


if __name__ == "__main__":
    print("writing assets:")
    write("stack.svg", stack())
    write("shipped.svg", shipped())
