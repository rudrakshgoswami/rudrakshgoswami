# -*- coding: utf-8 -*-
"""Build preview-cards.html: the README's image stack, in page order.

Every card goes in as a data: URI inside an <img>, which is the same sandbox
GitHub puts them in, so if the type renders here the embedded fonts are working.
The page background toggles between GitHub dark and GitHub light.
"""
import base64
import io
import os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, os.pardir))
ASSETS = os.path.join(ROOT, "assets")

# The README's order. A row of one spans the width, a row of three splits it.
ROWS = [
    ["hero.svg"],
    ["t-record.svg"],
    ["record.svg"],
    ["tile-shipped.svg", "tile-running.svg", "tile-learning.svg"],
    ["t-work.svg"],
    ["store-helios.svg", "store-sanmar.svg"],
    ["t-source.svg"],
    ["repo-roadmap.svg", "repo-vincent.svg", "repo-ipl.svg"],
    ["toolkit.svg"],
    ["now.svg"],
    ["contact.svg"],
]

# The contact row, at its natural size rather than stretched to a column.
CHIPS = ["links/site.svg", "links/linkedin.svg", "links/email.svg",
         "links/views.svg", "links/portfolio.svg", "links/fiverr.svg",
         "links/freelancer.svg", "links/upwork.svg", "links/x.svg",
         "links/instagram.svg", "links/behance.svg", "links/codepen.svg",
         "links/bluesky.svg", "links/reddit.svg", "links/quora.svg",
         "links/pinterest.svg"]

CSS = """
 :root{--page:#0d1117;--label:#7d8590}
 body.light{--page:#ffffff;--label:#59636e}
 body{margin:0;background:var(--page);font:14px -apple-system,"Segoe UI",sans-serif;
      color:var(--label);transition:background .2s}
 main{width:860px;max-width:calc(100% - 32px);margin:0 auto;padding:26px 0 70px}
 h2{font-size:11px;text-transform:uppercase;letter-spacing:1.6px;margin:34px 0 10px;
    font-weight:600}
 img{display:block;border-radius:14px}
 .full{width:100%}
 /* Natural pixel widths that wrap, exactly as the README does it, so this
    preview breaks where GitHub breaks instead of squeezing cards to fit. */
 .row{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
 .row img{flex:0 0 auto}
 .chips{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:14px}
 .chips img{border-radius:0}
 .full+.full{margin-top:12px}
 .bar{position:fixed;top:12px;right:16px;display:flex;gap:8px;z-index:2}
 button{padding:8px 13px;background:#21262d;color:#e6edf3;border:1px solid #30363d;
        border-radius:6px;cursor:pointer;font-size:13px}
 body.light button{background:#f6f8fa;color:#1f2328;border-color:#d1d9e0}
 p{font-size:12px;line-height:1.6;max-width:64ch;margin-top:26px}
"""


def uri(path):
    raw = io.open(path, encoding="utf-8").read()
    ET.fromstring(raw)                                   # well formed, or raise
    if "@font-face" in raw:
        assert "ui-monospace" not in raw, path + " embeds a font and names a stack"
    return "data:image/svg+xml;base64," + base64.b64encode(raw.encode("utf-8")).decode()


def block(title, d):
    out, shown = ["<h2>" + title + "</h2>"], 0
    for row in ROWS:
        have = [f for f in row if os.path.exists(os.path.join(d, f))]
        if not have:
            continue
        shown += len(have)
        if len(row) == 1:
            out.append('<img class="full" src="' + uri(os.path.join(d, have[0]))
                       + '" alt="' + have[0] + '">')
        else:
            out.append('<div class="row">')
            for f in have:
                out.append('<img src="' + uri(os.path.join(d, f))
                           + '" alt="' + f + '">')
            out.append("</div>")
    chips = [c for c in CHIPS if os.path.exists(os.path.join(d, c))]
    if chips:
        shown += len(chips)
        out.append('<div class="chips">')
        for c in chips:
            out.append('<img src="' + uri(os.path.join(d, c))
                       + '" alt="' + c + '">')
        out.append("</div>")
    return "".join(out) if shown else "", shown


def main():
    places = [("profile", ASSETS)]
    spike = os.path.join(ASSETS, "spike")
    if os.path.isdir(spike):
        places += [("spike: " + n, os.path.join(spike, n))
                   for n in sorted(os.listdir(spike))
                   if os.path.isdir(os.path.join(spike, n))]
    body, counts = "", []
    for title, d in places:
        html, n = block(title, d)
        body += html
        if n:
            counts.append("%s %d" % (title, n))
    html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Card preview</title><style>" + CSS + "</style></head><body>"
        '<div class="bar">'
        "<button onclick=\"document.body.classList.toggle('light')\">"
        "GitHub light / dark</button>"
        '<button onclick="location.reload()">replay</button></div><main>'
        + body
        + "<p>Each card is a data: URI inside an img tag, the same sandbox GitHub "
          "uses. Toggle the page background to check both GitHub themes. Reload to "
          "replay the animations.</p></main></body></html>"
    )
    out = os.path.join(ROOT, "preview-cards.html")
    io.open(out, "w", encoding="utf-8", newline=chr(10)).write(html)
    print("preview-cards.html  %.0f KB  (%s)" % (len(html) / 1024.0, ", ".join(counts)))


if __name__ == "__main__":
    main()
