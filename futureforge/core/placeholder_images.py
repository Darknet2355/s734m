"""
Generates simple, clearly-labeled placeholder images for demo/sample data.
These make it obvious in the admin dashboard which images are sample content
that should be replaced with real photos/logos.
"""
import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

PALETTE = [
    (10, 20, 66), (14, 34, 102), (26, 92, 255), (5, 11, 31), (0, 130, 158),
]


def _get_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except Exception:
        return ImageFont.load_default()


def make_placeholder_image(label, size=(800, 500)):
    """Return a ContentFile of a PNG placeholder image labeled with `label`."""
    bg = random.choice(PALETTE)
    img = Image.new("RGB", size, color=bg)
    draw = ImageDraw.Draw(img)

    # Subtle dot grid decoration (circuit-inspired)
    for x in range(0, size[0], 28):
        for y in range(0, size[1], 28):
            draw.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255, 40))

    title_font = _get_font(34)
    sub_font = _get_font(18)

    draw.text((40, size[1] // 2 - 46), "FutureForge Labs", font=title_font, fill=(0, 217, 255))

    # Wrap label text manually to fit width
    words = label.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) > 34:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)

    y = size[1] // 2
    for line in lines[:2]:
        draw.text((40, y), line, font=sub_font, fill=(255, 255, 255))
        y += 26

    draw.text((40, size[1] - 40), "SAMPLE / DEMO IMAGE — replace from dashboard", font=_get_font(13), fill=(255, 157, 46))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read())
