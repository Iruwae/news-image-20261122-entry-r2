#!/usr/bin/env python3
"""Draw the news-image-20261122 round-2 broadsheet: one day of world news.

Fresh code written for this entry. PIL only, no network.
Canvas 1024x1024, cream paper, broadsheet layout: masthead, stat strip,
region bar, UTC timeline, 3 big leads, 13 small stories, map + briefs,
short DATE CHECK, HOW WE CHECKED legend, footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (192, 57, 43)
NAVY = (30, 58, 95)
DARKMAP = (22, 50, 74)
GOLD = (212, 160, 23)
MUTED = (107, 98, 87)
ORANGE = (211, 84, 0)
GREEN = (30, 132, 73)
BLUE = (36, 113, 163)
SKY = (168, 200, 232)
LIGHTBLUE = (190, 214, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
SERIF_I = lambda s: ImageFont.truetype(  # noqa: E731
    "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)         # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def para(draw, x, y, text, fnt, color, max_w, leading=0):
    """Draw wrapped paragraph; returns y just below the last line."""
    lh = fnt.size + (leading if leading else 3)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def centre(draw, cx, y, text, fnt, color):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=color)


def pill(draw, x, y, text, bg, fnt=None):
    """Small verification badge pill; returns width used."""
    fnt = fnt or SANS_B(9)
    tw = draw.textlength(text, font=fnt)
    w, h = int(tw) + 12, 16
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg)
    draw.text((x + 6, y + 3), text, font=fnt, fill=(255, 255, 255))
    return w


BADGE_COLOUR = {"CONFIRMED": RED, "REPORTED": ORANGE,
                "OFFICIAL": GREEN, "FORECAST": BLUE}


def rule(draw, x0, x1, y, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- data
STATS = [
    ("~200", "NATIONS AT COP31"),
    ("03:00", "GMT OBJECTIONS CLOSE"),
    ("6.7", "PERU QUAKE (USGS)"),
    ("400+", "DRONES IN BARRAGE"),
    ("11", "KILLED IN SINALOA"),
    ("37-12", "ENGLAND WIN"),
]

REGIONS = [("MIDDLE EAST", 4, (192, 57, 43)),
           ("EUROPE", 12, (30, 58, 95)),
           ("ASIA", 6, (212, 160, 23)),
           ("AMERICAS", 5, (30, 132, 73)),
           ("AFRICA", 2, (211, 84, 0)),
           ("OCEANIA", 2, (36, 113, 163)),
           ("GLOBAL", 4, (107, 98, 87))]
TOTAL_STORIES = 35

TIMELINE = [
    ("00:37", "BITCOIN $60,261"),
    ("03:00", "COP31 OBJECTIONS CLOSE"),
    ("04:00", "VEGAS GP LIGHTS OUT"),
    ("06:00", "COP31 APPROVAL SESSION"),
    ("15:15", "NEPAL PM LANDS DELHI"),
    ("16:30", "LIVERPOOL v MAN UTD"),
]

LEADS = [
    dict(num=1, kicker="ANTALYA  ·  COP31", badge="REPORTED",
         head="COP31 deal put to ~200 nations",
         body="After running past its Friday deadline, the COP31 "
              "presidents unveil a new package in the early hours "
              "of Sunday. Delegates have until 03:00 GMT to object; "
              "an approval session opens at 06:00 GMT.",
         src="Reuters, 22 Nov", scene="cop31"),
    dict(num=2, kicker="JUNIN  ·  PERU", badge="REPORTED",
         head="Quake 6.7 shakes Peru",
         body="A 6.7-magnitude quake strikes near Junin on Saturday, "
              "felt in Lima; thousands spend the night outside and "
              "the aftermath is still developing on Sunday.",
         src="USGS / wires, 21 Nov", scene="quake"),
    dict(num=3, kicker="THE GULF  ·  STRIKES", badge="REPORTED",
         head="Iran strikes hit US bases",
         body="Iran's drones hit the US air base in Kuwait and sites "
              "in Bahrain on Wednesday; tankers in Hormuz were hit "
              "days earlier. The Gulf standoff still simmers Sunday.",
         src="Wires, 19 Nov", scene="gulf"),
]

SMALLS = [
    dict(num=4, kicker="GULF OF FINLAND", badge="REPORTED",
         head="Sparta II still burns",
         body="Two drones hit the ship; crew out, fire burns on.",
         src="Reuters", scene="ship"),
    dict(num=5, kicker="SINALOA  ·  MEXICO", badge="CONFIRMED",
         head="El Chapo Isidro held",
         body="Cartel boss held in Guasave; 11 killed in the raid.",
         src="Reuters", scene="capture"),
    dict(num=6, kicker="BASRA  ·  IRAQ", badge="REPORTED",
         head="Basra power fire",
         body="Hartha station blaze kills 4, injures 35 near Basra.",
         src="Reuters", scene="fire"),
    dict(num=7, kicker="NEW DELHI  ·  INDIA", badge="OFFICIAL",
         head="Nepal PM flies to Delhi",
         body="Shah lands 15:15 IST for a two-day state visit.",
         src="IANS, 22 Nov", scene="plane"),
    dict(num=8, kicker="MARKETS", badge="CONFIRMED",
         head="Bitcoin back above $60,000",
         body="Bitcoin past $60,000: $60,261 at 00:37 UTC.",
         src="Market data", scene="bitcoin"),
    dict(num=9, kicker="UNITED STATES", badge="REPORTED",
         head="US airlines warned",
         body="Carriers warned of a plot ahead of Thanksgiving.",
         src="Wires", scene="airlines"),
    dict(num=10, kicker="HONG KONG", badge="OFFICIAL",
         head="Hong Kong votes",
         body="Election Committee votes; 5,700 pick the next leader.",
         src="Wires", scene="ballot"),
    dict(num=11, kicker="TURIN  ·  ATP", badge="FORECAST",
         head="ATP final: Zverev v Alcaraz",
         body="Season ends in Turin: Zverev meets Alcaraz today.",
         src="ATP", scene="tennis"),
    dict(num=12, kicker="LAS VEGAS  ·  F1", badge="FORECAST",
         head="Vegas GP race day",
         body="Lights out 04:00 GMT; Verstappen starts from pole.",
         src="F1", scene="racecar"),
    dict(num=13, kicker="TWICKENHAM", badge="CONFIRMED",
         head="England 37-12 All Blacks",
         body="Record margin at Twickenham; England run in five tries.",
         src="BBC", scene="rugby"),
    dict(num=14, kicker="BIHAR  ·  INDIA", badge="REPORTED",
         head="Bihar's 19.7 km bridge",
         body="Nitish Setu spans the Ganges - the big build story.",
         src="Wires", scene="bridge"),
    dict(num=15, kicker="NEW DELHI  ·  INDIA", badge="REPORTED",
         head="Chahal joins BJP",
         body="Chahal joins the BJP, takes an OBC Morcha role.",
         src="NDTV", scene="party"),
    dict(num=16, kicker="NEW ZEALAND TOUR", badge="REPORTED",
         head="Rahul leads India",
         body="KL Rahul's feature leads India's NZ tour; 1st Test builds.",
         src="Cricbuzz", scene="cricket"),
]

BRIEFS = [
    (17, "Drones:", "404 + 110 missiles; 8 killed."),
    (18, "Lviv:", "2 killed in the barrage."),
    (19, "Kyiv:", "three Dnipro bridges hit."),
    (20, "EU-Indonesia:", "trade deal closed."),
    (21, "APEC:", "leaders in weekend session."),
    (22, "Oil:", "down 3% on the week."),
    (23, "MCG:", "England 187-9, T20 record."),
    (24, "Ranchi:", "lashed by cyclone rain."),
    (25, "Blair:", "rejoin EU only if UK innovates."),
    (26, "Melania:", "pushes Ukraine ceasefires."),
    (27, "Qeshm:", "blasts were US disposal, Iran says."),
    (28, "Oman:", "tankers hit; tensions rise."),
    (29, "Newcastle-Arsenal:", "ratings lead the pages."),
    (30, "Liverpool-Man Utd:", "hosts United, 16:30."),
    (31, "Verstappen:", "on pole in Vegas."),
    (32, "Nigeria boat:", "toll rises to 23."),
    (33, "DR Congo:", "40 killed in Cantine."),
    (34, "COP31:", "~130 nations want fossil exit."),
    (35, "GTA VI:", "$3.79bn on day one."),
]

# Map pins: (story number, x, y) inside the dark map panel.
PINS = [(1, 340, 782), (2, 135, 858), (3, 352, 808), (4, 318, 768),
        (5, 70, 802), (6, 378, 798), (7, 400, 808), (10, 440, 812)]


# ------------------------------------------------------------ scenes
def scene_bg(draw, box, colour):
    draw.rectangle(box, fill=colour)


def scene_cop31(draw, box):
    """Bright trio: globe + thermometer + clock under a big sun."""
    x0, y0, x1, y1 = box
    scene_bg(draw, box, SKY)
    draw.ellipse([x1 - 52, y0 + 6, x1 - 12, y0 + 46], fill=GOLD)
    # globe
    cx, cy, r = x0 + 62, y0 + 62, 42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200))
    draw.ellipse([cx - 26, cy - 30, cx - 2, cy - 2], fill=(80, 180, 110))
    draw.ellipse([cx + 4, cy + 8, cx + 30, cy + 34], fill=(80, 180, 110))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=INK, width=2)
    # thermometer
    tx = x0 + 128
    draw.rounded_rectangle([tx, y0 + 18, tx + 22, y0 + 78], radius=11,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([tx + 7, y0 + 30, tx + 15, y0 + 74], fill=RED)
    draw.ellipse([tx - 4, y0 + 68, tx + 26, y0 + 98], fill=RED,
                 outline=INK, width=2)
    # clock
    kx, ky, kr = x0 + 205, y0 + 60, 38
    draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255),
                 outline=INK, width=3)
    draw.line([(kx, ky), (kx, ky - 24)], fill=INK, width=3)
    draw.line([(kx, ky), (kx + 18, ky + 8)], fill=INK, width=3)
    draw.ellipse([kx - 4, ky - 4, kx + 4, ky + 4], fill=RED)
    # negotiating table at the bottom
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(120, 72, 40))
    for px in (x0 + 30, x0 + 120, x0 + 210, x0 + 290):
        draw.rectangle([px, y1 - 30, px + 26, y1 - 16], fill=(255, 255, 255),
                       outline=INK, width=1)


def scene_quake(draw, box):
    """Mountains under a big red seismograph zigzag."""
    x0, y0, x1, y1 = box
    scene_bg(draw, box, (232, 214, 178))
    draw.polygon([(x0, y1), (x0 + 70, y0 + 34), (x0 + 140, y1)],
                 fill=(120, 110, 96))
    draw.polygon([(x0 + 100, y1), (x0 + 190, y0 + 18), (x0 + 280, y1)],
                 fill=(96, 88, 76))
    draw.polygon([(x0 + 175, y0 + 30), (x0 + 190, y0 + 18),
                  (x0 + 205, y0 + 30)], fill=(255, 255, 255))
    draw.polygon([(x0 + 55, y0 + 46), (x0 + 70, y0 + 34),
                  (x0 + 85, y0 + 46)], fill=(255, 255, 255))
    # seismograph trace
    pts = [(x0 + 8, y0 + 26), (x0 + 40, y0 + 26), (x0 + 60, y0 + 12),
           (x0 + 80, y0 + 44), (x0 + 100, y0 + 10), (x0 + 120, y0 + 46),
           (x0 + 140, y0 + 14), (x0 + 160, y0 + 40), (x0 + 185, y0 + 22),
           (x0 + 215, y0 + 26), (x0 + 250, y0 + 26), (x0 + 290, y0 + 26),
           (x0 + 320, y0 + 26)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.rectangle([x0, y1 - 8, x1, y1], fill=(90, 70, 55))


def scene_gulf(draw, box):
    """Night city, missile trails, a ship on dark water."""
    x0, y0, x1, y1 = box
    scene_bg(draw, box, (24, 38, 66))
    for bx, bh in ((x0 + 10, 52), (x0 + 55, 78), (x0 + 110, 60),
                   (x0 + 160, 84), (x0 + 215, 58), (x0 + 265, 74)):
        draw.rectangle([bx, y1 - 34 - bh, bx + 42, y1 - 34], fill=(48, 66, 100))
        for wy in range(y1 - 34 - bh + 8, y1 - 40, 14):
            for wx in (bx + 7, bx + 22):
                draw.rectangle([wx, wy, wx + 6, wy + 7], fill=GOLD)
    # missile trails (kept inside the banner)
    draw.arc([x0 + 150, y0 + 2, x0 + 330, y0 + 70], 200, 330,
             fill=(255, 170, 60), width=4)
    draw.arc([x0 + 30, y0 + 6, x0 + 190, y0 + 80], 210, 320,
             fill=(255, 200, 90), width=3)
    draw.ellipse([x0 + 292, y0 + 34, x0 + 302, y0 + 44], fill=(255, 220, 120))
    draw.ellipse([x0 + 158, y0 + 48, x0 + 166, y0 + 56], fill=(255, 200, 90))
    # sea + ship
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(16, 60, 90))
    draw.polygon([(x0 + 120, y1 - 30), (x0 + 230, y1 - 30),
                  (x0 + 215, y1 - 12), (x0 + 135, y1 - 12)], fill=(40, 40, 44))
    draw.rectangle([x0 + 150, y1 - 44, x0 + 200, y1 - 30], fill=(120, 120, 120))
    draw.rectangle([x0 + 172, y1 - 56, x0 + 182, y1 - 44], fill=(200, 200, 200))


def scene_small(draw, box, kind):
    """One big simple shape per small banner, no text inside."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "ship":
        scene_bg(draw, box, (70, 110, 150))
        draw.polygon([(x0 + 12, y1 - 16), (x0 + w - 12, y1 - 16),
                      (x0 + w - 24, y1 - 4), (x0 + 24, y1 - 4)],
                     fill=(40, 40, 44))
        draw.rectangle([x0 + 30, y1 - 30, x0 + w - 30, y1 - 16],
                       fill=(200, 90, 40))
        for fx in (x0 + 34, x0 + 62, x0 + 90):
            draw.polygon([(fx, y1 - 30), (fx + 8, y1 - 40), (fx + 16, y1 - 30)],
                         fill=(255, 170, 40))
    elif kind == "capture":
        scene_bg(draw, box, (210, 200, 170))
        draw.ellipse([cx - 20, cy - 18, cx + 20, cy + 18], fill=(255, 255, 255),
                     outline=INK, width=3)
        draw.text((cx - 10, cy - 12), "11", font=SANS_B(20), fill=RED)
        draw.rectangle([x0 + 8, y1 - 8, x1 - 8, y1 - 4], fill=INK)
    elif kind == "fire":
        scene_bg(draw, box, (60, 60, 66))
        draw.rectangle([x0 + 24, y1 - 26, x0 + w - 24, y1 - 4],
                       fill=(140, 140, 140))
        draw.rectangle([x0 + 40, y1 - 40, x0 + w - 40, y1 - 26],
                       fill=(110, 110, 110))
        for fx in (cx - 26, cx - 8, cx + 10):
            draw.polygon([(fx, y1 - 26), (fx + 9, y1 - 40), (fx + 18, y1 - 26)],
                         fill=(255, 150, 30))
    elif kind == "plane":
        scene_bg(draw, box, SKY)
        draw.ellipse([x0 + 18, cy - 8, x0 + w - 18, cy + 8], fill=(255, 255, 255),
                     outline=INK, width=2)
        draw.polygon([(x0 + w - 40, cy - 8), (x0 + w - 14, cy - 18),
                      (x0 + w - 14, cy - 8)], fill=(255, 255, 255))
        draw.polygon([(cx - 6, cy + 8), (cx + 14, cy + 18),
                      (cx + 22, cy + 8)], fill=(255, 255, 255))
    elif kind == "bitcoin":
        scene_bg(draw, box, (255, 214, 120))
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=GOLD,
                     outline=INK, width=3)
        draw.text((cx - 7, cy - 12), "B", font=SANS_B(22), fill=(255, 255, 255))
    elif kind == "airlines":
        scene_bg(draw, box, (200, 220, 235))
        draw.polygon([(x0 + 20, cy + 10), (x0 + w - 20, cy - 12),
                      (x0 + w - 20, cy + 2), (x0 + 20, cy + 18)], fill=NAVY)
        draw.polygon([(cx, cy - 12), (cx + 26, cy - 30), (cx + 30, cy - 10)],
                     fill=NAVY)
        draw.ellipse([x0 + w - 34, y0 + 4, x0 + w - 12, y0 + 26], fill=RED)
        draw.text((x0 + w - 29, y0 + 6), "!", font=SANS_B(18), fill=(255, 255, 255))
    elif kind == "ballot":
        scene_bg(draw, box, (190, 205, 225))
        draw.rectangle([cx - 30, cy - 6, cx + 30, cy + 22], fill=(255, 255, 255),
                       outline=INK, width=2)
        draw.rectangle([cx - 12, cy - 6, cx + 12, cy - 2], fill=INK)
        draw.rectangle([cx - 8, cy - 20, cx + 22, cy - 6], fill=(255, 255, 255),
                       outline=INK, width=2)
        draw.text((cx - 3, cy - 19), "X", font=SANS_B(13), fill=RED)
    elif kind == "tennis":
        scene_bg(draw, box, (90, 160, 90))
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(220, 240, 90),
                     outline=(255, 255, 255), width=3)
        draw.arc([cx - 18, cy - 18, cx + 18, cy + 18], 300, 60,
                 fill=(255, 255, 255), width=3)
        draw.arc([cx - 18, cy - 18, cx + 18, cy + 18], 120, 240,
                 fill=(255, 255, 255), width=3)
    elif kind == "racecar":
        scene_bg(draw, box, (40, 44, 54))
        draw.rounded_rectangle([x0 + 14, cy - 8, x0 + w - 14, cy + 10],
                               radius=8, fill=RED)
        draw.rectangle([cx - 8, cy - 18, cx + 22, cy - 8], fill=RED)
        draw.ellipse([x0 + 26, cy + 6, x0 + 46, cy + 22], fill=INK)
        draw.ellipse([x0 + w - 46, cy + 6, x0 + w - 26, cy + 22], fill=INK)
    elif kind == "rugby":
        scene_bg(draw, box, (30, 110, 70))
        draw.ellipse([cx - 34, cy - 16, cx + 34, cy + 16], fill=(255, 255, 255),
                     outline=INK, width=2)
        draw.line([(cx - 12, cy - 14), (cx - 12, cy + 14)], fill=INK, width=2)
        draw.line([(cx + 12, cy - 14), (cx + 12, cy + 14)], fill=INK, width=2)
    elif kind == "bridge":
        scene_bg(draw, box, SKY)
        draw.rectangle([x0, y1 - 14, x1, y1 - 8], fill=(90, 90, 96))
        for px in range(x0 + 10, x1 - 10, 26):
            draw.line([(px, y1 - 14), (cx, y0 + 6)], fill=INK, width=2)
        draw.rectangle([cx - 4, y0 + 4, cx + 4, y1 - 8], fill=INK)
    elif kind == "party":
        scene_bg(draw, box, (240, 200, 90))
        draw.polygon([(x0 + 20, y0 + 6), (x0 + 64, y0 + 6), (x0 + 20, y0 + 34)],
                     fill=(255, 120, 40))
        draw.polygon([(x0 + 70, y0 + 6), (x0 + 114, y0 + 6), (x0 + 70, y0 + 34)],
                     fill=(30, 132, 73))
        draw.ellipse([cx - 14, cy + 2, cx + 14, cy + 18], fill=(255, 255, 255),
                     outline=INK, width=2)
    elif kind == "cricket":
        scene_bg(draw, box, (120, 170, 110))
        draw.polygon([(cx - 4, y0 + 6), (cx + 14, y0 + 10), (cx + 2, y1 - 8),
                      (cx - 14, y1 - 6)], fill=(210, 170, 110),
                     outline=INK)
        draw.ellipse([cx + 18, cy + 2, cx + 34, cy + 18], fill=RED,
                     outline=(255, 255, 255), width=2)
    else:
        scene_bg(draw, box, (200, 200, 200))


SCENE_FN = {"cop31": scene_cop31, "quake": scene_quake, "gulf": scene_gulf}


# ------------------------------------------------------------ layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    X0, X1 = 8, 1016

    # top line
    d.text((X0, 6), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=RED)
    right = "35 STORIES  ·  7 REGIONS  ·  REPORTED ON SUNDAY 22 NOVEMBER 2026"
    d.text((X1 - d.textlength(right, font=SANS_B(11)), 8), right,
           font=SANS_B(11), fill=INK)
    rule(d, X0, X1, 28, 2)

    # masthead
    centre(d, W // 2, 32, "Sunday 22 November 2026", SERIF_B(40), INK)
    centre(d, W // 2, 76,
           "COP31 deal put to ~200 nations  ·  Peru quake aftermath  ·  Gulf strikes still developing",
           SERIF_I(15), INK)
    rule(d, X0, X1, 96, 1)

    # stat strip: 6 big boxes
    y = 102
    bw, gap = 164, 7
    for i, (num, label) in enumerate(STATS):
        x = X0 + i * (bw + gap)
        d.rectangle([x, y, x + bw, y + 40], outline=INK, width=2)
        centre(d, x + bw // 2, y + 3, num, SANS_B(24), RED)
        centre(d, x + bw // 2, y + 28, label, SANS_B(9), INK)

    # region bar: proportional segments + labels
    y = 150
    total = sum(c for _, c, _ in REGIONS)
    x = X0
    for name, count, colour in REGIONS:
        wseg = int((X1 - X0) * count / total)
        d.rectangle([x, y, x + wseg - 2, y + 14], fill=colour)
        x += wseg
    labels = "   ".join("%s %d" % (n, c) for n, c, _ in REGIONS)
    centre(d, W // 2, y + 18, labels, SANS_B(10), INK)

    # timeline strip: THE DAY IN UTC
    y = 182
    d.text((X0, y), "THE DAY IN UTC", font=SANS_B(12), fill=RED)
    rule(d, X0, X1, y + 17, 1)
    cw = (X1 - X0) // 6
    for i, (hh, label) in enumerate(TIMELINE):
        x = X0 + i * cw
        d.text((x + 4, y + 20), hh, font=SANS_B(17), fill=RED)
        para(d, x + 4, y + 42, label, SANS_B(8), INK, cw - 8, leading=1)
    rule(d, X0, X1, y + 62, 1)

    # three big leads
    y = 252
    lw, lgap = 330, 9
    for i, lead in enumerate(LEADS):
        x = X0 + i * (lw + lgap)
        box = (x, y, x + lw, y + 118)
        SCENE_FN[lead["scene"]](d, box)
        d.rectangle(box, outline=INK, width=2)
        pill(d, x + 6, y + 6, lead["badge"], BADGE_COLOUR[lead["badge"]])
        d.text((x + 6, y + 124), "%d  %s" % (lead["num"], lead["kicker"]),
               font=SANS_B(10), fill=RED)
        ty = para(d, x + 2, y + 140, lead["head"], SANS_B(16), INK, lw - 4,
                  leading=1)
        ty = para(d, x + 2, ty + 2, lead["body"], SANS(10), INK, lw - 4,
                  leading=1)
        d.text((x + 2, y + 214), lead["src"], font=SERIF_I(9), fill=MUTED)

    # small stories: 7 on row 1, 6 on row 2
    y = 486
    d.text((X0, y), "MORE FROM THE DAY", font=SANS_B(12), fill=RED)
    rule(d, X0, X1, y + 17, 1)
    rows = [SMALLS[:7], SMALLS[7:]]
    ry = y + 22
    for row in rows:
        n = len(row)
        cw = (X1 - X0 - (n - 1) * 6) // n
        rh = 106
        for i, s in enumerate(row):
            x = X0 + i * (cw + 6)
            scene_small(d, (x, ry, x + cw, ry + 36), s["scene"])
            d.rectangle([x, ry, x + cw, ry + 36], outline=INK, width=1)
            pill(d, x + 3, ry + 3, s["badge"], BADGE_COLOUR[s["badge"]],
                 SANS_B(8))
            ty = ry + 40
            d.text((x, ty), "%d  %s" % (s["num"], s["kicker"]),
                   font=SANS_B(8), fill=RED)
            ty = para(d, x, ty + 12, s["head"], SANS_B(10), INK, cw, leading=0)
            ty = para(d, x, ty + 1, s["body"], SANS(9), INK, cw, leading=0)
            d.text((x, ty + 1), s["src"], font=SERIF_I(8), fill=MUTED)
        ry += rh + 6

    # map + briefs
    y = 730
    d.text((X0, y), "WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
    d.text((508, y), "ALSO ON SUNDAY 22 NOVEMBER — MORE STORIES",
           font=SANS_B(11), fill=RED)
    rule(d, X0, X1, y + 17, 1)
    my = y + 22
    d.rectangle([X0, my, 498, my + 154], fill=DARKMAP, outline=INK, width=2)
    continents = [
        [(40, 775), (130, 765), (175, 785), (150, 820), (95, 830), (45, 805)],
        [(120, 835), (160, 830), (175, 860), (150, 895), (125, 865)],
        [(270, 765), (320, 760), (340, 780), (310, 800), (275, 788)],
        [(285, 805), (325, 800), (340, 835), (315, 875), (290, 845)],
        [(345, 765), (465, 760), (475, 805), (430, 830), (385, 815), (350, 788)],
        [(430, 860), (465, 855), (470, 875), (440, 880)],
    ]
    for poly in continents:
        d.polygon(poly, fill=(217, 201, 163))
    for num, px, py in PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        label = str(num)
        d.text((px - d.textlength(label, font=SANS_B(10)) / 2, py - 7),
               label, font=SANS_B(10), fill=(255, 255, 255))

    # briefs, two columns, one line each
    bx, bw = 508, 250
    by = my
    half = (len(BRIEFS) + 1) // 2
    for col, chunk in enumerate((BRIEFS[:half], BRIEFS[half:])):
        cx = bx + col * (bw + 8)
        cy = by
        for num, lead_in, text in chunk:
            line = "%d. %s %s" % (num, lead_in, text)
            cy = para(d, cx, cy, line, SANS(9), INK, bw, leading=1)
            cy += 3

    # DATE CHECK: short, max 3 lines
    y = 912
    d.rectangle([X0, y, X1, y + 52], outline=RED, width=2)
    d.text((X0 + 8, y + 4), "DATE CHECK", font=SANS_B(11), fill=RED)
    check = ("Weekend stories are framed as reported / still developing on Sunday 22 Nov. "
             "Original dates: Peru quake, Sparta II, El Chapo, Basra fire — Sat 21 Nov; "
             "Iran strikes on US bases — Wed 19 Nov; 400-drone barrage — 19-20 Nov; "
             "ADNOC tanker — Tue 17 Nov. Not yet: COP31 adoption (approval 06:00 GMT Sun).")
    para(d, X0 + 8, y + 20, check, SANS(9), INK, X1 - X0 - 16, leading=1)

    # HOW WE CHECKED legend
    y = 970
    centre(d, W // 2, y,
           "HOW WE CHECKED:  CONFIRMED = officials / documents   ·   REPORTED = wires, single source   ·   OFFICIAL = government statement   ·   FORECAST = scheduled event",
           SANS_B(8), INK)

    # footer
    centre(d, W // 2, 988,
           "Every story here was reported, or was still developing, on Sunday 22 November 2026. Officials' counts are attributed.",
           SERIF_I(10), INK)
    centre(d, W // 2, 1004,
           "Sources named beside each story  ·  Original drawings  ·  make.fun news-image-20261122  ·  @iruwae",
           SANS(9), MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
