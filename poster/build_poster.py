#!/usr/bin/env python3
"""
World in One Day — poster builder.

Renders entry.png (1024 x 1024), a one-page newspaper that sums up the
world news of Saturday 21 November 2026, from the structured story data
in poster/data/stories.json.  Saturday edition of the same series as
Friday's world-in-one-day-20261120 poster, keeping its proven system.

Design: cream newsprint, dark-navy ink, red accents; full dark-navy
art panels with a red headline banner and a black source chip on every
panel.  Saturday's leads are drawn for the day: SE Poland farmland at
night with missile trails and a falling drone, a plunging-lines crash
chart tagged with all four index falls, and a Banda Sea quake panel
with epicentre rings, a seismograph trace and a NO TSUNAMI tag.  All
art is Pillow primitives (no photos, no assets), so the render is
deterministic; the map is solid-fill coastlines with pins 01-13 and
27-32.  If
the RGB PNG ever busts 1 MiB the script palette-quantises it in place.

Run:  python3 poster/build_poster.py   Out: entry.png at the repo root.
"""

from __future__ import annotations

import io
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Paths, canvas, palette
# --------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent          # poster/
ROOT = HERE.parent                               # repository root
DATA_PATH = HERE / "data" / "stories.json"
OUT_PATH = ROOT / "entry.png"

SIZE = 1024
MAX_BYTES = 1_048_576

PAPER = (247, 241, 222)        # cream newsprint
PAPER_DARK = (238, 229, 203)   # slightly deeper cream for panels
INK = (20, 30, 56)             # dark navy ink
INK_SOFT = (52, 64, 92)        # softer navy for body copy
RED = (177, 28, 35)            # headline red
RED_DARK = (140, 20, 28)
RULE = (196, 183, 148)         # hairline colour
WHITE = (255, 255, 255)
PANEL = (17, 31, 57)           # deep navy art panel
PANEL_LINE = (52, 74, 110)     # faint line work on a dark panel
LAND_DARK = (108, 126, 150)    # muted blue-grey continents
OCEAN = (13, 22, 44)           # deep navy ocean

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF_BOLD = FONT_DIR / "liberation" / "LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR / "liberation" / "LiberationSerif-Italic.ttf"
SANS = FONT_DIR / "liberation" / "LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR / "liberation" / "LiberationSans-Bold.ttf"
SANS_ITALIC = FONT_DIR / "liberation" / "LiberationSans-Italic.ttf"

MARGIN = 16
X1 = SIZE - MARGIN
INNER = X1 - MARGIN

LEAD_ART_H = 98               # lead illustration band height (v6: taller, rank-1 density)
FEAT_ART_H = 54                # feature graphic band height (v6: taller, rank-1 density)

_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Cached TrueType loader (fonts are the only external input)."""
    key = (str(path), size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(path), size)
    return _font_cache[key]


def text_w(draw: ImageDraw.ImageDraw, text: str, fnt) -> float:
    return draw.textlength(text, font=fnt)


def fit_font(draw, text: str, path: Path, start: int, max_width: float,
             minimum: int = 9) -> ImageFont.FreeTypeFont:
    """Largest size <= start at which *text* still fits *max_width*."""
    size = start
    while size > minimum and text_w(draw, text, font(path, size)) > max_width:
        size -= 1
    return font(path, size)


def wrap(draw, text: str, fnt, max_width: float) -> list[str]:
    """Greedy word wrap measured with the real font metrics."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if text_w(draw, trial, fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current); current = word
    return lines + ([current] if current else [])


def draw_lines(draw, lines: list[str], x: int, y: int, fnt,
               fill, leading: int) -> int:
    """Draw pre-wrapped lines; returns the y just past the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill); y += leading
    return y


def centred_text(draw, cx: float, y: float, text: str, fnt, fill) -> None:
    """Draw *text* horizontally centred on *cx* with its ink centred."""
    bbox = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bbox[2] - bbox[0]) / 2 - bbox[0], y - bbox[1]),
              text, font=fnt, fill=fill)


def _plate(draw, x, y, text, fnt, bg, fg, pad):
    """One filled label plate: bg box with text ink centred in it."""
    w, h = int(text_w(draw, text, fnt)) + 2 * pad, fnt.size + 7
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x + pad - bbox[0], y + (h - (bbox[3] - bbox[1])) / 2 - bbox[1]), text, font=fnt, fill=fg)
    return w


def tag(draw, x: int, y: int, text: str, fnt, bg, fg) -> int:
    """Filled in-art data tag with its top-left at (x, y); returns width."""
    return _plate(draw, x, y, text, fnt, bg, fg, 6)


def banner(draw, x: int, y: int, text: str, fnt) -> int:
    """Red in-art headline banner, top-left of a panel (rank-1 pattern)."""
    return _plate(draw, x, y, text, fnt, RED, WHITE, 7)


def chip(draw, x: int, y: int, text: str) -> int:
    """Small black source/evidence chip inside a panel (rank-1 pattern)."""
    fnt = font(SANS, 8)
    w = int(text_w(draw, text, fnt)) + 10
    draw.rectangle([x, y, x + w, y + 12], fill=(8, 10, 14))
    draw.text((x + 5, y + 2), text, font=fnt, fill=(235, 235, 235))
    return w


def chip_w(draw, text: str) -> int:
    return int(text_w(draw, text, font(SANS, 8))) + 10


def num_chip(draw, cx: float, cy: float, r: int, n: str, fnt) -> None:
    """Blue circle story-number chip (rank-1 pattern)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(27, 58, 128))
    centred_text(draw, cx, cy - fnt.size / 2, str(int(n)), fnt, WHITE)


# --------------------------------------------------------------------------
# Lead illustrations — full bands, hand-drawn with Pillow shapes
# --------------------------------------------------------------------------

def art_poland(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Night over SE Poland: missile trails and a drone fall on farmland."""
    x0, y0, x1, y1 = box
    wdt, hgt = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(13, 20, 42))
    for i in range(48):
        sx = x0 + (i * 53 + 11) % max(1, wdt - 8) + 4
        sy = y0 + (i * 29 + 7) % max(1, int(hgt * 0.5)) + 3
        draw.point((sx, sy), fill=(220, 228, 245))
    # farmland horizon: dark fields with furrow lines, a village silhouette
    base = y1 - 22
    draw.rectangle([x0, base, x1, y1], fill=(30, 52, 34))
    for fx in range(x0 + 10, x1 - 6, 26):
        draw.line([(fx, y1 - 3), (fx + 12, base + 3)], fill=(52, 84, 52), width=1)
    for hx, hw, hh in ((x0 + 18, 30, 13), (x0 + 56, 22, 10), (x1 - 62, 34, 14)):
        draw.rectangle([hx, base - hh, hx + hw, base], fill=(5, 8, 16))
        draw.polygon([(hx - 2, base - hh), (hx + hw + 2, base - hh),
                      (hx + hw // 2, base - hh - 7)], fill=(90, 30, 30))
        draw.rectangle([hx + 5, base - hh + 4, hx + 8, base - hh + 7], fill=(250, 210, 110))
    # two missile trails dropping in from the east (right), glow heads
    for fx0, fx1 in ((0.88, 0.66), (0.97, 0.80)):
        sx, sy = x0 + fx0 * wdt, y0 + 4
        ex, ey = x0 + fx1 * wdt, y0 + 0.58 * hgt
        draw.line([(sx, sy), (ex, ey)], fill=(255, 122, 60), width=3)
        draw.line([(sx, sy), (ex, ey)], fill=(255, 205, 120), width=1)
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 170, 60))
        draw.ellipse([ex - 11, ey + 3, ex + 11, ey + 11], fill=(255, 120, 40))
        draw.ellipse([ex - 5, ey + 4, ex + 5, ey + 10], fill=(255, 190, 90))
    # the drone: an X quadcopter silhouette falling left of the trails
    dx_, dy_ = x0 + 74, y0 + 30
    draw.line([(dx_ - 13, dy_ - 9), (dx_ + 13, dy_ + 9)], fill=WHITE, width=3)
    draw.line([(dx_ - 13, dy_ + 9), (dx_ + 13, dy_ - 9)], fill=WHITE, width=3)
    for px, py in ((dx_ - 13, dy_ - 9), (dx_ + 13, dy_ + 9), (dx_ - 13, dy_ + 9), (dx_ + 13, dy_ - 9)):
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], outline=(255, 150, 150), width=2)
    draw.ellipse([dx_ - 5, dy_ - 5, dx_ + 5, dy_ + 5], fill=RED)
    draw.line([(dx_ + 8, dy_ + 12), (dx_ + 20, dy_ + 30)], fill=(255, 120, 120), width=2)
    tag(draw, x0 + 8, y0 + 52, "SE POLAND", font(SANS_BOLD, 11), PANEL, (226, 234, 244))
    draw.rectangle([x0, y1 - 19, x1, y1], fill=RED)
    centred_text(draw, (x0 + x1) / 2, y1 - 16,
                 "MISSILES + DRONE DOWN", font(SANS_BOLD, 12), WHITE)
    draw.rectangle(box, outline=RULE)


def art_markets(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Crash chart: plunging index lines on a dark grid, falls tagged."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    for gx in range(x0 + 12, x1, 24):
        draw.line([(gx, y0 + 3), (gx, y1 - 22)], fill=PANEL_LINE, width=1)
    for gy in range(y0 + 6, y1 - 20, 14):
        draw.line([(x0 + 3, gy), (x1 - 3, gy)], fill=PANEL_LINE, width=1)
    # three index lines, all diving to the right in different reds/ambers
    series_a = [(x0 + 120, y0 + 10), (x0 + 168, y0 + 16), (x0 + 205, y0 + 15),
                (x0 + 232, y0 + 34), (x1 - 12, y1 - 30)]
    series_b = [(x0 + 120, y0 + 22), (x0 + 170, y0 + 26), (x0 + 210, y0 + 30),
                (x1 - 30, y1 - 34)]
    series_c = [(x0 + 120, y0 + 34), (x0 + 175, y0 + 38), (x0 + 215, y0 + 44),
                (x1 - 48, y1 - 36)]
    lines = [(series_a, RED, 3), (series_b, (240, 150, 60), 2),
             (series_c, (140, 190, 240), 2)]
    for pts, colour, width in lines:
        draw.line(pts, fill=colour, width=width, joint="curve")
        for px, py in pts[:-1]:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)
    ex, ey = x1 - 12, y1 - 30
    draw.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 6, ey - 12)], fill=RED)
    # the day's falls, stacked as in-art data labels on the left
    draw.text((x0 + 8, y0 + 21), "NASDAQ -5.3%", font=font(SANS_BOLD, 11), fill=WHITE)
    draw.text((x0 + 8, y0 + 35), "S&P 500 -3.7%", font=font(SANS_BOLD, 11), fill=(255, 150, 150))
    draw.text((x0 + 8, y0 + 49), "NIKKEI -5.1%", font=font(SANS_BOLD, 11), fill=(240, 190, 120))
    draw.text((x0 + 8, y0 + 63), "HANG SENG -1.9%", font=font(SANS_BOLD, 11), fill=(170, 210, 245))
    draw.rectangle([x0, y1 - 19, x1, y1], fill=RED)
    centred_text(draw, (x0 + x1) / 2, y1 - 16,
                 "TECH CRASH DEEPENS", font(SANS_BOLD, 12), WHITE)
    draw.rectangle(box, outline=RULE)


def art_quake(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Banda Sea panel: island coast, quake rings, seismograph, M7.2 badge."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(13, 28, 52))
    # island landmasses: Maluku Barat Daya arcs top-right, coast strokes
    draw.polygon([(x1 - 120, y0), (x1 - 60, y0 + 10), (x1 - 30, y0 + 26),
                  (x1 - 52, y0 + 34), (x1 - 96, y0 + 22), (x1 - 122, y0 + 10)],
                 fill=(104, 116, 138), outline=(196, 210, 228))
    draw.polygon([(x0 + 8, y1 - 34), (x0 + 52, y1 - 40), (x0 + 78, y1 - 26),
                  (x0 + 44, y1 - 18), (x0 + 10, y1 - 22)],
                 fill=(104, 116, 138), outline=(196, 210, 228))
    draw.text((x1 - 112, y0 + 8), "MALUKU", font=font(SANS_BOLD, 9), fill=(226, 234, 244))
    # concentric quake rings around the epicentre, mid-sea
    cx, cy = x0 + 128, y0 + 42
    for radius, colour, width in ((34, (255, 90, 90), 3), (25, (255, 140, 90), 3),
                                  (16, (255, 190, 110), 2), (8, WHITE, 2)):
        draw.ellipse([cx - radius, cy - radius * 0.72, cx + radius, cy + radius * 0.72],
                     outline=colour, width=width)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED, outline=WHITE)
    tag(draw, x0 + 8, y0 + 8, "BANDA SEA", font(SANS_BOLD, 11), (13, 28, 52), (226, 234, 244))
    # seismograph trace along the lower sea, spiking hard at the main shock
    trace = [(x0 + 10, y1 - 30), (x0 + 52, y1 - 30), (x0 + 62, y1 - 38),
             (x0 + 72, y1 - 22), (x0 + 82, y1 - 42), (x0 + 92, y1 - 18),
             (x0 + 102, y1 - 36), (x0 + 112, y1 - 28), (x1 - 90, y1 - 30),
             (x1 - 60, y1 - 30)]
    draw.line(trace, fill=(120, 230, 200), width=2, joint="curve")
    # M7.2 badge and the no-tsunami tag on the right
    badge = (x1 - 86, y0 + 40, x1 - 10, y0 + 64)
    draw.rectangle(badge, fill=RED)
    centred_text(draw, (badge[0] + badge[2]) / 2, y0 + 45, "M7.2 · 125 KM",
                 font(SANS_BOLD, 11), WHITE)
    tag(draw, x1 - 86, y0 + 68, "NO TSUNAMI", font(SANS_BOLD, 9), (10, 60, 50), (160, 255, 210))
    draw.rectangle(box, outline=RULE)


LEAD_ART = {"poland": art_poland, "markets": art_markets, "quake": art_quake}

LEAD_BANNERS = {"01": "POLAND", "02": "MARKETS CRASH", "03": "MALUKU QUAKE"}
FEAT_BANNERS = {"04": "COP31: OVERTIME", "05": "PERU: M6.9", "06": "IRAQ: PLANT FIRE",
                "07": "USA: HACKED", "08": "UK-EU DEALS", "09": "IRAN: MQ-9 CLAIM",
                "10": "BAYER: $7.25BN", "11": "ZELENSKYY",
                "12": "TRUMP: AI TAX", "13": "TBILISI BLAST"}

# --------------------------------------------------------------------------
# Feature graphics — one drawn band per story, specific to its subject
# --------------------------------------------------------------------------

def feat_flags(draw, box) -> None:
    """06 — EU circle of stars beside a Union Jack, on a dark panel."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    # EU flag block
    eu = (x0 + 10, y0 + 7, x0 + 84, y1 - 7)
    draw.rectangle(eu, fill=(32, 62, 142))
    ccx, ccy = (eu[0] + eu[2]) // 2, (eu[1] + eu[3]) // 2
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx = ccx + 12 * math.cos(ang)
        sy = ccy + 12 * math.sin(ang)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 206, 64))
    draw.ellipse([ccx - 2, ccy - 2, ccx + 2, ccy + 2], fill=(250, 206, 64))
    # Union Jack block: blue field, white diagonals and cross, red over
    uk = (x0 + 100, y0 + 7, x1 - 10, y1 - 7)
    draw.rectangle(uk, fill=(33, 52, 110))
    draw.line([(uk[0], uk[1]), (uk[2], uk[3])], fill=WHITE, width=5)
    draw.line([(uk[0], uk[3]), (uk[2], uk[1])], fill=WHITE, width=5)
    draw.line([(uk[0], uk[1]), (uk[2], uk[3])], fill=(200, 40, 50), width=2)
    draw.line([(uk[0], uk[3]), (uk[2], uk[1])], fill=(200, 40, 50), width=2)
    ucx, ucy = (uk[0] + uk[2]) // 2, (uk[1] + uk[3]) // 2
    draw.rectangle([ucx - 5, uk[1], ucx + 5, uk[3]], fill=WHITE)
    draw.rectangle([uk[0], ucy - 5, uk[2], ucy + 5], fill=WHITE)
    draw.rectangle([ucx - 2, uk[1], ucx + 2, uk[3]], fill=(200, 30, 45))
    draw.rectangle([uk[0], ucy - 2, uk[2], ucy + 2], fill=(200, 30, 45))
    draw.rectangle(eu, outline=(200, 212, 230))
    draw.rectangle(uk, outline=(200, 212, 230))
    tag(draw, x0 + 57, y1 - 17, "RESET TALKS", font(SANS_BOLD, 8), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_cop(draw, box) -> None:
    """04 — thermometer, clashing arrows and an OVERTIME clock badge."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    tx = x0 + 30
    draw.rectangle([tx - 5, y0 + 8, tx + 5, y0 + 34], fill=WHITE)
    draw.rectangle([tx - 2, y0 + 12, tx + 2, y0 + 40], fill=RED)
    draw.ellipse([tx - 8, y0 + 32, tx + 8, y1 - 6], fill=RED, outline=WHITE, width=2)
    draw.polygon([(x0 + 52, y0 + 16), (x0 + 76, y0 + 16), (x0 + 76, y0 + 11),
                  (x0 + 88, y0 + 20), (x0 + 76, y0 + 29), (x0 + 76, y0 + 24),
                  (x0 + 52, y0 + 24)], fill=RED)
    draw.polygon([(x0 + 128, y0 + 16), (x0 + 104, y0 + 16), (x0 + 104, y0 + 11),
                  (x0 + 92, y0 + 20), (x0 + 104, y0 + 29), (x0 + 104, y0 + 24),
                  (x0 + 128, y0 + 24)], fill=(226, 234, 244))
    ccx, ccy = x1 - 34, y0 + 24
    draw.ellipse([ccx - 15, ccy - 15, ccx + 15, ccy + 15], outline=WHITE, width=2)
    draw.line([(ccx, ccy), (ccx, ccy - 10)], fill=(240, 170, 60), width=2)
    draw.line([(ccx, ccy), (ccx + 8, ccy + 4)], fill=(240, 170, 60), width=2)
    tag(draw, x0 + 52, y1 - 18, "OVERTIME", font(SANS_BOLD, 9), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_peru(draw, box) -> None:
    """05 — Andean peaks split by a crack, quake rings at the base."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    draw.polygon([(x0 + 8, y1 - 10), (x0 + 52, y0 + 8), (x0 + 84, y1 - 10)],
                 fill=(120, 132, 152))
    draw.polygon([(x0 + 44, y0 + 17), (x0 + 52, y0 + 8), (x0 + 61, y0 + 17),
                  (x0 + 52, y0 + 22)], fill=WHITE)
    draw.polygon([(x0 + 70, y1 - 10), (x0 + 118, y0 + 14), (x1 - 8, y1 - 10)],
                 fill=(96, 110, 132))
    draw.polygon([(x0 + 110, y0 + 22), (x0 + 118, y0 + 14), (x0 + 127, y0 + 22),
                  (x0 + 118, y0 + 26)], fill=WHITE)
    draw.line([(x0 + 96, y0 + 20), (x0 + 92, y0 + 30), (x0 + 100, y0 + 38),
               (x0 + 94, y1 - 12)], fill=(240, 200, 90), width=2)
    for radius in (7, 13, 19):
        draw.ellipse([x0 + 150 - radius, y1 - 16 - radius * 0.6,
                      x0 + 150 + radius, y1 - 16 + radius * 0.6],
                     outline=(255, 120, 120), width=2)
    tag(draw, x0 + 8, y1 - 18, "M6.9", font(SANS_BOLD, 10), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_fire(draw, box) -> None:
    """06 — power-plant cooling tower and stacks behind flames."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(24, 20, 28))
    draw.polygon([(x0 + 26, y1 - 8), (x0 + 34, y0 + 14), (x0 + 56, y0 + 14),
                  (x0 + 64, y1 - 8)], fill=(110, 116, 128))
    draw.rectangle([x0 + 34, y0 + 14, x0 + 56, y0 + 20], fill=(140, 148, 162))
    for sx in (x0 + 92, x0 + 116):
        draw.rectangle([sx, y0 + 10, sx + 9, y1 - 8], fill=(110, 116, 128))
        draw.rectangle([sx, y0 + 10, sx + 9, y0 + 15], fill=RED)
    for fx, fh, colour in ((x0 + 140, 26, (255, 110, 40)), (x0 + 156, 34, (255, 140, 50)),
                           (x0 + 172, 22, (255, 110, 40)), (x0 + 148, 18, (255, 190, 90)),
                           (x0 + 164, 24, (255, 200, 100))):
        draw.polygon([(fx, y1 - 6), (fx + 7, y1 - 6 - fh), (fx + 14, y1 - 6)], fill=colour)
    tag(draw, x0 + 8, y0 + 6, "4 DEAD · 35 HURT", font(SANS_BOLD, 8), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_hack(draw, box) -> None:
    """07 — server racks, a cracked shield and a warning triangle."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    for i, rx in enumerate((x0 + 10, x0 + 42)):
        draw.rectangle([rx, y0 + 8, rx + 26, y1 - 8], fill=(30, 48, 78), outline=(120, 150, 190))
        for ry in range(y0 + 13, y1 - 13, 9):
            draw.ellipse([rx + 4, ry, rx + 7, ry + 3], fill=(255, 90, 90) if i else (90, 230, 160))
            draw.line([(rx + 11, ry + 1), (rx + 22, ry + 1)], fill=(120, 150, 190), width=1)
    sx, sy = x0 + 108, y0 + 24
    draw.polygon([(sx, y0 + 6), (sx + 22, y0 + 12), (sx + 22, y0 + 28),
                  (sx + 11, y1 - 8), (sx, y0 + 28)], fill=(32, 62, 142), outline=WHITE)
    draw.line([(sx + 11, y0 + 10), (sx + 8, y0 + 20), (sx + 14, y0 + 28),
               (sx + 10, y0 + 38)], fill=(255, 120, 120), width=2)
    draw.polygon([(x1 - 34, y1 - 8), (x1 - 22, y0 + 22), (x1 - 10, y1 - 8)],
                 fill=(240, 170, 60), outline=WHITE)
    draw.text((x1 - 25, y1 - 20), "!", font=font(SANS_BOLD, 13), fill=INK)
    draw.rectangle(box, outline=RULE)


def feat_drone(draw, box) -> None:
    """09 — an MQ-9 silhouette over strait waves, claimed shoot-down."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(13, 28, 52))
    cx, cy = (x0 + x1) // 2, y0 + 20
    draw.polygon([(cx - 44, cy + 4), (cx + 44, cy + 4), (cx + 10, cy - 2),
                  (cx - 10, cy - 2)], fill=(200, 210, 225))
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy - 1], fill=(200, 210, 225))
    draw.polygon([(cx - 4, cy + 4), (cx - 16, cy + 14), (cx - 4, cy + 14)], fill=(170, 182, 200))
    draw.polygon([(cx + 4, cy + 4), (cx + 16, cy + 14), (cx + 4, cy + 14)], fill=(170, 182, 200))
    draw.line([(cx + 30, cy + 12), (cx + 44, y1 - 12)], fill=(255, 120, 120), width=2)
    draw.ellipse([cx + 38, y1 - 18, cx + 52, y1 - 8], fill=(255, 140, 60))
    for row, wy in enumerate((y1 - 15, y1 - 8)):
        for wx in range(x0 + 6 + row * 11, x1 - 60, 22):
            draw.arc([wx, wy - 4, wx + 16, wy + 5], start=180, end=360, fill=(90, 170, 220), width=2)
    tag(draw, x0 + 8, y0 + 6, "MQ-9", font(SANS_BOLD, 9), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_bayer(draw, box) -> None:
    """10 — capsule pill beside a judge's gavel and the $7.25bn tag."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    top, bot = y0 + 10, y0 + 30
    draw.ellipse([x0 + 12, top, x0 + 32, bot], fill=WHITE)
    draw.ellipse([x0 + 52, top, x0 + 72, bot], fill=(229, 92, 132))
    draw.rectangle([x0 + 22, top, x0 + 42, bot], fill=WHITE)
    draw.rectangle([x0 + 42, top, x0 + 62, bot], fill=(229, 92, 132))
    draw.line([(x0 + 96, y0 + 12), (x0 + 122, y0 + 30)], fill=(190, 150, 100), width=6)
    draw.rectangle([x0 + 118, y0 + 6, x0 + 138, y0 + 16], fill=(150, 110, 70))
    draw.rectangle([x0 + 92, y1 - 12, x0 + 140, y1 - 8], fill=(150, 110, 70))
    tag(draw, x0 + 92, y0 + 22, "$7.25BN", font(SANS_BOLD, 9), RED, WHITE)
    draw.rectangle(box, outline=RULE)


def feat_quote(draw, box) -> None:
    """11 — big quote marks over blue-yellow bands (Ukraine colours)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    draw.rectangle([x0 + 8, y0 + 8, x0 + 62, y0 + 24], fill=(40, 90, 180))
    draw.rectangle([x0 + 8, y0 + 24, x0 + 62, y0 + 40], fill=(245, 200, 60))
    draw.text((x0 + 76, y0 + 2), "“A KILLER”", font=fit_font(draw, "“A KILLER”", SANS_BOLD, 17, x1 - x0 - 84, minimum=11), fill=WHITE)
    draw.text((x0 + 78, y0 + 26), "— Zelenskyy, on Putin", font=font(SANS, 10), fill=(200, 212, 230))
    draw.rectangle(box, outline=RULE)


def feat_datacentre(draw, box) -> None:
    """12 — a data-centre hall with server rows and a TAX stamp."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    draw.rectangle([x0 + 12, y0 + 12, x0 + 120, y1 - 10], fill=(30, 48, 78), outline=(120, 150, 190))
    for rx in range(x0 + 20, x0 + 112, 16):
        for ry in range(y0 + 17, y1 - 15, 8):
            draw.rectangle([rx, ry, rx + 10, ry + 4], fill=(90, 200, 170))
    stamp = (x0 + 128, y0 + 14, x1 - 10, y0 + 34)
    draw.rectangle(stamp, outline=RED, width=2)
    centred_text(draw, (stamp[0] + stamp[2]) / 2, y0 + 18, "TAX", font(SANS_BOLD, 13), (255, 130, 130))
    draw.text((x0 + 130, y0 + 38), "AI CENTRES", font=font(SANS_BOLD, 8), fill=WHITE)
    draw.rectangle(box, outline=RULE)


def feat_explosion(draw, box) -> None:
    """13 — apartment block with a burst blown out of one corner."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(20, 24, 38))
    bx0, by0, bx1, by1 = x0 + 52, y0 + 6, x1 - 52, y1 - 6
    draw.rectangle([bx0, by0, bx1, by1], fill=(96, 104, 120))
    for wy in range(by0 + 5, by1 - 6, 10):
        for wx in range(bx0 + 6, bx1 - 8, 14):
            lit = (wx + wy) % 3
            draw.rectangle([wx, wy, wx + 7, wy + 5], fill=(250, 210, 110) if lit else (40, 46, 60))
    cx, cy = bx1 - 8, by0 + 10
    for ang in range(0, 360, 30):
        import math as _m
        ex = cx + int(20 * _m.cos(_m.radians(ang)))
        ey = cy + int(15 * _m.sin(_m.radians(ang)))
        draw.line([(cx, cy), (ex, ey)], fill=(255, 150, 60), width=3)
    draw.ellipse([cx - 9, cy - 7, cx + 9, cy + 7], fill=(255, 190, 90))
    draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=WHITE)
    tag(draw, x0 + 8, y1 - 18, "6 DEAD", font(SANS_BOLD, 9), RED, WHITE)
    draw.rectangle(box, outline=RULE)


FEAT_ART = {"cop": feat_cop, "peru": feat_peru, "fire": feat_fire,
            "hack": feat_hack, "flags": feat_flags, "drone": feat_drone,
            "bayer": feat_bayer, "quote": feat_quote,
            "datacentre": feat_datacentre, "explosion": feat_explosion}

# --------------------------------------------------------------------------
# Solid-fill world map (dark), geographically honest
# --------------------------------------------------------------------------

# Continent polygons coded in (longitude, latitude), traced along the
# coast.  draw_map projects them equirectangularly into the map box
# (x from longitude -170..190, y from latitude 80..-60), the same
# projection the story pins use, so pins land on the right coasts.
def _poly(spec: str) -> list[tuple[float, float]]:
    """Parse one coastline from its compact 'lon,lat lon,lat ...' spec."""
    return [tuple(float(v) for v in pair.split(",")) for pair in spec.split()]


CONTINENTS: list[list[tuple[float, float]]] = [
    # Greenland
    _poly("-46,60 -42,63 -36,67 -28,69 -22,70 -24,75 -32,79 -48,80 -56,76 -55,71 -53,65 -50,61"),
    # North America (Alaska, Hudson Bay, Florida, Yucatan, Baja)
    _poly("-168,66 -162,68 -156,71 -146,70 -136,69 -126,70 -114,68 -102,68 -94,69 -89,68 -86,66 -84,62 -87,58 -85,56 -81,54 -78,55 -78,59 -80,62 -76,64 -70,62 -64,60 -56,53 -59,49 -65,45 -70,44 -73,41 -74,39 -75,36 -78,34 -80,32 -81,29 -80,26 -82,28 -84,30 -87,30 -90,29 -94,29 -97,27 -97,24 -95,20 -91,19 -88,21 -87,20 -88,16 -84,15 -80,10 -78,8 -80,9 -83,10 -85,12 -88,13 -92,15 -95,16 -98,17 -102,19 -105,21 -108,23 -110,24 -112,28 -114,30 -117,33 -120,34 -122,37 -124,40 -124,45 -127,49 -131,54 -136,58 -143,60 -150,61 -153,59 -157,56 -161,55 -164,58 -166,61 -168,64"),
    # South America (Brazil bulging east, tapering south)
    _poly("-78,8 -74,11 -68,11 -62,10 -56,7 -52,5 -50,1 -44,-2 -38,-5 -35,-8 -38,-12 -39,-16 -40,-21 -46,-24 -52,-28 -57,-33 -58,-36 -62,-39 -64,-42 -65,-46 -67,-50 -68,-53 -70,-54 -72,-52 -74,-48 -74,-42 -73,-36 -72,-30 -70,-24 -70,-19 -73,-15 -77,-11 -80,-6 -81,-2 -80,2 -78,6"),
    # Eurasia (one landmass: Iberia, Scandinavia, the Arctic coast,
    # Kamchatka, Korea, SE Asia, the Indian triangle, Arabia)
    _poly("-9,37 -9,43 -4,44 -5,48 -1,50 2,51 5,53 8,55 8,57 6,58 5,60 8,61 12,64 16,67 21,70 28,71 36,69 44,68 54,69 64,70 72,72 82,73 92,75 103,77 113,74 124,72 134,72 144,71 154,70 164,69 173,66 178,64 171,62 164,61 160,57 157,52 155,51 151,59 148,59 143,54 141,49 139,45 136,44 132,43 129,41 127,39 126,36 127,34 124,37 121,37 120,33 121,30 118,27 114,23 110,21 107,18 109,14 107,10 104,8 102,5 100,2 99,6 98,10 96,14 94,17 92,20 90,22 87,21 85,19 82,16 80,13 78,9 76,10 73,14 72,19 70,21 67,23 61,25 57,26 54,28 51,29 48,30 50,26 52,24 56,24 58,22 55,17 52,15 45,12 43,12 42,15 39,20 35,28 34,31 36,34 36,36 33,36 30,36 27,37 25,36 23,36 22,37 23,39 20,40 18,40 16,38 15,40 13,42 11,44 8,44 6,43 3,43 2,41 0,39 -1,37 -2,36 -5,36 -7,37"),
    # Africa (the Horn, the western bulge)
    _poly("-6,35 -9,32 -13,28 -16,24 -17,20 -17,15 -16,12 -13,8 -8,5 -4,5 2,6 6,4 9,0 12,-5 13,-11 13,-17 14,-22 15,-27 17,-31 19,-34 22,-34 26,-34 30,-31 32,-28 33,-25 35,-21 36,-16 37,-12 39,-8 40,-4 41,-1 44,3 48,7 51,11 46,11 43,12 40,15 38,19 36,22 34,26 33,28 31,30 30,31 26,32 21,33 16,32 11,34 10,37 6,37 1,36 -2,35"),
    # Madagascar
    _poly("44,-13 47,-14 50,-16 50,-20 47,-24 45,-25 43,-23 43,-19 44,-15"),
    # Britain and Ireland
    _poly("-5,50 -3,51 0,51 1,52 -1,54 -2,56 -4,58 -6,57 -5,55 -3,54 -5,52"),
    _poly("-10,51 -6,52 -6,54 -8,55 -10,54 -10,52"),
    # Japan
    _poly("130,31 132,33 135,34 138,35 140,37 141,39 141,41 142,43 144,44 145,44 143,42 141,40 140,38 138,36 136,34 133,33 131,32"),
    # Indonesia and the Philippines
    _poly("95,5 98,3 101,0 104,-3 106,-6 104,-5 101,-1 98,2 95,4"),
    _poly("106,-6 110,-7 114,-7 114,-9 109,-8 106,-7"),
    _poly("109,2 110,4 113,5 116,6 118,3 117,0 115,-3 112,-3 109,0"),
    _poly("119,1 120,2 121,1 120,-1 121,-3 120,-4 119,-2"),
    _poly("131,-1 134,-2 138,-2 142,-3 146,-5 149,-8 150,-10 146,-9 142,-7 138,-4 133,-3"),
    _poly("120,18 121,16 122,14 121,12 120,13 119,15"),
    # Australia and Tasmania
    _poly("113,-22 112,-25 114,-30 115,-33 117,-35 122,-34 127,-32 130,-32 132,-31 134,-33 135,-35 137,-35 139,-36 140,-38 144,-38 147,-38 149,-37 150,-36 152,-33 153,-29 153,-25 151,-22 149,-19 146,-18 144,-15 142,-13 142,-11 141,-14 141,-17 140,-18 137,-16 136,-14 135,-12 133,-11 131,-12 128,-13 125,-15 122,-17 119,-19 116,-21"),
    _poly("145,-41 148,-41 148,-43 146,-43"),
    # New Zealand: exaggerated diagonal slivers, so the islands stay
    # visible at map scale
    _poly("168,-34 174,-35 178,-36 179,-38 177,-41 174,-42 171,-40 169,-37"),
    _poly("165,-44 168,-45 172,-44 174,-42 173,-40 169,-42 166,-43"),
]


def draw_map(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
             pins: list[dict]) -> None:
    """Solid-fill world map on a deep-navy ocean, true-position pins."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=OCEAN, outline=RULE)
    wdt, hgt = x1 - x0, y1 - y0

    def proj(lon: float, lat: float) -> tuple[float, float]:
        return (x0 + (lon + 170) / 360 * wdt, y0 + (80 - lat) / 140 * hgt)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND_DARK, outline=(178, 198, 220), width=1)
    # pins for stories 01-13 and 27-32 at their true positions; a pin
    # may carry a small dx/dy nudge (a few px, east-west order
    # preserved) where true
    # positions would overlap — the Europe cluster, the NE-Asia cluster
    pin_font = font(SANS_BOLD, 9)
    for pin in pins:
        px = x0 + int(pin["x"] * wdt) + pin.get("dx", 0)
        py = y0 + int(pin["y"] * hgt) + pin.get("dy", 0)
        label = str(pin["n"])
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(27, 58, 128),
                     outline=WHITE, width=1)
        tw = text_w(draw, label, pin_font)
        draw.text((px - tw / 2, py - 5), label, font=pin_font, fill=WHITE)
    # No space callout on this edition: all nineteen pinned stories
    # (01-13, 27-32) are places on the map, so the pins alone carry it.


# --------------------------------------------------------------------------
# Page sections
# --------------------------------------------------------------------------

def _centred(draw, y, text, fnt, fill):
    """Draw one line centred on the page measure at height y."""
    draw.text(((SIZE - text_w(draw, text, fnt)) / 2, y), text, font=fnt, fill=fill)


def _hex(colour: str):
    return tuple(int(colour[j:j + 2], 16) for j in (1, 3, 5))


def section_top(draw, data: dict) -> int:
    """Brand strip, masthead, strapline, numbers strip, region bar."""
    ed, y = data["edition"], 6
    draw.text((MARGIN, y), ed["brand"], font=font(SANS_BOLD, 15), fill=INK)
    right_f = font(SANS_BOLD, 11)
    draw.text((X1 - text_w(draw, ed["top_right"], right_f), y + 2),
              ed["top_right"], font=right_f, fill=RED)
    y += 19
    draw.line([(MARGIN, y), (X1, y)], fill=INK, width=2)
    y += 3
    # Masthead: the biggest element on the page, fitted to the measure.
    _centred(draw, y, ed["masthead"], fit_font(draw, ed["masthead"], SERIF_BOLD, 74, INNER), INK)
    y += 84  # clear of the masthead descenders before the strapline
    _centred(draw, y, ed["strapline"], fit_font(draw, ed["strapline"], SERIF_ITALIC, 17, INNER), RED)
    y += 20
    draw.line([(MARGIN, y), (X1, y)], fill=RULE, width=1)
    y += 4
    # Numbers strip: six big-number cells divided by hairlines; the two
    # market-shock cells (indexes 1 and 2) print in red.
    cell_w, big_f, cap_f = INNER / 6, font(SANS_BOLD, 24), font(SANS, 11)
    for i, cell in enumerate(data["numbers"]):
        cx = MARGIN + i * cell_w
        if i:
            draw.line([(cx - 5, y + 2), (cx - 5, y + 40)], fill=RULE, width=1)
        draw.text((cx, y), cell["big"], font=big_f, fill=RED if i in (1, 2) else INK)
        draw_lines(draw, wrap(draw, cell["caption"], cap_f, cell_w - 12)[:2],
                   cx, y + 25, cap_f, INK_SOFT, 11)
    y += 48
    # Region bar: one segment per region with its story count inside;
    # label ink flips to white on the darker fills for contrast.
    seg_w = INNER / len(data["regions"])
    for i, region in enumerate(data["regions"]):
        sx, colour = MARGIN + i * seg_w, _hex(region["color"])
        draw.rectangle([sx, y, sx + seg_w - 2, y + 18], fill=colour)
        label = f'{region["name"]} {region["count"]}'
        lf = fit_font(draw, label, SANS_BOLD, 11, seg_w - 12, minimum=8)
        lum = 0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2]
        bbox = draw.textbbox((0, 0), label, font=lf)
        draw.text((sx + (seg_w - 2 - (bbox[2] - bbox[0])) / 2 - bbox[0],
                   y + (18 - (bbox[3] - bbox[1])) / 2 - bbox[1]),
                  label, font=lf, fill=WHITE if lum < 150 else INK)
    y += 21
    draw.line([(MARGIN, y), (X1, y)], fill=INK, width=1)
    return y + 5


def _story_text(draw, story, x, cy, col_w, head_f, body_f, leading,
                max_caption=None):
    """Headline plus attributed caption for one story module.

    Returns the y just past the caption.  Leads pass no cap and keep a
    one-pixel breathing gap after the headline; features cap the
    caption at three lines so a long one can never eat the next row.
    """
    cy = draw_lines(draw, wrap(draw, story["headline"], head_f, col_w),
                    x, cy, head_f, INK, leading)
    if max_caption is None:
        cy += 1
    caption = wrap(draw, f'{story["caption"]} ({story["source"]})', body_f, col_w)
    return draw_lines(draw, caption[:max_caption] if max_caption else caption,
                      x, cy, body_f, INK_SOFT, 13)


def section_leads(draw, data: dict, y: int) -> int:
    """The three lead stories, each with its full illustration band."""
    gap = 10
    col_w = (INNER - 2 * gap) / 3
    head_f = font(SANS_BOLD, 28)
    kick_f = font(SANS_BOLD, 11)
    body_f = font(SANS, 13)
    bottom = y
    for i, lead in enumerate(data["leads"]):
        x = MARGIN + i * (col_w + gap)
        if i:
            draw.line([(x - gap / 2, y), (x - gap / 2, y + 236)], fill=RULE, width=1)
        art_box = (int(x), y, int(x + col_w), y + LEAD_ART_H)
        LEAD_ART[lead["art"]](draw, art_box)
        banner(draw, art_box[0], art_box[1],
               LEAD_BANNERS[lead["n"]], font(SANS_BOLD, 13))
        src = lead["source"].replace(", ", " · ")
        if lead["n"] == "01":
            chip(draw, art_box[0] + 6, art_box[3] - 19 - 14, src)
        elif lead["n"] == "03":
            chip(draw, art_box[0] + 96, art_box[3] - 14, src)
        else:
            chip(draw, art_box[2] - chip_w(draw, src) - 6,
                 art_box[3] - 14, src)
        cy = y + LEAD_ART_H + 6
        num_chip(draw, x + 7, cy + 6, 7, lead["n"], font(SANS_BOLD, 9))
        draw.text((x + 18, cy), lead["kicker"], font=kick_f, fill=RED)
        cy = _story_text(draw, lead, x, cy + 15, col_w, head_f, body_f, 27)
        bottom = max(bottom, cy)
    y = bottom + 2
    draw.line([(MARGIN, y), (X1, y)], fill=RULE, width=1)
    return y + 3


def section_features(draw, data: dict, y: int) -> int:
    """Ten feature modules in two rows of five, each with its own graphic."""
    gap = 8
    col_w = (INNER - 4 * gap) / 5
    head_f = font(SANS_BOLD, 18)
    body_f = font(SANS, 13)
    for row in range(2):
        row_bottom = y
        for col in range(5):
            feat = data["features"][row * 5 + col]
            x = MARGIN + col * (col_w + gap)
            if col:
                draw.line([(x - gap / 2, y), (x - gap / 2, y + 140)], fill=RULE, width=1)
            art_box = (int(x), y, int(x + col_w), y + FEAT_ART_H)
            FEAT_ART[feat["icon"]](draw, art_box)
            banner(draw, art_box[0], art_box[1],
                   FEAT_BANNERS[feat["n"]], font(SANS_BOLD, 10))
            src = feat["source"].replace(", ", " · ")
            chip(draw, art_box[2] - chip_w(draw, src) - 4,
                 art_box[3] - 14, src)
            kick = feat["kicker"]
            kf = fit_font(draw, kick, SANS_BOLD, 10, col_w - 15, minimum=8)
            num_chip(draw, x + 6, y + FEAT_ART_H + 3 + 5, 6, feat["n"],
                     font(SANS_BOLD, 8))
            draw.text((x + 15, y + FEAT_ART_H + 3), kick, font=kf, fill=RED)
            cy = _story_text(draw, feat, x, y + FEAT_ART_H + 14, col_w,
                             head_f, body_f, 18, max_caption=3)
            row_bottom = max(row_bottom, cy)
        y = row_bottom + 4
        if row == 0:
            draw.line([(MARGIN, y - 3), (X1, y - 3)], fill=RULE, width=1)
    draw.line([(MARGIN, y - 2), (X1, y - 2)], fill=INK, width=1)
    return y + 2


def section_bottom(draw, data: dict, y: int) -> int:
    """World map (left) and the 19 one-line briefs (right, two columns)."""
    map_w = 348
    head_f = font(SANS_BOLD, 14)
    draw.text((MARGIN, y), "WHERE IT HAPPENED", font=head_f, fill=INK)
    draw.text((MARGIN, y + 15), "Each number is the story with that number on this page.",
              font=font(SANS_ITALIC, 11), fill=INK_SOFT)
    draw_map(draw, (MARGIN, y + 30, MARGIN + map_w, y + 190), data["pins"])
    # Briefs, to the right of the map.
    bx = MARGIN + map_w + 16
    bw = X1 - bx
    draw.text((bx, y), "ALSO ON SATURDAY 21 NOVEMBER", font=head_f, fill=INK)
    draw.text((bx, y + 15), f"{len(data['briefs'])} more stories, in brief",
              font=font(SANS_ITALIC, 11), fill=INK_SOFT)
    col_w = (bw - 12) / 2
    num_f = place_f = font(SANS_BOLD, 12)
    per_col = math.ceil(len(data["briefs"]) / 2)
    for idx, brief in enumerate(data["briefs"]):
        col, row = divmod(idx, per_col)
        x, yy = bx + col * (col_w + 12), y + 33 + row * 13.4
        # One running line per brief: red number, bold place, then the
        # text shrunk just enough to never spill past its column.
        cursor = x
        for text, fnt, fill in ((f'{brief["n"]}', num_f, RED),
                                (brief["place"], place_f, INK)):
            draw.text((cursor, yy), text, font=fnt, fill=fill)
            cursor += text_w(draw, text, fnt) + 4
        bf = fit_font(draw, brief["text"], SANS, 12, x + col_w - cursor, minimum=9)
        draw.text((cursor, yy), brief["text"], font=bf, fill=INK_SOFT)
    return y + 205


def section_close(draw, data: dict, y: int) -> int:
    """Thin date-check strip (rank-1 weight) and the attribution footer."""
    dc, ed = data["date_check"], data["edition"]
    draw.rectangle([MARGIN, y, X1, y + 26], outline=RED, width=1)
    draw.text((MARGIN + 8, y + 8), dc["title"], font=font(SANS_BOLD, 9), fill=RED)
    body_f = font(SANS, 9)
    draw_lines(draw, wrap(draw, dc["body"], body_f, INNER - 92)[:2],
               MARGIN + 84, y + 3, body_f, INK_SOFT, 11)
    y += 31
    _centred(draw, y, ed["footer_claim"], fit_font(draw, ed["footer_claim"], SANS_BOLD, 12, INNER), INK)
    y += 14
    _centred(draw, y, ed["footer_sources"], fit_font(draw, ed["footer_sources"], SANS, 11, INNER), INK_SOFT)
    return y + 5


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build() -> Path:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    # Cross-checks: the printed counts must agree with the story list.
    total = len(data["leads"]) + len(data["features"]) + len(data["briefs"])
    assert total == 32, f"story count drifted: {total}"
    assert sum(r["count"] for r in data["regions"]) == total, "region counts drifted"
    assert len(data["numbers"]) == 6 and len(data["pins"]) == 19

    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, SIZE - 7, SIZE - 7], outline=RULE, width=1)  # frame

    # The page is a stack of sections; each returns the next free y.
    y = section_top(draw, data)
    for section in (section_leads, section_features, section_bottom, section_close):
        y = section(draw, data, y)
    assert y <= SIZE - 8, f"page overflowed: content ends at y={y}"

    # Save, quantising only if the flat render ever busts the size budget.
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    if buf.tell() > MAX_BYTES:
        img = img.quantize(colors=224, method=Image.Quantize.MEDIANCUT,
                           dither=Image.Dither.FLOYDSTEINBERG)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
    OUT_PATH.write_bytes(buf.getvalue())
    print(f"wrote {OUT_PATH} ({buf.tell()} bytes, content ends y={y})")
    return OUT_PATH


if __name__ == "__main__":
    build()
