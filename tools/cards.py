# -*- coding: utf-8 -*-
"""Animated SVG cards for the profile README, in two themes.

Fonts are subset to the glyphs each card actually draws and embedded as base64
WOFF2. GitHub serves SVG through <img>, which is sandboxed and cannot fetch a
font, so a font-family naming a system stack renders in whatever the viewer
happens to have. Text is positioned from the font's own advance widths too, so
it cannot drift between machines.

  python tools/cards.py            both themes into assets/spike/<theme>/
  STATIC=1 python tools/cards.py   every animation frozen at its end state
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# The isometric vocabulary, and the font subsetting both generators share.
from iso import _budget, adv, face, fits  # noqa: E402  (shared font subsetting)

STATIC = os.environ.get("STATIC") == "1"

MONO = os.path.join(HERE, "fonts", "mono.ttf")


def font(name):
    return os.path.join(HERE, "fonts", name)

# Avi's cards are light paper against GitHub's dark page, and that figure/ground
# contrast is most of why they read. The dark theme is the existing house style.
THEMES = {
    # Dark had to earn its place. Three things were killing it:
    #   Instrument Serif is a hairline display face made for ink on paper, and
    #     those strokes disappear on near-black, so this uses Fraunces at 650.
    #   The tiles were mid-tones. On a dark ground colour has to go brighter,
    #     not darker, to read as bold.
    #   The sheen faded the name into a murky blue-grey, so it now stays bright
    #     the whole way down and the grid is dialled right back.
    "dark": dict(
        serif=font("fraunces.ttf"),
        bg0="#070912", bg1="#0E1222", ink="#E8EAF6", dim="#949DC2", faint="#6A72A0",
        grid="#1B2140", gridop=0.22, rule="#232A4D", accent="#A5B4FC",
        sheen=("#FFFFFF", "#F2F4FF", "#DCE2FF"), shine=0.42, halo=True,
        tiles=[("#6366F1", "#E0E7FF"), ("#0EA5E9", "#E0F2FE"), ("#A855F7", "#F5E9FF")],
        # Flat system: the 56-square grid and the toolkit chips.
        flat=dict(net="#3B4270", store="#38BDF8", folio="#E8EAF6", repo="#A78BFA",
                  chip="#161C33", chipedge="#2A3160"),
    ),
    "paper": dict(
        serif=font("serif.ttf"),
        bg0="#FBF9F4", bg1="#F1EDE3", ink="#16140F", dim="#5E584B", faint="#9A9284",
        grid="#E6E0D2", gridop=0.9, rule="#DED7C7", accent="#4338CA",
        sheen=("#16140F", "#16140F", "#2E2719"), shine=0.0, halo=False,
        tiles=[("#4F46E5", "#DDE1FF"), ("#0284C7", "#DCF0FF"), ("#7C3AED", "#EBE2FF")],
        flat=dict(net="#C9C2B0", store="#0284C7", folio="#16140F", repo="#7C3AED",
                  chip="#F1EDE3", chipedge="#DED7C7"),
    ),
}
T = THEMES["dark"]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


KEYFRAMES = (
    "@keyframes rise{from{transform:translateY(26px);opacity:0}to{transform:translateY(0);opacity:1}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    "@keyframes sweep{0%{transform:translateX(-120%)}55%,100%{transform:translateX(220%)}}"
    "@keyframes breathe{0%,100%{opacity:.30}50%{opacity:.85}}"
    ".rise{animation:rise .85s cubic-bezier(.17,.84,.26,1) both}"
    ".fade{animation:fade .7s ease-out both}"
    ".sweep{animation:sweep 4.6s ease-in-out 1.4s infinite}"
    ".breathe{animation:breathe 3.6s ease-in-out infinite}"
)
CALM = ("{.rise,.fade,.sweep,.breathe{animation:none!important;opacity:1!important;"
        "transform:none!important}}")


def shell(w, h, label, fonts, body, delays=(), solid=None):
    d = "".join(".d%d{animation-delay:%.3fs}" % (ms, ms / 1000.0)
                for ms in sorted(set(delays)))
    calm = "@media (prefers-reduced-motion:reduce)" + CALM
    if STATIC:
        calm += CALM[1:-1]
    if solid:
        ground = '<rect width="%d" height="%d" rx="14" fill="%s"/>' % (w, h, solid)
    else:
        ground = '<rect width="%d" height="%d" rx="14" fill="url(#bg)"/>' % (w, h)
        if T["halo"]:
            ground += '<rect width="%d" height="%d" rx="14" fill="url(#halo)"/>' % (w, h)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
        'role="img" aria-label="%s"><defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<radialGradient id="halo" cx="0.22" cy="0.12" r="0.85">'
        '<stop offset="0" stop-color="#818CF8" stop-opacity="0.26"/>'
        '<stop offset="0.55" stop-color="#6366F1" stop-opacity="0.06"/>'
        '<stop offset="1" stop-color="#6366F1" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0.6">'
        '<stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/>'
        '<stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="%.2f"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        '<clipPath id="card"><rect width="%d" height="%d" rx="14"/></clipPath>'
        '</defs><style>%s%s%s%s</style>%s'
        '<g clip-path="url(#card)">%s</g>'
        '<rect width="%d" height="%d" rx="14" fill="none" stroke="%s"/></svg>'
    ) % (w, h, w, h, esc(label), T["bg0"], T["bg1"],
         T["sheen"][0], T["sheen"][1], T["sheen"][2], T["shine"],
         w, h, fonts, KEYFRAMES, d, calm, ground, body, w, h, T["rule"])


def countup(final, x, y, size, fill, cls, start_at, step=0.045, frames=14):
    """SMIL count-up. CSS cannot animate text, so each value is its own node."""
    head = ('<text x="%.1f" y="%.1f" font-family="Display" font-size="%d" fill="%s"'
            % (x, y, size, fill))
    if STATIC:
        return head + ">" + esc(final) + "</text>"
    digits = "".join(c for c in final if c.isdigit())
    n = frames if digits else 0
    out = []
    for i in range(n):
        v = str(int(int(digits) * (i + 1) / float(n + 1)))
        out.append(head + ' visibility="hidden">%s<set attributeName="visibility" '
                   'to="visible" begin="%.3fs" dur="%.3fs" fill="remove"/></text>'
                   % (v, start_at + i * step, step))
    out.append(head + ' visibility="hidden" class="%s">%s<set attributeName="visibility" '
               'to="visible" begin="%.3fs" fill="freeze"/></text>'
               % (cls, esc(final), start_at + n * step))
    return "".join(out)


def mono(text, x, y, size, fill, tracking=0.0, cls="", anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    return ('<text x="%.1f" y="%.1f" font-family="Mono" font-size="%.1f" fill="%s" '
            'letter-spacing="%.2f" class="%s"%s>%s</text>'
            % (x, y, size, fill, tracking, cls, a, esc(text)))


def grid(w, h, step=48):
    v = "".join('<line x1="%d" y1="0" x2="%d" y2="%d"/>' % (x, x, h)
                for x in range(step, w, step))
    z = "".join('<line x1="0" y1="%d" x2="%d" y2="%d"/>' % (y, w, y)
                for y in range(step, h, step))
    return '<g stroke="%s" stroke-width="1" opacity="%.2f">%s%s</g>' % (
        T["grid"], T["gridop"], v, z)


NAME = "Rudraksh Goswami"
# Rudraksh's own framing, the one on his LinkedIn and his resume. An earlier
# version of this card said "WEB DEVELOPER @ VOCSY INFOTECH" on my advice;
# he overruled it on 2026-11-24 and the whole set now matches him.
KICKER = "WORDPRESS DEVELOPER → AI ENGINEER"
TAG = "I get handed a domain and give back a site that is live."
LINK = "rudrakshgoswami.vercel.app"


def swatches(cells, x0, y0, size, pitch, start=650, step=60, cols=None):
    """A block of rounded squares. The one motif the flat system repeats."""
    cols = cols or (int(len(cells) ** 0.5 + 0.5) if len(cells) <= 16 else 14)
    out, used = [], set()
    for i, key in enumerate(cells):
        d = start + (i % cols) * step if len(cells) <= 16 else start + (i // cols) * step
        used.add(d)
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s" '
                   'class="fade d%d"/>'
                   % (x0 + (i % cols) * pitch, y0 + (i // cols) * pitch,
                      size, size, max(2, size // 4), T["flat"][key], d))
    return "".join(out), sorted(used)


def hero():
    """Flat. The isometric mark that sat on the right went with the scenes."""
    W, H = 860, 210
    fonts = face(T["serif"], NAME, "Display") + face(MONO, KICKER + TAG + LINK, "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append('<rect x="56" y="46" width="8" height="8" rx="2" fill="%s" '
             'class="fade breathe"/>' % T["accent"])
    b.append(mono(KICKER, 74, 54, 10.5, T["faint"], 1.9, "fade d150"))
    b.append('<clipPath id="nm"><text x="56" y="124" font-family="Display" '
             'font-size="58">%s</text></clipPath>' % esc(NAME))
    b.append('<text x="56" y="124" font-family="Display" font-size="58" '
             'fill="url(#sheen)" class="rise d270">%s</text>' % esc(NAME))
    if T["shine"]:
        b.append('<g clip-path="url(#nm)"><rect x="0" y="66" width="150" height="90" '
                 'fill="url(#shine)" class="sweep"/></g>')
    b.append(mono(TAG, 58, 160, 13, T["dim"], 0, "fade d450"))
    b.append('<a href="https://%s"><text x="58" y="186" font-family="Mono" '
             'font-size="13" fill="%s" class="fade d580">%s &#8599;</text></a>'
             % (LINK, T["accent"], esc(LINK)))
    # Sixteen of the same squares record.svg draws 56 of, so the two rhyme.
    mix = ["net", "net", "store", "net", "net", "repo", "net", "net",
           "store", "net", "net", "folio", "net", "net", "repo", "net"]
    art, d = swatches(mix, 700, 58, 22, 28)
    b.append(art)
    return shell(W, H, "Rudraksh Goswami, web developer at Vocsy Infotech in Surat",
                 fonts, "".join(b), [150, 270, 450, 580] + d)


TILES = [
    ("tile-shipped.svg", "SHIPPED", "100+", "sites",
     ["Blog network, built on a", "standardised WordPress base.", "About a day per site."]),
    ("tile-running.svg", "RUNNING", "2", "stores",
     ["heliosexport.com and", "shop.sanmarfoods.com,", "both live in production."]),
    ("tile-learning.svg", "LEARNING", "314", "resources",
     ["An AI engineering curriculum", "rebuilt as a site you can", "actually work through."]),
]


def tile(i, fname, kicker, value, unit, lines):
    W, H = 280, 190
    fill, soft = T["tiles"][i]
    fonts = face(T["serif"], value + unit, "Display") + face(
        MONO, kicker + "".join(lines) + "0123456789", "Mono")
    b = [mono(kicker, 24, 36, 10.5, soft, 2.0, "fade")]
    b.append('<text x="256" y="36" text-anchor="end" font-family="Mono" font-size="12" '
             'fill="%s" class="fade breathe">&#8594;</text>' % soft)
    # Shrink the headline until value + unit actually fits. "314 resources" is
    # half again as wide as "2 stores", and real metrics are the point of
    # embedding the font in the first place.
    size, gap = 42, 10
    while size > 24 and (adv(T["serif"], value, size) + gap
                         + adv(T["serif"], unit, size)) > W - 48:
        size -= 1
    b.append(countup(value, 24, 96, size, "#FFFFFF", "rise d270", 0.30))
    b.append('<text x="%.1f" y="96" font-family="Display" font-size="%d" fill="%s" '
             'class="rise d450">%s</text>'
             % (24 + adv(T["serif"], value, size) + gap, size, soft, esc(unit)))
    for n, ln in enumerate(lines):
        fits(MONO, ln, 12, W - 48, "tile " + kicker)
        b.append(mono(ln, 24, 127 + n * 18, 12, soft, 0, "fade d%d" % (580 + n * 70)))
    b.append('<rect x="0" y="0" width="90" height="%d" fill="url(#shine)" '
             'class="sweep"/>' % H)
    label = "%s: %s %s. %s" % (kicker.title(), value, unit, " ".join(lines))
    return fname, shell(W, H, label, fonts, "".join(b),
                        (270, 450, 580, 650, 720), solid=fill)


CELLS = (440, 568, 696)          # stat column x positions, 110px of copy each
CELLW = 110

# The headline was "50+ sites, live", which the SHIPPED tile repeats word for
# word two rows down. It is the total now, so it captions the field above it
# and the tiles below are the breakdown.
NUMBERS = dict(
    kicker="THE RECORD SO FAR",
    value="106", unit="shipped",
    sub="100 sites, two stores, a portfolio, three repos.",
    cells=[("2", ["live client stores", "in production"]),
           ("26", ["months at Vocsy,", "intern to developer"]),
           ("~1", ["day per build,", "standardised base"])],
)


def numbers():
    """The headline number, plus the three stats no tile carries."""
    W, H = 860, 168
    N = NUMBERS
    labels = "".join("".join(ls) for _, ls in N["cells"])
    fonts = (face(T["serif"], N["value"] + N["unit"]
                  + "".join(v for v, _ in N["cells"]) + "0123456789", "Display")
             + face(MONO, N["kicker"] + N["sub"] + labels, "Mono"))
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append('<rect x="56" y="48" width="8" height="8" rx="2" fill="%s" '
             'class="fade breathe"/>' % T["accent"])
    b.append(mono(N["kicker"], 74, 56, 10.5, T["faint"], 1.9, "fade"))
    # Headline shares the shrink-to-fit trick with the tiles.
    size, gap = 46, 12
    room = CELLS[0] - 18 - 56
    while size > 28 and (adv(T["serif"], N["value"], size) + gap
                         + adv(T["serif"], N["unit"], size)) > room:
        size -= 1
    b.append(countup(N["value"], 56, 110, size, T["ink"], "rise d270", 0.30))
    b.append('<text x="%.1f" y="110" font-family="Display" font-size="%d" fill="%s" '
             'class="rise d450">%s</text>'
             % (56 + adv(T["serif"], N["value"], size) + gap, size,
                T["accent"], esc(N["unit"])))
    fits(MONO, N["sub"], 11.5, room, "numbers sub")
    b.append(mono(N["sub"], 58, 142, 11.5, T["dim"], 0, "fade d580"))
    for i, (x, (v, ls)) in enumerate(zip(CELLS, N["cells"])):
        if i:
            b.append('<line x1="%d" y1="46" x2="%d" y2="140" stroke="%s" '
                     'class="fade d650"/>' % (x - 9, x - 9, T["rule"]))
        b.append(countup(v, x, 92, 26, T["ink"], "rise d%d" % (580 + i * 70),
                         0.45 + i * 0.09))
        for n, ln in enumerate(ls):
            fits(MONO, ln, 9.5, CELLW, "numbers cell %d" % i)
            b.append(mono(ln, x, 116 + n * 15, 9.5,
                          T["dim"] if n == 0 else T["faint"], 0,
                          "fade d%d" % (720 + i * 70)))
    label = "%s %s. %s %s" % (N["value"], N["unit"], N["sub"],
                              " ".join("%s %s" % (v, " ".join(ls))
                                       for v, ls in N["cells"]))
    return shell(W, H, label, fonts, "".join(b),
                 (270, 450, 580, 650, 720, 790))


# Linguist's own colours, so the dot means the same thing it does on the repo page.
REPOS = [
    ("repo-roadmap.svg", "ai-engineer-roadmap", "HTML", "#E34C26",
     ["Search, filters, progress and", "two themes over 314 counted",
      "resources. Live on Vercel."]),
    ("repo-vincent.svg", "vincent-app", "JavaScript", "#F1E05A",
     ["MERN booking platform. Venue", "slots lock in real time over",
      "Socket.io, so no double books."]),
    ("repo-ipl.svg", "ipl-data-analysis", "Python", "#3572A5",
     ["Nine IPL seasons in pandas.", "The toss is a 50.7% coin flip",
      "and the model loses to chance."]),
]


def repo(fname, name, lang, dot, lines):
    """Gradient ground, not a solid fill, so this row reads quieter than the tiles."""
    W, H = 280, 190
    fonts = face(T["serif"], name, "Display") + face(
        MONO, lang.upper() + "".join(lines), "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append('<circle cx="28" cy="32" r="5" fill="%s" class="fade breathe"/>' % dot)
    b.append(mono(lang.upper(), 42, 36, 10, T["faint"], 1.6, "fade d150"))
    b.append('<text x="256" y="36" text-anchor="end" font-family="Mono" font-size="12" '
             'fill="%s" class="fade d150">&#8599;</text>' % T["accent"])
    size = 24
    while size > 14 and adv(T["serif"], name, size) > W - 48:
        size -= 1
    b.append('<text x="24" y="86" font-family="Display" font-size="%d" fill="url(#sheen)" '
             'class="rise d270">%s</text>' % (size, esc(name)))
    b.append('<line x1="24" y1="104" x2="%d" y2="104" stroke="%s" class="fade d450"/>'
             % (W - 24, T["rule"]))
    for n, ln in enumerate(lines):
        fits(MONO, ln, 12, W - 48, "repo " + name)
        b.append(mono(ln, 24, 127 + n * 18, 12, T["dim"], 0,
                      "fade d%d" % (450 + n * 70)))
    return fname, shell(W, H, "%s, %s. %s" % (name, lang, " ".join(lines)),
                        fonts, "".join(b), (150, 270, 450, 520, 590))


def title(num, label):
    """A numbered rule. The one idea worth taking from the reference. 860 x 56."""
    W, H = 860, 56
    cap = label.upper()
    fonts = face(MONO, num + cap, "Mono")
    b = [mono(num, 56, 35, 13, T["accent"], 1.0, "fade")]
    x = 56 + adv(MONO, num, 13, 1.0) + 16
    b.append(mono(cap, x, 35, 12, T["ink"], 2.4, "fade d150"))
    x += adv(MONO, cap, 12, 2.4) + 20
    b.append('<line x1="%.1f" y1="31" x2="804" y2="31" stroke="%s" class="fade d270"/>'
             % (x, T["rule"]))
    return shell(W, H, "%s %s" % (num, label), fonts, "".join(b), (150, 270))


# A literal count, not a decoration: one square per thing that is live.
GRID = [(100, "net", "Blog network"), (2, "store", "Live client stores"),
        (1, "folio", "Portfolio site"), (3, "repo", "Open-source repos")]


def record():
    """Replaces shipped.svg and numbers.svg at once: the headline, the stat
    column, and the 56 as a flat grid with the legend it used to carry."""
    W, H = 860, 300
    N = NUMBERS
    fonts = (face(T["serif"], N["value"] + N["unit"]
                  + "".join(v for v, _ in N["cells"]) + "0123456789", "Display")
             + face(MONO, N["kicker"] + N["sub"] + "0123456789"
                    + "".join("".join(ls) for _, ls in N["cells"])
                    + "".join(l for _, _, l in GRID), "Mono"))
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append('<rect x="56" y="48" width="8" height="8" rx="2" fill="%s" '
             'class="fade breathe"/>' % T["accent"])
    b.append(mono(N["kicker"], 74, 56, 10.5, T["faint"], 1.9, "fade"))
    size, gap = 46, 12
    room = CELLS[0] - 18 - 56
    while size > 28 and (adv(T["serif"], N["value"], size) + gap
                         + adv(T["serif"], N["unit"], size)) > room:
        size -= 1
    b.append(countup(N["value"], 56, 110, size, T["ink"], "rise d270", 0.30))
    b.append('<text x="%.1f" y="110" font-family="Display" font-size="%d" fill="%s" '
             'class="rise d450">%s</text>'
             % (56 + adv(T["serif"], N["value"], size) + gap, size,
                T["accent"], esc(N["unit"])))
    fits(MONO, N["sub"], 11.5, room, "record sub")
    b.append(mono(N["sub"], 58, 142, 11.5, T["dim"], 0, "fade d580"))
    for i, (x, (v, ls)) in enumerate(zip(CELLS, N["cells"])):
        if i:
            b.append('<line x1="%d" y1="46" x2="%d" y2="140" stroke="%s" '
                     'class="fade d650"/>' % (x - 9, x - 9, T["rule"]))
        b.append(countup(v, x, 92, 26, T["ink"], "rise d%d" % (580 + i * 70),
                         0.45 + i * 0.09))
        for n, ln in enumerate(ls):
            fits(MONO, ln, 9.5, CELLW, "record cell %d" % i)
            b.append(mono(ln, x, 116 + n * 15, 9.5,
                          T["dim"] if n == 0 else T["faint"], 0,
                          "fade d%d" % (720 + i * 70)))
    b.append('<line x1="56" y1="170" x2="804" y2="170" stroke="%s" class="fade d720"/>'
             % T["rule"])
    seq = []
    for n, key, _ in GRID:
        seq += [key] * n
    art, sw = swatches(seq, 56, 196, 10, 13, start=800, step=40, cols=27)
    b.append(art)
    for j, (n, key, lbl) in enumerate(GRID):
        y = 208 + j * 24
        b.append('<rect x="%d" y="%d" width="11" height="11" rx="3" fill="%s" '
                 'class="fade d840"/>' % (CELLS[0], y - 9, T["flat"][key]))
        b.append(mono(str(n), CELLS[0] + 44, y, 12.5, T["ink"], 0, "fade d840", "end"))
        fits(MONO, lbl, 11, 804 - (CELLS[0] + 56), "record legend")
        b.append(mono(lbl, CELLS[0] + 56, y, 11, T["dim"], 0, "fade d880"))
    label = "%s %s. %s %s" % (N["value"], N["unit"], N["sub"],
                              " ".join("%d %s" % (n, l) for n, _, l in GRID))
    return shell(W, H, label, fonts, "".join(b),
                 sorted({270, 450, 580, 650, 720, 790, 860} | set(sw)))


STORES = [
    ("store-helios.svg", "heliosexport.com", "WooCommerce", "store",
     ["Jewellery export storefront.", "Product catalogue, categories",
      "and checkout, built from scratch."]),
    ("store-sanmar.svg", "shop.sanmarfoods.com", "Shopify + Liquid", "repo",
     ["Food and snacks retailer in", "Singapore. Theme sections and",
      "product pages customised in Liquid."]),
]


def store(fname, domain, stack, key, lines):
    """Replaces the two-row markdown table. 416 x 210, two to a row."""
    W, H = 416, 210
    fonts = face(T["serif"], domain, "Display") + face(
        MONO, stack.upper() + "LIVE" + "".join(lines), "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append('<rect x="24" y="26" width="10" height="10" rx="3" fill="%s" '
             'class="fade breathe"/>' % T["flat"][key])
    b.append(mono(stack.upper(), 44, 35, 10, T["faint"], 1.8, "fade d150"))
    b.append(mono("LIVE", W - 24, 35, 10, T["flat"]["store"], 1.8, "fade d150", "end"))
    size = 26
    while size > 15 and adv(T["serif"], domain, size) > W - 48:
        size -= 1
    b.append('<text x="24" y="90" font-family="Display" font-size="%d" '
             'fill="url(#sheen)" class="rise d270">%s</text>' % (size, esc(domain)))
    b.append('<line x1="24" y1="110" x2="%d" y2="110" stroke="%s" class="fade d450"/>'
             % (W - 24, T["rule"]))
    for n, ln in enumerate(lines):
        fits(MONO, ln, 12, W - 48, "store " + domain)
        b.append(mono(ln, 24, 136 + n * 18, 12, T["dim"], 0,
                      "fade d%d" % (450 + n * 70)))
    b.append('<text x="%d" y="192" font-family="Mono" font-size="12" fill="%s" '
             'text-anchor="end" class="fade d660">&#8599;</text>'
             % (W - 24, T["accent"]))
    return fname, shell(W, H, "%s, %s, live. %s" % (domain, stack, " ".join(lines)),
                        fonts, "".join(b), (150, 270, 450, 520, 590, 660))


# Exactly what stack.svg listed, same six layers, as chips you can scan.
LAYERS = [
    ("AI LAYER", ["Claude Code", "agents", "automation"]),
    ("CODE", ["PHP", "JavaScript", "Liquid", "Python"]),
    ("PLATFORM", ["WordPress", "WooCommerce", "Shopify"]),
    ("DATABASE", ["MySQL"]),
    ("SERVER", ["DigitalOcean", "Hostinger", "cPanel", "Cloudways"]),
    ("DNS & EDGE", ["Cloudflare", "Namecheap", "SSL"]),
]
FOOT = "every layer I ship on and still maintain"


def toolkit():
    """What stack.svg drew, as labels. A grid of words beats an exploded
    diagram for the one job this card has, which is being scanned."""
    W, H = 860, 366
    fonts = face(MONO, "04TOOLKIT" + FOOT
                 + "".join(n + "".join(c) for n, c in LAYERS), "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append(mono("04", 56, 46, 13, T["accent"], 1.0, "fade"))
    b.append(mono("TOOLKIT", 90, 46, 12, T["ink"], 2.4, "fade d150"))
    b.append('<line x1="200" y1="42" x2="804" y2="42" stroke="%s" class="fade d270"/>'
             % T["rule"])
    for i, (name, chips) in enumerate(LAYERS):
        y, d = 86 + i * 38, 300 + i * 70
        b.append(mono(name, 56, y + 17, 10.5, T["faint"], 1.6, "fade d%d" % d))
        x = 190
        for c in chips:
            w = adv(MONO, c, 11) + 24
            b.append('<rect x="%.1f" y="%d" width="%.1f" height="26" rx="13" '
                     'fill="%s" stroke="%s" class="fade d%d"/>'
                     % (x, y, w, T["flat"]["chip"], T["flat"]["chipedge"], d))
            b.append(mono(c, x + 12, y + 17, 11, T["ink"], 0, "fade d%d" % d))
            x += w + 8
        assert x <= W - 40, "toolkit row %r runs to %.0f" % (name, x)
    b.append('<line x1="56" y1="322" x2="804" y2="322" stroke="%s" class="fade d720"/>'
             % T["rule"])
    b.append(mono(FOOT, 56, 346, 10.5, T["faint"], 0, "fade d720"))
    return shell(W, H, "Toolkit. " + " ".join("%s: %s." % (n, ", ".join(c))
                                              for n, c in LAYERS),
                 fonts, "".join(b), [150, 270] + [300 + i * 70 for i in range(7)])


NOW = [
    ("LEARNING", "LLM evaluation, agent orchestration and Python for production ML"),
    ("AVAILABLE", "Freelance website, e-commerce and automation work"),
    ("ASK ME", "Shipping e-commerce stores, AI-assisted development, hosting, migrations"),
]


def now():
    """Replaces the Right now bullets. 860 x 210."""
    W, H = 860, 210
    fonts = face(MONO, "05RIGHTNOW" + "".join(k + v for k, v in NOW), "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append(mono("05", 56, 46, 13, T["accent"], 1.0, "fade"))
    b.append(mono("RIGHT NOW", 90, 46, 12, T["ink"], 2.4, "fade d150"))
    b.append('<line x1="222" y1="42" x2="804" y2="42" stroke="%s" class="fade d270"/>'
             % T["rule"])
    for i, (k, v) in enumerate(NOW):
        y, d = 92 + i * 40, 300 + i * 80
        b.append('<rect x="56" y="%d" width="8" height="8" rx="2" fill="%s" '
                 'class="fade d%d"/>' % (y - 8, T["accent"], d))
        b.append(mono(k, 76, y, 10.5, T["faint"], 1.8, "fade d%d" % d))
        fits(MONO, v, 12.5, W - 40 - 230, "now " + k)
        b.append(mono(v, 230, y, 12.5, T["dim"], 0, "fade d%d" % (d + 40)))
    return shell(W, H, "Right now. " + " ".join("%s: %s." % (k, v) for k, v in NOW),
                 fonts, "".join(b),
                 [150, 270] + [300 + i * 80 for i in range(3)]
                 + [340 + i * 80 for i in range(3)])


def contact():
    """Closing card. 860 x 160."""
    W, H = 860, 160
    line = "Let's build something that ships."
    mail = "rudrakshgoswami5555@gmail.com"
    fonts = face(T["serif"], line, "Display") + face(MONO, "06REACHME" + mail, "Mono")
    b = [grid(W, H)] if T["gridop"] > 0.3 else []
    b.append(mono("06", 56, 46, 13, T["accent"], 1.0, "fade"))
    b.append(mono("REACH ME", 90, 46, 12, T["ink"], 2.4, "fade d150"))
    b.append('<line x1="212" y1="42" x2="804" y2="42" stroke="%s" class="fade d270"/>'
             % T["rule"])
    size = 34
    while size > 20 and adv(T["serif"], line, size) > W - 112:
        size -= 1
    b.append('<text x="56" y="106" font-family="Display" font-size="%d" '
             'fill="url(#sheen)" class="rise d270">%s</text>' % (size, esc(line)))
    b.append(mono(mail, 56, 134, 12.5, T["accent"], 0, "fade d450"))
    return shell(W, H, line + " " + mail, fonts, "".join(b), (150, 270, 450))


def write(theme, name, svg):
    # Dark is the profile. Any other theme is a comparison spike, kept aside.
    tail = ["assets"] if theme == "dark" else ["assets", "spike", theme]
    out = os.path.normpath(os.path.join(HERE, os.pardir, *tail))
    if not os.path.isdir(out):
        os.makedirs(out)
    with io.open(os.path.join(out, name), "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(svg)
    print("  %-8s %-20s %6d bytes" % (theme, name, len(svg.encode("utf-8"))))


if __name__ == "__main__":
    only = os.environ.get("THEME", "dark")       # "paper" or "both" for the spike
    print("rendering %s%s" % (only, " (STATIC)" if STATIC else ""))
    for theme in ("dark", "paper"):
        if only != "both" and theme != only:
            continue
        T = THEMES[theme]
        write(theme, "hero.svg", hero())
        write(theme, "t-record.svg", title("01", "The record"))
        write(theme, "record.svg", record())
        for i, args in enumerate(TILES):
            write(theme, *tile(i, *args))
        write(theme, "t-work.svg", title("02", "Selected work"))
        for args in STORES:
            write(theme, *store(*args))
        write(theme, "t-source.svg", title("03", "Open source"))
        for args in REPOS:
            write(theme, *repo(*args))
        write(theme, "toolkit.svg", toolkit())
        write(theme, "now.svg", now())
        write(theme, "contact.svg", contact())
    print("  embedded font payload: %.1f KB across %d faces"
          % (sum(_budget) / 1024.0, len(_budget)))
