"""Fetch the current GitHub avatar and embed it in a circular SVG.

The avatar auto-updates whenever the update-profile-art workflow runs, so
whatever profile picture the account uses will appear here.
"""
import base64
import os

import requests

USERNAME = os.environ.get("GITHUB_USERNAME", "su7xon")
URL = f"https://github.com/{USERNAME}.png?size=460"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "avatar.svg")


def main():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    b64 = base64.b64encode(r.content).decode("ascii")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="280" height="280" viewBox="0 0 280 280">
  <defs>
    <clipPath id="avatarClip"><circle cx="140" cy="140" r="118"/></clipPath>
    <radialGradient id="avatarGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="140" cy="140" r="136" fill="url(#avatarGlow)"/>
  <circle cx="140" cy="140" r="126" fill="none" stroke="#ef4444" stroke-opacity="0.25" stroke-width="1"/>
  <image href="data:image/png;base64,{b64}" x="22" y="22" width="236" height="236" preserveAspectRatio="xMidYMid slice" clip-path="url(#avatarClip)"/>
  <circle cx="140" cy="140" r="118" fill="none" stroke="#ef4444" stroke-width="3"/>
  <circle cx="234" cy="232" r="12" fill="#0a0a0a"/>
  <circle cx="234" cy="232" r="8" fill="#22c55e"/>
</svg>
'''
    out_path = os.path.abspath(OUT)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path} ({len(r.content)} bytes avatar)")


if __name__ == "__main__":
    main()
