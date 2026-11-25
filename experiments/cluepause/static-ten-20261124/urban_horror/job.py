"""Genre-local entry point; shared pipeline remains read-only. Run with -B."""
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PIPE = ROOT.parent / 'pipeline'
spec = importlib.util.spec_from_file_location('static_storyboard', PIPE / 'static_storyboard.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
# Shared output_for otherwise puts siblings directly under the batch root.
p.OUTPUTS = REPO / 'artifacts/static-ten-20261124/urban_horror'

def main():
    action, sid, *rest = sys.argv[1:]
    story = ROOT / sid
    # Audio uses the existing read-only TTS environment, which lacks jsonschema.
    # Inputs must first be validated with the normal Python entry point.
    if action == 'audio':
        data, refs = p.read(story/'shots.json'), p.read(story/'references.json')
    else:
        data, refs = p.validate(story)
    out = p.output_for(data['story_id'])
    if action == 'validate':
        print('VALID', sid)
    elif action == 'prompts':
        p.export_prompts(story, bool(rest))
    elif action == 'log':
        sheet, filename, status = rest
        p.record_image(story, sheet, filename, status == 'accepted')
    elif action == 'audio':
        with p.owned_output(out):
            shots, cues = p.prepare_audio(story, data, out)
            import shutil
            (story/'assets/voice').mkdir(exist_ok=True)
            for line in data['narration']:
                filename = 'assets/voice/'+line['id']+'.wav'
                shutil.copy2(out/'cache/voice'/ (line['id']+'.wav'), story/filename)
                line['file'] = filename
            p.save(story/'shots.json',data)
        print(json.dumps({'id':sid,'duration':shots[-1]['end'],'cues':[(c.get('id','sfx'),round(c['start'],3),round(c['end'],3)) for c in cues]}))
    elif action == 'run':
        print(p.run_story(story).relative_to(REPO).as_posix())
    else:
        raise ValueError('Unknown action')

if __name__ == '__main__':
    main()
