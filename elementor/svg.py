"""Decorative SVGs from the design, encoded for use as CSS backgrounds."""
from urllib.parse import quote


def data_uri(svg: str) -> str:
    return 'url("data:image/svg+xml,' + quote(svg, safe=" =:/,'-.()") + '")'


def _wave(path_y, fill, opacity):
    a, b, c = path_y  # baseline, crest, trough
    d = (f"M0 {a} C240 {b} 480 {b} 720 {a} C960 {c} 1200 {c} 1440 {a} "
         f"C1680 {b} 1920 {b} 2160 {a} C2400 {c} 2640 {c} 2880 {a} V120 H0 Z")
    return data_uri(
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 2880 120' preserveAspectRatio='none'>"
        f"<path d='{d}' fill='{fill}' fill-opacity='{opacity}'/></svg>")


# Card waves: back (w1) to front (w3).
CARD_W1 = _wave((50, 10, 90), "#A2C3D3", 0.35)
CARD_W2 = _wave((72, 40, 104), "#7eb1cb", 0.28)
CARD_W3 = _wave((92, 72, 112), "#6A8CA3", 0.22)

# "Beneath the surface" water line.
SURF_W1 = _wave((50, 10, 90), "#7EB1CB", 0.55)
SURF_W2 = _wave((70, 38, 102), "#2E6680", 0.8)
SURF_W3 = _wave((88, 66, 110), "#1D5067", 1)

# Breathing exercise.
BREATH_W1 = _wave((50, 10, 90), "#A2C3D3", 0.35)
BREATH_W2 = _wave((70, 38, 102), "#7EB1CB", 0.45)
BREATH_W3 = _wave((88, 66, 110), "#7EB1CB", 0.55)

HERO_EDGE = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 80' preserveAspectRatio='none'>"
    "<path d='M0 46 C180 14 360 14 540 40 C720 66 900 70 1080 44 C1240 22 1360 24 1440 36 V80 H0 Z' fill='#F7F5EF'/></svg>")

CTA_EDGE = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 90' preserveAspectRatio='none'>"
    "<path d='M0 0 H1440 V40 C1300 70 1160 72 1010 52 C860 32 720 30 560 52 C400 74 220 76 0 50 Z' fill='#F7F5EF'/>"
    "<path d='M0 50 C220 76 400 74 560 52 C720 30 860 32 1010 52 C1160 72 1300 70 1440 40' fill='none' stroke='#ffffff' stroke-width='5' stroke-linecap='round' opacity='0.9'/>"
    "<path d='M0 62 C220 86 400 84 560 64 C720 44 860 46 1010 64 C1160 82 1300 80 1440 54' fill='none' stroke='#ffffff' stroke-width='2' stroke-linecap='round' opacity='0.5'/></svg>")

GP_MARK = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>"
    "<path d='M40 420 C 140 300, 220 240, 330 260 C 260 300, 250 380, 320 420' fill='none' stroke='#A2C3D3' stroke-width='22' stroke-linecap='round'/>"
    "<path d='M300 80 A 260 260 0 1 1 120 520' fill='none' stroke='#A2C3D3' stroke-width='22' stroke-linecap='round'/></svg>")

PORTRAIT_LINES = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 120' preserveAspectRatio='none'>"
    "<path d='M0 40 C70 20 130 20 200 40 S330 60 400 40' fill='none' stroke='#EBE7DB' stroke-opacity='0.35' stroke-width='2'/>"
    "<path d='M0 70 C70 50 130 50 200 70 S330 90 400 70' fill='none' stroke='#EBE7DB' stroke-opacity='0.25' stroke-width='2'/>"
    "<path d='M0 100 C70 80 130 80 200 100 S330 120 400 100' fill='none' stroke='#EBE7DB' stroke-opacity='0.18' stroke-width='2'/></svg>")

ICE_TIP = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 90'>"
    "<path d='M118 90 L176 26 L202 42 L234 8 L292 90 Z' fill='#A2C3D3'/>"
    "<path d='M234 8 L250 40 L292 90 L262 90 Z' fill='#7EB1CB'/></svg>")

ICE_BELOW = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300' preserveAspectRatio='none'>"
    "<path d='M128 0 L282 0 L350 80 L336 176 L262 292 L140 278 L58 176 L66 70 Z' fill='#A2C3D3' fill-opacity='0.16'/></svg>")

CARE_LINE = data_uri(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 500' preserveAspectRatio='none'>"
    "<path d='M24 0 C 40 20 40 30 24 50 C 8 70 8 80 24 100 C 40 120 40 130 24 150 C 8 170 8 180 24 200 "
    "C 40 220 40 230 24 250 C 8 270 8 280 24 300 C 40 320 40 330 24 350 C 8 370 8 380 24 400 C 40 420 40 430 24 450 "
    "C 8 470 8 480 24 500' fill='none' stroke='#6A8CA3' stroke-width='2.5' stroke-linecap='round' "
    "stroke-dasharray='1 9' vector-effect='non-scaling-stroke'/></svg>")

# Shoreline: sea-foam waves lapping onto the sand.
SHORE_W1 = _wave((40, 8, 72), "#EEF5F7", 0.95)   # foam at the waterline
SHORE_W2 = _wave((58, 30, 90), "#BBD8E3", 1)
SHORE_W3 = _wave((76, 54, 100), "#8FBFD2", 1)
