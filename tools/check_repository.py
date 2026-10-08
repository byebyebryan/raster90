#!/usr/bin/env python3
"""Portable, read-only repository checks; use --docs-only for a prose change."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def inventory(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, check=True, capture_output=True,
    )
    return sorted(set(result.stdout.decode().split("\0")) - {""})


def prose(text: str) -> str:
    """Exclude fenced examples from link and heading interpretation."""
    output = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            output.append("")
        else:
            output.append(line if fence is None else "")
    return "\n".join(output)


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value and key in {"href", "src"}:
                self.links.append(value)
            if value and key == "id":
                self.ids.add(value)


def anchors(text: str) -> set[str]:
    parser = References()
    parser.feed(prose(text))
    result = parser.ids
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose(text), re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        result.add(slug if count == 0 else f"{slug}-{count}")
        seen[slug] = count + 1
    return result


def check_docs(root: Path, files: list[str]) -> int:
    documents = [name for name in files if name.endswith(".md")]
    for name in documents:
        path = root / name
        text = path.read_text()
        if not text.endswith("\n") or text.endswith("\n\n"):
            raise ValueError(f"{name}: expected one final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line != line.rstrip():
                raise ValueError(f"{name}:{number}: trailing whitespace")
        visible = prose(text)
        parser = References()
        parser.feed(visible)
        links = parser.links + re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", visible)
        for target in links:
            target = target.split(' "', 1)[0].strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                raise ValueError(f"{name}: missing local destination {target}")
            if url.fragment and destination.suffix == ".md":
                if unquote(url.fragment) not in anchors(destination.read_text()):
                    raise ValueError(f"{name}: missing heading {target}")
    return len(documents)


def validate_media(root: Path) -> list[dict]:
    manifest = json.loads((root / "docs/media/manifest.json").read_text())
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported public-media manifest schema")
    captures = manifest["captures"]
    names = set()
    for capture in captures:
        name = capture["file"]
        if not re.fullmatch(r"[a-z0-9._-]+\.png", name) or name in names:
            raise ValueError(f"unsafe or duplicate public capture name: {name}")
        names.add(name)
        data = (root / "docs/media" / name).read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"not a PNG: {name}")
        if hashlib.sha256(data).hexdigest() != capture["sha256"]:
            raise ValueError(f"public capture hash drift: {name}")
        if struct.unpack(">II", data[16:24]) != (capture["width"], capture["height"]):
            raise ValueError(f"public capture dimensions drift: {name}")
        source = (root / capture["source"]).resolve()
        if not source.is_relative_to(root.resolve() / "outputs"):
            raise ValueError(f"public capture source outside outputs: {name}")
        if source.exists() and source.read_bytes() != data:
            raise ValueError(f"capture differs from original: {name}")
        if not (root / capture["checkpoint"]).is_file():
            raise ValueError(f"missing capture checkpoint: {name}")
        for key in ("date", "target", "kind", "mode", "claim"):
            if not capture.get(key):
                raise ValueError(f"capture has no {key}: {name}")
    actual = {path.name for path in (root / "docs/media").glob("*.png")}
    if names != actual:
        raise ValueError("public capture manifest does not cover exact PNG closure")
    return captures


def check_boundaries(root: Path, files: list[str]) -> None:
    forbidden = {"build", "dist", "node_modules", "__pycache__", ".gradle", "outputs"}
    for name in files:
        path = Path(name)
        if forbidden.intersection(path.parts) or path.suffix in {
            ".apk", ".aab", ".zab", ".pyc", ".log", ".jks", ".keystore", ".pem", ".p12", ".pfx",
        }:
            raise ValueError(f"transient or private file in repository inventory: {name}")
        if name.startswith("watchfaces/raster90/src/") and path.suffix in {".java", ".kt", ".ttf", ".otf"}:
            raise ValueError(f"application code/runtime font in resource-only WFF bundle: {name}")
    android = "{http://schemas.android.com/apk/res/android}"
    app = ET.parse(root / "watchfaces/raster90/src/main/AndroidManifest.xml").getroot().find("application")
    if app is None or app.get(android + "hasCode") != "false":
        raise ValueError("WFF application must declare hasCode=false")
    properties = {node.get(android + "name"): node.get(android + "value") for node in app.findall("property")}
    if properties.get("com.google.wear.watchface.format.version") != "2":
        raise ValueError("WFF format must remain v2")
    for name in ("LICENSE", "LICENSES/CC0-1.0.txt", "third_party/pixel-operator/LICENSE.txt"):
        if not (root / name).is_file():
            raise ValueError(f"missing license: {name}")


def run(root: Path, args: list[str]) -> None:
    print("Check:", " ".join(args), flush=True)
    subprocess.run([sys.executable, "-B", *args], cwd=root, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-only", action="store_true")
    args = parser.parse_args()
    try:
        files = inventory(ROOT)
        count = check_docs(ROOT, files)
        check_boundaries(ROOT, files)
        captures = validate_media(ROOT)
        print(f"Repository/docs OK: {count} documents, {len(captures)} provenance-checked captures", flush=True)
        if not args.docs_only:
            for tool in ("generate_raster90_assets", "generate_raster90_zepp_assets", "render_raster90_font_family", "render_raster90_icon_family"):
                run(ROOT, [f"tools/{tool}.py", "--check"])
            run(ROOT, ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"])
            run(ROOT, ["watchfaces/raster90-zepp/tests/test_generate_raster90_zepp_assets.py"])
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Repository check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
