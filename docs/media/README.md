# Documentation media

A small, tracked publication subset of unretouched runtime captures. The full
local evidence archive stays Git-ignored; these copies do not replace it.
[manifest.json](manifest.json) is the machine-readable provenance used by the
asset site and repository checker.

| File | Record | Supported claim |
|---|---|---|
| `raster90-interactive-watch3-centered-466.png` | [2026-10-07 physical](../checkpoints/2026-10-07-centered-rows.md) | Current centered-row interactive composition; live weather; still image |
| `raster90-interactive-wear5-opw3-466.png` | [2026-08-21 emulator](../checkpoints/2026-08-21-simulated-weather.md) | Earlier tree; simulated-location provider weather |
| `raster90-ambient-wear5-opw3-466.png` | [2026-08-21 emulator](../checkpoints/2026-08-21-simulated-weather.md) | Earlier tree in confirmed time-only Dozing |
| `raster90-interactive-amazfit-balance-480.png` | [2026-08-29 owner screenshot](../checkpoints/2026-08-29-zepp-balance.md) | Static Amazfit interactive appearance before debug metadata changed |

Every manifest entry records source path, date, target, kind, mode, dimensions,
SHA-256, checkpoint, and claim. The checker verifies tracked bytes and compares
the original when present. A fresh checkout can validate the published hash
without requiring ignored local evidence.

Copy bytes from a completed checkpoint, add precise provenance, and keep claims
within its evidence. Never retouch runtime captures or imply that an old ambient
image validates a newer physical tree. Licensing covers Raster 90's own artwork,
not third-party platform UI; see [Licensing](../licensing.md).
