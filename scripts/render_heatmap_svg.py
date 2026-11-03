"""Render data/contributions.json as an animated contribution heatmap SVG."""
import json
import os
from datetime import date, timedelta

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")
TOTAL_OVERRIDE = os.environ.get("TOTAL_OVERRIDE")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

BOX = 11
GAP = 3
LEFT = 44
TOP = 46
DAY_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]


def color_for_level(level):
    if level <= 0:
        return PALETTE[0]
    idx = min(level, 4)
    # top level gets neon end
    if idx == 4:
        idx = 5
    return PALETTE[idx]


def main():
    with open(os.path.abspath(DATA), encoding="utf-8") as f:
        payload = json.load(f)
    days = payload["days"]
    stats = payload["stats"]
    day_map = {d["date"]: d for d in days}

    dates = [d["date"] for d in days]
    first = date.fromisoformat(min(dates))
    last = date.fromisoformat(max(dates))

    # align start to Sunday on or before first date
    start_sunday = first - timedelta(days=(first.weekday() + 1) % 7)
    # number of weeks to cover through last date
    total_days = (last - start_sunday).days + 1
    num_weeks = (total_days + 6) // 7
    if num_weeks < 53:
        num_weeks = 53

    width = LEFT + num_weeks * (BOX + GAP) + 20
    height = TOP + 7 * (BOX + GAP) + 60

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">')
    parts.append("<style>")
    parts.append("""
@keyframes slideIn {
  0% { opacity: 0; transform: translateY(-6px); }
  100% { opacity: 1; transform: translateY(0); }
}
.box { animation: slideIn 0.45s ease-out both; }
""")
    parts.append("</style>")

    # title (TOTAL_OVERRIDE lets you show a custom headline number)
    display_total = int(TOTAL_OVERRIDE) if TOTAL_OVERRIDE else stats["total"]
    parts.append(f'<text x="{LEFT}" y="24" fill="#c9d1d9" font-size="13" font-weight="600">{display_total:,} contributions in the last year</text>')

    # weekday labels
    for r in range(7):
        y = TOP + r * (BOX + GAP) + BOX - 2
        label = DAY_LABELS[r]
        if label:
            parts.append(f'<text x="{LEFT - 6}" y="{y}" fill="#8b949e" font-size="9" text-anchor="end">{label}</text>')

    # month labels: place at first week where month changes
    # compute for each week the month of first day
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    seen_months = set()
    for w in range(num_weeks):
        week_start = start_sunday + timedelta(weeks=w)
        m = week_start.month
        # label only if this is the first week whose month != previous labeled
        # simple: label on first day-of-month week
        day = week_start
        if day.day <= 7:
            x = LEFT + w * (BOX + GAP)
            parts.append(f'<text x="{x}" y="{TOP - 8}" fill="#8b949e" font-size="9">{month_names[m-1]}</text>')

    # boxes
    for w in range(num_weeks):
        for r in range(7):
            d = start_sunday + timedelta(weeks=w, days=r)
            if d < first or d > last:
                continue
            ds = d.isoformat()
            info = day_map.get(ds, {"level": 0, "count": 0})
            level = info.get("level", 0)
            count = info.get("count", 0)
            x = LEFT + w * (BOX + GAP)
            y = TOP + r * (BOX + GAP)
            color = color_for_level(level)
            delay = round((w + r) * 0.012, 3)
            tooltip = f"{count} contribution{'s' if count != 1 else ''} on {d.strftime('%b %-d')}" if False else f"{count} contributions on {d.isoformat()}"
            # use simple title
            parts.append(f'<rect class="box" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" ry="2" fill="{color}" style="animation-delay:{delay}s"><title>{count} contributions on {ds}</title></rect>')

    # legend
    leg_y = TOP + 7 * (BOX + GAP) + 14
    parts.append(f'<text x="{LEFT}" y="{leg_y + BOX - 2}" fill="#8b949e" font-size="9">Less</text>')
    lx = LEFT + 34
    for i, c in enumerate(PALETTE):
        parts.append(f'<rect x="{lx + i*(BOX+2)}" y="{leg_y}" width="{BOX}" height="{BOX}" rx="2" ry="2" fill="{c}"/>')
    parts.append(f'<text x="{lx + len(PALETTE)*(BOX+2) + 4}" y="{leg_y + BOX - 2}" fill="#8b949e" font-size="9">More</text>')

    # stats footer
    footer_y = leg_y + BOX + 18
    cs = stats["current_streak"]
    ls = stats["longest_streak"]
    bd = stats.get("best_day") or {}
    parts.append(f'<text x="{LEFT}" y="{footer_y}" fill="#8b949e" font-size="10">current streak: {cs} days   ·   longest streak: {ls} days   ·   best day: {bd.get("count",0)} on {bd.get("date","-")}</text>')

    parts.append("</svg>")

    out_path = os.path.abspath(OUT)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
