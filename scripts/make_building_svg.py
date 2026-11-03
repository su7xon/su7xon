"""Generate a 'Currently Building' progress card SVG."""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "building.svg")

TITLE = "NeuroKoon"
SUBTITLE = "GenAI · Full Stack · n8n"
PROGRESS = 72

W, H = 860, 170


def main():
    bar_x, bar_y, bar_w, bar_h = 30, 118, 800, 12
    fill_w = int(bar_w * PROGRESS / 100)
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Fira Code, ui-monospace, SFMono-Regular, Menlo, monospace">')
    p.append("""<style>
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
    .dot { animation: blink 1.1s steps(1) infinite; }
    </style>""")
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0a0a0a" stroke="#ef4444" stroke-opacity="0.55"/>')
    p.append(f'<text x="30" y="36" fill="#ef4444" font-size="11" letter-spacing="3">CURRENTLY BUILDING</text>')
    p.append(f'<circle class="dot" cx="225" cy="32" r="4" fill="#22c55e"/>')
    p.append(f'<text x="30" y="72" fill="#f3f4f6" font-size="28" font-weight="700">{TITLE}</text>')
    p.append(f'<text x="30" y="96" fill="#9ca3af" font-size="12">{SUBTITLE}</text>')
    p.append(f'<text x="{W-30}" y="72" fill="#ef4444" font-size="22" font-weight="700" text-anchor="end">{PROGRESS}%</text>')
    p.append(f'<text x="{W-30}" y="94" fill="#6b7280" font-size="10" text-anchor="end">shipping soon</text>')
    p.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="#1f2937"/>')
    p.append(f'<rect x="{bar_x}" y="{bar_y}" width="0" height="{bar_h}" rx="6" fill="#ef4444">')
    p.append(f'<animate attributeName="width" from="0" to="{fill_w}" dur="1.5s" fill="freeze"/>')
    p.append('</rect>')
    p.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="none" stroke="#ef4444" stroke-opacity="0.25"/>')
    p.append(f'<text x="{bar_x}" y="{bar_y+32}" fill="#6b7280" font-size="10">idea</text>')
    p.append(f'<text x="{bar_x+bar_w}" y="{bar_y+32}" fill="#6b7280" font-size="10" text-anchor="end">launch</text>')
    p.append("</svg>")
    out = os.path.abspath(OUT)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
