# -*- coding: utf-8 -*-
"""Build the three isometric scenes for the profile README."""
import contextlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso import (ACCENT, DIM, FAINT, INK, MONO, MUTED, SANS, SLAB, VIOLET,
                 Scene, write)


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
    sc.text(x, y, path, size=12.5, fill="#818CF8", weight="600", cls="fade")
    sc.text(x + len(path) * 7.52, y, " $ " + cmd, size=12.5, fill=FAINT, cls="fade")
    sc.add('<rect x="%.1f" y="%.1f" width="7" height="14" fill="#818CF8" '
           'opacity="0.75" class="blink"/>'
           % (x + (len(path) + len(cmd) + 3) * 7.52 + 3, y - 10.5))


# --------------------------------------------------------------------- hero
def hero():
    sc = Scene(860, 300, 0, 0)

    with at(sc, 96, 44, 44):
        sc.grid(14, 9, opacity=0.9)

    prompt(sc, 56, 66, "~/rudrakshgoswami", "whoami")

    sc.open_group("rise", 0.15)
    sc.extruded(54, 146, "RUDRAKSH", 54)
    sc.close_group()
    sc.open_group("rise", 0.27)
    sc.extruded(54, 202, "GOSWAMI", 54)
    sc.close_group()

    sc.open_group("fade", 0.62)
    sc.text(56, 238, "WordPress Developer", size=13.5, fill=DIM, weight="600")
    sc.text(56 + 19 * 7.9, 238, "\u2192", size=14, fill="#818CF8", weight="700")
    sc.text(56 + 21 * 7.9, 238, "AI Engineer", size=13.5, fill="#A5B4FC", weight="600")
    sc.text(56, 261, "Surat, India  \u00b7  two years in production  \u00b7  I ship things that go live",
            size=11.5, fill=FAINT)
    sc.close_group()

    # three floating slabs: a small rhyme of the stack section below
    with at(sc, 692, 168, 44):
        for i, pal in enumerate((MUTED, SLAB, ACCENT)):
            z = i * 1.16
            sc.open_group("rise", 0.45 + i * 0.13)
            sc.slab(0, 0, 2, 2, z, z + 0.26, pal, glow=(i == 2))
            sc.close_group()
        a = sc.p(2, 0, 0.26)
        b = sc.p(2, 0, 2.32)
        sc.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#818CF8" '
               'stroke-width="1" opacity="0.4" stroke-dasharray="3 4" class="fade %s"/>'
               % (a[0], a[1], b[0], b[1], sc.delay(0.9)))

    return sc.render("Rudraksh Goswami, WordPress Developer turned AI Engineer")


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

    NX, NY, SCALE = 11, 5, 32
    GAP, H_NET, H_FOLIO, H_REPO, H_TALL = 0.08, 0.22, 1.0, 0.7, 1.45

    stores = {(1, 0): "heliosexport.com", (9, 0): "shop.sanmarfoods.com"}
    repos = {(3, 2), (7, 2)}
    folio = {(5, 0)}

    def kind(cell):
        if cell in stores:
            return H_TALL, ACCENT, True
        if cell in repos:
            return H_REPO, VIOLET, False
        if cell in folio:
            return H_FOLIO, SLAB, False
        return H_NET, MUTED, False

    with at(sc, 250, 172, SCALE):
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

    LX = 606
    legend = [
        (ACCENT, H_TALL, "Live client stores", "2", "WooCommerce \u00b7 Shopify"),
        (SLAB, H_FOLIO, "Portfolio site", "1", "rudrakshgoswami.vercel.app"),
        (VIOLET, H_REPO, "Open-source repos", "2", "vincent-app · ipl-data-analysis"),
        (MUTED, H_NET, "Blog network", "50", "WordPress, built with Claude Code"),
    ]
    sc.open_group("fade", 1.25)
    sc.text(LX, 118, "55 TILES, 55 THINGS THAT ARE LIVE", size=11, fill=INK,
            weight="700", ls="1.2")
    sc.close_group()
    for i, (pal, h, title, count, note) in enumerate(legend):
        y = 150 + i * 64
        with at(sc, LX + 16, y, 22):
            sc.open_group("rise", 1.35 + i * 0.1)
            sc.slab(0, 0, 1, 1, 0, max(h, 0.3), pal)
            sc.close_group()
        sc.open_group("fade", 1.42 + i * 0.1)
        sc.text(LX + 52, y - 4, count, size=15, fill=pal["edge"], weight="800")
        sc.text(LX + 52 + len(count) * 9.6 + 6, y - 4, title, size=12, fill=INK, weight="600")
        sc.text(LX + 52, y + 12, note, size=10.5, fill=FAINT)
        sc.close_group()

    sc.open_group("fade", 1.9)
    sc.text(36, 452, "each tile is one site that is live, not one commit",
            size=11, fill=FAINT)
    sc.close_group()
    return sc.render("Fifty-five live sites, two client stores and two open-source repositories")


if __name__ == "__main__":
    print("writing assets:")
    write("hero.svg", hero())
    write("stack.svg", stack())
    write("shipped.svg", shipped())
