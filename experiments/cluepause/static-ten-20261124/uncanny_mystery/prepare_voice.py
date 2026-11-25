"""Synthesize each authored line once, then use measured prerecorded WAV inputs."""
import json
from pathlib import Path
import shutil
import sys
import time
from run_local import pipeline, HERE

for code in sys.argv[1:]:
    started=time.monotonic()
    story=HERE/code
    data=pipeline.read(story/'shots.json')
    out=pipeline.output_for(data['story_id'])
    with pipeline.owned_output(out):
        # Preserve measured WAVs even if the initial editorial timing needs adjustment.
        try:
            pipeline.prepare_audio(story,data,out)
        except ValueError as exc:
            print(code, type(exc).__name__, str(exc))
        for line in data['narration']:
            src=out/'cache/voice'/(line['id']+'.wav')
            if src.exists():
                name='assets/voice-'+line['id']+'.wav'
                shutil.copyfile(src,story/name)
                line['file']=name
        pipeline.save(story/'shots.json',data)
        pipeline.save(out/'voice-production.json',{'provider':'local Kokoro ONNX','voice':'af_heart','speed':1.08,'seconds':round(time.monotonic()-started,3),'per_line_synthesis':1,'models':pipeline.MODEL_HASHES})
    print(code,'voice files prepared')
