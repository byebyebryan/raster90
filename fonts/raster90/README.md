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

The family contains two named optical cuts on one solid 3×3 physical-cell grid,
plus a retained legacy comparison control:

- **Primary square:** `PRIMARY_SQUARE_DIGITS` and
  `PRIMARY_SQUARE_COLON` preserve the unmodified square construction.
- **Primary clean chamfer:** `PRIMARY_CLEAN_CHAMFER_DIGITS` and
  `PRIMARY_CLEAN_CHAMFER_COLON` contain the reviewed fine-raster edit. The
  stable runtime aliases `PRIMARY_DIGITS` and `PRIMARY_COLON` point here, so
  the watch face uses this cut.
- **Legacy fine chamfer:** `PRIMARY_LEGACY_FINE_CHAMFER_DIGITS` retains the
  earlier algorithmic one-cell/global chamfer as a named study control; it is
  not selected by the runtime.
- Both primary variants use fixed-width `0–9` and colon glyphs, 26×32 digit
  boxes, a 10×32 colon box, and a plain closed zero. The tracked
  `primary-display-cut.png` shows clean chamfer; `primary-square-cut.png`
  shows the square control.
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
