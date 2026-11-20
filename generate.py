#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: THE WORLD IN ONE DAY.

Pillow only, deterministic (no randomness, no clock, no network, no
reading of the system date). Running `python3 generate.py` writes
entry.png beside it. All facts are the verified stories for Friday
20 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (247, 242, 231)
INK = (22, 21, 19)
RED = (166, 25, 46)
BLUE = (29, 78, 121)
GOLD = (180, 138, 44)
GREY = (90, 86, 78)
LIGHT = (232, 227, 216)
SKY_TOP = (38, 48, 86)
SKY_BOT = (214, 132, 74)
RIVER = (52, 92, 128)
DARK = (28, 30, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}.ttf", size)


def serif_b(size):
    return load_font("DejaVuSerif-Bold", size)


def serif(size):
    return load_font("DejaVuSerif", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold", size)


def sans(size):
    return load_font("DejaVuSans", size)


# Substring of a loaded font's path -> the DejaVu file that provides it.
_FONT_NAMES = (("Serif-Bold", "DejaVuSerif-Bold"),
               ("Serif", "DejaVuSerif"),
               ("Sans-Bold", "DejaVuSans-Bold"),
               ("Sans", "DejaVuSans"))


def font_file(font):
    for key, name in _FONT_NAMES:
        if key in font.path:
            return name
    return "DejaVuSans"


def wrap_words(draw, text, font, first_w, rest_w):
    """Word-wrap text; the first line may use first_w, the rest rest_w."""
    words, lines, cur = text.split(), [], ""
    limit = first_w
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur, limit = word, rest_w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, max_w, max_lines, min_size=14):
    """Word-wrap text to max_w; shrink the font until it fits max_lines.

    Returns (lines, font). Deterministic: sizes only ever go down by 1.
    """
    size = font.size
    while True:
        cur_font = load_font(font_file(font), size)
        lines = wrap_words(draw, text, cur_font, max_w, max_w)
        if len(lines) <= max_lines or size <= min_size:
            return lines, cur_font
        size -= 1


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centred(draw, y, text, font, fill, x0=0, x1=W):
    draw.text(((x0 + x1 - draw.textlength(text, font=font)) / 2, y),
              text, font=font, fill=fill)


def hrule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_art(draw, x0, y0, x1, y1):
    """Dusk over the Dnipro: sky, skyline, river, three struck bridges."""
    bands = 20
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * t)
                    for c in range(3))
        yy0 = y0 + int((y1 - y0) * i / bands)
        yy1 = y0 + int((y1 - y0) * (i + 1) / bands)
        draw.rectangle([x0, yy0, x1, yy1], fill=col)
    # Low sun behind smoke.
    draw.ellipse([x1 - 110, y0 + 26, x1 - 46, y0 + 90], fill=(240, 196, 120))
    # Far skyline silhouettes.
    heights = [46, 78, 56, 102, 66, 88, 50, 110, 70, 60, 96, 52]
    col_w = (x1 - x0) // len(heights)
    base = y0 + int((y1 - y0) * 0.62)
    for i, hgt in enumerate(heights):
        bx0 = x0 + i * col_w
        draw.rectangle([bx0 + 2, base - hgt, bx0 + col_w - 2, base], fill=DARK)
    # River.
    draw.rectangle([x0, base, x1, y1], fill=RIVER)
    for k in range(4):
        yy = base + 14 + k * 16
        draw.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(96, 140, 175), width=2)
    # Three bridges: decks, pylons, cables, smoke, one fire.
    decks = [base + 12, base + 34, base + 56]
    for j, deck_y in enumerate(decks):
        draw.line([(x0, deck_y), (x1, deck_y)], fill=INK, width=6)
        for px in (x0 + 70, x0 + 190, x1 - 90):
            draw.line([(px, deck_y - 34), (px, deck_y)], fill=INK, width=4)
            draw.line([(px, deck_y - 34), (px - 46, deck_y)], fill=INK, width=2)
            draw.line([(px, deck_y - 34), (px + 46, deck_y)], fill=INK, width=2)
        if j == 1:
            # Fire on the middle bridge.
            fire_x = x0 + 150
            draw.polygon([(fire_x, deck_y - 30), (fire_x - 14, deck_y),
                          (fire_x + 14, deck_y)], fill=(226, 88, 34))
            draw.polygon([(fire_x + 6, deck_y - 20), (fire_x - 4, deck_y),
                          (fire_x + 16, deck_y)], fill=(240, 196, 60))
    # Smoke columns rising from the decks.
    for smoke_x, smoke_h in ((x0 + 96, 96), (x0 + 236, 120), (x1 - 120, 84)):
        draw.ellipse([smoke_x - 11, y0 + 30, smoke_x + 11, y0 + 30 + smoke_h],
                     fill=(120, 116, 108))
        draw.ellipse([smoke_x - 5, y0 + 8, smoke_x + 17, y0 + 8 + smoke_h],
                     fill=(150, 146, 138))


def draw_card(draw, x0, y0, w, height, kicker, headline, body, accent):
    draw.rectangle([x0, y0, x0 + w, y0 + height], outline=GREY, width=1)
    draw.rectangle([x0, y0, x0 + w, y0 + 5], fill=accent)
    cx, cy = x0 + 12, y0 + 12
    inner = w - 24
    draw.text((cx, cy), kicker, font=sans_b(15), fill=accent)
    cy += 24
    lines, font = fit_lines(draw, headline, serif_b(21), inner, 2)
    cy = draw_lines(draw, cx, cy, lines, font, INK, font.size + 5)
    cy += 4
    lines, font = fit_lines(draw, body, sans(15), inner, 5)
    draw_lines(draw, cx, cy, lines, font, INK, font.size + 4)


CARDS = [
    ("POLAND", "Russian missiles cross into Poland",
     "A Kh-101 fell near Nowy Lipowiec, a second missile at Rudnik nad "
     "Sanem, a jet drone at Molodycz. No casualties. Warsaw seeks more "
     "NATO air cover.", RED),
    ("BRUSSELS", "UK and EU seal post-Brexit reset",
     "Youth mobility: 100,000 a year each way, ages 18-31, for up to 3 "
     "years, by January 2030. Food deal from March 2028, worth "
     "\u00a35.1bn a year. Fees unresolved.", BLUE),
    ("RIYADH", "Saudi intercepts Houthi missile and drones",
     "Air defences downed a ballistic missile and drones aimed at Riyadh "
     "and the south on Friday morning. Alerts sounded, then lifted, a "
     "day after the PIF Tower was damaged.", RED),
    ("MARKETS", "Asia stocks sink as AI fear spreads",
     "Nikkei -4.8% to 56,594, a seven-month low; Kospi about -5%; "
     "Taiwan -6.6%. SoftBank fell 11-16% as Thursday's Anthropic debut "
     "failed to calm the AI sell-off.", BLUE),
    ("NEW YORK", "Mamdani: Rikers Island to close in 2032",
     "Mayor delays the August 2027 deadline by five years, replacing "
     "Rikers with four borough jails; population ~6,600 to ~4,100, plus "
     "$146m for jail mental health.", BLUE),
    ("EUROPE", "Youth strike: \u2018Money for schools, not war\u2019",
     "Tens of thousands marched in 25+ countries. Italy's CGIL strike "
     "hit 100+ cities; pupils left 350+ UK schools; 10,000 rallied in "
     "Cologne.", RED),
]

TICKER_ITEMS = [
    "GTA VI day one (reported Fri): ~24.6m copies, ~$2.36bn \u2014 Sensor "
    "Tower estimate",
    "Follow-up: Kushner says Russia \u2018comfortable\u2019 with NATO-style "
    "guarantees for Ukraine",
    "Follow-up: UK expels Myanmar defence attache; Myanmar rejects ICJ "
    "ruling",
    "Prabowo meets Xi on South China Sea cooperation",
    "Trump: no Iran decision until the new year",
    "Estonia shuts Russia border for six months",
    "Iraq moves troops into Kataib Hezbollah stronghold",
]


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # ---- masthead ---------------------------------------------------
    centred(draw, 20, "THE WORLD'S NEWS  \u2022  ONE DAY  \u2022  ONE PAGE",
            sans_b(18), GREY)
    centred(draw, 46, "THE WORLD IN ONE DAY", serif_b(62), INK)
    draw.rectangle([MARGIN, 118, W - MARGIN, 160], fill=RED)
    centred(draw, 126, "FRIDAY, 20 NOVEMBER 2026", sans_b(29), (255, 255, 255))
    hrule(draw, 166, MARGIN, W - MARGIN, width=3)

    # ---- lead story -------------------------------------------------
    text_x, text_w = MARGIN, 588
    art_x0, art_y0, art_x1, art_y1 = 648, 178, W - MARGIN, 448
    draw.text((text_x, 180), "UKRAINE \u2014 THE LEAD", font=sans_b(20),
              fill=RED)
    lines, font = fit_lines(
        draw, "Russia smashes three Kyiv bridges in overnight blitz",
        serif_b(42), text_w, 3)
    y = draw_lines(draw, text_x, 210, lines, font, INK, font.size + 8)
    y += 10
    lines, font = fit_lines(
        draw, "Eight killed, 28 hurt as ~110 missiles and ~400 drones hit "
        "Kyiv; power cut across regions.",
        sans(20), text_w, 3)
    y = draw_lines(draw, text_x, y, lines, font, INK, font.size + 6)
    y += 10
    draw.text((text_x, y), "Retaliation for Ukraine's Kerch Bridge strikes",
              font=sans_b(17), fill=RED)
    draw_lead_art(draw, art_x0, art_y0, art_x1, art_y1)
    draw.rectangle([art_x0, art_y1, art_x1, art_y1 + 2], fill=INK)
    draw.text((art_x0, art_y1 + 8),
              "Three Dnipro crossings hit overnight.",
              font=sans(14), fill=GREY)

    # ---- cards ------------------------------------------------------
    hrule(draw, 484, MARGIN, W - MARGIN, width=2)
    card_w, card_h, gap = 306, 192, 17
    top = 496
    for row in range(2):
        for col in range(3):
            kicker, headline, body, accent = CARDS[row * 3 + col]
            draw_card(draw, MARGIN + col * (card_w + gap),
                      top + row * (card_h + 12),
                      card_w, card_h, kicker, headline, body, accent)

    # ---- ticker -----------------------------------------------------
    draw.rectangle([0, 898, W, H], fill=INK)
    prefix = "ALSO TODAY  \u2014  "
    prefix_w = draw.textlength(prefix, font=sans_b(16))
    # First ticker line shares its row with the label, so it gets a
    # shorter width; the rest use the full width.
    lines = wrap_words(draw, "  \u2022  ".join(TICKER_ITEMS), sans(16),
                       W - 2 * MARGIN - prefix_w, W - 2 * MARGIN)
    y = 908
    draw.text((MARGIN, y), prefix, font=sans_b(16), fill=GOLD)
    draw.text((MARGIN + prefix_w, y), lines[0], font=sans(16), fill=PAPER)
    y += 21
    for line in lines[1:]:
        draw.text((MARGIN, y), line, font=sans(16), fill=PAPER)
        y += 21
    draw.text((MARGIN, 1002),
              "Sources: Reuters, AP, BBC, CNN, The Times  \u2014  All events "
              "of Friday 20 November 2026",
              font=sans(13), fill=(170, 164, 150))

    canvas.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
