"""Draw the newspaper front page for 25 November 2026.

All drawing is done with PIL shapes and the bundled DejaVu fonts.
Deterministic: no timestamps, no randomness, fixed colours and layout.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RULE = (40, 40, 40)
MUTED = (90, 84, 72)
ACCENT = (150, 30, 25)
SEA = (38, 84, 110)
SEA_DARK = (24, 58, 82)
SKY_TOP = (214, 228, 235)
SKY_BOT = (238, 226, 198)

_BASE = os.path.dirname(os.path.abspath(__file__))
_FONTS = os.path.join(_BASE, "fonts")


def _font(name, size):
    return ImageFont.truetype(os.path.join(_FONTS, name), size)


def serif(size, bold=False):
    return _font("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return _font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, font, max_w, leading, fill=INK):
    x, y = xy
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_mine(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 30, 30),
                 outline=(0, 0, 0))
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        x2, y2 = cx + dx * r * 1.7, cy + dy * r * 1.7
        draw.line([(cx + dx * r * 0.8, cy + dy * r * 0.8), (x2, y2)],
                  fill=(30, 30, 30), width=3)


def draw_tanker(draw, x, y, scale, hull=(122, 32, 28)):
    """Simple side-view oil tanker, length ~ 150*scale."""
    L = int(150 * scale)
    h = int(26 * scale)
    draw.polygon([(x, y), (x + L, y), (x + L - int(14 * scale), y + h),
                  (x + int(8 * scale), y + h)], fill=hull)
    draw.rectangle([x + int(18 * scale), y - int(26 * scale),
                    x + int(52 * scale), y], fill=(240, 238, 230))
    draw.rectangle([x + int(58 * scale), y - int(18 * scale),
                    x + int(78 * scale), y], fill=(210, 205, 190))
    draw.rectangle([x + int(96 * scale), y - int(34 * scale),
                    x + int(104 * scale), y], fill=(60, 60, 60))
    # smoke from the funnel
    for i, (sx, sy, sr) in enumerate([(0, -46, 7), (10, -58, 9), (22, -70, 11)]):
        draw.ellipse([x + int(96 * scale) + sx - sr, y + sy - sr,
                      x + int(96 * scale) + sx + sr, y + sy + sr],
                     fill=(120, 118, 112))
    # containers / deck line
    draw.line([(x + 4, y + 4), (x + L - 16, y + 4)], fill=(240, 200, 170),
              width=2)


def draw_lead_scene(draw, box):
    """Strait of Hormuz scene: sky, sun, sea, three tankers, mines."""
    x0, y0, x1, y1 = box
    horizon = y0 + int((y1 - y0) * 0.52)
    # sky bands
    for i in range(horizon - y0):
        t = i / max(1, horizon - y0)
        c = tuple(int(SKY_TOP[k] + (SKY_BOT[k] - SKY_TOP[k]) * t)
                  for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    # sun
    draw.ellipse([x1 - 118, y0 + 26, x1 - 58, y0 + 86], fill=(226, 160, 60))
    # distant headland
    draw.polygon([(x0, horizon), (x0 + 150, horizon - 42),
                  (x0 + 300, horizon), (x0, horizon)], fill=(140, 130, 110))
    draw.polygon([(x1 - 260, horizon), (x1 - 120, horizon - 30),
                  (x1, horizon), (x1, horizon)], fill=(150, 140, 118))
    # sea bands
    for i in range(y1 - horizon):
        t = i / max(1, y1 - horizon)
        c = tuple(int(SEA[k] + (SEA_DARK[k] - SEA[k]) * t) for k in range(3))
        draw.line([(x0, horizon + i), (x1, horizon + i)], fill=c)
    # wave lines
    for wy in (horizon + 26, horizon + 58, horizon + 92):
        for wx in range(x0 + 20, x1 - 40, 90):
            draw.arc([wx, wy - 5, wx + 56, wy + 5], 180, 360,
                     fill=(190, 215, 225), width=2)
    # mines floating in the water
    draw_mine(draw, x0 + 150, horizon + 46, 9)
    draw_mine(draw, x0 + 640, horizon + 78, 10)
    draw_mine(draw, x0 + 850, horizon + 40, 8)
    # three tankers at different scales
    draw_tanker(draw, x0 + 60, horizon - 6, 1.0)
    draw_tanker(draw, x0 + 380, horizon + 22, 1.15, hull=(96, 26, 22))
    draw_tanker(draw, x0 + 700, horizon + 2, 0.85, hull=(140, 40, 30))
    # frame
    draw.rectangle(box, outline=INK, width=3)


def draw_thumb_ship(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(205, 222, 232))
    draw.rectangle([x0, y0 + int((y1 - y0) * 0.62), x1, y1],
                   fill=(52, 96, 122))
    draw_tanker(draw, x0 + 14, y0 + int((y1 - y0) * 0.55), 0.62)
    draw.rectangle(box, outline=INK, width=2)


def draw_thumb_flats(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(228, 220, 205))
    bw, bh = 34, 62
    for i, bx in enumerate((x0 + 12, x0 + 56, x0 + 100)):
        by = y1 - 8 - bh + (6 if i == 1 else 0)
        draw.rectangle([bx, by, bx + bw, y1 - 8], fill=(96, 88, 80))
        for wy in range(by + 8, y1 - 14, 14):
            for wx in (bx + 6, bx + 19):
                draw.rectangle([wx, wy, wx + 8, wy + 8],
                               fill=(245, 225, 140))
    # smoke column
    for i, (sx, sy, sr) in enumerate([(0, 0, 7), (6, -12, 9), (-2, -24, 11)]):
        draw.ellipse([x0 + 118 + sx - sr, y0 + 34 + sy - sr,
                      x0 + 118 + sx + sr, y0 + 34 + sy + sr],
                     fill=(110, 106, 100))
    draw.rectangle(box, outline=INK, width=2)


def draw_thumb_oil(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 222, 196))
    # derrick
    cx = x0 + 70
    draw.polygon([(cx - 34, y1 - 8), (cx - 8, y0 + 12), (cx + 8, y0 + 12),
                  (cx + 34, y1 - 8)], outline=(60, 52, 44), width=3)
    draw.line([(cx - 22, y1 - 34), (cx + 22, y1 - 34)], fill=(60, 52, 44),
              width=3)
    draw.line([(cx - 12, y1 - 62), (cx + 12, y1 - 62)], fill=(60, 52, 44),
              width=3)
    # pumpjack
    draw.line([(x0 + 108, y1 - 8), (x0 + 108, y1 - 46)], fill=(40, 40, 40),
              width=4)
    draw.line([(x0 + 92, y1 - 52), (x0 + 140, y1 - 40)], fill=(40, 40, 40),
              width=4)
    draw.ellipse([x0 + 128, y1 - 52, x0 + 142, y1 - 38], fill=(40, 40, 40))
    draw.rectangle(box, outline=INK, width=2)


def draw_thumb_chart(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 236, 228))
    base = y1 - 14
    heights = [26, 44, 38, 62, 78]
    for i, hgt in enumerate(heights):
        bx = x0 + 12 + i * 28
        col = ACCENT if i == len(heights) - 1 else (110, 110, 105)
        draw.rectangle([bx, base - hgt, bx + 20, base], fill=col)
    draw.line([(x0 + 8, base), (x1 - 8, base)], fill=INK, width=2)
    draw.line([(x0 + 8, y0 + 10), (x0 + 8, base)], fill=INK, width=2)
    draw.rectangle(box, outline=INK, width=2)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    right = W - mx

    # ---- masthead ----
    y = 30
    d.text((W // 2, y), "THE WORLD TODAY", font=serif(64, bold=True),
           fill=INK, anchor="mt")
    y = 118
    rule(d, mx, right, y, width=4)
    rule(d, mx, right, y + 6, width=1)
    y += 16
    d.text((mx, y), "Wednesday, 25 November 2026", font=sans(20, bold=True),
           fill=INK)
    d.text((right, y), "WORLD NEWS  •  ONE DAY IN PICTURES",
           font=sans(16), fill=MUTED, anchor="rt")
    y += 34
    rule(d, mx, right, y, width=2)

    # ---- lead story ----
    y += 18
    d.text((mx, y), "LEAD STORY  —  THE STRAIT OF HORMUZ",
           font=sans(17, bold=True), fill=ACCENT)
    y += 30
    y = para(d, (mx, y), "THREE TANKERS HIT BY MINES IN STRAIT OF HORMUZ",
             serif(40, bold=True), right - mx, 48)
    y += 8
    scene = (mx, y, right, y + 190)
    draw_lead_scene(d, scene)
    y = scene[3] + 14
    y = para(d, (mx, y),
             "Iran's Revolutionary Guard Navy says three oil tankers were "
             "struck by naval mines in the Strait of Hormuz, escalating the "
             "Iran war and raising fears for shipping through the vital "
             "waterway.",
             serif(21), right - mx, 28)
    y += 16
    rule(d, mx, right, y, width=2)

    # ---- secondary stories, 2 x 2 grid ----
    y += 16
    col_w = (right - mx - 24) // 2
    row_h = 166
    stories = [
        ("UKRAINE  •  OFF LIBYA", "Ukraine sinks Russian warship off Libya",
         "President Zelenskyy confirms Ukrainian forces struck two Russian "
         "vessels off the Libyan coast, sinking a warship in Benghazi "
         "harbour, taking the war beyond Europe.",
         draw_thumb_ship),
        ("UKRAINE  •  NEAR KYIV", "Eleven killed in Russian strike on flats near Kyiv",
         "Rescuers race to find survivors after drones hit an apartment "
         "block in the Kyiv region.",
         draw_thumb_flats),
        ("IRAQ  •  KURDISTAN", "Iraq orders seizure of Kurdish oilfields",
         "Prime Minister Ali al-Zaidi orders federal forces to take control "
         "of oilfields in Kurdish-run regions, deepening tensions with the "
         "Kurdistan region.",
         draw_thumb_oil),
        ("UKRAINE WAR  •  TOLL", "700,000 Russian soldiers killed, analysis finds",
         "A new analysis puts Russian military deaths in the nearly "
         "five-year Ukraine war above 700,000.",
         draw_thumb_chart),
    ]
    for idx, (kicker, head, body, thumb_fn) in enumerate(stories):
        cx = mx + (idx % 2) * (col_w + 24)
        cy = y + (idx // 2) * (row_h + 14)
        d.text((cx, cy), kicker, font=sans(14, bold=True), fill=ACCENT)
        hy = para(d, (cx, cy + 22), head, serif(21, bold=True), col_w, 26)
        ty = hy + 6
        thumb = (cx, ty, cx + 150, ty + 84)
        thumb_fn(d, thumb)
        para(d, (cx + 162, ty), body, serif(15), col_w - 162, 20)
    y = y + 2 * row_h + 14 + 8

    # ---- footer ----
    rule(d, mx, right, y, width=2)
    y += 10
    d.text((mx, y), "The World Today  •  Wednesday, 25 November 2026",
           font=sans(15), fill=MUTED)
    d.text((right, y), "All stories from 25 November 2026",
           font=sans(15), fill=MUTED, anchor="rt")
    return img
