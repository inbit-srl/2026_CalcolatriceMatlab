from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent
BG = (30, 30, 30)      # matches app background
FG = (78, 201, 176)    # teal accent (matches --prompt)
ACCENT = (220, 220, 170)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def pick_font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def make_icon(size, path, maskable=False):
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)

    # rounded-square accent "badge" (skip on maskable so safe area isn't clipped)
    if not maskable:
        pad = size // 12
        d.rounded_rectangle(
            [pad, pad, size - pad, size - pad],
            radius=size // 8,
            outline=FG,
            width=max(2, size // 48),
        )

    # draw π — shrink inner area on maskable so it stays inside the safe circle (~80%)
    inner = int(size * 0.62) if maskable else int(size * 0.72)
    font = pick_font(inner)
    text = "π"  # π
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    d.text((x, y), text, fill=ACCENT, font=font)

    img.save(path, "PNG", optimize=True)
    print(f"wrote {path}")

make_icon(192, OUT / "icon-192.png")
make_icon(512, OUT / "icon-512.png")
make_icon(512, OUT / "icon-maskable-512.png", maskable=True)
