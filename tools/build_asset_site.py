#!/usr/bin/env python3
"""Build the static Visuals guide from canonical artwork and verified captures."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fonts.raster90 import family as fonts  # noqa: E402
from icons.raster90 import family as icons  # noqa: E402
from icons.raster90 import animation  # noqa: E402
from check_repository import validate_media  # noqa: E402

SOURCE = "https://github.com/byebyebryan/raster90/blob/main/"
DEFAULT_OUTPUT = ROOT / "outputs/raster90/site"


def catalog(root: Path = ROOT) -> dict:
    def source(name: str) -> str:
        return SOURCE + name

    font_data = {
        "clean": {"label": "Clean chamfer", "role": "Selected time cut", "glyphs": dict(fonts.PRIMARY_CLEAN_CHAMFER_DIGITS) | {":": fonts.PRIMARY_CLEAN_CHAMFER_COLON}},
        "compact": {"label": "Compact text", "role": "Complete source vocabulary; runtime packages a subset", "glyphs": dict(fonts.SECONDARY_GLYPHS)},
        "square": {"label": "Square", "role": "Source-only comparison cut", "glyphs": dict(fonts.PRIMARY_SQUARE_DIGITS) | {":": fonts.PRIMARY_SQUARE_COLON}},
        "legacy": {"label": "Legacy fine chamfer", "role": "Historical comparison cut", "glyphs": dict(fonts.PRIMARY_LEGACY_FINE_CHAMFER_DIGITS) | {":": fonts.PRIMARY_LEGACY_FINE_CHAMFER_COLON}},
    }
    weather = []
    for phase, mapping in (("day", icons.WEATHER_DAY), ("night", icons.WEATHER_NIGHT)):
        for condition, rows in mapping.items():
            family = next((key for key, frames in animation.WEATHER_ANIMATION_FRAMES.items() if tuple(rows) == tuple(frames[0])), None)
            weather.append({"id": f"{phase}-{condition:02d}", "condition": condition, "name": icons.WEATHER_CONDITIONS[condition].replace("_", " "), "phase": phase, "rows": rows, "motion": family})
    utility = [
        {"id": "steps", "name": "Steps", "rows": icons.APPROVED_STEP_ICON},
        {"id": "battery", "name": "Battery", "rows": icons.BATTERY_ICON},
        {"id": "unavailable", "name": "Unavailable weather", "rows": icons.UNAVAILABLE_WEATHER_ICON},
        {"id": "stale", "name": "Stale marker", "rows": icons.STALE_MARKER},
    ]
    captures = []
    for entry in validate_media(root):
        captures.append({key: value for key, value in entry.items() if key != "source"} | {"url": "media/" + entry["file"], "record_url": source(entry["checkpoint"])})
    source_paths = ["fonts/raster90/family.py", "icons/raster90/family.py", "icons/raster90/animation.py"]
    return {
        "schema_version": 1, "art_license": "CC0-1.0", "code_license": "MIT",
        "cell_scale": 3, "frame_cells": 150, "icon_storage_cells": icons.MATRIX_CELLS,
        "icon_drawable_cells": icons.DRAWABLE_CELLS,
        "palette": dict(icons.PALETTE), "fonts": font_data,
        "runtime_compact_keys": list(fonts.RUNTIME_SECONDARY_GLYPHS),
        "weather": weather, "utility": utility,
        "battery_bands": [{"name": name, "minimum_exclusive": minimum, "maximum_inclusive": maximum, "rgba": color} for name, minimum, maximum, color in icons.BATTERY_COLOR_BANDS],
        "motion": {"fps": animation.FRAME_RATE, "frames": animation.FRAME_COUNT, "families": dict(animation.WEATHER_ANIMATION_FRAMES)},
        "captures": captures,
        "sources": [{"path": path, "url": source(path), "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest()} for path in source_paths],
    }


def encoded(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


class LocalReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag, attrs):
        self.references.extend(value for key, value in attrs if key in {"src", "href"} and value)


def expected_outputs(root: Path = ROOT) -> dict[str, bytes]:
    data = catalog(root)
    json_text = encoded(data).decode().replace("<", "\\u003c").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (root / "site/index.html").read_text()
    if template.count("<!-- CATALOG -->") != 1:
        raise ValueError("site template must contain one catalog insertion point")
    output = {"index.html": template.replace("<!-- CATALOG -->", f'<script type="application/json" id="catalog">{json_text}</script>').encode(), ".nojekyll": b""}
    for name in ("site.css", "app.js"):
        output[name] = (root / "site" / name).read_bytes()
        digest = hashlib.sha256(output[name]).hexdigest()[:12]
        output["index.html"] = output["index.html"].replace(f'"{name}"'.encode(), f'"{name}?v={digest}"'.encode())
    output["assets/artwork.json"] = encoded({key: value for key, value in data.items() if key != "captures"})
    output["licenses/MIT.txt"] = (root / "LICENSE").read_bytes()
    output["licenses/CC0-1.0.txt"] = (root / "LICENSES/CC0-1.0.txt").read_bytes()
    output["previews/composition-466.png"] = (root / "fonts/raster90/preview/family-native-face-466.png").read_bytes()
    output["previews/composition-466.gif"] = (root / "icons/raster90/preview/icon-family-native-face-466.gif").read_bytes()
    for capture in data["captures"]:
        output[capture["url"]] = (root / "docs/media" / capture["file"]).read_bytes()
    parser = LocalReferences()
    parser.feed(output["index.html"].decode())
    for target in parser.references:
        url = urlsplit(target)
        if not url.scheme and not url.netloc and url.path and url.path not in output:
            raise ValueError(f"site template refers to unpublished file: {target}")
    return output


def validate_build(output: Path, expected: dict[str, bytes]) -> None:
    actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
    if actual != set(expected):
        raise ValueError("site build file closure differs from expected output")
    for name, data in expected.items():
        if (output / name).read_bytes() != data:
            raise ValueError(f"site build drift: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="validate sources and any existing build without writing")
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        if not output.is_relative_to(DEFAULT_OUTPUT):
            raise ValueError("site output must stay under outputs/raster90/site")
        expected = expected_outputs()
        if args.check:
            if output.exists():
                validate_build(output, expected)
            print(f"Asset site OK: {len(expected)} files; canonical artwork and verified media")
        else:
            if output.exists():
                for path in output.rglob("*"):
                    if path.is_symlink():
                        raise ValueError("site output must not contain symlinks")
                shutil.rmtree(output)
            output.mkdir(parents=True)
            for name, data in expected.items():
                path = output / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            validate_build(output, expected)
            print(f"Asset site built: {len(expected)} files at {output}")
        return 0
    except (ValueError, OSError) as error:
        print(f"Asset site failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
