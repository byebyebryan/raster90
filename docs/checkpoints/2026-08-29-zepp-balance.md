# Amazfit Balance interactive checkpoint — 2026-08-29

The owner identified the original Amazfit Balance at Zepp API level 307 /
firmware `3.28.8.1` and provided a native 480×480 screenshot of the QR-preview
package. It rendered native weather with `15°C`, complete `SAT 29 AUG`, unclipped
`10:17`, fixed-width `00000` steps, and `61%` battery.

The retained owner-provided PNG is
`outputs/references/amazfit-balance-native-weather-render.png`, SHA-256
`600337b245a89c8cc0750d9c5cffbc16b7fbd15c778ac896ee7acf1ea536146c`.
This proves sampled interactive appearance for the then-debug-enabled package.
It does not establish AOD, controlled refresh/lifecycle behavior, power impact,
or the later metadata-only debug-disabled rebuild.

The subsequent test-drive package uses `debug: false`. On 2026-10-07 the owner
reported reliable regular use of both platforms without notable issues, with
AOD unused on either. That report supplements this dated screenshot without
identifying an exact installed package hash. See [Validation](../validation.md)
for the current platform comparison and remaining limits.
