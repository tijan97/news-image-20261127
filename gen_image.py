#!/usr/bin/env python3
"""Render the entry image: a newspaper front page summing up
Friday 27 November 2026 world news. Writes entry.png next to this file."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 240, 226)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 76)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, spacing=4):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def panel(draw, x, y, w, h, accent, kicker, headline, caption, hsize=25):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=accent)
    draw.text((x + 10, y + 6), kicker, font=font(SANS_B, 15), fill=(255, 255, 255))
    hf = font(SERIF_B, hsize)
    lines = wrap(draw, headline, hf, w - 20)
    yy = draw_lines(draw, lines, x + 10, y + 40, hf, INK, spacing=2)
    cf = font(SANS, 16)
    clines = wrap(draw, caption, cf, w - 20)
    draw_lines(draw, clines, x + 10, yy + 4, cf, GREY, spacing=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 22), title, font=tf, fill=INK)
    d.rectangle([m, 100, W - m, 104], fill=INK)
    d.rectangle([m, 108, W - m, 110], fill=INK)
    df = font(SANS_B, 20)
    dateline = "FRIDAY 27 NOVEMBER 2026"
    d.text((m, 118), dateline, font=df, fill=RED)
    right = "WORLD NEWS  •  ONE IMAGE  •  $100 BOUNTY"
    rw = d.textlength(right, font=font(SANS, 15))
    d.text((W - m - rw, 122), right, font=font(SANS, 15), fill=GREY)
    d.rectangle([m, 148, W - m, 151], fill=INK)

    # ---- Lead story ----
    lx, ly, lw, lh = m, 162, W - 2 * m, 206
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=RULE, width=3)
    d.rectangle([lx, ly, lx + lw, ly + 34], fill=RED)
    d.text((lx + 12, ly + 7), "LEAD  •  MIDDLE EAST", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    hf = font(SERIF_B, 36)
    # wrap short of the drone glyph at the top-right so no glyph overlaps text
    lines = wrap(d, "Iranian drone strike on Kuwait kills two Italian workers",
                 hf, lw - 170)
    yy = draw_lines(d, lines, lx + 12, ly + 44, hf, INK, spacing=2)
    cf = font(SANS, 19)
    cap = ("Tehran denies responsibility as Rome demands answers — "
           "the day's biggest story, and a reminder of how fast "
           "a regional crisis can turn deadly.")
    clines = wrap(d, cap, cf, lw - 24)
    draw_lines(d, clines, lx + 12, yy + 6, cf, GREY, spacing=3)
    # simple drone glyph top-right of lead panel, clear of the headline
    gx, gy = lx + lw - 132, ly + 56
    d.ellipse([gx, gy, gx + 88, gy + 24], fill=(60, 60, 60))
    d.ellipse([gx - 14, gy - 8, gx + 14, gy + 8], fill=(120, 120, 120))
    d.ellipse([gx + 74, gy - 8, gx + 102, gy + 8], fill=(120, 120, 120))
    d.line([gx + 44, gy + 24, gx + 44, gy + 48], fill=(60, 60, 60), width=4)
    d.ellipse([gx + 34, gy + 48, gx + 54, gy + 62], fill=RED)

    # ---- Grid: 6 panels, 2 cols x 3 rows ----
    gx0, gy0 = m, 384
    pw, ph = (W - 2 * m - 16) // 2, 150
    stories = [
        ("GAZA", (40, 40, 40),
         "Israel kills 10 in Gaza",
         "Hamas weighs its response; at least 16 schoolchildren killed in Gaza since November began."),
        ("UNITED KINGDOM", (30, 70, 130),
         "UK net migration falls to lowest since 1997",
         "The sharpest drop in decades — excluding the pandemic years."),
        ("NORTH KOREA", (120, 30, 30),
         "Kim vows to build more nuclear weapons",
         "Pyongyang ignores Trump's overture and doubles down."),
        ("THAILAND", (180, 90, 10),
         "Massive fire at Bangkok oil refinery",
         "Several injured; Bangchak shuts all units after the blaze."),
        ("SPAIN", (20, 110, 110),
         "Diesel tanker capsizes off Ibiza",
         "Up to 7,000 tonnes aboard; one person killed."),
        ("UNITED STATES", (150, 60, 20),
         "Storm postpones Macy's Thanksgiving parade",
         "100th parade delayed for the first time; 500,000+ homes lose power, ~80m travel, flights cancelled."),
    ]
    for i, (kick, acc, head, cap) in enumerate(stories):
        x = gx0 + (i % 2) * (pw + 16)
        y = gy0 + (i // 2) * (ph + 12)
        panel(d, x, y, pw, ph, acc, kick, head, cap, hsize=23)

    # ---- Bottom strip: 4 mini headlines ----
    by = gy0 + 3 * ph + 2 * 12 + 14
    d.rectangle([m, by, W - m, by + 2], fill=INK)
    bf = font(SERIF_B, 17)
    sf = font(SANS, 14)
    minis = [
        ("BLACK FRIDAY", "“Black November” sales sweep the shops"),
        ("CHESS", "Gukesh vs Sindarov: Game 3 ends in a thrilling draw"),
        ("TENNIS", "Sinner out of Australian Open 2027 with knee injury"),
        ("HEALTH", "Ebola in Congo passes 12,000 cases"),
    ]
    mw = (W - 2 * m - 3 * 12) // 4
    for i, (kick, head) in enumerate(minis):
        x = m + i * (mw + 12)
        d.text((x, by + 12), kick, font=font(SANS_B, 13), fill=RED)
        lines = wrap(d, head, bf, mw)
        draw_lines(d, lines, x, by + 34, bf, INK, spacing=1)

    # ---- Footer ----
    fy = H - 34
    d.rectangle([m, fy - 8, W - m, fy - 6], fill=INK)
    foot = ("THE WORLD IN ONE DAY  •  Friday 27 November 2026  •  "
            "Stories as reported on 27 November 2026")
    ff = font(SANS, 14)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy), foot, font=ff, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
