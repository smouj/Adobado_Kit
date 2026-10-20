#!/usr/bin/env python3
"""Check that Adobado Kit, launcher and app repositories share canonical icons."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys


APPS = {
    "photo": ("PhotoAdobado", "photocraft"),
    "art": ("ArtAdobado", "vectorcraft"),
    "film": ("FilmAdobado", "filmcraft"),
    "effect": ("EffectAdobado", "effectcraft"),
    "light": ("LightAdobado", "lightcraft"),
    "sound": ("SoundAdobado", "soundcraft"),
    "design": ("DesignAdobado", "designcraft"),
    "pdf": ("PdfAdobado", "pdfcraft"),
}
KIT_ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_equal(label: str, paths: tuple[Path, ...]) -> list[str]:
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        return [f"FAIL {label}: missing " + ", ".join(missing)]
    hashes = {digest(path) for path in paths}
    if len(hashes) != 1:
        return [f"FAIL {label}: files differ: " + ", ".join(map(str, paths))]
    return [f"OK   {label}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--app-repos-root",
        type=Path,
        help="Optional directory containing the eight standalone app repositories",
    )
    parser.add_argument("--kit-root", type=Path, default=KIT_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = args.kit_root.resolve()
    checks: list[str] = []

    checks += check_equal(
        "launcher PNG and logo lockup",
        (
            root / "launcher/launcher.png",
            root / "launcher/icons/launcher.png",
            root / "assets/icons/launcher.png",
        ),
    )
    checks += check_equal(
        "launcher SVG logo lockup",
        (root / "launcher/launcher.svg", root / "assets/logo.svg"),
    )

    launcher_icons = (
        root / "launcher/launcher.ico",
        root / "launcher/icons/launcher.ico",
        root / "installer/theme/setup.ico",
        root / "installer/theme/uninstall.ico",
    )
    checks += check_equal("launcher icon, embedded copy and installer icons", launcher_icons)

    for slug in APPS:
        for extension in ("png", "ico"):
            checks += check_equal(
                f"{slug} {extension}: hub and launcher",
                (
                    root / f"assets/icons/{slug}.{extension}",
                    root / f"launcher/icons/{slug}.{extension}",
                ),
            )

    if args.app_repos_root:
        repos_root = args.app_repos_root.resolve()
        for slug, (repo, crate) in APPS.items():
            icon_svg = "icon.svg" if slug == "sound" else f"{crate}.svg"
            checks += check_equal(
                f"{repo} canonical SVG",
                (
                    root / f"assets/icons/svg/{slug}.svg",
                    repos_root / repo / f"assets/app-icon/{icon_svg}",
                ),
            )
            app_root = repos_root / repo
            product_png_paths = [
                root / f"assets/icons/{slug}.png",
                app_root / "assets/adobado/icon.png",
                app_root / f"assets/app-icon/{crate}-1024.png",
            ]
            for logo in (app_root / "docs/brand/adobado-logo.png", app_root / "docs/brand/adobado-logo-white.png"):
                if logo.is_file():
                    product_png_paths.append(logo)
            checks += check_equal(f"{repo} product PNG and documentation logos", tuple(product_png_paths))
            checks += check_equal(
                f"{repo} product ICO",
                (
                    root / f"assets/icons/{slug}.ico",
                    repos_root / repo / "assets/adobado/icon.ico",
                    repos_root / repo / f"assets/app-icon/{crate}.ico",
                ),
            )

    for line in checks:
        print(line)
    return 1 if any(line.startswith("FAIL") for line in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
