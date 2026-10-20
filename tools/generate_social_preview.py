#!/usr/bin/env python3
"""Compose an honest social preview from a real Adobado app screenshot.

The screenshot is used only as a softly blurred background. Product logos are
loaded from the canonical icon directory, and the caption names the app shown.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH, HEIGHT = 1280, 640
INK = (8, 10, 14)
PANEL = (17, 21, 28)
TEXT = (238, 242, 246)
MUTED = (180, 190, 202)
LIME = (184, 243, 74)
LINE = (255, 255, 255, 42)
APPS = (
    ("Photo", "photo"),
    ("Art", "art"),
    ("Film", "film"),
    ("Effect", "effect"),
    ("Light", "light"),
    ("Sound", "sound"),
    ("Design", "design"),
    ("PDF", "pdf"),
)


def font(bold: bool, size: int) -> ImageFont.ImageFont:
    candidates = (
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    )
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def crop_cover(source: Image.Image) -> Image.Image:
    scale = max(WIDTH / source.width, HEIGHT / source.height)
    resized = source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def kit_mark(size: int = 96) -> Image.Image:
    scale = 4
    canvas = Image.new("RGBA", (64 * scale, 64 * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (2 * scale, 2 * scale, 62 * scale, 62 * scale),
        radius=16 * scale,
        fill="#11151c",
        outline="#2a323e",
        width=2 * scale,
    )
    draw.ellipse((13 * scale, 13 * scale, 37 * scale, 37 * scale), fill=(255, 122, 89, 235))
    draw.ellipse((28 * scale, 13 * scale, 52 * scale, 37 * scale), fill=(108, 182, 255, 209))
    draw.rounded_rectangle((14 * scale, 43 * scale, 50 * scale, 51 * scale), radius=4 * scale, fill="#b8f34a")
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def render(screenshot: Path, icon_dir: Path, output: Path) -> None:
    source = Image.open(screenshot).convert("RGB")
    background = crop_cover(source).filter(ImageFilter.GaussianBlur(11))

    # Dark, graded scrim preserves the real app as context while keeping the
    # title and app marks readable at small social-preview sizes.
    scrim = Image.new("RGBA", (WIDTH, HEIGHT), (INK[0], INK[1], INK[2], 150))
    grad = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for x in range(WIDTH):
        alpha = round(45 + 80 * (1 - x / WIDTH))
        gd.line((x, 0, x, HEIGHT), fill=(8, 10, 14, alpha))
    background = Image.alpha_composite(background.convert("RGBA"), scrim)
    background = Image.alpha_composite(background, grad)

    # Soft brand glows; they tint the photograph without replacing its content.
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((-190, -180, 360, 370), fill=(255, 122, 89, 35))
    draw.ellipse((970, 330, 1470, 820), fill=(108, 182, 255, 28))
    background = Image.alpha_composite(background, glow.filter(ImageFilter.GaussianBlur(95)))
    draw = ImageDraw.Draw(background)

    # Main Kit lockup matches assets/logo.svg.
    mark = kit_mark(92)
    background.alpha_composite(mark, (76, 58))
    draw.text((190, 67), "Adobado Kit", font=font(True, 43), fill=TEXT)
    draw.text((192, 121), "HERRAMIENTAS CREATIVAS LOCALES", font=font(True, 14), fill=LIME)

    draw.text((78, 228), "Creatividad", font=font(True, 64), fill=TEXT)
    draw.text((78, 304), "sin nube.", font=font(True, 64), fill=TEXT)
    draw.text(
        (82, 397),
        "Ocho apps de escritorio open source para tus archivos.",
        font=font(False, 21),
        fill=MUTED,
    )
    draw.text((82, 464), "LA FAMILIA ADOBADO", font=font(True, 13), fill=LIME)

    # Every mark is loaded from the canonical hub assets used by the launcher
    # and each app repository.
    icon_size = 52
    gap = 21
    x0 = 82
    for index, (label, slug) in enumerate(APPS):
        icon_path = icon_dir / f"{slug}.png"
        if not icon_path.is_file():
            raise FileNotFoundError(f"Missing canonical app icon: {icon_path}")
        x = x0 + index * (icon_size + gap)
        icon = Image.open(icon_path).convert("RGBA")
        icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
        draw.rounded_rectangle((x - 4, 518, x + icon_size + 4, 578), radius=12, fill=(17, 21, 28, 210), outline=LINE)
        background.alpha_composite(icon, (x, 522))
        bbox = draw.textbbox((0, 0), label, font=font(False, 11))
        label_width = bbox[2] - bbox[0]
        draw.text((x + (icon_size - label_width) / 2, 585), label, font=font(False, 11), fill=MUTED)

    # Explicit provenance: this image is a real FilmAdobado capture, not a
    # synthetic product interface.
    pill = (866, 514, 1204, 570)
    draw.rounded_rectangle(pill, radius=16, fill=(8, 10, 14, 216), outline=(184, 243, 74, 185), width=1)
    draw.ellipse((886, 535, 896, 545), fill=LIME)
    draw.text((908, 528), "CAPTURA REAL", font=font(True, 12), fill=LIME)
    draw.text((908, 546), "FilmAdobado · Windows", font=font(False, 14), fill=TEXT)

    output.parent.mkdir(parents=True, exist_ok=True)
    background.convert("RGB").save(output, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", type=Path, required=True, help="Real FilmAdobado screenshot")
    parser.add_argument("--icon-dir", type=Path, required=True, help="Canonical eight-app PNG icon directory")
    parser.add_argument("--output", type=Path, required=True, help="Output PNG path, 1280x640")
    args = parser.parse_args()
    render(args.screenshot, args.icon_dir, args.output)


if __name__ == "__main__":
    main()
