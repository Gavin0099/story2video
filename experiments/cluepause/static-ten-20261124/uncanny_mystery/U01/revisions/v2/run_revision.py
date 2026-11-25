"""U01-only routing for the unchanged shared renderer; tools supplied by environment."""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[6]
spec = importlib.util.spec_from_file_location('u01_static', HERE.parents[3]/'pipeline/static_storyboard.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)
pipeline.OUTPUTS = REPO/'artifacts/static-ten-20261124/uncanny_mystery'

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'validate':
        pipeline.validate(HERE)
        print('VALID')
    elif mode == 'run':
        print(pipeline.run_story(HERE).relative_to(REPO).as_posix())
    elif mode == 'log-image':
        sheet, filename, status = sys.argv[2:5]
        pipeline.record_image(HERE,sheet,filename,status=='accepted')
        print(json.dumps(pipeline.ledger_rows(pipeline.output_for('uncanny-u01-v2'))[-1]))
