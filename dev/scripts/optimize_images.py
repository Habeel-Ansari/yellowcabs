import os
from PIL import Image, ImageOps
import json

SRC = r"C:\Users\habza\Documents\Yellow cabs Whitecourt\Assets"
OUT = r"C:\Users\habza\Documents\Yellow cabs Whitecourt\website\images"

THUMB_W = 640
FULL_W = 1600
HERO_W = 2400

# Skip exact duplicate
SKIP = {"IMG_9775 (1).jpeg"}

files = sorted([f for f in os.listdir(SRC) if f.lower().endswith((".jpg", ".jpeg", ".png")) and f not in SKIP])

manifest = []

def process(path, slug):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    w, h = img.size

    # Thumb
    tw = THUMB_W
    th = int(h * (tw / w))
    thumb = img.resize((tw, th), Image.LANCZOS)
    thumb.save(os.path.join(OUT, "gallery", "thumb", f"{slug}.webp"), "WEBP", quality=68, method=6)

    # Full (for lightbox) - cap width
    fw = min(FULL_W, w)
    fh = int(h * (fw / w))
    full = img.resize((fw, fh), Image.LANCZOS) if fw != w else img
    full.save(os.path.join(OUT, "gallery", "full", f"{slug}.webp"), "WEBP", quality=70, method=6)

    return {"slug": slug, "w": w, "h": h, "orientation": "landscape" if w >= h else "portrait"}

for i, fname in enumerate(files, start=1):
    slug = f"cab-{i:02d}"
    path = os.path.join(SRC, fname)
    try:
        info = process(path, slug)
        info["src"] = fname
        manifest.append(info)
        print(f"OK {fname} -> {slug} ({info['orientation']}, {info['w']}x{info['h']})")
    except Exception as e:
        print(f"FAIL {fname}: {e}")

with open(os.path.join(OUT, "gallery", "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

# Also emit as a plain JS global so gallery.html works over file:// (fetch() of
# local JSON is blocked by browsers under the file: origin).
with open(os.path.join(OUT, "gallery", "manifest.js"), "w") as f:
    f.write("window.GALLERY_ITEMS = ")
    json.dump(manifest, f)
    f.write(";\n")

print(f"\nTotal processed: {len(manifest)}")

# Hero images (curated best shots, landscape, wide crop for banners)
HERO_PICKS = {
    "home-hero": "IMG_9773.jpeg",
    "home-fleet": "83a6fc55-e7c0-489b-a4b4-786fd39ece07.jpeg",
    "about-hero": "IMG_9762.jpeg",
    "about-story": "IMG_9745.jpeg",
    "contact-hero": "IMG_9770.jpeg",
    "gallery-hero": "IMG_9730.jpeg",
}

for slug, fname in HERO_PICKS.items():
    path = os.path.join(SRC, fname)
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size
    hw = min(HERO_W, w)
    hh = int(h * (hw / w))
    hero = img.resize((hw, hh), Image.LANCZOS) if hw != w else img
    hero.save(os.path.join(OUT, "hero", f"{slug}.webp"), "WEBP", quality=72, method=6)
    print(f"HERO {fname} -> {slug} ({hw}x{hh})")
