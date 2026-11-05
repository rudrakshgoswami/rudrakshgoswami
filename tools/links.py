# -*- coding: utf-8 -*-
"""Build the contact row as bespoke SVG chips.

The rest of the profile draws its own art (hero.svg, stack.svg, shipped.svg);
the contact row was the one piece still using off-the-shelf shields.io badges,
which is why it read as pasted on. These chips use the same palette, the same
type stack and the same glass treatment as the cards above them.

Hierarchy is the point. Five chips that matter get a label and a tinted brand
glyph; the eight social links collapse to muted icon-only squares. One filled
chip, the portfolio, is the single place the eye is meant to land.

Glyph paths come from Simple Icons (CC0). Run with the icon directory as argv[1]:

    python tools/links.py <dir-of-simple-icons-svgs>

Writes assets/links/*.svg.
"""
import io
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'assets', 'links')

# Palette lifted from assets/hero.svg so the row belongs to the same system.
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SURFACE_TOP, SURFACE_BOT = '#151B30', '#0E1222'
EDGE = '#2B3360'
INK = '#E8EAF6'
MUTED = '#99A2C4'
ACCENT_A, ACCENT_B = '#4F46E5', '#7C83F2'

# Segoe UI Semibold advance widths as a fraction of the em. Biased ~4% high so
# a label can never clip; the slack lands in the right padding.
ADV = {
    'a': .52, 'b': .55, 'c': .47, 'd': .55, 'e': .52, 'f': .33, 'g': .55,
    'h': .55, 'i': .25, 'j': .25, 'k': .51, 'l': .25, 'm': .84, 'n': .55,
    'o': .54, 'p': .55, 'q': .55, 'r': .37, 's': .45, 't': .36, 'u': .55,
    'v': .49, 'w': .75, 'x': .48, 'y': .49, 'z': .44,
    'A': .63, 'B': .60, 'C': .60, 'D': .66, 'E': .55, 'F': .52, 'G': .68,
    'H': .68, 'I': .28, 'J': .47, 'K': .62, 'L': .52, 'M': .86, 'N': .70,
    'O': .72, 'P': .58, 'Q': .72, 'R': .61, 'S': .56, 'T': .58, 'U': .68,
    'V': .63, 'W': .95, 'X': .60, 'Y': .59, 'Z': .56,
    ' ': .26, '.': .28, '-': .35,
}


def text_width(s, size):
    return sum(ADV.get(c, .55) for c in s) * size * 1.04


# Not every brand ships a square symbol. Simple Icons' Fiverr and Behance are
# wordmarks, so they need their own scale to sit optically level with the rest.
GLYPH_FIX = {'fiverr': (1.45, 1.0), 'behance': (1.12, 0.0), 'codepen': (1.06, 0.0)}


def glyph(icon_dir, name):
    """Pull the single path out of a Simple Icons file."""
    raw = io.open(os.path.join(icon_dir, name + '.svg'), encoding='utf-8').read()
    m = re.search(r'\sd="([^"]+)"', raw)
    if not m:
        raise SystemExit('no path in %s' % name)
    return m.group(1)


def defs(uid, filled):
    """Surface gradient plus the hairline highlight that reads as glass."""
    if filled:
        stops = ('<stop offset="0" stop-color="%s"/>'
                 '<stop offset="1" stop-color="%s"/>' % (ACCENT_A, ACCENT_B))
    else:
        stops = ('<stop offset="0" stop-color="%s"/>'
                 '<stop offset="1" stop-color="%s"/>' % (SURFACE_TOP, SURFACE_BOT))
    return ('<linearGradient id="s%s" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
            % (uid, stops))


def chip(label, icon_d, tint, filled=False, uid='c', fix=''):
    """A labelled chip: margin, surface, tinted glyph, label."""
    H, PAD_L, ICON, GAP, PAD_R, FS, M = 40, 15, 16, 10, 17, 13.5, 4
    tw = text_width(label, FS)
    w = PAD_L + ICON + GAP + tw + PAD_R
    total = w + M * 2

    edge = '#9AA4F2' if filled else EDGE
    edge_op = '0.55' if filled else '1'
    ink = '#FFFFFF' if filled else INK
    k, dy = GLYPH_FIX.get(fix, (1.0, 0.0))
    gi = ICON / 24.0 * k                  # Simple Icons draw on a 24u grid
    gx = M + PAD_L - (ICON * k - ICON) / 2.0
    gy = (H - ICON * k) / 2.0 + 2 + dy

    sweep = ''
    if filled:
        # One slow highlight pass, echoing the sheen on hero.svg.
        sweep = (
            '<style>@keyframes sw{0%%{transform:translateX(-60%%)}'
            '60%%,100%%{transform:translateX(%.0f%%)}}'
            '.sw{animation:sw 4.5s cubic-bezier(.4,0,.2,1) .6s infinite}</style>'
            '<g clip-path="url(#r%s)"><rect class="sw" x="%.1f" y="2" width="42" '
            'height="%d" fill="url(#sh%s)" opacity="0.5"/></g>'
            % (w / 42.0 * 100 + 40, uid, M, H, uid))

    return total, H + 4, (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%.1f" height="%d" '
        'viewBox="0 0 %.1f %d" role="img" aria-label="%s">'
        '<title>%s</title><defs>%s'
        '<linearGradient id="sh%s" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.55"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        '<clipPath id="r%s"><rect x="%d" y="2" width="%.1f" height="%d" rx="11"/>'
        '</clipPath></defs>'
        '<rect x="%d" y="2" width="%.1f" height="%d" rx="11" fill="url(#s%s)" '
        'stroke="%s" stroke-opacity="%s"/>'
        '%s'
        '<path d="M%d 8.5a6.5 6.5 0 0 1 6.5-6.5h%.1f" fill="none" stroke="#FFFFFF" '
        'stroke-opacity="0.07"/>'
        '<g transform="translate(%.1f %.1f) scale(%.4f)" fill="%s"><path d="%s"/></g>'
        '<text x="%.1f" y="26.5" font-family="%s" font-size="%.1f" font-weight="600" '
        'fill="%s">%s</text></svg>'
        % (total, H + 4, total, H + 4, label, label, defs(uid, filled),
           uid, uid, M, w, H,
           M, w, H, uid, edge, edge_op,
           sweep,
           M, w - 13,
           gx, gy, gi, tint, icon_d,
           gx + ICON + GAP, SANS, FS, ink, label))


def square(icon_d, uid='s', fix=''):
    """Icon-only square for the quiet social tail."""
    S, ICON, M = 34, 15, 4
    total = S + M * 2
    k, dy = GLYPH_FIX.get(fix, (1.0, 0.0))
    gi = ICON / 24.0 * k
    off = M + (S - ICON * k) / 2.0
    return total, S + 8, (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img"><defs>%s</defs>'
        '<rect x="%d" y="4" width="%d" height="%d" rx="10" fill="url(#s%s)" '
        'stroke="%s" stroke-opacity="0.75"/>'
        '<path d="M%d 10.5a6.5 6.5 0 0 1 6.5-6.5h%d" fill="none" stroke="#FFFFFF" '
        'stroke-opacity="0.06"/>'
        '<g transform="translate(%.1f %.1f) scale(%.4f)" fill="%s"><path d="%s"/></g>'
        '</svg>'
        % (total, S + 8, total, S + 8, defs(uid, False),
           M, S, S, uid, EDGE,
           M, S - 13,
           off, off + 0.5 + dy, gi, MUTED, icon_d))


# shields returns the view count as digits alone, so everything except the
# number is drawn here: the label half is a chip like any other, and the count
# sits beside it as the only coloured thing, the way an unread badge does.
EYE = ('M12 5C6 5 1.7 11.3 1.7 12S6 19 12 19s10.3-6.3 10.3-7S18 5 12 5Zm0 11.5A4.5 '
       '4.5 0 1 1 16.5 12 4.5 4.5 0 0 1 12 16.5Zm0-7A2.5 2.5 0 1 0 14.5 12 2.5 2.5 '
       '0 0 0 12 9.5Z')


def stat_label(text='profile views'):
    """The label half of the counter, drawn to match the chips."""
    H, PAD_L, ICON, GAP, PAD_R, FS, GAP_R = 20, 9, 12, 6, 12, 11.5, 5
    w = PAD_L + ICON + GAP + text_width(text, FS) + PAD_R
    return w + GAP_R, H, (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%.1f" height="%d" '
        'viewBox="0 0 %.1f %d" role="img" aria-label="%s"><title>%s</title><defs>'
        '<linearGradient id="sv" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient></defs>'
        '<rect x="0.5" y="0.5" width="%.1f" height="%.1f" rx="%.1f" fill="url(#sv)" '
        'stroke="%s"/>'
        '<g transform="translate(%d %.1f) scale(%.4f)" fill="#9AA4F2"><path d="%s"/></g>'
        '<text x="%.1f" y="13.9" font-family="%s" font-size="%.1f" font-weight="600" '
        'fill="#AEB6DC">%s</text></svg>'
        % (w + GAP_R, H, w + GAP_R, H, text, text, SURFACE_TOP, SURFACE_BOT,
           w - 1, H - 1.0, (H - 1) / 2.0, EDGE,
           PAD_L, (H - ICON) / 2.0, ICON / 24.0, EYE,
           PAD_L + ICON + GAP, SANS, FS, text))


# A portfolio is not a Vercel product, so it gets its own mark rather than
# Vercel's triangle: a plain arrow leaving the page, drawn on the same 24u grid.
SITE = 'M4.6 17.7L15.8 6.5l1.7 1.7L6.3 19.4ZM9.2 5.0h9.8v9.8l-2.4-.1V7.4H9.2Z'

PRIMARY = [
    ('portfolio',  'Portfolio',  SITE,         '#FFFFFF', True),
    # The row at the top of the README keeps the domain visible, as the
    # badge it replaces did: at the top the URL is the useful part.
    ('site', 'rudrakshgoswami.vercel.app', SITE, '#FFFFFF', True),
    ('email',      'Email',      'gmail',      '#F08A80', False),
    ('linkedin',   'LinkedIn',   'linkedin',   '#5AA9E6', False),
    ('fiverr',     'Fiverr',     'fiverr',     '#2BD68A', False),
    ('freelancer', 'Freelancer', 'freelancer', '#4FBFFF', False),
    ('upwork',     'Upwork',     'upwork',     '#7FE05A', False),
]

SOCIAL = ['x', 'instagram', 'behance', 'codepen', 'bluesky', 'reddit',
          'quora', 'pinterest']


def main():
    icon_dir = sys.argv[1]
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    report = []

    for i, (slug, label, icon, tint, filled) in enumerate(PRIMARY):
        d = icon if icon.startswith('M') else glyph(icon_dir, icon)
        w, h, svg = chip(label, d, tint, filled, uid=chr(97 + i), fix=icon)
        io.open(os.path.join(OUT, slug + '.svg'), 'w',
                encoding='utf-8', newline='\n').write(svg)
        report.append('%-12s %4.0fx%d' % (slug, w, h))

    for i, slug in enumerate(SOCIAL):
        w, h, svg = square(glyph(icon_dir, slug), uid='q' + chr(97 + i),
                            fix=slug)
        io.open(os.path.join(OUT, slug + '.svg'), 'w',
                encoding='utf-8', newline='\n').write(svg)
        report.append('%-12s %4dx%d' % (slug, w, h))

    w, h, svg = stat_label()
    io.open(os.path.join(OUT, 'views.svg'), 'w',
            encoding='utf-8', newline='\n').write(svg)
    report.append('%-12s %4.0fx%d' % ('views', w, h))

    print('\n'.join(report))
    print('%d files -> %s' % (len(PRIMARY) + len(SOCIAL) + 1, OUT))


if __name__ == '__main__':
    main()
