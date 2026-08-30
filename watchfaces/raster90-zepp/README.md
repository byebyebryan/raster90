# Raster 90 — Amazfit Balance study package

This directory is an isolated Zepp OS v3 watch-face package for the original
Amazfit Balance.  It is deliberately separate from the Wear OS/WFF Gradle
module.  The target watch was observed by the project owner at Zepp API level
307 (firmware `3.28.8.1`), which corresponds to the v3 API family.  The
package declares `compatible: 3.0.0`, `minVersion: 3.0.0`, and
`target: 3.7.0`; `IMG_TIME` and `TEXT_IMG` are the lowest documented API
surface used by this static slice.

The package uses the native 480x480 Balance coordinate space.  Raster 90's
450x450 active frame remains centered at `(15,15)`, with one source cell
expanded to one solid 3x3 pixel square.  `preview.png` is generated from the
same native composition and reduced deterministically to the 324x324 picker
size.

## Local workflow

From this directory:

```sh
npm ci
npm run generate
npm run check
```

The generator imports the canonical matrices from `fonts/raster90/family.py`
and `icons/raster90/family.py`; it does not duplicate or hand-edit runtime
art.  `generate:check` verifies the exact PNG bytes, dimensions, palette,
transparent icon gutter, and complete `assets/balance.r/images/` closure.
Zeus build output is written below the ignored `dist/` directory.

## Static weather mapping

Zepp's documented forecast indices 0–28 are represented by one generated
transparent `weather/NN.png` tile and one opaque-black
`weather-bound/NN.png` replacement plane each.  The native watch-face
`IMG_LEVEL` weather binding uses the replacement planes so a valid condition
cleanly covers the neutral fallback beneath it.  The adapter maps indices to
the nearest authored Raster 90 family: cloudy (0,4,26), rain (1,7,27), snow
(2,8), clear day (3), light rain (5), light snow (6), heavy snow (9,16), heavy
rain (10,18,19,21,24), windy (11,23), mist (14,17,22), sleet (12), fog (13),
thunderstorm (15,20), unknown (25), and clear night (28).  The runtime only
displays a condition when the sensor returns a valid 0–28 record; missing or
malformed data stays on the neutral icon with `--`.  Stale-age semantics are
intentionally outside this checkpoint.

The interactive face contains time, centered date, weather plus system-unit
temperature, steps, and battery.  Data rows are normal-mode-only; AOD exposes
the time digits and static colon alone.  Battery state uses four static
canonical tints and the Zepp sensor's current percentage.  Seconds, weather
animation, custom unit overrides, and stale presentation are not included
here.

The face requests only `data:user.hd.step`, which allows the runtime to format
the current step count as Raster 90's fixed five-digit value with leading
zeroes.  Condition and temperature use Zepp's watch-face-native `WEATHER` and
`WEATHER_CURRENT` widget bindings; the deprecated Mini Program `Weather` class
is not used, and the face neither polls weather nor starts geolocation.  Date
refreshes on a bounded 60-second timer, while steps and battery use their v3
`onChange` callbacks.  UI and sensor access use the `@zos/ui` and `@zos/sensor`
modules rather than firmware-injected legacy globals.  A
`WIDGET_DELEGATE.resume_call` refreshes all four data rows when the face appears
or returns; teardown removes listeners and clears timers.  Debug mode is
disabled for the test-drive build.  The lifecycle and build-stage log calls
remain available for a future debug build.

## Tooling boundary

The package pins `@zeppos/zeus-cli` 1.9.3, the current npm `latest` release as
checked on 2026-08-29.  A clean `npm ci` reports no production dependency
advisories with `npm audit --omit=dev`, but the CLI's local-only transitive
development tree reports 31 advisories, including old `lodash` and `tar`
branches.  These npm packages build the ZAB and are not included in the watch
runtime.  Do not apply npm's proposed forced fix: it offers a downgrade to
Zeus 1.6.7.  Recheck this boundary when Zepp publishes a newer CLI.

## Physical checkpoint and open gates

`app.json` uses the registered Raster 90 watchface appId `1125469`.  The v3
screen-adaptation target is resolved to the current Balance device sources by
Zeus when building or previewing with `--target "Amazfit Balance"`.  Zepp login,
QR preview, simulator, and device actions remain separate explicit steps.

The 2026-08-29 physical preview on API level 307 / firmware `3.28.8.1` rendered
the native weather condition with `15°C`, complete `SAT 29 AUG`, unclipped
`10:17`, fixed-width `00000` steps, and `61%` battery on the original Balance.
The retained owner-provided 480×480 PNG is
`outputs/references/amazfit-balance-native-weather-render.png`, SHA-256
`600337b245a89c8cc0750d9c5cffbc16b7fbd15c778ac896ee7acf1ea536146c`.
It proves interactive resting appearance for the then-debug-enabled package;
it does not prove AOD, long-term refresh, power impact, or the later
metadata-only debug-disabled rebuild.

The current checkpoint has `debug: false` for a wearer test drive.  Remaining
acceptance includes selecting that exact package, sustained AOD, resume and
weather refresh over time, step changes, all battery tint thresholds,
12/24-hour behavior, unavailable weather, and a repeatable Balance-simulator
state matrix.  No simulator or still capture substitutes for final physical
AMOLED and battery judgment.
