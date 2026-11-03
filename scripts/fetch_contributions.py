"""Scrape the public contribution calendar for a GitHub user.

No token required: GitHub serves the calendar as public HTML at
https://github.com/users/<username>/contributions
"""
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "su7xon")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def parse_count(text):
    text = (text or "").strip().lower()
    m = re.search(r"(\d+)\s+contribution", text)
    if m:
        return int(m.group(1))
    if "no contribution" in text:
        return 0
    return 0


def fetch():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    tds = soup.find_all("td", attrs={"data-date": True})
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}

    days = []
    for td in tds:
        d = td.get("data-date")
        level = int(td.get("data-level", 0))
        tid = td.get("id")
        count = parse_count(tips.get(tid))
        days.append({"date": d, "level": level, "count": count})

    days.sort(key=lambda x: x["date"])

    # derived stats
    total = sum(d["count"] for d in days)
    # monthly totals
    monthly = {}
    for d in days:
        ym = d["date"][:7]
        monthly[ym] = monthly.get(ym, 0) + d["count"]

    # streaks (consecutive days with count > 0)
    day_set = {d["date"]: d["count"] for d in days}
    dates_sorted = sorted(day_set)
    longest = 0
    cur = 0
    for ds in dates_sorted:
        if day_set[ds] > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0

    # current streak ending at most recent day with data
    current = 0
    for ds in reversed(dates_sorted):
        if day_set[ds] > 0:
            current += 1
        else:
            break

    best_day = max(days, key=lambda d: d["count"]) if days else None

    payload = {
        "username": USERNAME,
        "generated": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "stats": {
            "total": total,
            "current_streak": current,
            "longest_streak": longest,
            "best_day": best_day,
            "monthly": monthly,
            "start": days[0]["date"] if days else None,
            "end": days[-1]["date"] if days else None,
        },
    }

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(days)} days to {out_path}")
    print(f"Total contributions: {total}")


if __name__ == "__main__":
    fetch()
