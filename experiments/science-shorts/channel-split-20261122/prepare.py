"""Prepare separate manual channel delivery records; performs no network writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    scripts = json.loads((ROOT / 'experiments/science-shorts/batch-20261121/scripts-final.json').read_text(encoding='utf-8'))
    episodes = []
    for episode in scripts['episodes']:
        topic = episode['id']
        directory = ROOT / ('artifacts/science-shorts/ice-visual-v2' if topic == 'ice' else f'artifacts/science-shorts/sky-space-visual-v2/{topic}')
        video = directory / f'{topic}-v2-zh.mp4'
        qa = json.loads((directory / 'qa.json').read_text(encoding='utf-8'))
        report = qa['reports'][video.name]
        assert qa['status'] == 'PASS', f'{topic}: QA not PASS'
        actual = digest(video)
        assert actual == report['sha256'], f'{topic}: MP4 differs from reviewed output'
        sources = sorted({url for claim in episode['claims'] for url in claim['source_urls']})
        entries = {}
        for language, filename in [('en', 'en.srt'), ('zh-Hant', 'zh-Hant.srt')]:
            subtitle = directory / filename
            assert subtitle.is_file() and subtitle.stat().st_size > 0
            entries[language] = {'path': subtitle.relative_to(ROOT).as_posix(), 'sha256': digest(subtitle)}
        description_en = ('A short visual explanation of an everyday science question.\n'
                          'English narration with Traditional Chinese on-screen captions.\n'
                          'Illustrations and animations are explanatory schematics, not experimental footage. '
                          'Created with AI-assisted illustrations and synthetic narration.\n\nSources:\n' + '\n'.join(sources))
        description_zh = ('用圖解與動畫看懂日常科學問題。英文旁白，繁體中文字幕。\n'
                          '畫面為解說示意，並非實驗錄影；使用 AI 輔助插畫與合成旁白。\n\n參考來源：\n' + '\n'.join(sources))
        episodes.append({'episode_id': topic, 'route': 'science', 'target_channel_id': None,
                         'video_id': None, 'upload_status': 'not_uploaded', 'visibility': None,
                         'video_path': video.relative_to(ROOT).as_posix(), 'sha256': actual,
                         'bytes': video.stat().st_size, 'duration_seconds': float(report['duration']),
                         'title_en': episode['title_en'], 'title_zh_Hant': episode['title_zh'],
                         'description_en': description_en, 'description_zh_Hant': description_zh,
                         'video_language': 'en-US', 'subtitle_files': entries,
                         'audience_recommendation': 'general_audience_not_made_for_kids',
                         'audience_basis': 'Broad general-audience science explanations; not specifically directed at children.',
                         'disclosure_note': 'Review Studio synthetic-content question against actual schematic animation; description discloses AI-assisted assets and voice.',
                         'qa_path': (directory / 'qa.json').relative_to(ROOT).as_posix()})
    handoff = {'schema_version': 'manual-channel-delivery.v1', 'prepared_at': '2026-11-22',
               'status': 'ready_for_account_and_visibility_selection',
               'automatic_upload_enabled': False, 'public_release_authorized': False,
               'channels': {
                   'turtle_soup': {'display_name': 'CluePause｜謎底之前', 'handle': '@CluePause',
                                   'channel_id': 'UCG_nXXBzgg54w2zhkZ33Row',
                                   'identity_evidence': 'prior_session_record_not_reverified_this_turn',
                                   'content_promise': 'Original mysteries, fair clues, and a complete reveal.'},
                   'science': {'display_name': None, 'handle': None, 'channel_id': None,
                               'name_candidates': ['WhyNest Lab｜一分鐘科普', 'WhyPocket Lab｜一分鐘科普'],
                               'creation_status': 'not_created',
                               'description_en': 'Everyday questions, explained through clear visual science. Short illustrated explanations with English narration and Traditional Chinese captions. Start with ice, skies, and sound.',
                               'description_zh_Hant': '一個問題，懂一個原理。用插畫與動畫解說日常科學，從冰、天空與聲音開始。英文旁白，繁體中文字幕。',
                               'content_promise': 'Understand one everyday scientific mechanism per video.'}},
               'episodes': episodes}
    target = OUT / 'delivery-preflight.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing delivery record; preserve live IDs and state.')
    target.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'clips': [{'id': e['episode_id'], 'seconds': e['duration_seconds'], 'qa_hash_matches': True} for e in episodes], 'record': str(target)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
