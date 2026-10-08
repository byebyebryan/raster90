# Raster 90 Visuals guide

Public site: <https://dev.byebyebryan.com/raster90/>.

The static guide presents design, typography, icons, source-cell motion, and
dated runtime examples. `tools/build_asset_site.py` reads the canonical font,
icon, and animation modules and verifies `docs/media/manifest.json`. It emits
only a curated 13-file site under ignored `outputs/raster90/site/`.
Python builds the site; Node dependencies are browser-test tooling.

## Local build and inspection

From the repository root:

```sh
rtk python3 -B tools/build_asset_site.py
rtk python3 -B tools/build_asset_site.py --check
rtk python3 -m http.server 8765 --bind 127.0.0.1 \
  --directory outputs/raster90/site
```

Open `http://127.0.0.1:8765/`; stop only the server started for this task.
Relative assets work under the GitHub Pages `/raster90/` prefix. Component
self-contained local previews remain alongside their original sources.

## Browser checks

From `site/`:

```sh
rtk npm ci
rtk npm exec -- playwright install chromium firefox webkit
rtk npm test
```

For a Chromium-only local pass, use `rtk npm test -- --project=chromium`.
Firefox and WebKit require their host libraries; CI installs them on its runner.

Pretest builds the site. Playwright owns a temporary loopback server and checks
deep links, keyboard tabs, glyph coverage, filter/zoom behavior, transparent PNG
exports, automatic loops, visibly changing one-shot frames, reduced motion,
the animated hero, capture loading, and mobile/desktop overflow across Chromium,
Firefox, and WebKit. Artifacts go under `outputs/raster90/site-tests/`.
CI uses Node 24 and installs all three engines with their runner dependencies.

## Publishing

Repository/browser checks run on main pushes and pull requests. Publishing is
a separate manually dispatched GitHub Pages workflow:

```sh
rtk proxy gh workflow run publish.yml --ref main
```

The workflow verifies docs/media, builds the site, validates its exact file
closure, and uploads only `outputs/raster90/site/`. Initial setup enables Pages
with GitHub Actions as the source. Normal commits do not automatically publish.
Inspect the deployed URL after completion.

## Content and licensing

Matrices are never copied into hand-maintained site data. The builder exports
all four type cuts, day/night mappings, utility/state artwork, battery bands,
and exact motion frames. Motion loops on entering its section, with a one-second
resting gap; Pause, Play once, and frame stepping remain available. Reduced-
motion preferences start previews still. The generated full-face hero uses the
same canonical partly-day frames and has a pause control. Preview loops are
presentation-only; the watch still plays one fresh-weather gesture. This is an
inspector, not proof of device playback.

Art exports are CC0; code is MIT. Capture bytes remain unchanged with dated
limits and hashes; see [Licensing](../docs/licensing.md) and
[Validation](../docs/validation.md). Generated composition fixtures are labeled
separately from device captures.
