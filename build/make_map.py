#!/usr/bin/env python3
"""Render a small panoramic world map for the 19 November front page.

Reads the public-domain Natural Earth 110m land GeoJSON (downloaded to this
directory), projects it equirectangularly so the whole world fits a wide
strip, and marks the places behind the day's big stories.
Output: build/map.png at 2x (1928 x 400), displayed at 964 x 200.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1928, 400            # 2x of the 964 x 200 display size
LON_MIN, LON_MAX = -180.0, 180.0
LAT_MIN, LAT_MAX = -58.0, 84.0   # Antarctica left out, as on most news maps

PAPER = (251, 248, 240, 255)     # page background
LAND = (74, 68, 56, 255)         # dark warm grey, matches the masthead ink
LAND_EDGE = (138, 130, 114, 255)
RED = (160, 30, 30, 255)
INK = (26, 23, 18, 255)

# (label, lon, lat, label dx, label dy) — offsets in 2x pixels
PLACES = [
    ("THE HAGUE", 4.3, 52.1, -230, -46),
    ("SHENZHEN", 114.1, 22.5, 18, 10),
    ("HORMUZ", 56.3, 26.6, 18, -48),
    ("CRIMEA", 34.0, 45.0, -20, -50),
    ("GAZA", 34.5, 31.5, -140, 16),
    ("ADDIS ABABA", 38.7, 9.0, 18, 8),
]


def project(lon, lat):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * W
    # equirectangular y, then squash vertically into the strip height
    y_full = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * (W * (LAT_MAX - LAT_MIN) / 360.0)
    y = y_full * (H / (W * (LAT_MAX - LAT_MIN) / 360.0))
    return x, y


def split_ring(ring):
    """Split a ring wherever it jumps across the antimeridian."""
    parts, cur = [], [ring[0]]
    for a, b in zip(ring, ring[1:]):
        if abs(b[0] - a[0]) > 180:
            parts.append(cur)
            cur = [b]
        else:
            cur.append(b)
    parts.append(cur)
    return [p for p in parts if len(p) >= 3]


def draw_land(draw):
    with open(os.path.join(HERE, "ne_110m_land.geojson")) as f:
        data = json.load(f)
    for feat in data["features"]:
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]
        for poly in polys:
            for ring in poly:
                for part in split_ring(ring):
                    pts = [project(lon, lat) for lon, lat in part]
                    draw.polygon(pts, fill=LAND, outline=LAND_EDGE)


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_land(draw)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    for label, lon, lat, dx, dy in PLACES:
        x, y = project(lon, lat)
        draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED,
                     outline=(255, 255, 255, 255), width=3)
        draw.text((x + dx, y + dy), label, font=font, fill=INK,
                  stroke_width=4, stroke_fill=PAPER)

    out = os.path.join(HERE, "map.png")
    img.save(out)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
