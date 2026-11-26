#!/usr/bin/env python3
"""Draw the Tai Po Fire entry: one 1024x1024 newspaper front page.

Sums up the world's news of Thursday 26 November 2026 in a single image:
a burning tower block in Tai Po, Hong Kong, leads; six more stories sit
below it as cards, and a ticker runs along the foot of the page.

Pure Pillow + stdlib. No network, no randomness, no clock reads, so two
runs over the same code produce byte-identical PNGs.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (24, 24, 24)
NAVY = (19, 38, 77)
NAVY_DARK = (12, 26, 54)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 196, 90)
RED = (163, 22, 33)
CREAM = (248, 244, 233)
GREY_LINE = (185, 178, 160)
CARD_BG = (255, 255, 255)
SKY_TOP = (10, 18, 38)
SKY_BOT = (30, 52, 96)
FLAME = (255, 122, 26)
FLAME_HOT = (255, 196, 66)
FLAME_DEEP = (214, 48, 16)
SMOKE = (120, 122, 128)
TOWER = (52, 58, 74)
TOWER_LIT = (255, 205, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font, falling back to Pillow's default bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    """Draw text centred between x0 and x1 at height y."""
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


def flame(draw, cx, base_y, w, h):
    """A stylised flame: three nested teardrops in deep red, orange, gold."""
    for shrink, colour in ((1.0, FLAME_DEEP), (0.68, FLAME), (0.38, FLAME_HOT)):
        fw, fh = w * shrink, h * shrink
        x0, x1 = cx - fw / 2, cx + fw / 2
        y0, y1 = base_y - fh, base_y
        draw.pieslice([x0, y0, x1, y1], 180, 360, fill=colour)
        draw.polygon(
            [(x0 + fw * 0.12, y0 + fh * 0.55), (cx, y0 - fh * 0.28),
             (x1 - fw * 0.12, y0 + fh * 0.55)],
            fill=colour,
        )


def tower_block(draw, x, top, w, h, lit_rows, scaffold=False):
    """One apartment tower: dark slab, lit windows, roof line."""
    draw.rectangle([x, top, x + w, top + h], fill=TOWER,
                   outline=(20, 22, 32), width=2)
    draw.rectangle([x - 4, top - 8, x + w + 4, top], fill=(34, 38, 50))
    cols, rows = 6, 12
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            wx = x + c * cw + cw * 0.22
            wy = top + r * ch + ch * 0.24
            ww, wh = cw * 0.56, ch * 0.52
            lit = ((r * 7 + c * 3) % 11) < lit_rows
            draw.rectangle([wx, wy, wx + ww, wy + wh],
                           fill=TOWER_LIT if lit else (28, 32, 46))
    if scaffold:
        # Bamboo scaffolding: diagonal poles and cross ties on the face.
        for i in range(5):
            sx = x + 12 + i * (w - 24) / 4
            draw.line([sx, top + h, sx + 26, top + 6],
                      fill=(196, 164, 96), width=3)
        for j in range(4):
            sy = top + 26 + j * (h - 40) / 3
            draw.line([x + 4, sy, x + w - 4, sy],
                      fill=(196, 164, 96), width=3)


def draw_icon(draw, kind, cx, cy, r, colour):
    """A small white pictogram inside a coloured circle."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = (255, 255, 255)
    if kind == "drone":
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=w)
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            ex, ey = cx + dx * r * 0.62, cy + dy * r * 0.62
            draw.line([cx, cy, ex, ey], fill=w, width=3)
            draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], outline=w, width=2)
    elif kind == "home":
        draw.polygon([(cx - r * 0.62, cy + 2), (cx, cy - r * 0.62),
                      (cx + r * 0.62, cy + 2)], fill=w)
        draw.rectangle([cx - r * 0.42, cy, cx + r * 0.42, cy + r * 0.55],
                       fill=w)
        draw.rectangle([cx - 4, cy + r * 0.12, cx + 4, cy + r * 0.55],
                       fill=colour)
    elif kind == "scales":
        draw.line([cx, cy - r * 0.6, cx, cy + r * 0.55], fill=w, width=3)
        draw.line([cx - r * 0.6, cy - r * 0.42, cx + r * 0.6, cy - r * 0.42],
                  fill=w, width=3)
        for s in (-1, 1):
            px = cx + s * r * 0.6
            draw.line([px, cy - r * 0.42, px, cy - r * 0.05], fill=w, width=2)
            draw.polygon([(px - 9, cy - r * 0.05), (px + 9, cy - r * 0.05),
                          (px, cy + r * 0.28)], outline=w, width=2)
        draw.rectangle([cx - r * 0.55, cy + r * 0.55, cx + r * 0.55,
                        cy + r * 0.68], fill=w)
    elif kind == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r * 0.62 if i % 2 == 0 else r * 0.26
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=w)
    elif kind == "bolt":
        draw.polygon([(cx + 4, cy - r * 0.62), (cx - r * 0.42, cy + 2),
                      (cx - 2, cy + 2), (cx - 6, cy + r * 0.62),
                      (cx + r * 0.42, cy - 2), (cx + 2, cy - 2)],
                     fill=w)
    elif kind == "chart":
        draw.line([cx - r * 0.55, cy + r * 0.5, cx - r * 0.55, cy - r * 0.55],
                  fill=w, width=3)
        draw.line([cx - r * 0.55, cy + r * 0.5, cx + r * 0.6, cy + r * 0.5],
                  fill=w, width=3)
        draw.line([cx - r * 0.45, cy - r * 0.3, cx - r * 0.05, cy - r * 0.05,
                   cx + r * 0.25, cy - r * 0.2, cx + r * 0.55, cy + r * 0.35],
                  fill=w, width=3)
        draw.polygon([(cx + r * 0.55, cy + r * 0.35),
                      (cx + r * 0.28, cy + r * 0.28),
                      (cx + r * 0.52, cy + r * 0.08)], fill=w)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=GOLD)
    centre(d, 10, "THE WORLD TODAY", SERIF_B(52), CREAM)
    centre(d, 70, "THURSDAY  ·  26 NOVEMBER 2026", SANS_B(19), GOLD_LIGHT)

    # ---- Breaking strip --------------------------------------------------
    d.rectangle([0, 104, W, 134], fill=RED)
    centre(d, 110, "FIRE SWEEPS HONG KONG TOWERS  —  36 DEAD, 279 MISSING",
           SANS_B(19), (255, 255, 255))

    # ---- Lead illustration: three burning towers at night ----------------
    px0, py0, px1, py1 = 24, 142, 1000, 452
    for i in range(py1 - py0):
        t = i / (py1 - py0)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        d.line([px0, py0 + i, px1, py0 + i], fill=(r, g, b))
    # Deterministic stars.
    for i in range(30):
        sx = px0 + 14 + (i * 97) % (px1 - px0 - 28)
        sy = py0 + 10 + (i * 53) % 110
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 224, 240))
    # Smoke plumes. Keep them inside the picture: every plume top must
    # stay below the panel's top edge (y=142), clear of the masthead.
    for cx, cy, rx, ry in ((180, 196, 66, 22), (520, 186, 80, 24),
                           (850, 198, 62, 20), (330, 190, 56, 20)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=SMOKE)
        d.ellipse([cx - rx + 26, cy - ry - 10, cx + rx - 10, cy + ry - 8],
                  fill=(140, 142, 148))
    # Towers sit lower than in v1, so their flames (tip = base - 1.28*h)
    # never rise above the panel top into the date / breaking strip.
    tower_block(d, 70, 246, 190, 164, lit_rows=4, scaffold=True)
    tower_block(d, 420, 210, 200, 200, lit_rows=5)
    tower_block(d, 740, 252, 190, 158, lit_rows=3)
    # Flames licking the scaffold and the middle roof.
    flame(d, 165, 250, 84, 44)
    flame(d, 520, 214, 96, 48)
    flame(d, 835, 256, 64, 38)
    flame(d, 250, 320, 48, 34)
    # Street and fire engine.
    d.rectangle([px0, 410, px1, py1], fill=(16, 18, 26))
    d.rectangle([120, 372, 330, 404], fill=(178, 24, 32))
    d.rectangle([330, 380, 392, 404], fill=(198, 32, 40))
    d.rectangle([342, 384, 372, 396], fill=(180, 220, 240))
    for wx in (150, 210, 270):
        d.rectangle([wx, 378, wx + 34, 394], fill=(240, 240, 240))
    for wx in (150, 300, 360):
        d.ellipse([wx, 400, wx + 22, 422], fill=(10, 10, 10),
                  outline=(120, 120, 120), width=2)
    # Ladder reaching up to the middle tower's face.
    d.line([300, 372, 432, 264], fill=(220, 220, 220), width=5)
    d.line([312, 376, 444, 268], fill=(220, 220, 220), width=5)
    for i in range(7):
        t = i / 6
        x = 306 + t * 132
        y = 374 - t * 108
        d.line([x - 4, y + 6, x + 10, y - 4], fill=(220, 220, 220), width=2)
    # Caption bar on the picture.
    d.rectangle([px0, py1 - 26, px1, py1], fill=(0, 0, 0))
    d.text((px0 + 12, py1 - 22),
           "Wang Fuk Court, Tai Po — a bamboo scaffold burns above the city.",
           font=SANS(14), fill=(235, 235, 235))

    # ---- Lead headline + standfirst --------------------------------------
    d.text((24, 464), "Fire sweeps Hong Kong towers:",
           font=SERIF_B(31), fill=INK)
    d.text((24, 500), "36 dead, 279 missing in Tai Po blaze",
           font=SERIF_B(31), fill=INK)
    lead = ("A bamboo scaffold on a 32-storey tower under renovation caught "
            "fire at Wang Fuk Court, Tai Po, and spread to seven of the "
            "estate's eight blocks. A level-5 alarm — the highest — brought "
            "767 firefighters. At least 36 people are dead, including one "
            "firefighter; 279 are missing.")
    y = 544
    for line in wrap(d, lead, SANS(16), 976):
        d.text((24, y), line, font=SANS(16), fill=(40, 40, 40))
        y += 22
    d.line([24, 614, 1000, 614], fill=GREY_LINE, width=2)

    # ---- Six news cards ---------------------------------------------------
    cards = [
        ("SUDAN", "RSF drones kill 19 in Sudan",
         "Strikes hit Damazin and Roseires in Blue Nile; 19 civilians dead, 20 hurt.",
         "drone", (122, 60, 30)),
        ("SPAIN", "Puigdemont to return on 12 Dec",
         "Exiled nine years, he heads home as Spain's Supreme Court applies the amnesty.",
         "home", (24, 90, 140)),
        ("SOUTH AFRICA", "Ramaphosa wins court reprieve",
         "A court scraps the report behind the impeachment threat over cash in a sofa.",
         "scales", (90, 70, 110)),
        ("GAZA", "Israeli strike kills Hamas official",
         "An air strike on a Gaza flat kills a senior Hamas official, his wife and two children.",
         "star", (140, 30, 30)),
        ("UKRAINE", "Russia hits Ukraine's power grid",
         "Overnight strikes damage energy and gas sites; blackouts in five regions.",
         "bolt", (176, 124, 18)),
        ("MARKETS", "Trump tariffs rattle Wall Street",
         "New tariff plans, including 10% on Brazilian jets, send the Nasdaq down 4%.",
         "chart", (20, 100, 60)),
    ]
    cw, ch, gx, gy = 476, 100, 24, 10
    for i, (kicker, head, body, icon, colour) in enumerate(cards):
        cx = 24 + (i % 2) * (cw + gx)
        cy = 626 + (i // 2) * (ch + gy)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG,
                    outline=GREY_LINE, width=1)
        d.rectangle([cx, cy, cx + 6, cy + ch], fill=colour)
        draw_icon(d, icon, cx + 40, cy + 26, 21, colour)
        d.text((cx + 70, cy + 9), kicker, font=SANS_B(12), fill=colour)
        hy = cy + 27
        for line in wrap(d, head, SANS_B(17), cw - 84)[:1]:
            d.text((cx + 70, hy), line, font=SANS_B(17), fill=INK)
            hy += 21
        by = cy + 50
        for line in wrap(d, body, SANS(13), cw - 84)[:2]:
            d.text((cx + 70, by), line, font=SANS(13), fill=(60, 60, 60))
            by += 17

    # ---- Ticker -----------------------------------------------------------
    d.rectangle([0, 944, W, H], fill=NAVY_DARK)
    d.rectangle([0, 944, W, 948], fill=GOLD)
    centre(d, 962, "Spain votes in 3 days  ·  US markets shut  ·  "
                   "Colombia frees 20 hostages",
           SANS_B(19), (255, 255, 255))

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = draw_page()
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    img.save(out, format="PNG")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
