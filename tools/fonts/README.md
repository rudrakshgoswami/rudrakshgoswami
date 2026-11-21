# Bundled fonts

Subset into every card by `tools/cards.py`. GitHub serves SVG through
`<img>`, which cannot fetch a font, so the glyphs each card draws are
embedded in it as base64 WOFF2. Each subset keeps its copyright and
licence name records, and the full text of the SIL Open Font License 1.1
is at <https://openfontlicense.org>.

## fraunces.ttf

**Fraunces 9pt Black**

Copyright 2020 The Fraunces Project Authors (github.com/undercasetype/Fraunces)

Licence: SIL Open Font License 1.1, https://scripts.sil.org/OFL

## mono.ttf

**JetBrains Mono Regular**

Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)

Licence: SIL Open Font License 1.1, https://openfontlicense.org

## serif.ttf

**Instrument Serif Regular**

Copyright 2022 The Instrument Serif Project Authors (https://github.com/Instrument/instrument-serif)

Licence: SIL Open Font License 1.1, https://scripts.sil.org/OFL

`fraunces.ttf` is not the upstream release: it is the variable font
instanced at `opsz 72, wght 650, SOFT 20, WONK 1`, which the OFL permits
as a modified version. It is not named Fraunces in any card's output.
