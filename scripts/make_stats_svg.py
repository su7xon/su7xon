"""Generate compact red/black GitHub stats + languages cards."""
import base64
import os

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

# ---- display values (edit freely) ----
STATS = [
    ("★", "Total Stars Earned", "8"),
    ("◷", "Total Commits", "310"),
    ("⑂", "Total PRs", "12"),
    ("◉", "Total Issues", "5"),
    ("▣", "Contributed to", "6"),
]
RANK = "A+"

LANGS = [
    ("JavaScript", 62.0, "#f1e05a"),
    ("TypeScript", 20.0, "#3178c6"),
    ("Python", 10.0, "#3572A5"),
    ("HTML", 5.0, "#e34c26"),
    ("CSS", 3.0, "#563d7c"),
]
# ---------------------------------------


def stats_bg_data():
    """Base64 JPEG used as the card's inner background artwork."""
    path = os.path.abspath(os.path.join(ASSETS, "stats-bg.jpg"))
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def stats_svg():
    w, h = 440, 230
    bg = stats_bg_data()
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Fira Code, ui-monospace, monospace">')
    p.append("<defs>")
    p.append(f'<clipPath id="card"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12"/></clipPath>')
    p.append('<filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>')
    p.append('<filter id="tshadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="1" stdDeviation="2.2" flood-color="#000000" flood-opacity="0.9"/></filter>')
    p.append('<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0">')
    p.append('<stop offset="0" stop-color="#0a0a0a" stop-opacity="0.88"/>')
    p.append('<stop offset="0.55" stop-color="#0a0a0a" stop-opacity="0.78"/>')
    p.append('<stop offset="1" stop-color="#0a0a0a" stop-opacity="0.46"/>')
    p.append("</linearGradient>")
    p.append("</defs>")
    p.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#0a0a0a"/>')
    if bg:
        p.append(
            f'<image x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#card)" filter="url(#soft)" href="data:image/jpeg;base64,{bg}"/>'
        )
        p.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#shade)"/>')
    p.append(f'<text x="22" y="36" fill="#ef4444" font-size="17" font-weight="700" filter="url(#tshadow)">su7xon\'s GitHub Stats</text>')
    y = 70
    for icon, label, value in STATS:
        p.append(f'<text x="22" y="{y}" fill="#ef4444" font-size="14" filter="url(#tshadow)">{icon}</text>')
        p.append(f'<text x="44" y="{y}" fill="#f3f4f6" font-size="13" filter="url(#tshadow)">{label}:</text>')
        p.append(f'<text x="280" y="{y}" fill="#f3f4f6" font-size="13" font-weight="700" text-anchor="end" filter="url(#tshadow)">{value}</text>')
        y += 28
    # rank ring
    cx, cy, r = 368, 122, 44
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#3a1515" stroke-width="7"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ef4444" stroke-width="7" stroke-dasharray="230 360" stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>')
    p.append(f'<text x="{cx}" y="{cy+8}" fill="#f3f4f6" font-size="20" font-weight="700" text-anchor="middle" filter="url(#tshadow)">{RANK}</text>')
    p.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="none" stroke="#ef4444" stroke-width="1.5"/>')
    p.append("</svg>")
    return "\n".join(p)


def langs_svg():
    w, h = 360, 230
    total = sum(v for _, v, _ in LANGS) or 1
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Fira Code, ui-monospace, monospace">')
    p.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#0a0a0a" stroke="#ef4444" stroke-width="1.5"/>')
    p.append(f'<text x="22" y="36" fill="#ef4444" font-size="17" font-weight="700">Most Used Languages</text>')
    # stacked bar
    x = 22
    bar_w = w - 44
    y = 58
    for _, v, color in LANGS:
        seg = bar_w * v / total
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{seg:.1f}" height="12" fill="{color}"/>')
        x += seg
    # legend rows
    y = 104
    for name, v, color in LANGS:
        p.append(f'<circle cx="28" cy="{y-4}" r="5" fill="{color}"/>')
        p.append(f'<text x="44" y="{y}" fill="#f3f4f6" font-size="13">{name}</text>')
        p.append(f'<text x="{w-22}" y="{y}" fill="#9ca3af" font-size="12" text-anchor="end">{v:.2f}%</text>')
        y += 25
    p.append("</svg>")
    return "\n".join(p)


def main():
    os.makedirs(os.path.abspath(ASSETS), exist_ok=True)
    for name, content in [("stats.svg", stats_svg()), ("langs.svg", langs_svg())]:
        path = os.path.abspath(os.path.join(ASSETS, name))
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
