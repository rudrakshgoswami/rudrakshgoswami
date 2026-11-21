# Bundled fonts

Subset into every SVG by `tools/cards.py` and `tools/scenes.py`. GitHub
serves SVG through `<img>`, which cannot fetch a font, so the glyphs each
card draws are embedded in it as base64 WOFF2. Each subset keeps its
copyright and licence name records, and the full text of the SIL Open Font
License 1.1 is at <https://openfontlicense.org>.

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

## serif.ttf

**Instrument Serif Regular**

Copyright 2022 The Instrument Serif Project Authors (https://github.com/Instrument/instrument-serif)

Licence: SIL Open Font License 1.1, https://scripts.sil.org/OFL

## Instanced, not upstream releases

`fraunces.ttf` is Fraunces at `opsz 72, wght 650, SOFT 20, WONK 1` and
`monob.ttf` is JetBrains Mono at `wght 700`, both cut from the upstream
variable fonts. The OFL permits modified versions; neither is named for
its upstream family in any card's output.

`mono.ttf` carries weight 400 and `monob.ttf` weight 700. The scenes ask
for 600 and 800 as well, and CSS resolves both to the 700 face, which is
what a system monospace stack did anyway since few ship more weights.
