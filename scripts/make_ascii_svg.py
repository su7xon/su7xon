"""Convert source-prepped.png into a self-typing monochrome ASCII SVG."""
import os
import sys

try:
    from PIL import Image
except ImportError as e:
    print("Missing portrait dependency:", e)
    print("Install with: pip install pillow")
    sys.exit(1)

RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 100, 53
FONT_SIZE = 7
CHAR_W = FONT_SIZE * 0.62
ROW_H = FONT_SIZE * 1.05
FILL = "#9ca3af"

SRC = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")
OUT = os.path.join(os.path.dirname(__file__), "..", "avi-ascii.svg")


def main():
    if not os.path.exists(os.path.abspath(SRC)):
        print("source-prepped.png not found. Run prep_photo.py first.")
        sys.exit(1)
    img = Image.open(os.path.abspath(SRC)).convert("L").resize((COLS, ROWS))
    pixels = list(img.getdata())

    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            lum = pixels[r * COLS + c]
            idx = int((255 - lum) / 255 * (len(RAMP) - 1))
            row.append(RAMP[idx])
        grid.append("".join(row))

    width = int(COLS * CHAR_W) + 10
    height = int(ROWS * ROW_H) + 10

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">')
    # defs clipPaths
    parts.append("<defs>")
    for i in range(ROWS):
        rw = int(COLS * CHAR_W)
        delay = round(i * 0.06, 3)
        parts.append(f'<clipPath id="clip{i}"><rect x="0" y="{i*ROW_H}" width="0" height="{ROW_H+2}"><animate attributeName="width" from="0" to="{rw}" dur="0.5s" begin="{delay}s" fill="freeze"/></rect></clipPath>')
    parts.append("</defs>")

    for i, row in enumerate(grid):
        y = (i + 1) * ROW_H
        # escape xml
        safe = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(f'<text x="4" y="{y}" font-size="{FONT_SIZE}" fill="{FILL}" clip-path="url(#clip{i})" xml:space="preserve">{safe}</text>')

    parts.append("</svg>")
    out_path = os.path.abspath(OUT)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
