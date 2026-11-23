"""Generate the 23 Nov 2026 world-news infographic (1024x1024 PNG).

Layout: navy header with the date, then a 2x3 grid of story panels.
Each panel: coloured accent bar, small-caps tag, bold headline, detail lines.
Text is wrapped to fit; all facts verified against 23 Nov 2026 reporting
(AP, AFP, Reuters, BBC, Al Jazeera, The Hindu, IQAir/Dawn).
Drawn with PIL + DejaVu (no AI image model, so no garbled text).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 249, 246)
NAVY = (15, 42, 74)
INK = (24, 24, 24)
MUTED = (90, 96, 104)
LINE = (214, 210, 203)
WHITE = (255, 255, 255)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


PANELS = [
    ("CLIMATE", (22, 122, 74), "COP31 collapses with no deal",
     "EU rejects a text with no fossil-fuel phase-out; talks end in Antalya"),
    ("HORMUZ", (178, 34, 34), "Tankers struck in the Strait of Hormuz",
     "Three hit Fri\u2013Sat; two more strike mines on Sunday"),
    ("LIBYA", (146, 90, 16), "Sea drones hit Russian warship in Libya",
     "Corvette Merkury struck at Benghazi naval base"),
    ("UKRAINE", (21, 94, 117), "Drone hits Kyiv apartment block",
     "Two killed, 11 missing \u2014 incl. two children \u2014 in Dymer"),
    ("SPACE", (120, 53, 153), "BepiColombo enters Mercury orbit",
     "After an eight-year journey; only the second mission ever"),
    ("MARKETS", (27, 77, 158), "Asia stocks slide on AI fears",
     "South Korea's Kospi falls more than 3%"),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 174], fill=(198, 162, 60))
f_date = font(FONTB, 72)
f_sub = font(FONT, 26)
d.text((48, 26), "23 NOVEMBER 2026", font=f_date, fill=WHITE)
d.text((48, 112), "The world in one day  \u00b7  Monday", font=f_sub, fill=(205, 216, 230))

# Grid: 2 cols x 3 rows
gx, gy = 32, 198
gw, gh = 464, 236
gapx, gapy = 32, 24
f_tag = font(FONTB, 20)
f_head = font(FONTB, 34)
f_det = font(FONT, 22)

for i, (tag, accent, head, det) in enumerate(PANELS):
    col, row = i % 2, i // 2
    x0 = gx + col * (gw + gapx)
    y0 = gy + row * (gh + gapy)
    x1, y1 = x0 + gw, y0 + gh
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE, outline=LINE, width=2)
    d.rectangle([x0, y0 + 14, x0 + 8, y1 - 14], fill=accent)
    tx = x0 + 28
    d.text((tx, y0 + 22), tag, font=f_tag, fill=accent)
    lines = wrap(d, head, f_head, gw - 56)
    yy = y0 + 58
    for ln in lines[:2]:
        d.text((tx, yy), ln, font=f_head, fill=INK)
        yy += 42
    dlines = wrap(d, det, f_det, gw - 56)
    yy = y0 + gh - 30 - 28 * len(dlines)
    for ln in dlines:
        d.text((tx, yy), ln, font=f_det, fill=MUTED)
        yy += 28

# Footer
f_foot = font(FONT, 18)
d.text((32, H - 34), "Sources: AP  \u00b7  AFP  \u00b7  Reuters  \u00b7  BBC  \u00b7  Al Jazeera", font=f_foot, fill=MUTED)

img.save("/home/hatch/workspace/makefun/news-image-23/entry.png")
print("saved entry.png")
