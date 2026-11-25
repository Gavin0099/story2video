"""Run the unchanged puzzle adapter with existing tools and prerecorded WAVs."""
from pathlib import Path
import importlib.util
import os
import shutil
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[6]
# Explicit settings take precedence; the shared pipeline still checks tool hashes.
for variable, executable in (('S2V_FFMPEG', 'ffmpeg'), ('S2V_FFPROBE', 'ffprobe')):
    if variable not in os.environ:
        candidate = shutil.which(executable)
        if candidate is not None:
            os.environ[variable] = candidate
if 'WINDIR' in os.environ:
    os.environ.setdefault('S2V_QUESTION_FONT', str(Path(os.environ['WINDIR'])/'Fonts/msjh.ttc'))
spec=importlib.util.spec_from_file_location('p01_adapter',HERE.parents[2]/'run.py')
adapter=importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='validate':
        adapter.pipeline.validate(HERE)
        print('VALID')
    elif mode=='run':
        print(adapter.pipeline.run_story(HERE).relative_to(REPO).as_posix())
