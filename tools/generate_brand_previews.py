#!/usr/bin/env python3
"""Render honest Adobado brand cards for apps without a validated UI.

The script is intentionally offline and writes only into the requested output
directory. It does not modify app repositories or publish files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH, HEIGHT = 1200, 675
INK = (11, 14, 19)
CREAM = (238, 242, 246)
MUTED = (152, 163, 177)
DIM = (120, 132, 147)
LINE = (37, 44, 55)

APPS = (
    ("ArtAdobado", "art", (230, 82, 194), "Windows: compilación correcta · uso pendiente"),
    ("LightAdobado", "light", (245, 210, 76), "Windows: compilación correcta · uso pendiente"),
    ("EffectAdobado", "effect", (154, 117, 248), "Windows: compilación correcta · uso pendiente"),
    ("DesignAdobado", "design", (134, 223, 78), "Windows: compilación correcta · uso pendiente"),
    ("PdfAdobado", "pdf", (79, 131, 232), "Windows: compilación correcta · uso pendiente"),
)


def font_path(bold: bool) -> Path | None:
    candidates = (
        (Path(r"C:\Windows\Fonts\segoeuib.ttf"), Path(r"C:\Windows\Fonts\segoeui.ttf")),
        (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")),
    )
    for pair in candidates:
        candidate = pair[0 if bold else 1]
        if candidate.exists():
            return candidate
    return None


def fitted_font(text: str, max_width: int, preferred_size: int, bold: bool) -> ImageFont.ImageFont:
    path = font_path(bold)
    if path is None:
        return ImageFont.load_default()
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(preferred_size, 15, -1):
        font = ImageFont.truetype(str(path), size)
        left, _, right, _ = probe.textbbox((0, 0), text, font=font)
        if right - left <= max_width:
            return font
    return ImageFont.truetype(str(path), 16)


def background(accent: tuple[int, int, int]) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (*INK, 255))
    for cx, cy, radius, color, alpha in (
        (140, 130, 410, accent, 50),
        (1060, 590, 470, (91, 141, 239), 42),
        (780, 35, 330, (134, 223, 78), 22),
    ):
        glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(*color, alpha))
        image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(100)))
    return image.convert("RGB")


def render(app: str, slug: str, accent: tuple[int, int, int], status: str, icon_dir: Path, output_dir: Path) -> Path:
    icon_path = icon_dir / f"{slug}.png"
    if not icon_path.is_file():
        raise FileNotFoundError(f"Missing app icon: {icon_path}")

    image = background(accent)
    icon = Image.open(icon_path).convert("RGBA")
    icon.thumbnail((190, 190), Image.Resampling.LANCZOS)
    image.paste(icon, (88, 124), icon)

    draw = ImageDraw.Draw(image)
    text_x = 326
    max_width = WIDTH - text_x - 64
    title_font = fitted_font(app, max_width, 64, True)
    status_font = fitted_font(status, max_width, 34, False)
    subtitle = "Herramienta de escritorio para crear y editar tus proyectos"
    subtitle_font = fitted_font(subtitle, max_width, 30, False)
    label1 = "ADOBADO KIT  ·  IDENTIDAD DE PRODUCTO"
    label2 = "Vista de marca; la interfaz aún no se ha validado"
    footer_font = fitted_font(label1, 1040, 19, True)
    footer2_font = fitted_font(label2, 1040, 19, False)

    draw.text((text_x, 137), app, font=title_font, fill=CREAM)
    draw.text((text_x + 2, 232), status, font=status_font, fill=MUTED)
    draw.text((text_x + 2, 292), subtitle, font=subtitle_font, fill=MUTED)
    draw.line((80, 556, 1120, 556), fill=LINE, width=2)
    draw.text((80, 586), label1, font=footer_font, fill=MUTED)
    draw.text((80, 618), label2, font=footer2_font, fill=DIM)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{app}-preview.png"
    image.save(output_path, format="PNG", optimize=True)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icon-dir", type=Path, required=True, help="Directory containing the app PNG icons")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where preview PNGs are written")
    args = parser.parse_args()
    for app, slug, accent, status in APPS:
        print(render(app, slug, accent, status, args.icon_dir, args.output_dir))


if __name__ == "__main__":
    main()
