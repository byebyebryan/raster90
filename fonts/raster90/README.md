# Raster 90 Font Family

This directory is the first-class, project-owned bitmap font used by the
Raster 90 watch face. It is not an exported TTF/OTF and has no runtime font
dependency: the fictional display grid is the format.

## Contents

- `family.py` is the authoritative matrix source.
- `preview/index.html` is the tracked, self-contained overview with complete
  primary and secondary matrix sheets plus an interactive local preview.
- The PNGs under `preview/` are deterministic native-scale and magnified
  specimens generated from the same source.

The family contains two optical cuts on one solid 3×3 physical-cell grid:

- **Primary/display:** fixed-width `0–9` and colon for time, using 26×32 digit
  boxes, a 10×32 colon box, a plain closed zero, and the approved one-cell
  convex-corner chamfer.
- **Secondary/text:** a complete 5×7 source vocabulary containing space,
  symbols, digits, uppercase, lowercase, and common punctuation. The watch-face
  APK deliberately packages only the subset its current WFF expressions emit.

Regenerate and byte-check the tracked presentation from the repository root:

```sh
rtk python3 -B tools/render_raster90_font_family.py
rtk python3 -B tools/render_raster90_font_family.py --check
```

Do not edit files under `preview/` by hand. Update `family.py`, regenerate, and
review both the complete sheets and the native 466×466 face specimen.
