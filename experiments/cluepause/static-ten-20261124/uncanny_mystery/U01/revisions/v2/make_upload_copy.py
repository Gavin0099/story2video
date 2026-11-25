"""Create and verify a separate upload derivative; never write the master."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

ROOT = Path.cwd()
OUT = Path('artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2')
CHECKS = OUT / 'upload-copy-checks'
MASTER = OUT / 'uncanny-u01-v2.mp4'
UPLOAD = OUT / 'uncanny-u01-v2-upload.mp4'
TOOLS = {key: Path(os.environ[key]) for key in ('S2V_FFMPEG', 'S2V_FFPROBE')}
REPORT_ONLY = '--report-only' in sys.argv[1:]
COMMANDS = json.loads((CHECKS / 'commands.json').read_text(encoding='utf-8')) if REPORT_ONLY else []


def sha(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def save(name, data):
    (CHECKS / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(key, args, label):
    if REPORT_ONLY:
        previous = next(row for row in COMMANDS if row['label'] == label)
        assert previous['exit_code'] == 0
        assert previous['command'] == [f'${key}', *map(str, args)]
        print(f'{label}: existing successful command evidence retained', flush=True)
        return previous['stdout']
    result = subprocess.run([str(TOOLS[key]), *map(str, args)], capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    COMMANDS.append({'label': label, 'command': [f'${key}', *map(str, args)],
                     'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    save('commands.json', COMMANDS)
    if result.returncode:
        raise RuntimeError(f'{label} failed: {result.stderr}')
    print(f'{label}: PASS', flush=True)
    return result.stdout


def probe(path, label):
    data = json.loads(run('S2V_FFPROBE', ['-v', 'error', '-count_frames', '-show_streams',
                                       '-show_format', '-of', 'json', path], label))
    save(f'{label}.json', data)
    return data


CHECKS.mkdir(exist_ok=True)
assert REPORT_ONLY or not UPLOAD.exists(), 'Refuse to overwrite an existing upload copy'
manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
for key, name in [('S2V_FFMPEG', 'ffmpeg'), ('S2V_FFPROBE', 'ffprobe')]:
    assert sha(TOOLS[key]) == manifest['toolchain'][name]['sha256']
source_sha = sha(MASTER)
assert source_sha == '146f6f92fa651d07818f9b4bddda5a2819db5919a7a1a9116e4194f2bdff06d4'
source = probe(MASTER, 'source-probe')
common = ['-nostdin', '-hide_banner', '-loglevel', 'warning', '-i', MASTER,
          '-map', '0:v:0', '-c:v', 'libx264', '-preset', 'slow', '-b:v', '1700k',
          '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', '30', '-threads', '4',
          '-passlogfile', CHECKS / 'x264']
run('S2V_FFMPEG', [*common, '-pass', '1', '-an', '-f', 'null', 'NUL'], 'encode-pass-1')
run('S2V_FFMPEG', [*common, '-map', '0:a:0', '-pass', '2', '-c:a', 'aac', '-b:a', '384k',
                  '-movflags', '+faststart', '-n', UPLOAD], 'encode-pass-2')
output = probe(UPLOAD, 'upload-probe')
streams = {s['codec_type']: s for s in output['streams']}
v, a = streams['video'], streams['audio']
assert len(output['streams']) == 2
assert (v['codec_name'], v['profile'], v['pix_fmt']) == ('h264', 'High', 'yuv420p')
assert (v['width'], v['height'], v['r_frame_rate'], v['avg_frame_rate']) == (1080, 1920, '30/1', '30/1')
assert v['nb_read_frames'] == v['nb_frames'] == '1140'
assert a['codec_name'] == 'aac' and int(a['bit_rate']) >= 128000
assert a['sample_rate'] == '48000' and a['channels'] == 2
duration_delta = abs(float(output['format']['duration']) - float(source['format']['duration']))
assert duration_delta <= .05
for s in source['streams']:
    assert abs(float(s['duration']) - float(streams[s['codec_type']]['duration'])) <= .05
assert UPLOAD.stat().st_size < 9500000
run('S2V_FFMPEG', ['-nostdin', '-hide_banner', '-v', 'error', '-xerror', '-err_detect', 'explode',
                  '-threads', '2', '-i', UPLOAD, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', 'NUL'],
    'full-decode')
ssim_stats = CHECKS / 'ssim.log'
run('S2V_FFMPEG', ['-nostdin', '-hide_banner', '-loglevel', 'info', '-threads', '2', '-i', UPLOAD,
                  '-threads', '2', '-i', MASTER, '-filter_complex_threads', '2', '-filter_complex',
                  '[0:v]setpts=PTS-STARTPTS[dist];[1:v]setpts=PTS-STARTPTS[ref];'
                  f'[dist][ref]ssim=stats_file={ssim_stats.as_posix()}', '-an', '-f', 'null', 'NUL'], 'ssim')
scores = [float(re.search(r'All:([0-9.]+)', line).group(1))
          for line in ssim_stats.read_text(encoding='utf-8').splitlines()]
assert len(scores) == 1140
aggregate = float(re.search(r'All:([0-9.]+)', COMMANDS[-1]['stderr']).group(1))
boxes = []
with UPLOAD.open('rb') as movie:
    while movie.tell() < UPLOAD.stat().st_size:
        position = movie.tell()
        length, kind = struct.unpack('>I4s', movie.read(8))
        if length == 1:
            length = struct.unpack('>Q', movie.read(8))[0]
        if length == 0:
            length = UPLOAD.stat().st_size - position
        boxes.append({'type': kind.decode('ascii'), 'offset': position, 'bytes': length})
        movie.seek(position + length)
assert next(b['offset'] for b in boxes if b['type'] == 'moov') < next(b['offset'] for b in boxes if b['type'] == 'mdat')
assert sha(MASTER) == source_sha
git_sha = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
result = {'verified': datetime.now(timezone(timedelta(hours=8))).isoformat(), 'git_sha': git_sha,
          'master': {'path': MASTER.as_posix(), 'bytes': MASTER.stat().st_size, 'sha256': source_sha},
          'upload': {'path': UPLOAD.as_posix(), 'bytes': UPLOAD.stat().st_size, 'sha256': sha(UPLOAD)},
          'source_duration_seconds': float(source['format']['duration']),
          'upload_duration_seconds': float(output['format']['duration']), 'duration_delta_seconds': duration_delta,
          'audio_bitrate': int(a['bit_rate']), 'full_decode': 'PASS', 'ssim': {'mean': aggregate, 'min': min(scores),
          'frames': len(scores), 'min_frame_1_based': scores.index(min(scores)) + 1}, 'faststart': True,
          'top_level_boxes': boxes, 'master_unchanged': True,
          'tool_sha256': {key: sha(path) for key, path in TOOLS.items()}}
save('results.json', result)
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
