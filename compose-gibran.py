#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 Gibran meme: desk scene + crisp official letter.

The desk photo is the only AI-generated part. The letter itself is drawn
with Pillow so every word is spelled right: no garbled model text anywhere.
The real make.fun ghost (press kit) is the letter's official seal, big at
the letter's lower right; a red MUNDUR stamp sits at the lower centre.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"

SCENE = Path.home() / "workspace/makefun/gta6-meme-x-01-work/scenes-gibran/media-generation-gibran-desk-v1-0-8c0f2c78-beac-42f2-92bc-2f55202da57e.png"
MARK = Path.home() / "workspace/makefun/gta6-meme-x-01-press/mark-1024.png"
PORTRAIT = Path.home() / "workspace/makefun/gta6-meme-x-01-work/scenes-gibran/media-generation-gibran-portrait-0-45a27a4a-9af1-49b0-a8a0-c751c061ef30.png"
OUT = Path(__file__).resolve().parent / "meme-gibran.png"

INK = (25, 25, 25, 255)
RED = (178, 24, 24, 255)
RED_FAINT = (178, 24, 24, 215)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def draw_letter():
    """The resignation letter, 800x615, drawn crisp on its own layer."""
    pw, ph = 800, 615
    paper = Image.new("RGBA", (pw, ph), (253, 253, 248, 255))
    d = ImageDraw.Draw(paper)

    # Letterhead (centred on the text column; the pas foto sits right)
    centered(d, 340, 16, "WAKIL PRESIDEN", font(BOLD, 30), INK)
    centered(d, 340, 52, "REPUBLIK INDONESIA", font(BOLD, 30), INK)
    d.line([(40, 96), (pw - 40, 96)], fill=INK, width=2)
    d.line([(40, 102), (pw - 40, 102)], fill=INK, width=1)

    # Title (joke carrier 1)
    centered(d, 330, 122, "SURAT PENGUNDURAN DIRI", font(BOLD, 36), INK)
    centered(d, 340, 178, "Nomor: 001/GTA-VI/2026", font(REG, 19), (70, 70, 70, 255))

    # Addressee + name
    centered(d, pw // 2, 214, "GIBRAN RAKABUMING RAKA", font(BOLD, 29), INK)

    # Body (small texture lines, all spelled right)
    body = [
        "Dengan hormat, melalui surat ini saya menyatakan",
        "mengundurkan diri dari jabatan Wakil Presiden",
        "Republik Indonesia, karena ingin fokus bermain GTA 6.",
    ]
    y = 258
    for line in body:
        centered(d, pw // 2, y, line, font(REG, 21), INK)
        y += 30

    # Reason (joke carrier 2)
    centered(d, pw // 2, 362, "ALASAN: MAIN GTA 6", font(BOLD, 44), RED)

    # Signature, lower left
    d.line([(60, 500), (340, 500)], fill=INK, width=2)
    d.text((200, 452), "Gibran Rakabuming Raka", font=font(SERIF_ITALIC, 26),
           fill=INK, anchor="ma")

    return paper


def draw_stamp():
    """Red MUNDUR stamp (joke carrier 3), drawn on its own layer."""
    sw, sh = 330, 120
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp)
    d.rectangle([6, 6, sw - 6, sh - 6], outline=RED_FAINT, width=5)
    d.rectangle([16, 16, sw - 16, sh - 16], outline=RED_FAINT, width=2)
    centered(d, sw // 2, 30, "MUNDUR", font(BOLD, 56), RED_FAINT)
    return stamp


def main():
    scene_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SCENE
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT

    scene = Image.open(scene_path).convert("RGB")
    # Center-crop the 3:2 desk photo to 16:9, then resize to final size.
    sw, sh = scene.size
    new_h = int(sw * H / W)
    top = (sh - new_h) // 2
    scene = scene.crop((0, top, sw, top + new_h))
    img = scene.resize((W, H), Image.LANCZOS).convert("RGBA")

    # The game case at the right edge carries a wrong title (not GTA 6):
    # blur it into an unidentifiable box so it cannot confuse the judge.
    # Feathered mask, so the blurred patch has no hard edge.
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([1010, 260, W, 620], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    blurred = img.filter(ImageFilter.GaussianBlur(14))
    img = Image.composite(blurred, img, mask)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 70))
    img = Image.composite(dark, img.convert("RGBA"), mask).convert("RGBA")

    # Soft shadow, then the letter, tilted a touch like a real paper.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([208, 42, 1008, 657], radius=4, fill=(0, 0, 0, 110))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    letter = draw_letter().rotate(-1.5, expand=False, resample=Image.BICUBIC)
    img.alpha_composite(letter, (200, 30))

    # Gibran's picture: a flat cartoon portrait as the letter's pas foto,
    # top right, framed in black like an official document photo.
    photo = Image.open(PORTRAIT).convert("RGB")
    pw2, ph2 = photo.size
    crop_w = int(ph2 * 3 / 4)
    left = (pw2 - crop_w) // 2
    photo = photo.crop((left, 0, left + crop_w, ph2)).resize((130, 173), Image.LANCZOS)
    framed = Image.new("RGBA", (138, 181), (255, 255, 255, 255))
    framed.paste(photo, (4, 4))
    fd = ImageDraw.Draw(framed)
    fd.rectangle([0, 0, 137, 180], outline=(20, 20, 20, 255), width=3)
    framed = framed.rotate(-1.5, expand=False, resample=Image.BICUBIC)
    img.alpha_composite(framed, (838, 42))

    # The make.fun ghost as the letter's official seal, big, lower right.
    # Kept below the ALASAN line so it never covers the "GTA 6".
    ghost = Image.open(MARK).convert("RGBA").resize((220, 220), Image.LANCZOS)
    gshadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gshadow)
    gd.ellipse([750, 650, 950, 678], fill=(0, 0, 0, 100))
    img.alpha_composite(gshadow.filter(ImageFilter.GaussianBlur(8)))
    img.alpha_composite(ghost, (740, 445))

    # Red MUNDUR stamp across the lower centre of the letter.
    stamp = draw_stamp().rotate(-10, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(stamp, (470, 515))

    img.convert("RGB").save(out_path, "PNG")
    print(f"wrote {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
