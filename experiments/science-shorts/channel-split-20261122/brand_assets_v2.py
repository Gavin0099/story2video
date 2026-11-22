"""Typeset the original illustrated channel artwork and export crop previews."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'artifacts/science-shorts/channel-split-20261122/brand-v2'
FONT_DIR = Path('C:/Windows/Fonts')
CREAM = '#FFF1D7'
INDIGO = '#121E3D'
APRICOT = '#FFC892'
SAFE = (508, 509, 2052, 931)  # Inward-rounded from the official minimum-size safe area.


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def centered_text(draw, y, value, typeface, color):
    bounds = draw.textbbox((1280, y), value, font=typeface, anchor='mm')
    if not (SAFE[0] <= bounds[0] < bounds[2] <= SAFE[2] and SAFE[1] <= bounds[1] < bounds[3] <= SAFE[3]):
        raise ValueError(f'Text exceeds safe crop: {value} {bounds}')
    draw.text((1280, y), value, font=typeface, fill=color, anchor='mm')
    return bounds


def circular_avatar(avatar, size):
    mask = Image.new('L', (size * 3, size * 3))
    ImageDraw.Draw(mask).ellipse((0, 0, size * 3 - 1, size * 3 - 1), fill=255)
    icon = avatar.resize((size, size), Image.Resampling.LANCZOS).convert('RGBA')
    icon.putalpha(mask.resize((size, size), Image.Resampling.LANCZOS))
    return icon


def main():
    canvas = ImageOps.fit(Image.open(OUT / 'banner-illustration.png').convert('RGB'), (2560, 1440), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(canvas)
    d.line((1238, 599, 1322, 599), fill=APRICOT, width=3)
    title_bounds = centered_text(d, 675, 'WhyNest Lab', font('georgiab.ttf', 106), CREAM)
    zh_bounds = centered_text(d, 775, '一分鐘科普', font('msjhbd.ttc', 58), APRICOT)
    tag_bounds = centered_text(d, 847, 'Everyday science, made clear.', font('segoeui.ttf', 35), CREAM)
    banner_path = OUT / 'banner.jpg'
    canvas.save(banner_path, quality=94, subsampling=0, optimize=True)
    avatar = ImageOps.fit(Image.open(OUT / 'avatar-illustration.png').convert('RGB'), (800, 800), Image.Resampling.LANCZOS)
    avatar_path = OUT / 'avatar.png'
    avatar.save(avatar_path, optimize=True)
    mobile = canvas.crop(SAFE)
    mobile_path = OUT / 'mobile-crop.jpg'
    mobile.save(mobile_path, quality=92, subsampling=0)

    board = Image.new('RGB', (1380, 1140), '#F6EDDD')
    bd = ImageDraw.Draw(board)
    bd.text((54, 28), 'WhyNest Lab', font=font('georgiab.ttf', 45), fill=INDIGO)
    bd.text((1304, 50), '科普頻道品牌預覽', font=font('msjhbd.ttc', 27), fill=INDIGO, anchor='rm')
    board.paste(canvas.resize((960, 540), Image.Resampling.LANCZOS), (54, 108))
    swatches = [('#142348', '靛藍'), ('#38BCD4', '冰藍'), ('#F57D40', '夕照橘'), (CREAM, '暖白')]
    icon = circular_avatar(avatar, 166)
    board.paste(icon, (1100, 134), icon)
    bd.text((1183, 323), '圓形頭像', font=font('msjhbd.ttc', 24), fill=INDIGO, anchor='mm')
    for i, (color, label) in enumerate(swatches):
        x = 1064 + (i % 2) * 130
        y = 370 + (i // 2) * 92
        bd.rounded_rectangle((x, y, x + 112, y + 48), radius=7, fill=color, outline='#D9CBB4')
        bd.text((x + 56, y + 69), label, font=font('msjh.ttc', 20), fill=INDIGO, anchor='mm')
    bd.text((54, 681), '手機安全區預覽', font=font('msjhbd.ttc', 28), fill=INDIGO)
    board.paste(mobile.resize((1272, 348), Image.Resampling.LANCZOS), (54, 735))
    board.save(OUT / 'preview.jpg', quality=91, subsampling=0)

    if banner_path.stat().st_size > 6_000_000 or avatar_path.stat().st_size > 2_000_000:
        raise ValueError('Export exceeds the intended file-size limit')
    files = (banner_path, avatar_path, mobile_path, OUT / 'preview.jpg')
    report = {'safe_crop': SAFE, 'text_bounds': [title_bounds, zh_bounds, tag_bounds], 'outputs': {}}
    for path in files:
        with Image.open(path) as result:
            report['outputs'][path.name] = {'size': list(result.size), 'bytes': path.stat().st_size,
                                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
