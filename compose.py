#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme: AI scene + real make.fun ghost + big text.

Inputs (defaults point at this builder session's work files):
  scene  - the chosen AI-generated scene, no text in it
  mark   - the official make.fun press mark (white ghost, magenta disc)
Output:
  meme.png - 1200x675 landscape, text big enough to read at 768x480.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SCENE = Path.home() / "workspace/makefun/gta6-meme-x-01-work/scenes/media-generation-gta6-meme-scene-v2-0-f28663fc-9595-4b5f-9e65-9c0aef1deb29.png"
MARK = Path.home() / "workspace/makefun/gta6-meme-x-01-press/mark-1024.png"
OUT = Path(__file__).resolve().parent / "meme.png"

TOP_LINES = ["13 YEARS WAITING", "FOR GTA 6"]
BOTTOM_LINES = ["MY AGENT ALREADY", "GOT PAID ON MAKE.FUN"]


def fit_text(draw, text, max_width, start_size):
    """Largest bold size that fits max_width."""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT, size)


def vertical_band(base, y0, y1, max_alpha, fade_in=True):
    """Dark translucent band fading in (top) or out (bottom)."""
    band = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    steps = y1 - y0
    for i in range(steps):
        frac = i / max(steps - 1, 1)
        alpha = int(max_alpha * (frac if fade_in else 1 - frac))
        bd.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
    base.alpha_composite(band, (0, y0))


def main():
    scene_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SCENE
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT

    scene = Image.open(scene_path).convert("RGB")
    # Center-crop the 3:2 scene to 16:9, then resize to the final size.
    target_ratio = W / H
    sw, sh = scene.size
    if sw / sh > target_ratio:
        new_w = int(sh * target_ratio)
        left = (sw - new_w) // 2
        scene = scene.crop((left, 0, left + new_w, sh))
    else:
        new_h = int(sw / target_ratio)
        top = (sh - new_h) // 2
        scene = scene.crop((0, top, sw, top + new_h))
    img = scene.resize((W, H), Image.LANCZOS).convert("RGBA")

    # Legibility bands behind the top and bottom captions.
    vertical_band(img, 0, 195, 175, fade_in=True)
    vertical_band(img, 495, H, 190, fade_in=False)

    # The real make.fun ghost, big and floating on the right of the scene.
    ghost = Image.open(MARK).convert("RGBA")
    ghost_size = 330
    ghost = ghost.resize((ghost_size, ghost_size), Image.LANCZOS)
    gx, gy = 845, 165
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([gx + 25, gy + ghost_size - 5, gx + ghost_size - 25, gy + ghost_size + 28],
               fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(shadow)
    img.alpha_composite(ghost, (gx, gy))

    draw = ImageDraw.Draw(img)

    def caption(lines, y_start, start_size, gap):
        y = y_start
        for line in lines:
            font = fit_text(draw, line, W - 60, start_size)
            draw.text((W // 2, y), line, font=font, fill="white",
                      stroke_width=max(4, font.size // 11), stroke_fill="black",
                      anchor="ma")
            y += font.size + gap

    caption(TOP_LINES, 12, 88, 2)
    caption(BOTTOM_LINES, 512, 62, 2)

    img.convert("RGB").save(out_path, "PNG")
    print(f"wrote {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
