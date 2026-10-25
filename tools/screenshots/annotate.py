"""Annotate raw Webots captures (raw/*.png) and write them to docs/images/.

Usage (from the repo root):
    python3 tools/screenshots/annotate.py            # all specs
    python3 tools/screenshots/annotate.py 03-        # only names starting with "03-"

Each spec in specs.py names a raw capture, a crop box and a list of notes. A note outlines a
target rectangle and points at it from a numbered label. Coordinates are raw window pixels,
so the crop can change without touching the notes.
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

from specs import SPECS

HERE = pathlib.Path(__file__).parent
RAW = HERE / "raw"
OUT = HERE.parent.parent / "docs" / "images"

COLORS = {"red": (229, 57, 53), "blue": (30, 136, 229), "dark": (55, 71, 79)}
FONT = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 22)
NUM_FONT = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 18)
PAD_X, PAD_Y, GAP = 12, 7, 5


def outline(draw, box, color):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), radius=4, outline=color, width=3)


def label_box(draw, text, at, num):
    """Return the label rectangle whose top-left corner is `at`."""
    lines = text.split("\n")
    widths = [draw.textlength(line, font=FONT) for line in lines]
    line_h = FONT.size + GAP
    num_w = 34 if num else 0
    w = num_w + max(widths) + 2 * PAD_X
    h = len(lines) * line_h - GAP + 2 * PAD_Y
    return (at[0], at[1], at[0] + w, at[1] + h), lines, line_h, num_w


def draw_label(draw, text, at, color, num):
    box, lines, line_h, num_w = label_box(draw, text, at, num)
    draw.rounded_rectangle(box, radius=6, fill=color, outline="white", width=2)
    x0, y0, _, y1 = box
    if num:
        cy = (y0 + y1) // 2
        cx = x0 + PAD_X + 13
        draw.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill="white")
        draw.text((cx, cy), str(num), font=NUM_FONT, fill=color, anchor="mm")
    for i, line in enumerate(lines):
        draw.text((x0 + PAD_X + num_w, y0 + PAD_Y + i * line_h - 2), line, font=FONT, fill="white")
    return box


def edge_point(box, toward):
    """Point on the edge of `box` facing `toward`."""
    x0, y0, x1, y1 = box
    tx, ty = toward
    x = min(max(tx, x0), x1)
    y = min(max(ty, y0), y1)
    if x0 < tx < x1 and y0 < ty < y1:
        return (x0 + x1) // 2, (y0 + y1) // 2
    return x, y


def arrow(draw, start, end, color):
    draw.line((start, end), fill=color, width=3)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    size = 14
    left = (end[0] - size * ux + size * 0.5 * uy, end[1] - size * uy - size * 0.5 * ux)
    right = (end[0] - size * ux - size * 0.5 * uy, end[1] - size * uy + size * 0.5 * ux)
    draw.polygon((end, left, right), fill=color)


def render(name, spec):
    im = Image.open(RAW / f"{spec.get('raw', name)}.png").convert("RGB")
    draw = ImageDraw.Draw(im)
    for note in spec.get("notes", []):
        color = COLORS[note.get("color", "red")]
        target = note.get("box")
        if target:
            outline(draw, target, color)
        if "label" not in note and note.get("num"):  # bare number marker on the box corner
            cx, cy = note.get("mark", target[:2])
            draw.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=color, outline="white", width=2)
            draw.text((cx, cy), str(note["num"]), font=NUM_FONT, fill="white", anchor="mm")
        if "label" in note:
            box = draw_label(draw, note["label"], note["at"], color, note.get("num"))
            if target and note.get("arrow", True):
                tbox = (target[0] - 4, target[1] - 4, target[2] + 4, target[3] + 4)
                end = edge_point(tbox, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2))
                start = edge_point(box, end)
                arrow(draw, start, end, color)
    im = im.crop(spec["crop"])
    if "width" in spec:
        im = im.resize((spec["width"], round(im.height * spec["width"] / im.width)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / f"{name}.png", optimize=True)
    print(OUT / f"{name}.png", im.size)


if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    for name, spec in SPECS.items():
        if name.startswith(prefix):
            render(name, spec)
