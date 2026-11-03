"""Fetch the current GitHub avatar and build a big glitch-reveal hero SVG.

The image starts as a black-and-white glitch, then resolves to the clear
profile picture. The avatar is embedded as base64 so the SVG is self-contained.
"""
import base64
import os

import requests

USERNAME = os.environ.get("GITHUB_USERNAME", "su7xon")
URL = f"https://github.com/{USERNAME}.png?size=700"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "hero-v2.svg")

W, H = 1200, 560
IMG_X, IMG_Y, IMG_S = 60, 50, 460


def main():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    b64 = base64.b64encode(r.content).decode("ascii")
    pic = f'data:image/png;base64,{b64}'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Fira Code, ui-monospace, SFMono-Regular, Menlo, monospace">
  <style>
    @keyframes popIn {{
      0% {{ opacity: 0; transform: translateY(16px) scale(0.9); }}
      70% {{ opacity: 1; transform: translateY(-2px) scale(1.02); }}
      100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
    .letter {{ animation: popIn 0.55s cubic-bezier(.2,.8,.2,1) both; }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0a0a"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1"/>
    </pattern>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#ffffff" fill-opacity="0.10"/>
    </pattern>
    <clipPath id="frameClip"><rect x="{IMG_X}" y="{IMG_Y}" width="{IMG_S}" height="{IMG_S}" rx="18"/></clipPath>
    <clipPath id="slice1"><rect x="{IMG_X}" y="120" width="{IMG_S}" height="14"/></clipPath>
    <clipPath id="slice2"><rect x="{IMG_X}" y="250" width="{IMG_S}" height="22"/></clipPath>
    <clipPath id="slice3"><rect x="{IMG_X}" y="360" width="{IMG_S}" height="10"/></clipPath>
    <clipPath id="slice4"><rect x="{IMG_X}" y="430" width="{IMG_S}" height="18"/></clipPath>
    <filter id="mono"><feColorMatrix type="saturate" values="0"/></filter>
    <filter id="monoHigh">
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer>
        <feFuncR type="linear" slope="1.8" intercept="-0.25"/>
        <feFuncG type="linear" slope="1.8" intercept="-0.25"/>
        <feFuncB type="linear" slope="1.8" intercept="-0.25"/>
      </feComponentTransfer>
    </filter>
    <image id="pic" href="{pic}" x="{IMG_X}" y="{IMG_Y}" width="{IMG_S}" height="{IMG_S}" preserveAspectRatio="xMidYMid slice"/>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <ellipse cx="290" cy="280" rx="420" ry="300" fill="url(#glow)"/>

  <!-- clear image reveal -->
  <g clip-path="url(#frameClip)" opacity="0">
    <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.78;1" dur="2.8s" fill="freeze"/>
    <use href="#pic"/>
  </g>

  <!-- black & white glitch layers -->
  <g clip-path="url(#frameClip)">
    <g opacity="1">
      <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.78;1" dur="2.8s" fill="freeze"/>
      <use href="#pic" filter="url(#mono)">
        <animateTransform attributeName="transform" type="translate" values="0 0;-14 0;10 0;-6 2;0 0" dur="0.22s" repeatCount="12"/>
      </use>
      <use href="#pic" filter="url(#monoHigh)" opacity="0.75">
        <animateTransform attributeName="transform" type="translate" values="0 0;12 0;-8 0;5 -2;0 0" dur="0.19s" repeatCount="14"/>
      </use>
      <g clip-path="url(#slice1)">
        <use href="#pic" filter="url(#monoHigh)" opacity="0.9">
          <animateTransform attributeName="transform" type="translate" values="0 0;-26 0;18 0;-10 0;0 0" dur="0.16s" repeatCount="17"/>
        </use>
      </g>
      <g clip-path="url(#slice2)">
        <use href="#pic" filter="url(#mono)" opacity="0.9">
          <animateTransform attributeName="transform" type="translate" values="0 0;22 0;-16 0;8 0;0 0" dur="0.18s" repeatCount="15"/>
        </use>
      </g>
      <g clip-path="url(#slice3)">
        <use href="#pic" filter="url(#monoHigh)" opacity="0.8">
          <animateTransform attributeName="transform" type="translate" values="0 0;-18 0;14 0;-6 0;0 0" dur="0.14s" repeatCount="20"/>
        </use>
      </g>
      <g clip-path="url(#slice4)">
        <use href="#pic" filter="url(#mono)" opacity="0.85">
          <animateTransform attributeName="transform" type="translate" values="0 0;16 0;-12 0;6 0;0 0" dur="0.2s" repeatCount="14"/>
        </use>
      </g>
      <rect x="{IMG_X}" y="{IMG_Y}" width="{IMG_S}" height="{IMG_S}" fill="url(#scan)" opacity="0.5"/>
    </g>
  </g>

  <!-- white glitch flashes -->
  <rect x="{IMG_X}" y="{IMG_Y}" width="{IMG_S}" height="{IMG_S}" rx="18" fill="#ffffff" opacity="0">
    <animate attributeName="opacity" values="0;0.35;0;0.18;0;0.28;0" keyTimes="0;0.06;0.12;0.24;0.3;0.5;0.62" dur="2.4s" fill="freeze"/>
  </rect>

  <!-- frame -->
  <rect x="{IMG_X}" y="{IMG_Y}" width="{IMG_S}" height="{IMG_S}" rx="18" fill="none" stroke="#ef4444" stroke-width="2"/>
  <rect x="{IMG_X-6}" y="{IMG_Y-6}" width="{IMG_S+12}" height="{IMG_S+12}" rx="23" fill="none" stroke="#ef4444" stroke-opacity="0.22"/>

  <!-- right side text -->
  <text x="580" y="130" fill="#6b7280" font-size="13">~/su7xon $ whoami</text>
  <g fill="#f3f4f6" font-size="64" font-weight="700" text-anchor="middle">
    <text class="letter" style="animation-delay:2.55s" x="600" y="205">s</text>
    <text class="letter" style="animation-delay:2.62s" x="640" y="205">u</text>
    <text class="letter" style="animation-delay:2.69s" x="680" y="205" fill="#ef4444">7</text>
    <text class="letter" style="animation-delay:2.76s" x="720" y="205">x</text>
    <text class="letter" style="animation-delay:2.83s" x="760" y="205">o</text>
    <text class="letter" style="animation-delay:2.90s" x="800" y="205">n</text>
    <rect class="cursor" x="826" y="160" width="12" height="52" fill="#ef4444"/>
  </g>
  <text x="580" y="248" fill="#ef4444" font-size="17" font-weight="600">Developer · Builder · AI Explorer</text>
  <text x="580" y="280" fill="#9ca3af" font-size="14">AI can't replace thinking — it can only replace typing.</text>

  <rect x="580" y="310" width="540" height="1" fill="#ef4444" fill-opacity="0.35"/>

  <g font-size="13" fill="#9ca3af">
    <text x="580" y="344"><tspan fill="#ef4444">status   </tspan> building &amp; shipping</text>
    <text x="580" y="372"><tspan fill="#ef4444">focus    </tspan> full-stack, AI &amp; automation</text>
    <text x="580" y="400"><tspan fill="#ef4444">location </tspan> Haldwani, India</text>
    <text x="580" y="428"><tspan fill="#ef4444">github   </tspan> github.com/su7xon</text>
  </g>

  <g transform="translate(580, 470)">
    <rect width="186" height="30" rx="15" fill="#111827" stroke="#ef4444" stroke-opacity="0.6"/>
    <circle cx="18" cy="15" r="4" fill="#22c55e"/>
    <text x="32" y="20" fill="#d1d5db" font-size="12">open to collaborate</text>
  </g>

  <!-- roaming dot critter + trail -->
  <g opacity="0.55">
    <circle r="2.5" fill="#ef4444">
      <animateMotion dur="16s" repeatCount="indefinite" begin="-0.45s" path="M 80 528 C 220 506 320 548 460 528 S 700 506 840 528 S 1040 548 1130 522"/>
    </circle>
    <circle r="2" fill="#ef4444">
      <animateMotion dur="16s" repeatCount="indefinite" begin="-0.9s" path="M 80 528 C 220 506 320 548 460 528 S 700 506 840 528 S 1040 548 1130 522"/>
    </circle>
    <circle r="1.6" fill="#ef4444">
      <animateMotion dur="16s" repeatCount="indefinite" begin="-1.35s" path="M 80 528 C 220 506 320 548 460 528 S 700 506 840 528 S 1040 548 1130 522"/>
    </circle>
  </g>

  <g>
    <animateMotion dur="16s" repeatCount="indefinite" path="M 80 528 C 220 506 320 548 460 528 S 700 506 840 528 S 1040 548 1130 522"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="0.7s" repeatCount="indefinite"/>
      <ellipse cx="0" cy="15" rx="12" ry="3.5" fill="#000000" opacity="0.45"/>
      <circle cx="0" cy="-16" r="2.5" fill="#f87171"/>
      <rect x="-17" y="-10" width="34" height="4" rx="2" fill="#ef4444"/>
      <rect x="-15" y="-10" width="30" height="24" rx="10" fill="#ef4444"/>
      <circle cx="-6" cy="-1" r="2.6" fill="#0a0a0a"/>
      <circle cx="6" cy="-1" r="2.6" fill="#0a0a0a"/>
      <circle cx="-6" cy="-1.5" r="1" fill="#ffffff"/>
      <circle cx="6" cy="-1.5" r="1" fill="#ffffff"/>
      <rect x="-7" y="14" width="5" height="5" rx="2" fill="#ef4444"/>
      <rect x="2" y="14" width="5" height="5" rx="2" fill="#ef4444"/>
    </g>
  </g>
</svg>
'''
    out_path = os.path.abspath(OUT)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path} ({len(r.content)} bytes avatar)")


if __name__ == "__main__":
    main()
