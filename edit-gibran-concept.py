#!/usr/bin/env python3
"""Translate Mas's Gibran concept image to English by editing it in place.

The scene (faces, ghost, TV, banner) is kept pixel-for-pixel. Only the
Indonesian text is covered with matching background colour and redrawn in
English with a matching style. Output: meme-gibran.png (1536x1024).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path.home() / "workspace/makefun/gta6-meme-x-01-gibran-concept.png"
OUT = Path(__file__).resolve().parent / "meme-gibran.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BOLD_COND = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
REG_COND = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"

INK = (15, 15, 15)
PURPLE = (110, 45, 190)
BUBBLE_WHITE = (240, 238, 239)
LETTER_WHITE = (240, 240, 242)
HEADLINE_WHITE = (245, 243, 246)
BLACK = (0, 0, 0)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_size(text, path, start, max_w):
    """Largest font size <= start whose rendered width fits max_w."""
    size = start
    while size > 8:
        if font(path, size).getlength(text) <= max_w:
            return size
        size -= 1
    return size


def text_img(text, path, size, fill):
    """A small transparent image holding one line of text."""
    fnt = font(path, size)
    w = int(fnt.getlength(text)) + 8
    h = int(size * 1.35) + 8
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((4, 4), text, font=fnt, fill=fill + (255,))
    return img


def paste_centered(base, img, cx, cy):
    base.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


def paste_rotated(base, img, cx, cy, angle_deg):
    """Paste img rotated clockwise by angle_deg, centred on (cx, cy)."""
    rot = img.rotate(-angle_deg, expand=True, resample=Image.BICUBIC)
    paste_centered(base, rot, cx, cy)


def main():
    img = Image.open(SRC).convert("RGBA")
    d = ImageDraw.Draw(img)

    # --- Prabowo bubble (top left): cover, then 2 English lines. ---
    d.ellipse([24, 99, 206, 214], fill=BUBBLE_WHITE + (255,))
    size = fit_size("For GTA 6", BOLD_COND, 28, 160)
    paste_centered(img, text_img("For GTA 6", BOLD_COND, size, INK), 115, 142)
    paste_centered(img, text_img("too, sir?", BOLD_COND, size, INK), 115, 174)

    # --- Gibran bubble (top centre): cover, then 4 English lines. ---
    # Cover matches the real bubble (right edge ~1005 at mid-height):
    # a smaller ellipse left a sliver of the old "dulu" visible.
    d.ellipse([689, 20, 1005, 236], fill=BUBBLE_WHITE + (255,))
    lines = ["Yes, sir...", "I must wait", "for GTA 6", "to release first"]
    size = min(fit_size(t, BOLD_COND, 32, 235) for t in lines)
    print("gibran bubble font size:", size)
    step = int(size * 1.28)
    y0 = 128 - int(1.5 * step)
    for i, line in enumerate(lines):
        paste_centered(img, text_img(line, BOLD_COND, size, INK), 845, y0 + i * step)

    # --- Letter: cover the Indonesian text block (emblem + signature stay). ---
    d.polygon([(601, 390), (851, 407), (918, 604), (661, 598)],
              fill=LETTER_WHITE + (255,))
    # New letter text, rotated 7 degrees like the paper.
    letter = [
        ("LETTER OF", BOLD_COND, 30, 240, (728, 416)),
        ("RESIGNATION", BOLD_COND, 30, 240, (730, 448)),
        ("Gibran Rakabuming Raka", REG_COND, 24, 225, (742, 506)),
        ("Vice President of", REG_COND, 22, 225, (756, 554)),
        ("the Republic of Indonesia", REG_COND, 22, 210, (768, 580)),
    ]
    for text, path, start, max_w, (cx, cy) in letter:
        size = fit_size(text, path, start, max_w)
        print(f"letter {text!r}: {size}px")
        paste_rotated(img, text_img(text, path, size, INK), cx, cy, 7)
    # Divider lines under the title and under the name, rotated like the paper.
    for (cx, cy, w) in [(732, 476, 170), (738, 528, 150)]:
        line = Image.new("RGBA", (w, 3), (0, 0, 0, 0))
        ImageDraw.Draw(line).line([(0, 1), (w, 1)], fill=INK + (255,), width=2)
        paste_rotated(img, line, cx, cy, 7)

    # --- Headline banner: cover, then 2 English lines. ---
    # The cover steps right at the top: the old line-1 tail ("N" of
    # PRESIDEN) reaches x~1392, while the purple box top edge is at y~826,
    # so the upper part may extend to 1400 but the lower part stops at 1300.
    d.polygon([(15, 728), (1400, 728), (1400, 820), (1300, 820),
               (1300, 895), (15, 895)], fill=HEADLINE_WHITE + (255,))
    size = fit_size("GIBRAN RESIGNS AS VICE PRESIDENT", BOLD, 58, 1230)
    print("headline font size:", size)
    paste_centered(img, text_img("GIBRAN RESIGNS AS VICE PRESIDENT",
                                  BOLD, size, INK), 645, 772)
    # Line 2: black "TO WAIT FOR " + purple "GTA 6!"
    fnt = font(BOLD, size)
    part1, part2 = "TO WAIT FOR ", "GTA 6!"
    w1 = int(fnt.getlength(part1))
    w2 = int(fnt.getlength(part2))
    h = int(size * 1.35) + 8
    line2 = Image.new("RGBA", (w1 + w2 + 8, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(line2)
    dd.text((4, 4), part1, font=fnt, fill=INK + (255,))
    dd.text((4 + w1, 4), part2, font=fnt, fill=PURPLE + (255,))
    paste_centered(img, line2, 645, 852)

    # --- Ticker: cover, then the English ticker line. ---
    d.rectangle([118, 940, 1536, 1000], fill=BLACK + (255,))
    ticker = ("The public is shocked, yet understanding | MakeFun: AI agents "
              "are waiting for GTA 6 too | Indonesia remains solid")
    size = fit_size(ticker, REG, 26, 1370)
    print("ticker font size:", size)
    timg = text_img(ticker, REG, size, (255, 255, 255))
    img.alpha_composite(timg, (140, int(970 - timg.height / 2)))

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} (1536x1024)")


if __name__ == "__main__":
    main()
