"""Draw original, editable geometric channel branding; no third-party imagery."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'artifacts/science-shorts/channel-split-20261122'
OUT.mkdir(parents=True, exist_ok=True)
TEAL, CREAM, CORAL = '#12575A', '#FFF5E6', '#F48268'


def font(size, bold=False, zh=False):
    filename = ('msjhbd.ttc' if bold else 'msjh.ttc') if zh else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype('C:/Windows/Fonts/' + filename, size)


def mark(draw, x, y, size):
    draw.ellipse((x, y, x + size, y + size), fill=CREAM)
    draw.text((x + size / 2, y + size / 2 - size * .035), '?', font=font(round(size * .75), True), fill=TEAL, anchor='mm')
    dot = size * .13
    draw.ellipse((x + size * .80, y + size * .02, x + size * .80 + dot, y + size * .02 + dot), fill=CORAL)


avatar = Image.new('RGB', (800, 800), TEAL)
mark(ImageDraw.Draw(avatar), 140, 140, 520)
avatar.save(OUT / 'avatar.png')
banner = Image.new('RGB', (2560, 1440), TEAL)
d = ImageDraw.Draw(banner)
mark(d, 550, 578, 236)
d.text((840, 584), 'WhyNest Lab', font=font(112, True), fill=CREAM)
d.text((847, 730), '一分鐘科普', font=font(55, True, True), fill=CREAM)
d.text((847, 815), 'Everyday science, made clear.', font=font(39), fill=CREAM)
# Essential branding lies within the centered 1546 x 423 device-safe area.
banner.save(OUT / 'banner.png')
preview = Image.new('RGB', (1280, 860), CREAM)
preview.paste(banner.resize((1280, 720)), (0, 0))
preview.paste(avatar.resize((112, 112)), (40, 735))
pd = ImageDraw.Draw(preview)
pd.text((180, 746), 'WhyNest Lab｜一分鐘科普', font=font(36, True, True), fill=TEAL)
pd.text((180, 801), '一個問題，懂一個原理。', font=font(26, False, True), fill=TEAL)
preview.save(OUT / 'brand-preview.png')
print(json.dumps({'status': 'READY', 'avatar': str(OUT / 'avatar.png'), 'banner': str(OUT / 'banner.png'), 'preview': str(OUT / 'brand-preview.png')}, ensure_ascii=False))
