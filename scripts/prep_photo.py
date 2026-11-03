"""Prep a photo for ASCII conversion: remove bg, CLAHE contrast, composite on white."""
import sys
import os

try:
    from rembg import remove
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print("Missing portrait dependency:", e)
    print("Install with: pip install pillow numpy opencv-python rembg")
    sys.exit(1)

OUT = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <photo.jpg>")
        sys.exit(1)
    src = sys.argv[1]
    # remove background
    with open(src, "rb") as f:
        data = f.read()
    no_bg = remove(data)
    img = Image.open(__import__("io").BytesIO(no_bg)).convert("RGBA")

    # composite onto white
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    gray = bg.convert("L")

    # CLAHE via opencv
    arr = np.array(gray)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    arr = clahe.apply(arr)
    out = Image.fromarray(arr)
    out.save(os.path.abspath(OUT))
    print(f"Wrote {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
