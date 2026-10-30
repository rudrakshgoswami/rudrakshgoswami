# -*- coding: utf-8 -*-
"""Isometric SVG generator for the profile README.

Everything is computed rather than hand-typed: isometric coordinates are
unforgiving and a single wrong number shows up as a crooked box.

Projection is true 30-degree isometric:

    sx = (x - y) * cos(30)
    sy = (x + y) * sin(30) - z

x runs right-and-down the screen, y runs left-and-down, z is up. The viewer
sits at negative x and y looking down, so the two visible side faces of any
box are the ones at its minimum x (screen-left) and minimum y (screen-right).
Light comes from the upper left, which makes the top face brightest, the
x-face mid and the y-face darkest.

GitHub serves these through its image proxy as standalone documents, so SMIL
and CSS keyframes inside the file run, but there is no JavaScript and no way
to load an external font. Every typeface here is a system stack.
"""
import math
import os

COS30 = math.cos(math.radians(30))
SIN30 = 0.5

OUT = r"D:\portfolio\github-profile\assets"

MONO = "ui-monospace,'Cascadia Mono','Segoe UI Mono',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"

# ---------------------------------------------------------------- palette
BG0 = "#070912"
BG1 = "#0E1222"
GRID = "#1B2140"
INK = "#E8EAF6"
DIM = "#8A93B8"
FAINT = "#5A628C"

# one indigo family for the whole system, plus a single accent
SLAB = {"top": "#6F7AD4", "x": "#4B54A6", "y": "#333B78", "edge": "#9AA4F2"}
ACCENT = {"top": "#7DD3FC", "x": "#3B9ED4", "y": "#246C96", "edge": "#BAE6FD"}
VIOLET = {"top": "#A78BFA", "x": "#7C5CD6", "y": "#573C9E", "edge": "#C4B5FD"}
MUTED = {"top": "#4A5490", "x": "#363E6E", "y": "#262D52", "edge": "#6E79B8"}


def project(x, y, z=0.0):
    return (x - y) * COS30, (x + y) * SIN30 - z


class Scene:
    """Collects svg fragments and the animation delay classes they use."""

    def __init__(self, width, height, ox, oy, scale=1.0):
        self.w, self.h = width, height
        self.ox, self.oy, self.s = ox, oy, scale
        self.parts = []
        self.delays = set()

    def p(self, x, y, z=0.0):
        sx, sy = project(x, y, z)
        return self.ox + sx * self.s, self.oy + sy * self.s

    def add(self, fragment):
        self.parts.append(fragment)

    def delay(self, seconds):
        """Return a class name for this delay, registering it for the stylesheet."""
        ms = int(round(seconds * 1000))
        self.delays.add(ms)
        return "d%d" % ms

    # ------------------------------------------------------------ shapes
    def poly(self, pts, fill, opacity=None, stroke=None, sw=1.0, extra=""):
        d = " ".join("%.2f,%.2f" % pt for pt in pts)
        bits = ['<polygon points="%s" fill="%s"' % (d, fill)]
        if opacity is not None:
            bits.append(' opacity="%.3f"' % opacity)
        if stroke:
            bits.append(' stroke="%s" stroke-width="%.2f" stroke-linejoin="round"' % (stroke, sw))
        if extra:
            bits.append(" " + extra)
        bits.append("/>")
        self.add("".join(bits))

    def shadow(self, x0, y0, x1, y1, opacity=0.5):
        pts = [self.p(x0, y0), self.p(x1, y0), self.p(x1, y1), self.p(x0, y1)]
        self.poly(pts, "#000000", opacity)

    def slab(self, x0, y0, x1, y1, z0, z1, pal, edge=True, glow=False):
        """A box. Returns the screen point at the centre of its top face."""
        top = [self.p(x0, y0, z1), self.p(x1, y0, z1), self.p(x1, y1, z1), self.p(x0, y1, z1)]
        xface = [self.p(x0, y0, z0), self.p(x0, y1, z0), self.p(x0, y1, z1), self.p(x0, y0, z1)]
        yface = [self.p(x0, y0, z0), self.p(x1, y0, z0), self.p(x1, y0, z1), self.p(x0, y0, z1)]

        self.poly(yface, pal["y"])
        self.poly(xface, pal["x"])
        filt = ' filter="url(#soft)"' if glow else ""
        self.poly(top, pal["top"], stroke=pal["edge"] if edge else None, sw=0.9,
                  extra=filt.strip())
        cx, cy = self.p((x0 + x1) / 2.0, (y0 + y1) / 2.0, z1)
        return cx, cy

    def face_matrix(self, x, y, z, unit=1.0):
        """Matrix that lays flat text onto a top face at grid point (x,y,z)."""
        ox, oy = self.p(x, y, z)
        ux, uy = COS30 * self.s * unit, SIN30 * self.s * unit
        vx, vy = -COS30 * self.s * unit, SIN30 * self.s * unit
        return "matrix(%.4f,%.4f,%.4f,%.4f,%.2f,%.2f)" % (ux, uy, vx, vy, ox, oy)

    # ------------------------------------------------------------- text
    def text(self, x, y, s, size=12, fill=INK, family=MONO, weight="400",
             anchor="start", cls="", ls=None, opacity=None):
        a = [' x="%.2f" y="%.2f"' % (x, y),
             ' font-family="%s" font-size="%s" font-weight="%s" fill="%s"' % (family, size, weight, fill),
             ' text-anchor="%s"' % anchor]
        if ls is not None:
            a.append(' letter-spacing="%s"' % ls)
        if opacity is not None:
            a.append(' opacity="%.2f"' % opacity)
        if cls:
            a.append(' class="%s"' % cls)
        self.add("<text%s>%s</text>" % ("".join(a), esc(s)))

    def extruded(self, x, y, s, size, depth=13, step=(0.62, 0.36)):
        """Fake extrusion: the same glyphs stepped back along the iso axis."""
        rows = []
        for i in range(depth, 0, -1):
            t = i / float(depth)
            shade = mix("#2A2F5C", "#151934", t)
            rows.append('<text x="%.2f" y="%.2f" font-family="%s" font-size="%d" '
                        'font-weight="800" fill="%s" letter-spacing="1">%s</text>'
                        % (x + step[0] * i, y + step[1] * i, SANS, size, shade, esc(s)))
        rows.append('<text x="%.2f" y="%.2f" font-family="%s" font-size="%d" font-weight="800" '
                    'fill="url(#sheen)" letter-spacing="1">%s</text>' % (x, y, SANS, size, esc(s)))
        self.add("".join(rows))

    def grid(self, nx, ny, colour=GRID, opacity=0.55, z=0.0):
        lines = []
        for i in range(nx + 1):
            a, b = self.p(i, 0, z), self.p(i, ny, z)
            lines.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (a[0], a[1], b[0], b[1]))
        for j in range(ny + 1):
            a, b = self.p(0, j, z), self.p(nx, j, z)
            lines.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (a[0], a[1], b[0], b[1]))
        self.add('<g stroke="%s" stroke-width="1" opacity="%.2f" mask="url(#fade)">%s</g>'
                 % (colour, opacity, "".join(lines)))

    # ------------------------------------------------------------ output
    def group(self, body, cls=None, delay=None):
        c = [cls] if cls else []
        if delay is not None:
            c.append(self.delay(delay))
        attr = ' class="%s"' % " ".join(c) if c else ""
        return "<g%s>%s</g>" % (attr, body)

    def open_group(self, cls=None, delay=None):
        c = [cls] if cls else []
        if delay is not None:
            c.append(self.delay(delay))
        self.add("<g%s>" % (' class="%s"' % " ".join(c) if c else ""))

    def close_group(self):
        self.add("</g>")

    def render(self, title, keyframes_extra=""):
        delays = "".join(".d%d{animation-delay:%.3fs}" % (ms, ms / 1000.0)
                         for ms in sorted(self.delays))
        css = (
            "<style>"
            "@keyframes rise{from{transform:translateY(26px);opacity:0}to{transform:translateY(0);opacity:1}}"
            "@keyframes fade{from{opacity:0}to{opacity:1}}"
            "@keyframes draw{from{stroke-dashoffset:120}to{stroke-dashoffset:0}}"
            "@keyframes sweep{0%{transform:translateX(-120%)}55%,100%{transform:translateX(220%)}}"
            "@keyframes breathe{0%,100%{opacity:.30}50%{opacity:.85}}"
            "@keyframes blink{0%,45%{opacity:1}50%,95%{opacity:0}100%{opacity:1}}"
            ".rise{animation:rise .85s cubic-bezier(.17,.84,.26,1) both}"
            ".fade{animation:fade .7s ease-out both}"
            ".line{stroke-dasharray:120;animation:draw .7s ease-out both}"
            ".breathe{animation:breathe 3.6s ease-in-out infinite}"
            ".blink{animation:blink 1.15s step-end infinite}"
            + keyframes_extra + delays +
            "</style>"
        )
        defs = (
            "<defs>"
            '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="halo" cx="0.22" cy="0.12" r="0.85">'
            '<stop offset="0" stop-color="#818CF8" stop-opacity="0.26"/>'
            '<stop offset="0.55" stop-color="#6366F1" stop-opacity="0.06"/>'
            '<stop offset="1" stop-color="#6366F1" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0.6">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#C7CEFF"/>'
            '<stop offset="1" stop-color="#8C98F0"/></linearGradient>'
            '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
            '<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.5"/>'
            '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="fadeg"><stop offset="0.45" stop-color="#fff"/>'
            '<stop offset="1" stop-color="#000"/></radialGradient>'
            '<mask id="fade"><rect width="%d" height="%d" fill="url(#fadeg)"/></mask>'
            '<clipPath id="card"><rect width="%d" height="%d" rx="14"/></clipPath>'
            '<filter id="soft" x="-40%%" y="-40%%" width="180%%" height="180%%">'
            '<feGaussianBlur stdDeviation="2.6" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            "</defs>" % (BG0, BG1, self.w, self.h, self.w, self.h)
        )
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s'
            '<rect width="%d" height="%d" rx="14" fill="url(#bg)"/>'
            '<rect width="%d" height="%d" rx="14" fill="url(#halo)"/>'
            '<g clip-path="url(#card)">%s</g>'
            '<rect x="0.5" y="0.5" width="%d" height="%d" rx="13.5" fill="none" '
            'stroke="#2A3160" stroke-width="1"/>'
            "</svg>"
        ) % (self.w, self.h, self.w, self.h, esc(title), defs, css,
             self.w, self.h, self.w, self.h, "".join(self.parts),
             self.w - 1, self.h - 1)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def mix(a, b, t):
    """Blend two #rrggbb colours; t=1 gives a."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(round(pa[i] * t + pb[i] * (1 - t))) for i in range(3))


def write(name, svg):
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print("  %-16s %6d bytes" % (name, len(svg.encode("utf-8"))))
    return path
