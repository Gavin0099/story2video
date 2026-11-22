"""Isolated, review-bound production of English-first WhyNest Shorts."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTIFACTS = ROOT / 'artifacts/science-shorts/public-20-20261122'
BATCH = HERE.parent
TOOLS = ROOT / 'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
MODELS = ROOT / 'artifacts/73h-episode02/models'
MIN_SECONDS = 35


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load_module('existing_science_engine', BATCH / 'render.py')
scenes = load_module('science_scene_art', HERE / 'scenes.py')
sha, load, save = pilot.sha, pilot.load, pilot.save
BINDINGS = load(ROOT / 'experiments/episode-02-73h/render-manifest.json')
RUBRIC = load(BATCH / 'batch-20261121/gate-policy.json')['rubric']


def verified_rows(episode_id, script, paths, fact_path):
    digest = sha(script)
    reader_marks = []
    for expected, path in zip(('a', 'b'), paths, strict=True):
        if not path.name.startswith(f'reader-{expected}-'):
            raise ValueError('Reader records must be distinct A/B receipts')
        marks = [record for record in load(path) if record['id'] == episode_id]
        if len(marks) != 1:
            raise ValueError(f'No unique reader assessment for {episode_id}: {path.name}')
        record = marks[0]
        scores = record['scores']
        if (record['script_sha256'].lower() != digest or set(scores) != set(RUBRIC) or
                any(type(scores[key]) is not int or not 0 <= scores[key] <= maximum for key, maximum in RUBRIC.items()) or
                sum(scores.values()) != record['total'] or record['total'] < 85 or record['critical_defects']):
            raise ValueError(f'Editorial score gate failed: {episode_id}, reader {expected}')
        reader_marks.append(record['total'])
    findings = [f for f in load(fact_path) if f['id'] == episode_id]
    if (len(findings) != 1 or findings[0]['script_sha256'].lower() != digest or
            findings[0]['status'] != 'PASS' or findings[0]['critical_defects']):
        raise ValueError(f'No passing fact audit for {episode_id}')
    return reader_marks


def bound(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'size': path.stat().st_size}


def run_media(kind, args, cwd, capture=False):
    path = TOOLS / f'{kind}.exe'
    pilot.shared().verify_file(path, **BINDINGS[kind])
    return subprocess.run([str(path), *map(str, args)], cwd=cwd, env=pilot.ENV,
                          check=True, capture_output=capture, text=capture,
                          encoding='utf-8' if capture else None)


def preview(episode, dest, scene_art=scenes):
    for n in range(len(episode['cues'])):
        for p, suffix in ((.19, 'a'), (.7, 'b')):
            scene_art.frame(episode, n, p).save(dest / f'cue-{n+1:02}-{suffix}.png')


def write_subtitles(dest, timeline, helpers):
    _, _, pilot.font = pilot.painter()
    for language, filename in (('en','en.srt'), ('zh','zh-Hant.srt')):
        cues = []
        for index, cue in enumerate(timeline, 1):
            lines = '\n'.join(pilot.wrap(cue[language], language))
            start, end = (helpers.srt_time(cue[key]) for key in ('start','end'))
            cues.append(f"{index}\n{start} --> {end}\n{lines}")
        (dest / filename).write_text('\n\n'.join(cues) + '\n', encoding='utf-8')


def prepare(episode, script, dest, readers, fact):
    hashes = verified_rows(episode['id'], script, readers, fact)
    helpers = pilot.shared()
    for name in ('kokoro-v1.0.int8.onnx','voices-v1.0.bin'):
        helpers.verify_file(MODELS/name, **BINDINGS['inputs']['models/'+name])
    timeline = pilot.synthesize(episode, dest, MODELS, reuse=True, min_seconds=MIN_SECONDS)
    write_subtitles(dest, timeline, helpers)
    snapshot = dest / 'scene-source.py'
    shutil.copyfile(HERE / 'scenes.py', snapshot)
    scene_art = load_module('frozen_scene_art', snapshot)
    scene_art.ART = ARTIFACTS
    preview(episode, dest, scene_art)
    sources = [script, *readers, fact, snapshot, HERE / 'render.py', BATCH / 'render.py',
               ROOT / 'experiments/episode-02-73h/render.py', dest / 'narration.wav', dest / 'timeline.json',
               dest / 'en.srt', dest / 'zh-Hant.srt']
    sources += sorted(dest.glob('cue-*.png'))
    opening = dest / 'opening-art.png'
    if opening.exists():
        sources.append(opening)
    sources += [MODELS/'kokoro-v1.0.int8.onnx', MODELS/'voices-v1.0.bin', TOOLS/'ffmpeg.exe', TOOLS/'ffprobe.exe']
    prepared = {'id':episode['id'],'scores':hashes,'seconds':timeline[-1]['end']/30,
                'renderer_sha256':sha(HERE/'render.py'),'scenes_sha256':sha(snapshot),
                'inputs':[bound(p) for p in sources]}
    save(dest/'inputs.json', prepared)
    print(f"{episode['id']} prepared: readers {hashes}, {prepared['seconds']:.2f}s", flush=True)


def checked_inputs(dest, review):
    manifest = dest/'inputs.json'
    inputs = load(manifest)
    evidence = load(review)
    expected = {'id':inputs['id'],'status':'PASS','inputs_sha256':sha(manifest),
                'renderer_sha256':sha(HERE/'render.py'),'scenes_sha256':sha(dest/'scene-source.py')}
    if any(str(evidence.get(k)).lower()!=v.lower() for k,v in expected.items()) or evidence.get('critical_defects') != []:
        raise ValueError('Independent visual receipt is missing, stale, or failing')
    for item in inputs['inputs']:
        path = (ROOT/item['path']).resolve(strict=True)
        if not path.is_relative_to(ROOT) or path.stat().st_size != item['size'] or sha(path) != item['sha256']:
            raise ValueError(f'Production input changed: {item["path"]}')
    return inputs


def encode(episode, dest, review):
    inputs = checked_inputs(dest, review)
    opening = dest / 'opening-art.png'
    if opening.exists() and not any((ROOT / record['path']).resolve() == opening for record in inputs['inputs']):
        raise ValueError('Opening illustration was added after visual review')
    timeline = load(dest/'timeline.json')['cues']
    scene_art = load_module('frozen_scene_art', dest/'scene-source.py')
    scene_art.ART = ARTIFACTS
    ffmpeg = TOOLS/'ffmpeg.exe'
    pilot.shared().verify_file(ffmpeg, **BINDINGS['ffmpeg'])
    work = dest/'rendering.mp4'
    argv = [str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
            '-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','30','-i','pipe:0',
            '-i','narration.wav','-map','0:v','-map','1:a','-vf','scale=1080:1920:flags=lanczos',
            '-c:v','libx264','-threads','3','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
            '-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-ar','48000','-b:a','160k',
            '-movflags','+faststart',work.name]
    with subprocess.Popen(argv, stdin=subprocess.PIPE, cwd=dest, env=pilot.ENV) as proc:
        try:
            for idx, cue in enumerate(timeline):
                start = 0 if idx==0 else cue['start']
                for n in range(start,cue['end']):
                    p = (n-start)/max(1,cue['end']-start-1)
                    proc.stdin.write(scene_art.frame(episode, idx, p).tobytes())
            proc.stdin.close()
            if proc.wait(): raise RuntimeError('FFmpeg encode failed')
        except BaseException:
            if proc.poll() is None: proc.kill()
            proc.wait()
            raise
    work.replace(dest/'master.mp4')
    qa(episode, dest, timeline, review)


def qa(episode, dest, timeline, review):
    data = json.loads(run_media('ffprobe',['-v','error','-show_streams','-show_format','-of','json','master.mp4'],dest,True).stdout)
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    audio=next(s for s in data['streams'] if s['codec_type']=='audio')
    length=float(data['format']['duration'])
    if ((video['width'],video['height'],video['avg_frame_rate'],video['codec_name'],audio['codec_name']) !=
            (1080,1920,'30/1','h264','aac') or abs(length-timeline[-1]['end']/30)>.11 or not MIN_SECONDS<=length<=60.08):
        raise ValueError('Encoded media does not match geometry, codec or timing')
    run_media('ffmpeg',['-v','error','-xerror','-i','master.mp4','-map','0:v','-map','0:a','-f','null','NUL'],dest)
    summary=run_media('ffmpeg',['-hide_banner','-nostdin','-i','master.mp4','-vf','blackdetect=d=0.15:pix_th=0.08',
                               '-af','silencedetect=n=-45dB:d=2,ebur128=peak=true','-f','null','NUL'],dest,True).stderr
    (dest/'ffmpeg-analysis.txt').write_text(summary,encoding='utf-8')
    loudness=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',summary)[-1])
    peak=float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',summary)[-1])
    if 'black_start:' in summary or 'silence_start:' in summary or not -19<=loudness<=-13 or peak>0:
        raise ValueError('Decode finished but black, silence, or audio thresholds failed')
    for idx,cue in enumerate(timeline,1):
        for suffix,pct in (('a',.19),('b',.7)):
            offset=(cue['start']+pct*(cue['end']-cue['start']))/30
            run_media('ffmpeg',['-hide_banner','-nostdin','-loglevel','error','-y','-ss',f'{offset:.4f}','-i','master.mp4',
                                '-frames:v','1',f'encoded-{idx:02}-{suffix}.png'],dest)
    inputs=load(dest/'inputs.json')
    save(dest/'qa.json', {'id':episode['id'],'status':'PASS','mp4':bound(dest/'master.mp4'),'seconds':length,
                         'inputs_sha256':sha(dest/'inputs.json'),'visual_receipt_sha256':sha(review),
                         'scores':inputs['scores'],'loudness_lufs':loudness,'true_peak_dbfs':peak,
                         'english_graphics':True,'burned_captions':False,
                         'subtitle_hashes':{lang:sha(dest/filename) for lang,filename in [('en','en.srt'),('zh-Hant','zh-Hant.srt')]},
                         'encoded_science_review':'PENDING'})
    print(f"{episode['id']}: QA PASS, {length:.2f}s, independent MP4 review pending",flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('id',choices=tuple(scenes.SCENES))
    p.add_argument('mode',choices=('draft-preview','prepare','encode'))
    p.add_argument('--script',type=Path,required=True)
    p.add_argument('--reader-a',type=Path)
    p.add_argument('--reader-b',type=Path)
    p.add_argument('--fact',type=Path)
    p.add_argument('--visual',type=Path)
    args=p.parse_args()
    script=args.script.resolve(strict=True)
    episode=next(item for item in load(script)['episodes'] if item['id']==args.id)
    dest=ARTIFACTS/args.id
    dest.mkdir(parents=True,exist_ok=True)
    if args.mode=='draft-preview':
        draft=dest/'draft'
        draft.mkdir(exist_ok=True)
        preview(episode,draft)
    elif args.mode=='prepare':
        prepare(episode,script,dest,[args.reader_a.resolve(strict=True),args.reader_b.resolve(strict=True)],args.fact.resolve(strict=True))
    else:
        if not any(x['sha256']==sha(script) and (ROOT/x['path']).resolve()==script for x in load(dest/'inputs.json')['inputs']):
            raise ValueError('Script differs from reviewed production inputs')
        encode(episode,dest,args.visual.resolve(strict=True))


if __name__=='__main__':
    main()
