"""Turn the PC wallpaper video into a circular, spinning GIF.

Creates:
  assets/pc-wallpaper-spin.gif  (looping, circular crop, rotating, red HUD ring)
"""
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "assets", "pc-wallpaper.mp4")
OUT = os.path.join(ROOT, "assets", "pc-wallpaper-spin.gif")

CANVAS = 540          # final square canvas
DISC = 480            # inner video disc diameter
OFFSET = (CANVAS - DISC) // 2
FPS = 10
LOOP_S = 8            # seconds; matches source length and one full rotation
RED = (239, 68, 68)


def ffmpeg_exe():
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def make_mask(path):
    img = Image.new("L", (DISC, DISC), 0)
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, DISC - 1, DISC - 1), fill=255)
    img.save(path)


def make_ring(path):
    img = Image.new("RGBA", (DISC, DISC), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # soft outer glow
    for i, alpha in ((14, 18), (10, 30), (7, 45), (5, 65)):
        draw.ellipse(
            (i, i, DISC - 1 - i, DISC - 1 - i),
            outline=RED + (alpha,),
            width=2,
        )
    # crisp main ring
    draw.ellipse((1, 1, DISC - 3, DISC - 3), outline=RED + (255,), width=3)
    # thin inner accent
    draw.ellipse((12, 12, DISC - 13, DISC - 13), outline=RED + (70,), width=1)
    img.save(path)


def main():
    if not os.path.exists(SRC):
        raise SystemExit(f"missing source video: {SRC}")

    tmp = tempfile.mkdtemp(prefix="spin-")
    mask = os.path.join(tmp, "mask.png")
    ring = os.path.join(tmp, "ring.png")
    make_mask(mask)
    make_ring(ring)

    vf = (
        f"[0:v]fps={FPS},"
        f"scale={DISC}:{DISC}:force_original_aspect_ratio=increase,"
        f"crop={DISC}:{DISC},"
        f"rotate=2*PI*t/{LOOP_S}:ow=iw:oh=ih:c=none,"
        f"format=rgba[rot];"
        f"[1:v]format=gray[mask];"
        f"[rot][mask]alphamerge[disc];"
        f"color=c=0x0a0a0a:s={CANVAS}x{CANVAS}:r={FPS}:d={LOOP_S}[bg];"
        f"[bg][disc]overlay={OFFSET}:{OFFSET}:shortest=1[v1];"
        f"[v1][2:v]overlay={OFFSET}:{OFFSET}:shortest=1[full];"
        f"[full]split[s0][s1];"
        f"[s0]palettegen=max_colors=64:stats_mode=diff[p];"
        f"[s1][p]paletteuse=dither=none"
    )

    cmd = [
        ffmpeg_exe(), "-y",
        "-i", SRC,
        "-loop", "1", "-t", str(LOOP_S), "-i", mask,
        "-loop", "1", "-t", str(LOOP_S), "-i", ring,
        "-filter_complex", vf,
        "-loop", "0",
        "-an",
        OUT,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Wrote {OUT} ({os.path.getsize(OUT) / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
