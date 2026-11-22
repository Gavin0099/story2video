"""Prepare one byte-verified YouTube Studio package after independent film review."""
import argparse
import json
from pathlib import Path
import re
import shutil

from render import ARTIFACTS, ROOT, load, save, sha


CHANNEL = 'UCJpx-XFeS91Vd26QokWAWOw'


def verified_path(path, entry):
    return path.is_file() and path.stat().st_size == entry['size'] and sha(path) == entry['sha256']


def make_package(dest, script, review):
    qa_path = dest / 'qa.json'
    manifest_path = dest / 'inputs.json'
    qa, manifest, review_data = map(load, (qa_path, manifest_path, review))
    episode = next(ep for ep in load(script)['episodes'] if ep['id'] == dest.name)
    expected = {
        'id': episode['id'],
        'status': 'PASS',
        'mp4_sha256': qa['mp4']['sha256'],
        'qa_sha256': sha(qa_path),
        'critical_defects': [],
    }
    if any(review_data.get(key) != value for key, value in expected.items()):
        raise ValueError('Independent encoded-video review is absent, stale or failing')
    if (qa['id'] != episode['id'] or qa['status'] != 'PASS' or
            qa['inputs_sha256'] != sha(manifest_path) or not qa['english_graphics'] or qa['burned_captions'] or
            qa['scores'] != manifest['scores'] or len(qa['scores']) != 2 or min(qa['scores']) < 85 or
            not verified_path(dest / 'master.mp4', qa['mp4']) or
            not any((ROOT / row['path']).resolve() == script and verified_path(script,row)
                    for row in manifest['inputs'])):
        raise ValueError('Release package does not match approved inputs or media')
    tracks = {}
    for lang in ('en','zh-Hant'):
        path = dest / f'{lang}.srt'
        digest = sha(path)
        if digest != qa['subtitle_hashes'][lang]:
            raise ValueError(f'Changed {lang} captions')
        tracks[lang] = {'path':str(path), 'sha256':digest}
    slug = episode['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError('Unsafe upload filename')
    delivery = dest / f'whynest-{episode["id"]}-{slug}.mp4'
    shutil.copyfile(dest / 'master.mp4', delivery)
    if not verified_path(delivery, qa['mp4']):
        raise ValueError('Upload copy differs from the inspected master')
    citations = '\n'.join(f'{ref["publisher"]}: {ref["url"]}' for ref in episode['sources'])
    if not 2 <= len(episode['sources']):
        raise ValueError('Missing public source references')
    disclosure_en = 'English narration and explanatory animation with AI-assisted production. Captions: English and Traditional Chinese.'
    disclosure_zh = '製作使用 AI 輔助，提供英語旁白、科學圖解與可切換的英文、繁體中文字幕。'
    entry = {
        'episode_id':episode['id'], 'target_channel_id':CHANNEL, 'video_path':str(delivery),
        'sha256':qa['mp4']['sha256'], 'size':qa['mp4']['size'], 'scores':qa['scores'],
        'title_en':episode['title_en'], 'title_zh_Hant':episode['title_zh'],
        'description_en':f'{episode["description_en"]}\n\n{disclosure_en}\n\nSources\n{citations}',
        'description_zh_Hant':f'{episode["description_zh"]}\n\n{disclosure_zh}\n\n資料來源\n{citations}',
        'subtitle_files':tracks, 'qa_sha256':sha(qa_path), 'review_path':str(review), 'review_sha256':sha(review),
        'source_language':'en-US', 'ai_disclosure':True, 'made_for_kids':False,
        'publication_authorization':'Owner 2026-11-22 WhyNest Lab 20 public Shorts',
    }
    if max(len(entry[k]) for k in ('title_en','title_zh_Hant')) > 100:
        raise ValueError('YouTube title length exceeds 100 characters')
    save(dest / 'release-package.json', entry)
    return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', choices=[f'{i:02}' for i in range(4,21)])
    parser.add_argument('--script', required=True, type=Path)
    parser.add_argument('--review', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(make_package(ARTIFACTS / args.id, args.script.resolve(strict=True),
                                  args.review.resolve(strict=True)), ensure_ascii=True))
