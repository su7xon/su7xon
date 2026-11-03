"""Generate a neofetch-style info card SVG."""
import os
import sys
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
STATIC = os.environ.get("STATIC") == "1"

# ---- edit these to tell your story ----
TITLE = "su7xon@github"
ROWS = [
    ("Now", "Building cool stuff & learning in public"),
    ("Prev", "Exploring open source & side projects"),
    ("Stack", "Python · JavaScript · Git · Linux"),
    ("Highlights", "Terminal-style profile, daily auto-refresh"),
    ("Contact", "github.com/su7xon"),
]
# --------------------------------------

W, H = 490, 260


def main():
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">')
    if not STATIC:
        lines.append("""<style>
@keyframes fadeSlide { 0% { opacity:0; transform: translateX(-8px);} 100% { opacity:1; transform: translateX(0);} }
.row { animation: fadeSlide 0.5s ease-out both; }
</style>""")
    # background
    lines.append(f'<rect width="{W}" height="{H}" rx="10" ry="10" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')
    # title bar
    lines.append(f'<rect width="{W}" height="30" rx="10" ry="10" fill="#161b22"/>')
    lines.append(f'<rect y="20" width="{W}" height="10" fill="#161b22"/>')
    lines.append(f'<circle cx="16" cy="15" r="5" fill="#ff5f56"/>')
    lines.append(f'<circle cx="32" cy="15" r="5" fill="#ffbd2e"/>')
    lines.append(f'<circle cx="48" cy="15" r="5" fill="#27c93f"/>')
    lines.append(f'<text x="{W//2}" y="20" fill="#8b949e" font-size="12" text-anchor="middle">{escape(TITLE)}</text>')

    y = 56
    # neofetch-style ascii-ish header
    lines.append(f'<text x="20" y="{y}" fill="#39d353" font-size="12" font-weight="600">su7xon@github</text>')
    lines.append(f'<text x="20" y="{y+16}" fill="#8b949e" font-size="11">--------------</text>')
    y += 36

    for i, (k, v) in enumerate(ROWS):
        delay = 0 if STATIC else round(i * 0.18, 2)
        cls = "" if STATIC else 'class="row"'
        style = "" if STATIC else f' style="animation-delay:{delay}s; opacity:0;"'
        lines.append(f'<g {cls}{style}>')
        lines.append(f'<text x="20" y="{y}" fill="#58a6ff" font-size="12" font-weight="600">{escape(k)}:</text>')
        lines.append(f'<text x="110" y="{y}" fill="#c9d1d9" font-size="12">{escape(v)}</text>')
        lines.append("</g>")
        y += 22

    # footer hint
    lines.append(f'<text x="20" y="{H-14}" fill="#484f58" font-size="10">edit scripts/make_info_card.py to update</text>')

    lines.append("</svg>")
    out_path = os.path.abspath(OUT)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
