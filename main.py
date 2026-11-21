"""news-image-20261121 v3 — "The Saturday Paper", 1024x1024.

One-page newspaper summing up 21 November 2026 world news.
Drawn entirely with PIL primitives (no photos, no external assets).
Writes ONLY to $MAKEFUN_OUTPUT_DIR/entry.png. Deterministic.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

PAPER = (247, 242, 228)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (28, 54, 90)
GREY = (105, 100, 88)
LIGHT = (238, 231, 214)
RULE = (120, 110, 92)
DOT = (146, 130, 104)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif-Bold.ttf"
SERIF_R = FD + "DejaVuSerif.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(text, f):
    return f.getlength(text)


def wrap(text, f, width, max_lines=None):
    """Greedy word wrap; returns list of lines (never more than max_lines)."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def centre(d, cx, y, text, f, fill=INK):
    d.text((cx - tw(text, f) / 2, y), text, font=f, fill=fill)


def chip(d, x, y, text, f):
    """Small black label chip at the bottom-left of an illustration."""
    pad_x, pad_y = 6, 3
    w_ = int(tw(text, f)) + 2 * pad_x
    h_ = f.size + 2 * pad_y
    d.rectangle([x, y, x + w_, y + h_], fill=(12, 12, 12))
    d.text((x + pad_x, y + pad_y), text, font=f, fill=(255, 255, 255))
    return w_, h_


# ---------------------------------------------------------------- content
KICKER = "THE WORLD IN ONE DAY"
MASTHEAD = "The Saturday Paper"
DATE_LINE = "Saturday 21 November 2026"
SUBHEAD = ("Missiles fall on Riyadh  \u2022  Peru shakes at 00:09 UTC  "
           "\u2022  BepiColombo due at Mercury today")

REGIONS = [("MIDDLE EAST", 8, NAVY), ("ASIA", 5, RED), ("EUROPE", 7, NAVY),
           ("AMERICAS", 8, RED), ("SPACE", 2, NAVY), ("GLOBAL", 5, RED)]

NUMBERS = [
    ("3", "Houthi missiles to Riyadh\nintercepted, no casualties"),
    ("M6.7", "Peru quake, 00:09 UTC Sat\n108 km deep (USGS)"),
    ("M6.1", "Panama quake, 00:12 UTC\n310 km deep, offshore"),
    ("372,000", "evacuated before Akvan\nlandfall (Odisha officials)"),
    ("8 yrs", "BepiColombo's trip to\nMercury, ~6bn miles"),
    ("15% \u2192 40%", "Kalshi odds, GTA VI to\n50m+ copies by Jan 2027"),
]

LEADS = [
    dict(num=1, city="RIYADH", region="MIDDLE EAST",
         title="Saudi defences down three Houthi missiles aimed at Riyadh",
         body=("The Saudi-led coalition intercepted and destroyed three "
               "ballistic missiles early Saturday; two emergency alerts for "
               "the capital were issued, then lifted. No casualties."),
         source="Source: Al Jazeera / Al Arabiya / Reuters",
         chip="RIYADH \u00b7 NIGHT", art="riyadh"),
    dict(num=2, city="PERU", region="AMERICAS",
         title="M6.7 quake shakes central Peru \u2014 00:09 UTC Sat",
         body=("Late Friday in Peru, the USGS puts the quake 9 km NE of "
               "Carhuamayo, Jun\u00edn, 108 km deep. Felt in Lima; Congress "
               "evacuated; Costa Verde landslide. No tsunami threat."),
         source="Source: USGS / IGP / Reuters",
         chip="JUN\u00cdN \u00b7 00:09 UTC", art="peru"),
    dict(num=3, city="MERCURY", region="SPACE",
         title="BepiColombo due to enter Mercury orbit today",
         body=("After eight years and ~6bn miles, the ESA/JAXA craft is "
               "scheduled to enter Mercury orbit today. No confirmation "
               "of success had been received at press time."),
         source="Source: ESA / JAXA / BBC",
         chip="DUE TODAY \u00b7 8 YEARS", art="mercury"),
]

CARDS = [
    dict(num=4, city="ANTALYA", region="CLIMATE",
         title="COP31 runs into overtime, no deal yet",
         body=("Draft 2 drops all fossil-fuel mentions; draft 3 due "
               "Saturday. Panama may block consensus."),
         source="Source: Al Jazeera / BBC T\u00fcrk\u00e7e",
         chip="DRAFT 2", art="cop31"),
    dict(num=5, city="PANAMA", region="AMERICAS",
         title="Second big quake in three minutes",
         body=("M6.1 at 00:12 UTC, 310 km deep offshore; no damage "
               "reported."),
         source="Source: VolcanoDiscovery",
         chip="310 km DEEP", art="panama"),
    dict(num=6, city="ODISHA", region="ASIA",
         title="Akvan weakens to a low; floods linger",
         body=("Update 21 Nov \u2014 landfall was 20 Nov. IMD red/orange "
               "alerts; no deaths."),
         source="Source: IMD / KozmoX",
         chip="RED ALERT", art="odisha"),
    dict(num=7, city="GTA VI", region="CULTURE",
         title="Markets reprice the $3.79bn record",
         body=("Kalshi odds of GTA VI to 50m+ copies by Jan 2027 jump "
               "15% \u2192 40%. $3.79bn announced Friday."),
         source="Source: Kalshi / Take-Two",
         chip="$3.79bn *", art="gta"),
    dict(num=8, city="COPENHAGEN", region="EUROPE",
         title="Denmark expels Russian attach\u00e9",
         body=("Announced Friday 20 Nov, over a foiled murder plot. "
               "Attach\u00e9 out in 7 days."),
         source="Source: BBC / Reuters",
         chip="7 DAYS", art="denmark"),
    dict(num=9, city="LONDON", region="EUROPE",
         title="UK admits offensive cyber war",
         body=("Sky interview, published Friday, vs Russia, China, Iran, "
               "N. Korea."),
         source="Source: Sky News",
         chip="4 TARGETS", art="cyber"),
    dict(num=10, city="S. SAUDI", region="MIDDLE EAST",
         title="Houthi drone to southern Saudi downed",
         body=("Intercepted 21 Nov \u2014 separate from Sanaa/Hodeidah "
               "strikes 20 Nov."),
         source="Source: Roya News / @CJFCSpox",
         chip="21 NOV", art="drone"),
    dict(num=11, city="GAZA", region="MIDDLE EAST",
         title="Killing continues a day after \u201coperation ended\u201d",
         body=("Events 20 Nov: \u22656 killed in Deir al-Balah; tanks fire "
               "on Khan Younis tents."),
         source="Source: Al Jazeera",
         chip="20 NOV", art="gaza"),
    dict(num=12, city="POLAND", region="EUROPE",
         title="NATO jets scrambled as Russian missiles fall",
         body=("20 Nov: 3 Russian objects down in SE Poland. Tusk calls "
               "it a provocation."),
         source="Source: Reuters / ISW",
         chip="3 DOWN", art="poland"),
    dict(num=13, city="KYIV", region="EUROPE",
         title="Aftermath of the war\u2019s biggest barrage",
         body=("Strikes 19\u201320 Nov: 404 drones, 84 cruise, 27 "
               "ballistic; 3 Dnipro bridges hit."),
         source="Source: ISW / CNN",
         chip="404 DRONES", art="kyiv"),
]

ALSO = [
    (14, "Mercury at its best, pre-dawn Sat \u2014 greatest elongation, 05:45\u201306:15. (Azteca Noticias) [21 Nov]"),
    (15, "Riyadh alerts lifted. Two emergency alerts issued, then lifted. (The Times) [21 Nov]"),
    (16, "Reuters witness in Riyadh saw a missile-like object, heard a loud blast. (Reuters) [21 Nov]"),
    (17, "Drone to southern Saudi Arabia downed by the coalition. (Roya News) [21 Nov]"),
    (18, "COP31 third draft expected Saturday: \u201cclose to the finish line, not there yet\u201d. (BBC T\u00fcrk\u00e7e) [21 Nov]"),
    (19, "Akvan: 1,450 births in shelters; 4,470 pregnant women moved. (KozmoX) [21 Nov]"),
    (20, "IMD alerts, 21 Nov: Red Alert Mayurbhanj & Balasore; Orange Alert 14 districts. (IMD) [21 Nov]"),
    (21, "Akvan floods Odisha farms; paddy flattened; Jalaput dam discharge high. (Argus News) [21 Nov]"),
    (22, "Fog blankets Puri and the Jagannath complex after Akvan. (Sambad English) [21 Nov]"),
    (23, "Peru: no tsunami. Navy says no tsunami threat after the M6.7. (Bloomberg L\u00ednea) [21 Nov]"),
    (24, "Peru: Congress evacuated; Lima residents rushed into the streets. (Reuters) [21 Nov]"),
    (25, "Peru: Costa Verde landslide sends dust down the cliffs in Lima. (Citizen video) [21 Nov]"),
    (26, "Peru magnitude revised: USGS 6.9 \u2192 6.7; GFZ 6.8; Xinhua 6.8. (USGS) [21 Nov]"),
    (27, "Panama quake: deep and offshore; no damage reported. (VolcanoDiscovery) [21 Nov]"),
    (28, "COP31 protester: \u201cYOU ARE KILLING THE FUTURE\u201d, dragged out by security. (Al Jazeera) [20 Nov]"),
    (29, "Panama: \u201cWe will not put up with it\u201d \u2014 Navarro rejects text without fossil fuels. (Al Jazeera) [20 Nov]"),
    (30, "\u201c35 by 35\u201d downgraded: 2035 power target cut from mandatory to voluntary. (Earth Brief) [20 Nov]"),
    (31, "Denmark: attach\u00e9 out in 7 days; Schengen visas for Russians may halt. (BBC) [20\u201321 Nov]"),
    (32, "Denmark: two charged Friday over the September murder plot; third man arrested. (World From Here) [20 Nov]"),
    (33, "UK: cyber HQ opens \u2014 new National Cyber Force base at Samlesbury, Lancashire. (Sky News) [20 Nov]"),
    (34, "Gaza: 6 killed in Deir al-Balah, a day after the \u201coperation ended\u201d. (Al Jazeera) [20 Nov]"),
    (35, "Gaza: 200\u2013400 m past the line \u2014 troops advance beyond the Yellow Line. (n.news.media) [20 Nov]"),
]

DATECHECK = [
    "GTA VI launch 19 Nov + $3.79bn 20 Nov. Kyiv barrage 19\u201320 Nov. Akvan landfall 20 Nov. "
    "BepiColombo unconfirmed at press time (due today).",
    "Peru quake Friday night local = Sat 00:09 UTC. Denmark expulsion + UK cyber interview announced Friday 20 Nov.",
]

FOOTER = ("Sources: Reuters, AP, USGS, IMD, Al Jazeera, BBC, Sky News, CNN, ISW, VolcanoDiscovery, "
          "Kalshi, ESA/JAXA and others named per story. All illustrations are original drawings made for this page.")

# ------------------------------------------------------------ illustrations
def _stars(d, box, n, seed):
    import random
    rnd = random.Random(seed)
    x0, y0, w_, h_ = box
    for _ in range(n):
        sx = rnd.randint(x0 + 4, x0 + w_ - 4)
        sy = rnd.randint(y0 + 3, y0 + h_ - 12)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 235, 220))


def _sky(d, box, top=(16, 22, 48), bot=(38, 52, 92)):
    x0, y0, w_, h_ = box
    for i in range(h_):
        t = i / max(1, h_ - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x0 + w_, y0 + i)], fill=c)


def art_riyadh(d, box):
    x0, y0, w_, h_ = box
    _sky(d, box)
    _stars(d, box, 26, 11)
    # skyline silhouettes with lit windows
    import random
    rnd = random.Random(7)
    base = y0 + h_
    bx = x0 + 6
    while bx < x0 + w_ - 30:
        bw = rnd.randint(22, 42)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(10, 14, 32))
        for wy in range(base - bh + 6, base - 6, 9):
            for wx in range(bx + 5, bx + bw - 4, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 90))
        bx += bw + 4
    # Kingdom Centre tower with its inverted arch
    tx = x0 + w_ - 52
    d.rectangle([tx, y0 + 18, tx + 34, base], fill=(12, 16, 36))
    d.polygon([(tx + 2, y0 + 18), (tx + 32, y0 + 18), (tx + 17, y0 + 38)],
              fill=(16, 22, 48))
    d.rectangle([tx + 6, y0 + 44, tx + 28, y0 + 50], fill=(255, 205, 90))
    # interceptor arcs — bounding boxes kept inside the illustration box
    d.arc([x0 + 8, y0 + 2, x0 + w_ - 90, y0 + 118], 200, 330, fill=(255, 220, 130), width=2)
    d.arc([x0 + 40, y0 + 10, x0 + w_ - 30, y0 + 126], 205, 335, fill=(240, 240, 235), width=2)
    ex, ey = x0 + int(w_ * 0.62), y0 + 22
    for dx, dy in [(0, 0), (-6, -3), (6, -4), (-4, 5), (5, 4)]:
        d.ellipse([ex + dx - 3, ey + dy - 3, ex + dx + 3, ey + dy + 3], fill=(255, 170, 60))


def art_peru(d, box):
    x0, y0, w_, h_ = box
    _sky(d, box, top=(14, 26, 52), bot=(44, 66, 104))
    _stars(d, box, 18, 21)
    base = y0 + h_
    # mountain ridges
    d.polygon([(x0, base), (x0 + 40, y0 + 34), (x0 + 90, base)], fill=(24, 38, 66))
    d.polygon([(x0 + 60, base), (x0 + 150, y0 + 18), (x0 + 235, base)], fill=(18, 30, 56))
    d.polygon([(x0 + 190, base), (x0 + 265, y0 + 40), (x0 + w_, base)], fill=(24, 38, 66))
    d.polygon([(x0 + 138, y0 + 18), (x0 + 150, y0 + 30), (x0 + 162, y0 + 18),
               (x0 + 156, y0 + 26), (x0 + 144, y0 + 26)], fill=(240, 240, 235))
    d.polygon([(x0 + 32, y0 + 34), (x0 + 40, y0 + 42), (x0 + 48, y0 + 34)],
              fill=(240, 240, 235))
    # seismograph trace
    pts = [(x0 + 6, base - 26), (x0 + 30, base - 26), (x0 + 44, base - 34),
           (x0 + 56, base - 18), (x0 + 68, base - 30), (x0 + 82, base - 14),
           (x0 + 96, base - 38), (x0 + 110, base - 16), (x0 + 128, base - 26),
           (x0 + 150, base - 26), (x0 + 168, base - 20), (x0 + 190, base - 30),
           (x0 + 210, base - 22), (x0 + 240, base - 26), (x0 + w_ - 6, base - 26)]
    d.line(pts, fill=(255, 214, 90), width=2)
    # epicentre ring over Junin
    ex, ey = x0 + int(w_ * 0.56), y0 + 34
    d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], outline=(255, 90, 70), width=2)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 90, 70))


def art_mercury(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(8, 10, 24))
    _stars(d, box, 30, 31)
    # cratered Mercury
    cx, cy, r = x0 + int(w_ * 0.38), y0 + int(h_ * 0.52), 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 164, 138))
    for ox, oy, orr in [(-14, -10, 9), (10, 6, 12), (-2, 16, 7), (16, -14, 6)]:
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(150, 136, 112))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 108, 88))
    # sun
    sx, sy, sr = x0 + w_ - 34, y0 + 26, 20
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 205, 60))
    d.ellipse([sx - sr + 6, sy - sr + 6, sx + sr - 6, sy + sr - 6], fill=(255, 228, 130))
    # spacecraft + dashed trajectory
    px, py = x0 + w_ - 92, y0 + 30
    d.line([(x0 + 20, y0 + h_ - 18), (px - 8, py + 4)], fill=(220, 220, 210), width=1)
    for i in range(0, 5):
        d.line([(x0 + 20 + i * 16, y0 + h_ - 18 - i * 9),
                (x0 + 30 + i * 16, y0 + h_ - 20 - i * 9)], fill=(220, 220, 210), width=2)
    d.rectangle([px - 10, py - 5, px + 10, py + 5], fill=(150, 160, 175))
    d.rectangle([px - 22, py - 2, px - 10, py + 2], fill=(110, 120, 135))
    d.polygon([(px + 10, py - 5), (px + 20, py), (px + 10, py + 5)], fill=(255, 190, 80))


def art_cop31(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(28, 84, 72))
    # draft document
    dx, dy, dw, dh = x0 + 12, y0 + 6, w_ - 24, h_ - 12
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(250, 246, 236))
    d.rectangle([dx, dy, dx + dw, dy + dh], outline=(120, 110, 92))
    for i, yy in enumerate(range(dy + 8, dy + dh - 14, 8)):
        ln = dw - 24 if i % 2 == 0 else dw - 46
        d.line([(dx + 10, yy), (dx + 10 + ln, yy)], fill=(180, 172, 152), width=2)
    # "FOSSIL FUELS" struck through with one clean red line
    f = font(SANS_B, 11)
    t = "FOSSIL FUELS"
    tx = dx + (dw - tw(t, f)) / 2
    ty = dy + dh // 2 - 6
    d.text((tx, ty), t, font=f, fill=(40, 40, 40))
    d.line([(tx - 3, ty + 6), (tx + tw(t, f) + 3, ty + 6)], fill=(200, 30, 30), width=3)
    # red X in the top-right corner of the document
    ex, ey = dx + dw - 12, dy + 10
    d.line([(ex - 5, ey - 5), (ex + 5, ey + 5)], fill=(200, 30, 30), width=3)
    d.line([(ex - 5, ey + 5), (ex + 5, ey - 5)], fill=(200, 30, 30), width=3)


def art_panama(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(16, 40, 78))
    _stars(d, box, 10, 51)
    base = y0 + h_
    # sea swell lines
    for yy in (base - 16, base - 10, base - 5):
        for xx in range(x0 + 4, x0 + w_ - 8, 16):
            d.arc([xx, yy - 3, xx + 12, yy + 3], 180, 360, fill=(120, 170, 210), width=1)
    # two epicentres joined by a fault line
    e1 = (x0 + int(w_ * 0.30), y0 + 20)
    e2 = (x0 + int(w_ * 0.72), y0 + 26)
    d.line([e1, e2], fill=(255, 214, 90), width=2)
    for ex, ey in (e1, e2):
        d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], outline=(255, 110, 70), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 110, 70))


def art_odisha(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(30, 58, 66))
    # rain streaks
    import random
    rnd = random.Random(61)
    for _ in range(26):
        rx = rnd.randint(x0 + 3, x0 + w_ - 6)
        ry = rnd.randint(y0 + 2, y0 + h_ - 22)
        d.line([(rx, ry), (rx - 3, ry + 9)], fill=(170, 200, 215), width=1)
    # flooded field + hut roof
    base = y0 + h_
    d.rectangle([x0, base - 16, x0 + w_, base], fill=(96, 74, 52))
    d.rectangle([x0, base - 20, x0 + w_, base - 16], fill=(140, 180, 200))
    d.polygon([(x0 + int(w_ * 0.62), base - 34), (x0 + int(w_ * 0.78), base - 34),
               (x0 + int(w_ * 0.70), base - 46)], fill=(120, 84, 58))


def art_gta(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(12, 16, 34))
    # faint grid
    for gx in range(x0 + 18, x0 + w_, 18):
        d.line([(gx, y0 + 4), (gx, y0 + h_ - 4)], fill=(28, 34, 58), width=1)
    for gy in range(y0 + 12, y0 + h_, 12):
        d.line([(x0 + 4, gy), (x0 + w_ - 4, gy)], fill=(28, 34, 58), width=1)
    # rising Kalshi line with arrowhead
    pts = [(x0 + 10, y0 + h_ - 18), (x0 + 45, y0 + h_ - 24), (x0 + 78, y0 + h_ - 30),
           (x0 + 112, y0 + h_ - 26), (x0 + 145, y0 + 22), (x0 + w_ - 12, y0 + 10)]
    d.line(pts, fill=(80, 220, 130), width=2)
    for px, py in pts[1:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 8, ey + 8)], fill=(80, 220, 130))
    f = font(SANS_B, 11)
    d.text((x0 + 8, y0 + 4), "15% \u2192 40%", font=f, fill=(120, 240, 160))


def art_denmark(d, box):
    x0, y0, w_, h_ = box
    _sky(d, box, top=(20, 28, 60), bot=(40, 56, 96))
    base = y0 + h_
    # Copenhagen rooftops
    d.rectangle([x0 + 8, base - 26, x0 + 58, base], fill=(12, 16, 34))
    d.polygon([(x0 + 8, base - 26), (x0 + 33, base - 40), (x0 + 58, base - 26)],
              fill=(16, 20, 40))
    d.rectangle([x0 + 100, base - 34, x0 + 150, base], fill=(12, 16, 34))
    d.polygon([(x0 + 100, base - 34), (x0 + 125, base - 48), (x0 + 150, base - 34)],
              fill=(16, 20, 40))
    # Danish flag, top right
    fx, fy, fw, fh = x0 + w_ - 48, y0 + 6, 40, 26
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(198, 12, 48))
    d.rectangle([fx + 12, fy, fx + 18, fy + fh], fill=(255, 255, 255))
    d.rectangle([fx, fy + 10, fx + fw, fy + 16], fill=(255, 255, 255))
    # microphone
    mx, my = x0 + int(w_ * 0.52), y0 + h_ - 26
    d.ellipse([mx - 8, my - 16, mx + 8, my], fill=(200, 200, 200))
    d.line([(mx, my), (mx, my + 10)], fill=(200, 200, 200), width=3)
    d.line([(mx - 7, my + 10), (mx + 7, my + 10)], fill=(200, 200, 200), width=2)


def art_cyber(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(10, 14, 30))
    cx, cy, r = x0 + int(w_ * 0.42), y0 + int(h_ * 0.55), 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 210))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(160, 200, 240))
    d.line([(cx - r, cy), (cx + r, cy)], fill=(160, 200, 240), width=1)
    d.ellipse([cx - 6, cy - r, cx + 6, cy + r], outline=(160, 200, 240))
    # four target nodes linked to the globe
    for tx, ty in [(x0 + 18, y0 + 12), (x0 + w_ - 20, y0 + 14),
                   (x0 + 16, y0 + h_ - 12), (x0 + w_ - 18, y0 + h_ - 14)]:
        d.line([(cx, cy), (tx, ty)], fill=(120, 160, 220), width=1)
        d.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], outline=(255, 90, 70), width=2)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(255, 90, 70))


def art_drone(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(58, 30, 22))
    base = y0 + h_
    d.rectangle([x0, base - 14, x0 + w_, base], fill=(24, 52, 74))
    # quadcopter silhouette + interception burst
    cx, cy = x0 + int(w_ * 0.55), y0 + int(h_ * 0.45)
    d.ellipse([cx - 8, cy - 5, cx + 8, cy + 5], fill=(230, 230, 220))
    for dx, dy in [(-24, -10), (24, -10), (-24, 10), (24, 10)]:
        d.line([(cx + dx * 0.4, cy + dy * 0.4), (cx + dx, cy + dy)],
               fill=(200, 200, 190), width=2)
        d.ellipse([cx + dx - 5, cy + dy - 2, cx + dx + 5, cy + dy + 2],
                  fill=(200, 200, 190))
    bx, by = x0 + int(w_ * 0.82), y0 + 16
    for dx, dy in [(0, 0), (-6, -4), (6, -4), (-5, 5), (6, 4)]:
        d.ellipse([bx + dx - 3, by + dy - 3, bx + dx + 3, by + dy + 3],
                  fill=(255, 190, 80))


def art_gaza(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(74, 62, 40))
    base = y0 + h_
    d.rectangle([x0, base - 12, x0 + w_, base], fill=(52, 44, 30))
    # refugee tents
    for tx in (0.18, 0.50, 0.78):
        px = x0 + int(w_ * tx)
        d.polygon([(px - 24, base - 12), (px, base - 36), (px + 24, base - 12)],
                  fill=(214, 200, 164))
        d.polygon([(px - 24, base - 12), (px, base - 36), (px + 24, base - 12)],
                  outline=(120, 104, 74))
    # smoke wisps
    for sx, sy in [(x0 + 30, y0 + 12), (x0 + 90, y0 + 8), (x0 + 150, y0 + 14)]:
        d.ellipse([sx - 8, sy - 5, sx + 8, sy + 5], fill=(200, 190, 170))


def art_poland(d, box):
    x0, y0, w_, h_ = box
    _sky(d, box, top=(18, 30, 58), bot=(46, 68, 104))
    base = y0 + h_
    # land silhouette
    d.polygon([(x0, base), (x0 + 30, base - 18), (x0 + 90, base - 10),
               (x0 + 140, base - 20), (x0 + w_, base - 8), (x0 + w_, base)],
              fill=(24, 40, 62))
    # jet
    jx, jy = x0 + int(w_ * 0.78), y0 + 16
    d.polygon([(jx, jy), (jx - 16, jy + 6), (jx - 4, jy + 4), (jx - 14, jy + 12),
               (jx - 2, jy + 6), (jx + 12, jy + 4)], fill=(220, 220, 210))
    # three impact points
    for ix, iy in [(0.22, 0.62), (0.48, 0.70), (0.70, 0.60)]:
        px, py = x0 + int(w_ * ix), y0 + int(h_ * iy)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(255, 110, 70), width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 110, 70))


def art_kyiv(d, box):
    x0, y0, w_, h_ = box
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(16, 28, 52))
    base = y0 + h_
    # broken bridge: two spans, gap in the middle
    d.rectangle([x0 + 6, base - 26, x0 + int(w_ * 0.42), base - 20], fill=(180, 180, 170))
    d.rectangle([x0 + int(w_ * 0.58), base - 26, x0 + w_ - 6, base - 20], fill=(180, 180, 170))
    for px in (0.10, 0.28, 0.66, 0.86):
        d.rectangle([x0 + int(w_ * px), base - 40, x0 + int(w_ * px) + 3, base - 20],
                    fill=(150, 150, 140))
    # tilted fallen span + blasts
    d.line([(x0 + int(w_ * 0.44), base - 22), (x0 + int(w_ * 0.56), base - 12)],
           fill=(150, 150, 140), width=3)
    for bx, by in [(0.30, 0.30), (0.55, 0.45), (0.80, 0.28)]:
        ex, ey = x0 + int(w_ * bx), y0 + int(h_ * by)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 140, 50))
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 210, 90))


ART = {"riyadh": art_riyadh, "peru": art_peru, "mercury": art_mercury,
       "cop31": art_cop31, "panama": art_panama, "odisha": art_odisha,
       "gta": art_gta, "denmark": art_denmark, "cyber": art_cyber,
       "drone": art_drone, "gaza": art_gaza, "poland": art_poland,
       "kyiv": art_kyiv}

# ------------------------------------------------------------------ layout
MX = 28
CW = 968
RX = MX + CW  # 996


def draw_masthead(d):
    centre(d, W // 2, 8, KICKER, font(SANS_B, 13), RED)
    centre(d, W // 2, 26, MASTHEAD, font(SERIF, 62), INK)
    centre(d, W // 2, 92, DATE_LINE, font(SERIF, 21), RED)
    d.line([(MX, 116), (RX, 116)], fill=INK, width=2)
    d.line([(MX, 119), (RX, 119)], fill=INK, width=1)
    centre(d, W // 2, 126, SUBHEAD, font(SANS_B, 15), NAVY)


def draw_regions(d):
    y, h_ = 146, 19
    seg = CW // 6
    f = font(SANS_B, 11)
    for i, (name, n, col) in enumerate(REGIONS):
        x0 = MX + i * seg
        x1 = RX if i == 5 else x0 + seg
        d.rectangle([x0, y, x1, y + h_], fill=col)
        centre(d, (x0 + x1) // 2, y + 3, "%s  %d" % (name, n), f, (255, 255, 255))


def draw_numbers(d):
    f_lab = font(SANS_B, 11)
    d.text((MX, 170), "BY THE NUMBERS", font=f_lab, fill=RED)
    colw = CW // 6
    f_num = font(SANS_B, 19)
    f_cap = font(SANS, 10)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + i * colw + colw // 2
        centre(d, cx, 184, num, f_num, RED)
        lines = cap.split("\n")
        for j, ln in enumerate(lines):
            centre(d, cx, 206 + j * 11, ln, f_cap, (70, 66, 56))
        if i:
            d.line([(MX + i * colw, 184), (MX + i * colw, 226)], fill=(200, 192, 172), width=1)
    d.line([(MX, 230), (RX, 230)], fill=INK, width=1)


def draw_lead(d, item, x, w_):
    ART[item["art"]](d, (x, 236, w_, 96))
    chip(d, x + 4, 236 + 96 - 22, item["chip"], font(SANS_B, 10))
    f_lab = font(SANS_B, 11)
    d.text((x, 336), "%d \u00b7 %s \u2014 %s" % (item["num"], item["city"], item["region"]),
           font=f_lab, fill=RED)
    f_t = font(SERIF, 17)
    lines = wrap(item["title"], f_t, w_, max_lines=2)
    for j, ln in enumerate(lines):
        d.text((x, 350 + j * 19), ln, font=f_t, fill=INK)
    f_b = font(SANS, 11)
    blines = wrap(item["body"], f_b, w_, max_lines=3)
    for j, ln in enumerate(blines):
        d.text((x, 390 + j * 13), ln, font=f_b, fill=INK)
    d.text((x, 430), item["source"], font=font(SANS, 9), fill=GREY)


def draw_card(d, item, x, y_illo, w_):
    ART[item["art"]](d, (x, y_illo, w_, 60))
    chip(d, x + 3, y_illo + 60 - 19, item["chip"], font(SANS_B, 9))
    y_lab = y_illo + 64
    d.text((x, y_lab), "%d \u00b7 %s \u2014 %s" % (item["num"], item["city"], item["region"]),
           font=font(SANS_B, 10), fill=RED)
    f_t = font(SERIF, 13)
    lines = wrap(item["title"], f_t, w_, max_lines=2)
    for j, ln in enumerate(lines):
        d.text((x, y_lab + 14 + j * 15), ln, font=f_t, fill=INK)
    f_b = font(SANS, 10)
    blines = wrap(item["body"], f_b, w_, max_lines=3)
    for j, ln in enumerate(blines):
        d.text((x, y_lab + 46 + j * 11), ln, font=f_b, fill=INK)
    d.text((x, y_lab + 80), item["source"], font=font(SANS, 9), fill=GREY)


# ------------------------------------------------------------- dotted map
# Schematic continents as pixel-space blocks inside the map panel.
# (x0, y0, x1, y1, step_x, step_y) — North America uses a finer grid (v3).
BLOBS = [
    (70, 780, 330, 806, 6, 5),    # North America (denser)
    (70, 780, 150, 790, 6, 5),    # Alaska
    (255, 804, 320, 816, 6, 5),   # Central America (denser)
    (338, 778, 372, 788, 7, 6),   # Greenland
    (280, 810, 335, 822, 7, 6),   # South America, north
    (290, 820, 330, 840, 7, 6),   # South America, south
    (458, 784, 470, 792, 7, 6),   # Britain
    (462, 782, 545, 798, 7, 6),   # Europe
    (462, 798, 565, 838, 7, 6),   # Africa
    (545, 782, 640, 804, 7, 6),   # Middle East / W Asia
    (640, 780, 905, 808, 7, 6),   # Asia, north
    (700, 806, 800, 822, 7, 6),   # SE Asia
    (760, 820, 880, 828, 7, 6),   # Indonesia
    (895, 784, 910, 798, 7, 6),   # Japan
    (815, 812, 905, 830, 7, 6),   # Australia
]

# pin: (number, geo_x, geo_y, badge_x, badge_y)
# Badge centres are clamped to stay >= 2 px inside the panel (radius 9).
PINS = [
    (1, 582, 808, 598, 822),    # Riyadh
    (2, 262, 826, 270, 832),    # Peru
    (4, 522, 798, 510, 812),    # Antalya
    (5, 292, 810, 282, 802),    # Panama
    (6, 758, 804, 772, 798),    # Odisha
    (7, 205, 792, 200, 788),    # GTA VI / New York markets
    (8, 508, 784, 494, 788),    # Copenhagen
    (9, 478, 788, 468, 800),    # London
    (10, 566, 818, 544, 832),   # S. Saudi
    (11, 542, 806, 560, 816),   # Gaza
    (12, 530, 788, 540, 788),   # Poland
    (13, 550, 792, 574, 800),   # Kyiv — badge pushed down-right, fully inside
]


def draw_map(d):
    d.text((MX, 758), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    note = "pins 1\u201313 = lead + card stories"
    d.text((RX - tw(note, font(SANS, 9)), 760), note, font=font(SANS, 9), fill=GREY)
    top, bot = 774, 844
    d.rectangle([MX, top, RX, bot], fill=LIGHT, outline=RULE)
    # dotted continents — rows staggered by half a step, edges thinned
    # deterministically so the block borders read less like rectangles
    for (x0, y0, x1, y1, sx, sy) in BLOBS:
        yy = y0
        row = 0
        while yy <= y1:
            xx = x0 + (row % 2) * (sx // 2)
            while xx <= x1:
                edge = (xx - x0 < sx or x1 - xx < sx or
                        yy - y0 < sy or y1 - yy < sy)
                if not (edge and (xx * 3 + yy * 7) % 5 == 0):
                    d.ellipse([xx - 1, yy - 1, xx + 1, yy + 1], fill=DOT)
                xx += sx
            yy += sy
            row += 1
    # pins: geo dot + leader line + numbered badge (clamped inside panel)
    f_n = font(SANS_B, 10)
    for (n, gx, gy, bx, by) in PINS:
        bx = max(MX + 11, min(RX - 11, bx))
        by = max(top + 11, min(bot - 11, by))
        d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=RED)
        d.line([(gx, gy), (bx, by)], fill=RED, width=1)
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED, outline=(255, 255, 255))
        t = str(n)
        d.text((bx - tw(t, f_n) / 2, by - 7), t, font=f_n, fill=(255, 255, 255))
    # Mercury sits off-map, top-right corner of the panel
    mx, my = 960, 790
    d.text((RX - 46 - tw("Mercury", font(SANS_B, 11)), my - 6), "Mercury",
           font=font(SANS_B, 11), fill=NAVY)
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=RED, outline=(255, 255, 255))
    d.text((mx - tw("3", f_n) / 2, my - 7), "3", font=f_n, fill=(255, 255, 255))


def draw_also(d):
    d.text((MX, 850), "ALSO \u2014 THE REST OF THE DAY", font=font(SANS_B, 12), fill=RED)
    d.line([(MX, 864), (RX, 864)], fill=INK, width=1)
    f = font(SANS, 8)
    f_n = font(SANS_B, 8)
    col_x = [MX, 520]
    for i, (n, text) in enumerate(ALSO):
        col = 0 if i < 11 else 1
        row = i if i < 11 else i - 11
        y_ = 868 + row * 8.5
        x_ = col_x[col]
        d.text((x_, y_), "%d." % n, font=f_n, fill=RED)
        d.text((x_ + 16, y_), text, font=f, fill=INK)


def draw_datecheck(d):
    y_ = 964
    d.rectangle([MX, y_, RX, y_ + 40], outline=RED, width=2)
    d.rectangle([MX, y_, RX, y_ + 14], fill=RED)
    d.text((MX + 6, y_ + 2), "DATE CHECK \u2014 dated right, NOT shown as 21 November news:",
           font=font(SANS_B, 10), fill=(255, 255, 255))
    f = font(SANS, 10)
    d.text((MX + 6, y_ + 16), DATECHECK[0], font=f, fill=INK)
    d.text((MX + 6, y_ + 27), DATECHECK[1], font=f, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_regions(d)
    draw_numbers(d)
    lead_w = 314
    for i, item in enumerate(LEADS):
        draw_lead(d, item, MX + i * (lead_w + 12), lead_w)
    card_w = 185
    for i, item in enumerate(CARDS):
        x_ = MX + (i % 5) * (card_w + 10)
        y_ = 442 if i < 5 else 600
        draw_card(d, item, x_, y_, card_w)
    d.line([(MX, 756), (RX, 756)], fill=INK, width=1)
    draw_map(d)
    draw_also(d)
    draw_datecheck(d)
    d.text((MX, 1008), FOOTER, font=font(SANS, 9), fill=GREY)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    img.save(OUT, "PNG")


if __name__ == "__main__":
    main()
