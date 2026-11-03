"""Generate compact red/black GitHub stats + languages cards."""
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


def stats_svg():
    w, h = 440, 230
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Fira Code, ui-monospace, monospace">')
    p.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#0a0a0a" stroke="#ef4444" stroke-width="1.5"/>')
    p.append(f'<text x="22" y="36" fill="#ef4444" font-size="17" font-weight="700">su7xon\'s GitHub Stats</text>')
    y = 70
    for icon, label, value in STATS:
        p.append(f'<text x="22" y="{y}" fill="#ef4444" font-size="14">{icon}</text>')
        p.append(f'<text x="44" y="{y}" fill="#f3f4f6" font-size="13">{label}:</text>')
        p.append(f'<text x="280" y="{y}" fill="#f3f4f6" font-size="13" font-weight="700" text-anchor="end">{value}</text>')
        y += 28
    # rank ring
    cx, cy, r = 368, 122, 44
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#3a1515" stroke-width="7"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ef4444" stroke-width="7" stroke-dasharray="230 360" stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>')
    p.append(f'<text x="{cx}" y="{cy+8}" fill="#f3f4f6" font-size="20" font-weight="700" text-anchor="middle">{RANK}</text>')
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
