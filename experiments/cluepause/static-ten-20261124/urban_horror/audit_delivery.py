"""Read-only delivery audit; report is confined to genre artifacts."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import wave

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OUT=REPO/'artifacts/static-ten-20261124/urban_horror'
spec=importlib.util.spec_from_file_location('genre_job',ROOT/'job.py')
job=importlib.util.module_from_spec(spec); spec.loader.exec_module(job)
p=job.p

def main():
    checks={}; unique_images=set(); inspected=0
    for sid in ['H02','H03','H04']:
        folder=ROOT/sid
        data,refs=p.validate(folder)
        out=OUT/data['story_id']
        manifest=p.read(out/'manifest.json')
        checks[sid+'_input_hashes']=all(p.digest(folder/n)==h for n,h in manifest['inputs'].items())
        qa=p.read(out/'qa/report.json')
        checks[sid+'_technical']=qa['engineering']=='PASS' and all(qa['checks'].values())
        checks[sid+'_master_hash']=qa['master_sha256']==p.digest(out/(data['story_id']+'.mp4'))
        images=p.ledger_rows(out)
        checks[sid+'_image_hashes']=all(p.digest(folder/r['result_filename'])==r['result_sha256'] for r in images)
        unique_images.update(r['result_sha256'] for r in images)
        prompts=list((out/'prompts').glob('*.json'))
        prompt_hashes={p.read(f)['prompt_sha256'] for f in prompts if 'prompt_sha256' in p.read(f)}
        checks[sid+'_prompt_receipts']=all(r['prompt_sha256'] in prompt_hashes for r in images)
        checks[sid+'_duration']=float(p.read(out/'qa/probe.json')['format']['duration'])==36
        for cue in data['narration']:
            with wave.open(str(folder/cue['file']),'rb') as f:
                assert (f.getnchannels(),f.getframerate(),f.getsampwidth())==(1,24000,2)
        count=sum(len(p.read(out/'qa'/s['id']/'samples.json')['times']) for s in data['shots'])
        checks[sid+'_dense_frames']=count==162
        inspected+=count
    # Include untracked deliverables; git diff --check alone cannot inspect them.
    # Boundary excludes URL schemes and JSON-escaped "Metadata:\\n" diagnostics.
    pattern=re.compile(r'(?i)((?<![A-Za-z0-9_])[A-Z]:[\\/]|/(?:Users|home)/)')
    bad_paths=[]; whitespace=[]; scanned=0
    for root in [ROOT,OUT]:
        for f in root.rglob('*'):
            if f.is_file() and f.suffix in {'.md','.json','.jsonl','.py','.srt','.txt'}:
                text=f.read_text(encoding='utf-8',errors='replace'); scanned+=1
                if pattern.search(text): bad_paths.append(f.relative_to(REPO).as_posix())
                if f.is_relative_to(ROOT) and re.search(r'(?m)[ \t]+$',text):
                    whitespace.append(f.relative_to(REPO).as_posix())
    checks['no_personal_absolute_paths_in_text']=not bad_paths
    checks['no_trailing_whitespace_in_sources']=not whitespace
    checks['unique_imagegen_outputs']=len(unique_images)==10
    report={'result':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
            'text_files_scanned':scanned,'bad_path_files':bad_paths,'whitespace_files':whitespace,
            'final_dense_frames_reviewed':inspected,'unique_imagegen_calls':len(unique_images),
            'scope':'Local author engineering audit; no story/viewer/market gate approval.'}
    p.save(OUT/'delivery-audit.json',report)
    print(json.dumps(report,indent=2))
    assert report['result']=='PASS'

if __name__=='__main__': main()
