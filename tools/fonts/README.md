# Bundled fonts

Subset into every SVG by `tools/cards.py`, `tools/scenes.py` and
`tools/links.py`. GitHub serves SVG through `<img>`, which cannot fetch a
font, so the glyphs each file draws are embedded in it as base64 WOFF2.
Every subset keeps its copyright and licence name records, and the full
text of the SIL Open Font License 1.1 is at <https://openfontlicense.org>.

Text is also positioned from these files' own advance widths, so a label
and the shape around it cannot disagree on any machine.

## fraunces.ttf

**Fraunces 9pt Black**

Copyright 2020 The Fraunces Project Authors (github.com/undercasetype/Fraunces)

Licence: SIL Open Font License 1.1, https://scripts.sil.org/OFL

## mono.ttf

**JetBrains Mono Regular**

Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)

Licence: SIL Open Font License 1.1, https://openfontlicense.org

## monob.ttf

**JetBrains Mono Bold**

Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)

Licence: SIL Open Font License 1.1, https://openfontlicense.org

## sans.ttf

**Inter SemiBold**

Copyright 2016 The Inter Project Authors (https://github.com/rsms/inter)

Licence: SIL Open Font License 1.1, https://openfontlicense.org

## serif.ttf

**Instrument Serif Regular**

Copyright 2022 The Instrument Serif Project Authors (https://github.com/Instrument/instrument-serif)

Licence: SIL Open Font License 1.1, https://scripts.sil.org/OFL

## Instanced, not upstream releases

`fraunces.ttf` is Fraunces at `opsz 72, wght 650, SOFT 20, WONK 1`,
`monob.ttf` is JetBrains Mono at `wght 700`, and `sans.ttf` is Inter at
`wght 600`, each cut from the upstream variable font. The OFL permits
modified versions; none is named for its upstream family in any output.

`mono.ttf` carries weight 400 and `monob.ttf` weight 700. The scenes ask
for 600 and 800 as well, and CSS resolves both to the 700 face, which is
what a system monospace stack did anyway since few ship more weights.
