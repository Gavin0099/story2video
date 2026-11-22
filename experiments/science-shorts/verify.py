"""Independent, offline engineering acceptance for the isolated science pilot.

Use the existing render venv; no downloads, providers, publishing, or PATH lookup.
Preflight exercises render.main itself in disposable batches. Media QA reads the
encoded MP4s, not the renderer's preview PNGs. This is not human/market approval.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DEFAULT_BATCH = HERE / 'batch-20261121'
DEFAULT_OUTPUT = ROOT / 'artifacts/science-shorts/batch-20261121'
DEFAULT_TOOLS = ROOT / 'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
DEFAULT_MODELS = ROOT / 'artifacts/73h-episode02/models'
MANIFEST = ROOT / 'experiments/episode-02-73h/render-manifest.json'
RUBRIC = dict(hook=15, clarity=25, causal_retelling=25, visual_plan=20,
              pacing=10, natural_language=5)
EPISODES = {'ice', 'sky', 'space'}
ENV = {k: v for k, v in os.environ.items()
       if k.upper() in {'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP'}}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_sha():
    """Read local HEAD without launching an ambient Git executable."""
    gitdir = ROOT / '.git'
    if not gitdir.is_dir():
        return 'UNVERIFIED: .git is not a directory'
    value = (gitdir / 'HEAD').read_text(encoding='ascii').strip()
    if value.startswith('ref: '):
        ref = value[5:]
        target = (gitdir / ref).resolve()
        require(target.is_relative_to(gitdir.resolve()), 'Git ref escapes .git')
        if target.is_file():
            value = target.read_text(encoding='ascii').strip()
        else:
            packed = (gitdir / 'packed-refs').read_text(encoding='ascii')
            value = next(line.split()[0] for line in packed.splitlines()
                         if not line.startswith(('#', '^')) and line.endswith(' ' + ref))
    require(bool(re.fullmatch(r'[0-9a-f]{40}', value)), 'Invalid local Git HEAD')
    return value


def publisher_key(value):
    """NASA pages count once; normalize institution aliases, not page titles."""
    cleaned = re.sub(r'[^a-z0-9]', '', value.casefold())
    if cleaned.startswith('nasa'):
        return 'nasa'
    if cleaned.startswith(('noaa', 'nationalweatherservice')):
        return 'noaa'
    if cleaned.startswith(('esa', 'europeanspaceagency')):
        return 'esa'
    return cleaned


def verify_inputs(batch, renderer):
    policy = load(batch / 'gate-policy.json')
    scripts = load(batch / 'scripts-final.json')
    original = load(batch / 'scripts-v1.json')
    gate = load(batch / 'editorial-gate.json')
    audit = load(batch / 'reviews/fact-visual-v1.json')
    renderer.validate_gate(batch / 'scripts-final.json', gate, batch / 'reviews')
    require(policy['rubric'] == RUBRIC and policy['readers'] == 2
            and policy['minimum_score_each_reader'] == 85, 'Unexpected gate policy')
    require(scripts['parent_sha256'] == sha(batch / 'scripts-v1.json'), 'Parent hash mismatch')
    for field, path in [('script_sha256', batch / 'scripts-final.json'),
                        ('renderer_sha256', HERE / 'render.py'),
                        ('source_cards_sha256', batch / 'source-cards.json'),
                        ('gate_policy_sha256', batch / 'gate-policy.json')]:
        require(audit[field] == sha(path), f'Audit {field} mismatch')
    require(gate['reviewed_original_sha256'] == sha(batch / 'scripts-v1.json'),
            'Gate reviewed original hash mismatch')
    require(gate['renderer_sha256'] == sha(HERE / 'render.py'), 'Gate renderer hash mismatch')
    required_files = {'fact-visual-v1.json', 'reader-a-v1.json', 'reader-b-v1.json',
                      'reader-a-protocol.md', 'reader-b-protocol.md'}
    names = [item['path'] for item in gate['review_files']]
    require(len(names) == len(set(names)) and required_files <= set(names),
            'Missing/duplicate review evidence')
    for item in gate['review_files']:
        target = (batch / 'reviews' / item['path']).resolve(strict=True)
        require(target.is_relative_to((batch / 'reviews').resolve()), 'Review path escapes batch')
        require(sha(target) == item['sha256'], 'Review hash mismatch')
    final_by_id = {episode['id']: episode for episode in scripts['episodes']}
    original_by_id = {episode['id']: episode for episode in original['episodes']}
    require(set(final_by_id) == EPISODES and len(scripts['episodes']) == 3,
            'Unexpected episode coverage')
    require(set(original_by_id) == EPISODES, 'Unexpected original coverage')
    sources = load(batch / 'source-cards.json')['sources']
    source_by_url = {row['url']: row for row in sources}
    require(len(source_by_url) == len(sources), 'Duplicate source URL')
    access = {row['url']: row for row in audit['source_access']}
    readers = [load(batch / f'reviews/reader-{name}-v1.json') for name in ('a', 'b')]
    result = []
    for episode_id, episode in final_by_id.items():
        prior = original_by_id[episode_id]
        public_cues = lambda cues: [{key: value for key, value in cue.items() if key != 'pause'}
                                    for cue in cues]
        require(public_cues(episode['cues']) == public_cues(prior['cues']),
                f'{episode_id}: public cues changed')
        require(episode['visual_constraints'] == prior['visual_constraints'],
                f'{episode_id}: visual constraints changed')
        claims = []
        for claim in episode['claims']:
            publishers = set()
            for url in claim['source_urls']:
                require(url in source_by_url, f'Unknown source {url}')
                require(url in access and access[url]['result'] == 'SUCCESS',
                        f'Claim relies on unverified source {url}')
                key = publisher_key(source_by_url[url]['publisher'])
                require(key == publisher_key(access[url]['publisher']), 'Publisher identity mismatch')
                publishers.add(key)
            require(len(publishers) >= 2, f'{episode_id}.{claim["id"]}: independent publishers missing')
            claims.append({'id': claim['id'], 'publishers': sorted(publishers)})
        totals = []
        for reader in readers:
            rows = [row for row in reader if row['id'].lower() == episode_id]
            require(len(rows) == 1, 'Reader episode missing/duplicated')
            row = rows[0]
            require(set(row['scores']) == set(RUBRIC), 'Rubric fields differ')
            require(all(type(value) is int and 0 <= value <= RUBRIC[key]
                        for key, value in row['scores'].items()), 'Invalid score range/type')
            total = sum(row['scores'].values())
            require(total == row['total'] and total >= 85 and not row['critical_defects'],
                    'Reader score/defect gate failed')
            totals.append(total)
        gate_row = next(row for row in gate['episodes'] if row['id'] == episode_id)
        require(gate_row['scores'] == totals, 'Gate score does not match recomputation')
        result.append({'id': episode_id, 'scores': totals, 'claims': claims,
                       'public_cues_unchanged': True, 'visual_constraints_unchanged': True,
                       'timing_only_changes': [{'cue': index, 'before_pause': old.get('pause'),
                                                'after_pause': new.get('pause')}
                                               for index, (old, new) in enumerate(zip(prior['cues'], episode['cues']), 1)
                                               if old.get('pause') != new.get('pause')]})
    return {'status': 'PASS', 'episodes': result,
            'input_sha256': {name: sha(batch / name) for name in
                             ('scripts-v1.json', 'scripts-final.json', 'source-cards.json',
                              'gate-policy.json', 'editorial-gate.json')},
            'renderer_sha256': sha(HERE / 'render.py')}


class UnexpectedBoundary(RuntimeError):
    pass


def negative_tests(batch, tools, models, renderer):
    """Exercise the real argparse/main path; never run TTS or a child process."""
    cases = [
        ('stale_script', 'Script changed'),
        ('rewritten_gate_score', 'Gate score differs'),
        ('rewritten_reader_score', 'Gate score differs'),
        ('empty_episode_gate', 'Gate does not cover'),
        ('empty_review_files', 'Independent review evidence missing'),
        ('audit_renderer_hash_mismatch', 'Renderer changed'),
        ('audit_critical_visual', 'Independent scientific audit not passed'),
        ('bad_ffmpeg_size', 'File differs from the render manifest'),
        ('bad_ffmpeg_sha256', 'File differs from the render manifest'),
        ('bad_ffprobe_sha256', 'File differs from the render manifest'),
    ]
    results = []
    manifest = load(MANIFEST)
    # Same volume as pinned binaries: unchanged positive controls use hard links.
    with tempfile.TemporaryDirectory(prefix='science-acceptance-', dir=ROOT / 'artifacts') as temporary:
        base = Path(temporary)
        for case, expected in cases:
            current = base / case / 'batch'
            (current / 'reviews').mkdir(parents=True)
            for path in batch.glob('*.json'):
                shutil.copyfile(path, current / path.name)
            for path in (batch / 'reviews').iterdir():
                if path.is_file():
                    shutil.copyfile(path, current / 'reviews' / path.name)
            gate = load(current / 'editorial-gate.json')
            audit = load(current / 'reviews/fact-visual-v1.json')
            if case == 'stale_script':
                script = load(current / 'scripts-final.json')
                script['episodes'][0]['cues'][0]['en'] += ' Changed.'
                save(current / 'scripts-final.json', script)
            elif case == 'rewritten_gate_score':
                gate['episodes'][0]['scores'][0] += 1
            elif case == 'rewritten_reader_score':
                path = current / 'reviews/reader-a-v1.json'
                reader = load(path)
                reader[0]['scores']['hook'] -= 1
                save(path, reader)
            elif case == 'empty_episode_gate':
                gate['episodes'] = []
            elif case == 'empty_review_files':
                gate['review_files'] = []
            elif case == 'audit_renderer_hash_mismatch':
                audit['renderer_sha256'] = '0' * 64
            elif case == 'audit_critical_visual':
                audit['critical_defects'] = ['Injected critical scientific visual defect']
            save(current / 'reviews/fact-visual-v1.json', audit)
            # Rebind the changed receipt so rejection reaches the targeted check.
            for item in gate['review_files']:
                item['sha256'] = sha(current / 'reviews' / item['path'])
            save(current / 'editorial-gate.json', gate)
            selected_tools = tools
            if case.startswith('bad_'):
                selected_tools = base / case / 'tools'
                selected_tools.mkdir()
                bad_name = 'ffprobe' if case.startswith('bad_ffprobe') else 'ffmpeg'
                for name in ('ffmpeg', 'ffprobe'):
                    path = selected_tools / (name + '.exe')
                    if name != bad_name:
                        os.link(tools / (name + '.exe'), path)
                    else:
                        with path.open('wb') as handle:
                            handle.write(b'REJECT ME')
                            if not case.endswith('_size'):
                                handle.truncate(manifest[name]['size'])
            output = base / case / 'output-must-not-exist'
            argv = ['render.py', '--batch', str(current), '--output', str(output),
                    '--tools', str(selected_tools), '--models', str(models)]
            # No child launcher can run even if a regression incorrectly passes.
            with patch.object(sys, 'argv', argv), \
                 patch.object(renderer, 'synthesize', side_effect=UnexpectedBoundary('TTS reached')) as tts, \
                 patch.object(renderer, 'painter', side_effect=UnexpectedBoundary('Painter reached')) as paint, \
                 patch.object(subprocess, 'Popen', side_effect=UnexpectedBoundary('Popen reached')) as popen, \
                 patch.object(subprocess, 'run', side_effect=UnexpectedBoundary('run reached')) as run, \
                 patch.object(shutil, 'which', side_effect=UnexpectedBoundary('PATH fallback reached')) as which, \
                 patch.dict(os.environ, {'PATH': str(tools), 'PATHEXT': '.EXE;.CMD'}):
                rejected = None
                try:
                    renderer.main()
                except ValueError as error:
                    rejected = str(error)
                require(rejected is not None and expected in rejected,
                        f'{case}: wrong/no rejection: {rejected}')
                require(not output.exists(), f'{case}: output root created')
                calls = {'tts': tts.call_count, 'painter': paint.call_count,
                         'Popen': popen.call_count, 'run': run.call_count,
                         'PATH_lookup': which.call_count}
                require(not any(calls.values()), f'{case}: side-effect boundary reached {calls}')
            results.append({'case': case, 'status': 'PASS', 'rejection': rejected,
                            'calls': calls, 'output_root_exists': False,
                            'entrypoint': 'render.main with real argparse/sys.argv'})
        # A positive control proves the real main reaches the next boundary when
        # the original approvals, binaries and local models are all intact.
        output = base / 'positive-output-must-not-exist'
        argv = ['render.py', '--batch', str(batch), '--output', str(output),
                '--tools', str(tools), '--models', str(models)]
        with patch.object(sys, 'argv', argv), \
             patch.object(renderer, 'painter', side_effect=UnexpectedBoundary('positive painter stop')) as paint, \
             patch.object(renderer, 'synthesize', side_effect=UnexpectedBoundary('unexpected TTS')) as tts, \
             patch.object(subprocess, 'Popen', side_effect=UnexpectedBoundary('unexpected Popen')) as popen:
            stopped = False
            try:
                renderer.main()
            except UnexpectedBoundary as error:
                require(str(error) == 'positive painter stop', 'Positive control reached wrong boundary')
                stopped = True
            require(stopped and paint.call_count == 1 and not tts.call_count
                    and not popen.call_count and not output.exists(), 'Positive main control failed')
        results.append({'case': 'valid_inputs_reach_pre_output_painter', 'status': 'PASS',
                        'painter_calls': 1, 'tts_calls': 0, 'Popen_calls': 0,
                        'output_root_exists': False})
    return results


class BoundTools:
    def __init__(self, directory, output):
        self.bindings = load(MANIFEST)
        self.helper = module_at('science_qa_episode02', ROOT / 'experiments/episode-02-73h/render.py')
        self.paths = {name: (directory / (name + '.exe')).resolve(strict=True)
                      for name in ('ffmpeg', 'ffprobe')}
        self.commands = []
        self.output = output
        # Bind both before creating evidence directories or launching anything.
        for name, path in self.paths.items():
            self.helper.verify_file(path, **self.bindings[name])

    def run(self, name, args):
        path = self.paths[name]
        self.helper.verify_file(path, **self.bindings[name])
        argv = [str(path), *map(str, args)]
        process = subprocess.run(argv, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                 capture_output=True, encoding='utf-8', errors='strict',
                                 timeout=300, check=False)
        record = {'argv': argv, 'returncode': process.returncode,
                  'stdout': process.stdout, 'stderr': process.stderr}
        self.commands.append(record)
        require(process.returncode == 0, f'{name} failed: {process.stderr[-1500:]}')
        return process


def compact_text(value):
    return re.sub(r'\s+', '', value)


def parse_srt(value):
    value = value.lstrip('\ufeff').replace('\r\n', '\n').strip()
    result = []
    for block in re.split(r'\n\s*\n', value):
        lines = block.splitlines()
        require(len(lines) >= 3 and lines[0].isdigit(), 'Malformed SRT block')
        match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> '
                             r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
        require(match is not None, 'Malformed SRT time')
        values = list(map(int, match.groups()))
        times = [(values[i] * 3600 + values[i + 1] * 60 + values[i + 2]) * 1000
                 + values[i + 3] for i in (0, 4)]
        require(all(0 <= values[i] < 60 for i in (1, 2, 5, 6)), 'Invalid SRT clock')
        result.append({'index': int(lines[0]), 'start_ms': times[0], 'end_ms': times[1],
                       'text': '\n'.join(lines[2:])})
    return result


def verify_subtitles(rows, cues, language, duration):
    require(len(rows) == len(cues), f'{language}: subtitle count differs')
    prior_end = 0
    for index, (row, cue) in enumerate(zip(rows, cues), 1):
        require(row['index'] == index, 'Subtitle index differs')
        require(0 <= prior_end <= row['start_ms'] < row['end_ms'] <= duration * 1000 + 40,
                'Subtitle overlap/out-of-range')
        require(abs(row['start_ms'] - round(cue['start'] * 1000 / 30)) <= 1
                and abs(row['end_ms'] - round(cue['end'] * 1000 / 30)) <= 1,
                'Subtitle timing differs from timeline')
        require(compact_text(row['text']) == compact_text(cue[language]),
                'Subtitle semantics differ from reviewed cue')
        prior_end = row['end_ms']


def verify_ass(path, rows):
    events = [line.split(',', 9) for line in path.read_text(encoding='utf-8').splitlines()
              if line.startswith('Dialogue: ')]
    require(len(events) == len(rows), 'Burn-caption source count differs')
    def clock(value):
        hours, minutes, seconds = map(float, value.split(':'))
        return (hours * 3600 + minutes * 60 + seconds) * 1000
    for event, row in zip(events, rows):
        text = re.sub(r'\{[^}]*\}', '', event[9]).replace(r'\N', '\n')
        require(compact_text(text) == compact_text(row['text']), 'ASS/SRT text differs')
        require(abs(clock(event[1]) - row['start_ms']) <= 6
                and abs(clock(event[2]) - row['end_ms']) <= 6, 'ASS/SRT time differs')


def extract_frames(path, timeline, output, tools):
    """Decode MP4 pixels; Pillow only assembles/resizes the resulting images."""
    from PIL import Image
    frames = output / 'qa-evidence' / path.parent.name / path.stem
    frames.mkdir(parents=True, exist_ok=True)
    requested = [(f'cue-{index:02d}', (cue['start'] + cue['end']) // 2)
                 for index, cue in enumerate(timeline, 1)]
    requested += [('first-frame', 0), ('last-frame', timeline[-1]['end'] - 1)]
    if path.parent.name == 'sky':
        cue = next((row for row in timeline if row.get('scene') == 'sunset_mechanism'),
                   timeline[min(6, len(timeline) - 1)])
        # Frozen batch: frames 1050/1056 (35.0/35.2 s), clear of modulo resets.
        first = max(cue['start'], min(cue['end'] - 7, cue['start'] + 41))
        requested += [('sunset-pulse-a', first), ('sunset-pulse-b', min(cue['end'] - 1, first + 6))]
    indices = sorted({frame for _, frame in requested})
    selection = '+'.join(f'eq(n\\,{index})' for index in indices)
    tools.run('ffmpeg', ['-hide_banner', '-nostdin', '-v', 'error', '-y', '-i', path,
                         '-map', '0:v:0', '-vf', 'select=' + selection, '-fps_mode', 'vfr',
                         '-frames:v', len(indices), '-start_number', '1',
                         frames / 'decoded-%03d.png'])
    by_number = {frame: frames / f'decoded-{index:03d}.png'
                 for index, frame in enumerate(indices, 1)}
    sheet = Image.new('RGB', (270 * 5, 480 * math.ceil(len(timeline) / 5)), '#101d2b')
    evidence = []
    for name, frame_number in requested:
        image_path = frames / (name + '.png')
        shutil.copyfile(by_number[frame_number], image_path)
        with Image.open(image_path) as picture:
            require(picture.size == (1080, 1920), 'Extracted frame dimensions differ')
            if name.startswith('cue-'):
                index = int(name[4:]) - 1
                sheet.paste(picture.resize((270, 480)), ((index % 5) * 270, (index // 5) * 480))
        evidence.append({'name': name, 'frame': frame_number, 'seconds': frame_number / 30,
                         'path': str(image_path.relative_to(output)), 'sha256': sha(image_path)})
    contact = frames / 'actual-mp4-contact.png'
    sheet.save(contact)
    result = {'source_mp4': str(path), 'source_mp4_sha256': sha(path),
              'contact_sheet': str(contact.relative_to(output)),
              'contact_sheet_sha256': sha(contact), 'actual_mp4_frames': evidence,
              'method': 'Pinned FFmpeg decodes exact zero-based MP4 frame numbers; Pillow only assembles decoded PNGs'}
    save(frames / 'frames.json', result)
    return result


def verify_media_episode(episode, batch, output, tools):
    folder = output / episode['id']
    timeline_record = load(folder / 'timeline.json')
    timeline = timeline_record['cues']
    episode_hash = hashlib.sha256(json.dumps(episode, sort_keys=True,
                                             ensure_ascii=False).encode()).hexdigest()
    require(timeline_record['episode_sha256'] == episode_hash, 'Timeline input hash differs')
    require(timeline_record['audio_sha256'] == sha(folder / 'narration.wav'),
            'Narration hash differs')
    require(len(timeline) == len(episode['cues']), 'Timeline cue count differs')
    prior_end = 0
    for timed, original in zip(timeline, episode['cues']):
        require(all(timed[key] == value for key, value in original.items()),
                'Timeline public cue differs')
        require(all(type(timed[key]) is int for key in ('start', 'speech_end', 'end')),
                'Nonintegral frame timing')
        require(prior_end <= timed['start'] < timed['speech_end'] <= timed['end'],
                'Invalid timeline cue bounds')
        prior_end = timed['end']
    duration = timeline[-1]['end'] / 30
    require(45 <= duration <= 60, 'Timeline duration outside accepted range')
    provenance = load(folder / 'provenance.json')
    require(provenance['script_sha256'] == sha(batch / 'scripts-final.json')
            and provenance['renderer_sha256'] == sha(HERE / 'render.py')
            and provenance['editorial_gate_sha256'] == sha(batch / 'editorial-gate.json'),
            'Provenance input hashes differ')
    subtitles = {}
    for language, filename in [('en', 'en.srt'), ('zh', 'zh-Hant.srt')]:
        rows = parse_srt((folder / filename).read_text(encoding='utf-8'))
        verify_subtitles(rows, timeline, language, duration)
        verify_ass(folder / (language + '.ass'), rows)
        subtitles[language] = rows
    expected_names = {'master.mp4', *(f'{episode["id"]}-{profile}.mp4'
                                     for profile in ('en', 'zh', 'selectable'))}
    paths = sorted(folder.glob('*.mp4'))
    require({path.name for path in paths} == expected_names, 'Missing/unexpected MP4 profile')
    media = []
    for path in paths:
        probe = json.loads(tools.run('ffprobe', ['-v', 'error', '-show_streams',
                                                '-show_format', '-of', 'json', path]).stdout)
        videos = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        audios = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
        require(len(videos) == 1 and len(audios) == 1, 'Expected one video and audio stream')
        video, audio = videos[0], audios[0]
        require((video['width'], video['height']) == (1080, 1920)
                and video['codec_name'] == 'h264' and video['pix_fmt'] == 'yuv420p'
                and Fraction(video['avg_frame_rate']) == 30
                and Fraction(video['r_frame_rate']) == 30, 'Video format differs')
        require(audio['codec_name'] == 'aac' and int(audio['sample_rate']) == 48000,
                'Audio format differs')
        measured_duration = float(probe['format']['duration'])
        require(45 <= measured_duration <= 60 and abs(measured_duration - duration) < .1,
                'Encoded duration differs')
        require(int(video['nb_frames']) == timeline[-1]['end'], 'Encoded frame count differs')
        digest = sha(path)
        require(provenance['media'][path.name]['sha256'] == digest
                and provenance['media'][path.name]['size'] == path.stat().st_size,
                'Encoded MP4 differs from provenance')
        decoded = tools.run('ffmpeg', ['-hide_banner', '-nostdin', '-v', 'error', '-xerror',
                                      '-err_detect', 'explode', '-i', path, '-map', '0:v:0',
                                      '-map', '0:a:0', '-f', 'null', os.devnull])
        require(not decoded.stderr.strip(), 'Decode emitted errors')
        loud = tools.run('ffmpeg', ['-hide_banner', '-nostdin', '-i', path, '-map', '0:a:0',
                                   '-vn', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json',
                                   '-f', 'null', os.devnull])
        matches = re.findall(r'\{\s*"input_i".*?\}', loud.stderr, flags=re.S)
        require(len(matches) == 1, 'Loudness measurement absent')
        loudness = json.loads(matches[0])
        require(-18 <= float(loudness['input_i']) <= -14
                and -60 < float(loudness['input_tp']) <= -.5, 'Loudness/true peak outside QA limits')
        embedded = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
        if path.stem.endswith('-selectable'):
            require(len(embedded) == 2 and all(s['codec_name'] == 'mov_text' for s in embedded),
                    'Selectable subtitle streams missing')
            require([s.get('tags', {}).get('language') for s in embedded] == ['eng', 'zho'],
                    'Selectable language labels differ')
            for index, language in enumerate(('en', 'zh')):
                extracted = tools.run('ffmpeg', ['-hide_banner', '-nostdin', '-v', 'error',
                                                '-i', path, '-map', f'0:s:{index}',
                                                '-c:s', 'srt', '-f', 'srt', 'pipe:1']).stdout
                rows = parse_srt(extracted)
                verify_subtitles(rows, timeline, language, duration)
                require(all(compact_text(a['text']) == compact_text(b['text'])
                            for a, b in zip(rows, subtitles[language])), 'Embedded/SRT text differs')
        else:
            require(not embedded, 'Unexpected embedded subtitle stream')
        extracted = extract_frames(path, timeline, output, tools)
        media.append({'path': str(path.relative_to(output)), 'sha256': digest,
                      'duration_seconds': measured_duration, 'frames': int(video['nb_frames']),
                      'format': '1080x1920/30fps/H264/yuv420p/AAC/48000Hz',
                      'full_decode': 'PASS', 'loudness': loudness,
                      'subtitles': 'embedded EN/ZH readback PASS' if embedded else 'ASS/SRT source PASS; burn visual review pending',
                      **extracted})
    return {'id': episode['id'], 'status': 'PASS', 'duration_seconds': duration,
            'srt_semantics_timing': 'PASS against frozen bilingual cues/timeline', 'media': media}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('preflight', 'media', 'all', 'frames-only'), default='preflight')
    parser.add_argument('--episode', choices=('ice', 'sky', 'space'))
    parser.add_argument('--profile', choices=('zh', 'en', 'master', 'selectable'), default='zh',
                        help='Only used for frames-only mode')
    parser.add_argument('--batch', type=Path, default=DEFAULT_BATCH)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--tools', type=Path, default=DEFAULT_TOOLS)
    parser.add_argument('--models', type=Path, default=DEFAULT_MODELS)
    args = parser.parse_args()
    batch, output = args.batch.resolve(strict=True), args.output.resolve()
    if args.mode == 'frames-only':
        require(args.episode is not None, 'frames-only requires --episode')
        bound = BoundTools(args.tools, output)
        folder = output / args.episode
        name = 'master.mp4' if args.profile == 'master' else f'{args.episode}-{args.profile}.mp4'
        timeline = load(folder / 'timeline.json')['cues']
        result = extract_frames(folder / name, timeline, output, bound)
        save(output / f'frames-{args.episode}-{args.profile}-commands.json', bound.commands)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    renderer = module_at('science_acceptance_renderer', HERE / 'render.py')
    report = {'schema_version': 'science-engineering-qa.v1',
              'created_at_utc': datetime.now(timezone.utc).isoformat(),
              'git_sha': git_sha(), 'verify_sha256': sha(Path(__file__)),
              'command': [sys.executable, *sys.argv], 'status': 'FAIL',
              'selected_episode': args.episode,
              'engineering_acceptance': 'PENDING', 'human_acceptance': 'PENDING',
              'market_acceptance': 'PENDING',
              'limits': ['No human first-watch or phone listening/readability acceptance',
                         'No scientific approval inferred from media format checks',
                         'No public upload, channel creation, or external API calls',
                         'ASS/SRT consistency does not independently OCR burned pixels',
                         'No broad DLL/OS/Python interpreter trust attestation'],
              'media_status': 'NOT_RUN'}
    bound = None
    try:
        report['inputs'] = verify_inputs(batch, renderer)
        report['negative_tests'] = negative_tests(batch, args.tools.resolve(strict=True),
                                                  args.models.resolve(strict=True), renderer)
        bound = BoundTools(args.tools, output)
        report['tool_bindings'] = {name: {'path': str(path), **bound.bindings[name]}
                                   for name, path in bound.paths.items()}
        report['preflight_status'] = 'PASS'
        if args.mode in ('media', 'all'):
            report['media'] = []
            for episode in load(batch / 'scripts-final.json')['episodes']:
                if args.episode and episode['id'] != args.episode:
                    continue
                report['media'].append(verify_media_episode(episode, batch, output, bound))
                print('MEDIA PASS ' + episode['id'], flush=True)
            report['media_status'] = 'PASS_SELECTED_EPISODE' if args.episode else 'PASS'
            report['engineering_acceptance'] = ('SELECTED_EPISODE_MACHINE_CHECKS_PASS; OTHER_EPISODES_UNVERIFIED'
                                                if args.episode else
                                                'PASS_MACHINE_CHECKS; VISUAL/HUMAN_GATE_PENDING')
        else:
            report['engineering_acceptance'] = 'PREFLIGHT_PASS; FINAL_MEDIA_NOT_VERIFIED'
        report['status'] = 'PASS'
    except Exception as error:
        report['error'] = f'{type(error).__name__}: {error}'
        print(report['error'], file=sys.stderr, flush=True)
    finally:
        # QA output is separate from renderer's tested output roots.
        output.mkdir(parents=True, exist_ok=True)
        if bound is not None:
            logs = output / 'qa-evidence/commands'
            logs.mkdir(parents=True, exist_ok=True)
            report['command_results'] = []
            for index, record in enumerate(bound.commands, 1):
                path = logs / f'{index:03d}.json'
                save(path, record)
                report['command_results'].append({'argv': record['argv'],
                                                  'returncode': record['returncode'],
                                                  'log': str(path.relative_to(output)),
                                                  'sha256': sha(path)})
        save(output / 'qa.json', report)
    print(json.dumps({'status': report['status'], 'preflight': report.get('preflight_status'),
                      'media': report['media_status'], 'qa': str(output / 'qa.json')}, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
