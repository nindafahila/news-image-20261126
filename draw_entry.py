#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261126.

A one-page newspaper front page summing up the world news of
Thursday 26 November 2026: lead story (the Wang Fuk Court tower
fire in Hong Kong's Tai Po district) illustrated with a small
drawn scene, six more stories as cards with drawn icons, and a
footer ticker. Pure Pillow, deterministic, no network, no random
numbers: the same script always writes the same bytes.

Run: python3 draw_entry.py   (writes entry.png next to this file)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 33, 61)           # deep navy
INK_SOFT = (58, 68, 92)
GOLD = (201, 162, 39)
RED = (178, 34, 24)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
CARD = (255, 255, 255)
SKY = (40, 44, 58)           # night sky over the fire
SMOKE = (96, 100, 110)
ORANGE = (232, 122, 26)
YELLOW = (245, 197, 66)
EMBER = (214, 69, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, leading, fill):
    """Draw wrapped paragraph; returns y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def flame(draw, cx, base, w, h, color):
    """One stylised flame tongue rising from base."""
    pts = [
        (cx - w, base),
        (cx - w * 0.72, base - h * 0.55),
        (cx - w * 0.28, base - h * 0.45),
        (cx, base - h),
        (cx + w * 0.30, base - h * 0.42),
        (cx + w * 0.74, base - h * 0.55),
        (cx + w, base),
    ]
    draw.polygon(pts, fill=color)


def draw_fire_scene(draw, box):
    """Small drawn scene: Tai Po towers burning at night."""
    x0, y0, x1, y1 = box
    # night sky + glow
    draw.rectangle(box, fill=SKY)
    draw.ellipse([x0 + 60, y0 + 8, x0 + 260, y0 + 190], fill=(74, 52, 44))
    # stars
    for sx, sy in ((x0 + 20, y0 + 18), (x0 + 240, y0 + 30),
                   (x0 + 280, y0 + 12), (x0 + 60, y0 + 52)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 220, 200))
    # ground
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(24, 26, 34))
    # three towers, middle one ablaze
    towers = [
        (x0 + 18, y0 + 96, x0 + 104, RED, False),
        (x0 + 116, y0 + 52, x0 + 204, ORANGE, True),
        (x0 + 216, y0 + 108, x0 + 288, (58, 64, 78), False),
    ]
    for tx0, ty0, tx1, _c, burning in towers:
        draw.rectangle([tx0, ty0, tx1, y1 - 26], fill=(52, 56, 68))
        # lit windows
        for wy in range(ty0 + 12, y1 - 40, 18):
            for wx in range(tx0 + 10, tx1 - 12, 20):
                lit = (wx + wy) % 40 == 0
                col = YELLOW if lit else (30, 32, 40)
                draw.rectangle([wx, wy, wx + 9, wy + 11], fill=col)
        if burning:
            # scaffolding lines on the burning tower
            for sy in range(ty0 + 8, y1 - 30, 22):
                draw.line([tx0 - 4, sy, tx1 + 4, sy], fill=(120, 110, 90), width=2)
            draw.line([tx0 - 4, ty0, tx0 - 4, y1 - 26], fill=(120, 110, 90), width=2)
            draw.line([tx1 + 4, ty0, tx1 + 4, y1 - 26], fill=(120, 110, 90), width=2)
            # flames bursting from the top floors
            for fx in (tx0 + 18, tx0 + 44, tx0 + 68):
                flame(draw, fx, ty0 + 6, 16, 46, ORANGE)
                flame(draw, fx, ty0 + 6, 9, 30, YELLOW)
            # flames licking the mid floors
            flame(draw, tx0 + 30, ty0 + 96, 14, 34, EMBER)
            flame(draw, tx0 + 62, ty0 + 130, 12, 28, ORANGE)
    # embers rising
    for ex, ey, er in ((x0 + 140, y0 + 26, 3), (x0 + 176, y0 + 40, 2),
                       (x0 + 156, y0 + 14, 2), (x0 + 200, y0 + 30, 3)):
        draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=YELLOW)
    # smoke columns
    for sx, sy, sr in ((x0 + 148, y0 + 12, 11), (x0 + 182, y0 + 6, 13),
                       (x0 + 120, y0 + 14, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)
    # small fire engine at the base, left
    draw.rectangle([x0 + 12, y1 - 46, x0 + 96, y1 - 28], fill=(178, 34, 24))
    draw.rectangle([x0 + 66, y1 - 58, x0 + 96, y1 - 28], fill=(178, 34, 24))
    draw.rectangle([x0 + 72, y1 - 54, x0 + 90, y1 - 42], fill=(214, 226, 235))
    for wx in (x0 + 28, x0 + 78):
        draw.ellipse([wx - 7, y1 - 30, wx + 7, y1 - 16], fill=(20, 20, 24))
    draw.rectangle(box, outline=INK, width=2)


def icon(draw, kind, box, color):
    """Tiny geometric icon inside a square chip."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "drone":  # Sudan: quad-rotor drone
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
        for dx, dy in ((-13, -13), (13, -13), (-13, 13), (13, 13)):
            draw.line([cx, cy, cx + dx, cy + dy], fill=color, width=2)
            draw.ellipse([cx + dx - 5, cy + dy - 2, cx + dx + 5, cy + dy + 2],
                         outline=color, width=2)
    elif kind == "door":  # Puigdemont: open door / return
        draw.rectangle([x0 + 8, y0 + 4, x1 - 8, y1 - 4], outline=color, width=3)
        draw.line([cx, y0 + 4, cx, y1 - 4], fill=color, width=2)
        draw.polygon([(cx + 2, cy - 6), (cx + 10, cy), (cx + 2, cy + 6)],
                     fill=color)
    elif kind == "scale":  # Ramaphosa: scales of justice
        draw.line([cx, y0 + 6, cx, y1 - 8], fill=color, width=3)
        draw.line([x0 + 7, y0 + 10, x1 - 7, y0 + 10], fill=color, width=3)
        for px in (x0 + 9, x1 - 9):
            draw.line([px, y0 + 10, px, y0 + 18], fill=color, width=2)
            draw.polygon([(px - 7, y0 + 18), (px + 7, y0 + 18), (px, y0 + 26)],
                         outline=color, width=2)
        draw.rectangle([cx - 8, y1 - 8, cx + 8, y1 - 4], fill=color)
    elif kind == "burst":  # Gaza: blast star
        pts = []
        for i in range(16):
            ang = math.pi * i / 8
            r = 16 if i % 2 == 0 else 7
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=PAPER)
    elif kind == "bolt":  # Ukraine power: lightning bolt
        draw.polygon([(cx + 4, y0 + 4), (cx - 8, cy + 2), (cx - 1, cy + 2),
                      (cx - 5, y1 - 4), (cx + 8, cy - 2), (cx + 1, cy - 2)],
                     fill=color)
    elif kind == "chart":  # markets: falling bars + arrow
        for i, hgt in enumerate((26, 18, 10)):
            bx = x0 + 6 + i * 11
            draw.rectangle([bx, y1 - 5 - hgt, bx + 8, y1 - 5], fill=color)
        draw.line([x0 + 5, y0 + 12, x1 - 6, y0 + 24], fill=RED, width=3)
        draw.polygon([(x1 - 6, y0 + 24), (x1 - 13, y0 + 20), (x1 - 13, y0 + 27)],
                     fill=RED)


def card(draw, box, kicker, color, icon_kind, headline, body):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=(190, 184, 170), width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=color)
    ix0, iy0 = x0 + 16, y0 + 20
    draw.rectangle([ix0, iy0, ix0 + 40, iy0 + 40], fill=(238, 234, 224))
    icon(draw, icon_kind, (ix0, iy0, ix0 + 40, iy0 + 40), color)
    tx = ix0 + 54
    draw.text((tx, iy0 + 2), kicker, font=F_SANS_B(15), fill=color)
    hy = para(draw, (tx, iy0 + 24), headline, F_SANS_B(19),
              x1 - 16 - tx, 24, INK)
    para(draw, (x0 + 16, hy + 8), body, F_SANS(14),
         x1 - x0 - 32, 19, INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band ----
    d.rectangle([0, 0, W, 118], fill=INK)
    mast = "THE WORLD IN ONE PICTURE"
    mw = d.textlength(mast, font=F_SERIF_B(52))
    d.text(((W - mw) / 2, 16), mast, font=F_SERIF_B(52), fill=(255, 255, 255))
    date = "THURSDAY  ·  26 NOVEMBER 2026"
    dw = d.textlength(date, font=F_SANS_B(20))
    d.text(((W - dw) / 2, 82), date, font=F_SANS_B(20), fill=GOLD)
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # ---- lead story ----
    lx0, ly0, lx1, ly1 = 28, 136, 996, 436
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=(190, 184, 170), width=1)
    d.rectangle([lx0, ly0, lx1, ly0 + 5], fill=RED)
    tx = lx0 + 24
    d.text((tx, ly0 + 20), "THE LEAD — HONG KONG", font=F_SANS_B(16), fill=RED)
    hy = para(d, (tx, ly0 + 48), "FIRE SWEEPS HONG KONG TOWERS",
              F_SERIF_B(40), 596, 48, INK)
    deck = ("A blaze that began on bamboo scaffolding raced through seven "
            "of the eight blocks of Wang Fuk Court in Tai Po — a level-5 "
            "alarm, Hong Kong's worst fire in decades.")
    hy = para(d, (tx, hy + 10), deck, F_SERIF(19), 596, 26, INK_SOFT)
    d.text((tx, ly1 - 34),
           "TAI PO — at least 36 dead, 279 missing · 767 firefighters on scene",
           font=F_SANS_B(13), fill=INK_SOFT)
    draw_fire_scene(d, (672, 156, 972, 416))

    # ---- six story cards ----
    cards = [
        ("SUDAN", RED, "drone",
         "Drone strikes kill 19 in Sudan",
         "Rapid Support Forces drones hit Damazin and Roseires in Blue "
         "Nile state — 19 civilians dead, 20 wounded, among them six "
         "women, rights group Emergency Lawyers said."),
        ("SPAIN", INK, "door",
         "Puigdemont to return home",
         "Catalonia's former leader will return to Spain on 12 December "
         "after the Supreme Court applied the amnesty law and shelved his "
         "criminal case."),
        ("SOUTH AFRICA", TEAL, "scale",
         "Ramaphosa wins court reprieve",
         "South Africa's president won a court bid to set aside the "
         "official report behind the impeachment threat over cash found "
         "hidden in a sofa at his farm."),
        ("GAZA", (122, 28, 20), "burst",
         "Israeli strike kills Hamas official",
         "An airstrike on a Gaza apartment killed a senior Hamas security "
         "official, his wife and two children, Gaza's interior ministry "
         "and medics said early on Wednesday."),
        ("UKRAINE", (146, 110, 8), "bolt",
         "Russia hits Ukraine's power grid",
         "Overnight strikes damaged Ukraine's energy and gas sites and "
         "cut electricity across five regions, as the war spreads from "
         "the front to the grid."),
        ("MARKETS", GREEN, "chart",
         "Trump tariffs plan rattles Wall St",
         "The US proposed surprise new tariffs on Brazil and other big "
         "trading partners; the Nasdaq slid 4% as an AI sell-off deepened "
         "ahead of the Thanksgiving break."),
    ]
    gx, gy = 28, 452
    cw, ch, gap = 476, 148, 16
    for i, (kick, col, ic, head, body) in enumerate(cards):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        card(d, (cx, cy, cx + cw, cy + ch), kick, col, ic, head, body)

    # ---- ticker ----
    d.rectangle([0, 934, W, 978], fill=INK)
    tick = ("SPAIN VOTES IN 3 DAYS   •   US MARKETS SHUT   •   "
            "COLOMBIA FREES 20 HOSTAGES")
    tw = d.textlength(tick, font=F_SANS_B(15))
    d.text(((W - tw) / 2, 950), tick, font=F_SANS_B(15), fill=(255, 255, 255))
    src = "Sources: Reuters · AP · CBC · NBC — drawn from verified reports of 26 November 2026"
    sw = d.textlength(src, font=F_SANS(14))
    d.text(((W - sw) / 2, 992), src, font=F_SANS(14), fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
