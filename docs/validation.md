# Platform capabilities and validation

Reconciled 2026-10-07. Wear OS is the design baseline. The owner reported
regular use of both watch faces without notable issues and now uses Wear OS
more often. AOD was unused on both during that period. This is useful wearer
evidence, separate from the dated package/capture records below.

## Implemented behavior

| Capability | Wear OS / OnePlus Watch 3 | Zepp OS / original Amazfit Balance |
|---|---|---|
| Source artwork | Shared project-owned bitmap fonts and icons | Same canonical static artwork |
| Canvas / source cells | 466×466; 450×450 active frame; solid 3×3 cells | 480×480; 450×450 active frame; solid 3×3 cells |
| Time and date | No seconds; static colon; system 12/24-hour setting | No seconds; static colon; native time binding; bounded date refresh |
| Information rows | Complete weather/steps/battery rows centered by formatted width | Existing fixed horizontal anchors |
| Temperature | Celsius default; editor Fahrenheit override; provider-unit conversion | Native system unit; no custom override |
| Weather availability | Fresh, stale, unavailable, unknown branches | Valid native conditions; neutral fallback for missing/malformed data; no stale-age semantics |
| Weather motion | Eight exact frames at 4 fps; one fresh-data `ON_VISIBLE` gesture; return to first frame | Static; missing animation is a known gap |
| Steps | Formatted five/six-digit boundary handling | Fixed five-digit value |
| Battery | White/yellow/orange/red icon tints; percentage stays white | Same four canonical tint bands |
| Ambient/AOD | Monochrome time only | Time-only AOD layout implemented |
| Packaging | Resource-only WFF v2; no application logic or required companion | Independent Zepp OS v3 package; native UI/sensor bindings |

Implemented behavior is a source contract, not proof that every branch has
been observed on a device. The table does not promise equal platform features.
Sunrise/sunset display is [deferred](sunrise-sunset-spike.md). Rare color events
and additional complications are not scheduled.

## Latest useful evidence

| Record | What it establishes | Limits |
|---|---|---|
| [2026-10-07 centered rows](checkpoints/2026-10-07-centered-rows.md) | Exact current runtime's interactive composition on both Wear emulators and the physical Watch 3; live physical night-family weather; emulator `100%` and red `9%` battery rows | Still captures do not prove motion; no new ambient, 12/24-hour, stale-weather, physical low-battery, or battery-impact validation |
| [2026-08-29 Amazfit](checkpoints/2026-08-29-zepp-balance.md) | Owner-provided native 480×480 interactive appearance with live weather, date/time, steps, battery | Captured debug-enabled package predates the metadata-only debug-disabled rebuild; no AOD or simulator matrix |
| [2026-08-26 weather refresh](checkpoints/2026-08-26-weather-icons.md) | Earlier static WFF tree's physical interactive rendering with refreshed icons and live night weather | Historical tree; no sustained AOD or tint-transition evidence |
| [2026-08-21 simulated weather](checkpoints/2026-08-21-simulated-weather.md) | Earlier WFF tree's native emulator available-weather rendering and confirmed time-only Dozing | Simulated location; predates weather refresh, animation, and centering |
| [2026-08-20 clean chamfer](checkpoints/2026-08-20-clean-chamfer.md) | Earlier time cut's native interactive and Dozing rendering | Predates final steps/icon promotion |
| Reliable regular use, reported 2026-10-07 | Both platforms worked well over the reported period | Not an exact-package capture or controlled battery study; AOD unused |

The centered-row tree is the runtime committed at `ac8e6fa`. Its built and
installed APK SHA-256 is
`9d3b9efe5865a8dc955cd3a447169bf4dc8b8c195a84fff127f697c964f32cf2`.
Its source/asset, 56-test, build/lint, WFF schema, and memory gates passed at
that checkpoint. Maximum active/ambient memory was 1,863,648 / 155,520 bytes.
These are dated results, not the result of a new run merely because this page
was edited.

## Remaining evidence gaps

- Retained motion footage confirming WFF trigger, cadence, and return to rest.
- Live stale-weather behavior on the physical watch.
- Sustained physical AOD on either watch; no wearer-use evidence yet.
- Controlled physical battery tint transitions and battery impact.
- Exact-package Amazfit debug-disabled capture, simulator cases, unavailable
  weather, and controlled 12/24-hour/lifecycle checks.
- Explicit optical acceptance of the centering change at wrist distance and
  relevant brightness levels. Reliable routine use should inform this judgment
  rather than being discarded, but it is not a recorded decision on every edit.

These are validation limits, not automatically scheduled development work.
Physical screenshots establish sampled rendering; synthetic previews and
source tests establish their own narrower contracts. Preserve that distinction
when choosing public images or updating status text.
