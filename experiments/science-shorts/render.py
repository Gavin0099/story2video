"""Offline science pilot: source-gated scripts, local Kokoro and animated diagrams.

Experimental composition only; does not register episodes or access publishing.
Uses the existing Episode 02 executable binding and caption time helpers.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import time
import wave

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FPS, RATE = 30, 24000
W, H = 1080, 1920
BG, FG, MUTED = '#101d2b', '#f4f3e9', '#94aabd'
CYAN, GOLD, RED = '#74e5e2', '#ffcf75', '#fa8b82'
ENV = {k: v for k, v in os.environ.items() if k.upper() in {'SYSTEMROOT','WINDIR','TEMP','TMP'}}


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def shared():
    spec = importlib.util.spec_from_file_location('episode02', ROOT/'experiments/episode-02-73h/render.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_gate(scripts, gate, reviews):
    digest = sha(scripts)
    if gate.get('script_sha256') != digest or gate.get('status') != 'PASS':
        raise ValueError('Script changed or editorial gate not passed')
    if len(gate.get('review_files',[])) < 3:
        raise ValueError('Independent review evidence missing')
    for record in gate['review_files']:
        path = reviews/record['path']
        if sha(path) != record['sha256']:
            raise ValueError('Review record changed')
    if not gate.get('fact_pass') or not gate.get('visual_plan_pass'):
        raise ValueError('Independent fact/visual review missing')
    expected={e['id'] for e in load(scripts)['episodes']}
    if {e['id'] for e in gate['episodes']} != expected or len(gate['episodes']) != len(expected):
        raise ValueError('Gate does not cover every episode')
    readers=[load(reviews/f'reader-{reader}-v1.json') for reader in ['a','b']]
    for item in gate['episodes']:
        if len(item['scores']) != 2 or min(item['scores']) < 85 or item['critical_defects']:
            raise ValueError('Comprehension or critical-defect gate failed')
        for index,reader in enumerate(readers):
            rows=[r for r in reader if r['id'].lower()==item['id']]
            if len(rows)!=1 or rows[0]['critical_defects']:
                raise ValueError('Reader record incomplete or contains critical defects')
            actual=sum(rows[0]['scores'].values())
            if actual != rows[0]['total'] or actual != item['scores'][index]:
                raise ValueError('Gate score differs from independent reader evidence')
    audit=load(reviews/'fact-visual-v1.json')
    if audit.get('renderer_sha256') != sha(Path(__file__)):
        raise ValueError('Renderer changed since independent visual review')
    if audit.get('script_sha256')!=digest or audit.get('fact_pass') is not True or audit.get('visual_plan_pass') is not True or audit.get('critical_defects'):
        raise ValueError('Independent scientific audit not passed for this script')
    return digest


def synthesize(episode, output, models, reuse, min_seconds=45):
    import numpy as np
    from kokoro_onnx import Kokoro
    script_hash = hashlib.sha256(json.dumps(episode,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    cache = output/'timeline.json'
    if reuse and cache.exists():
        data = load(cache)
        if data['episode_sha256'] == script_hash and sha(output/'narration.wav') == data['audio_sha256']:
            if min_seconds*FPS <= data['cues'][-1]['end'] <= 60*FPS:
                return data['cues']
    narrator = Kokoro(str(models/'kokoro-v1.0.int8.onnx'),str(models/'voices-v1.0.bin'))
    cursor, parts, timeline = 6, [np.zeros(4800,dtype=np.float32)], []
    for cue in episode['cues']:
        samples, rate = narrator.create(cue['en'],voice='am_michael',speed=0.93,lang='en-us')
        if rate != RATE or not len(samples) or not np.isfinite(samples).all():
            raise ValueError('Invalid synthesized samples')
        speech = math.ceil(len(samples)/800)
        pause = max(9,round(cue.get('pause',0.35)*FPS))
        timeline.append({**cue,'start':cursor,'speech_end':cursor+speech,'end':cursor+speech+pause})
        parts.append(np.pad(samples,(0,(speech+pause)*800-len(samples))))
        cursor += speech+pause
    if not min_seconds*FPS <= cursor <= 60*FPS:
        raise ValueError(f"{episode['id']}: {cursor/FPS:.2f}s outside {min_seconds}–60s; revise the pacing")
    signal = np.concatenate(parts)
    peak = float(np.max(np.abs(signal)))
    if peak == 0:
        raise ValueError('Silent narration')
    signal *= .79/peak
    with wave.open(str(output/'narration.wav'),'wb') as wav:
        wav.setparams((1,2,RATE,0,'NONE','not compressed'))
        wav.writeframes((signal*32767).astype('<i2').tobytes())
    save(cache,{'episode_sha256':script_hash,'audio_sha256':sha(output/'narration.wav'),'cues':timeline})
    return timeline


def captions(output,timeline,helpers):
    for lang,filename in [('en','en.srt'),('zh','zh-Hant.srt')]:
        entries = [f"{i}\n{helpers.srt_time(c['start'])} --> {helpers.srt_time(c['end'])}\n{c[lang]}"
                   for i,c in enumerate(timeline,1)]
        (output/filename).write_text('\n\n'.join(entries)+'\n',encoding='utf-8')
        header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
'''
        face='Microsoft JhengHei' if lang=='zh' else 'Segoe UI'
        size=47 if lang=='zh' else 43
        header+=f'Style: Default,{face},{size},&H00E9F3F4,&H00E9F3F4,&H00201308,&H00201308,0,0,0,0,100,100,0,0,1,2,0,8,0,0,0,1\n'
        header+='\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
        events=[]
        for c in timeline:
            lines=wrap(c[lang],lang)
            value=r'\N'.join(lines)
            events.append(f"Dialogue: 0,{helpers.ass_time(c['start'])},{helpers.ass_time(c['end'])},Default,,0,0,0,,{{\\pos(510,1480)}}{value}\n")
        (output/f'{lang}.ass').write_text(header+''.join(events),encoding='utf-8')


def painter():
    from PIL import Image, ImageDraw, ImageFont
    fonts = {}
    def font(size,bold=False,zh=False):
        key=(size,bold,zh)
        if key not in fonts:
            name='msjh.ttc' if zh else ('seguisb.ttf' if bold else 'segoeui.ttf')
            fonts[key]=ImageFont.truetype(str(Path('C:/Windows/Fonts')/name),size)
        return fonts[key]
    return Image,ImageDraw,font


Image,ImageDraw,font = (None,None,None)


def text(d,xy,value,size=38,fill=FG,bold=False,zh=False,anchor=None):
    d.text(xy,value,font=font(size,bold,zh),fill=fill,anchor=anchor,spacing=12)


def wrap(value,lang):
    # Measure glyphs to wrap, rather than relying on character count.
    words = list(value) if lang=='zh' else value.split()
    joiner='' if lang=='zh' else ' '
    size=47 if lang=='zh' else 43
    lines, line=[],''
    for word in words:
        candidate=joiner.join([line,word]) if line else word
        if font(size,False,lang=='zh').getlength(candidate) > 830:
            lines.append(line); line=word
        else:
            line=candidate
    if line: lines.append(line)
    if len(lines)>3:
        raise ValueError('Caption exceeds three lines')
    return lines


def paragraph(d,value,y,lang):
    size=47 if lang=='zh' else 43
    lines=wrap(value,lang)
    for i,line in enumerate(lines):
        text(d,(510,y+i*64),line,size,zh=lang=='zh',anchor='mt')


def arrow(d,a,b,color=CYAN,width=7):
    d.line([a,b],fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    tip=[b,(b[0]-21*math.cos(angle-.5),b[1]-21*math.sin(angle-.5)),
         (b[0]-21*math.cos(angle+.5),b[1]-21*math.sin(angle+.5))]
    d.polygon(tip,fill=color)


def dot(d,x,y,r=13,color=CYAN):
    d.ellipse((x-r,y-r,x+r,y+r),fill=color)


def ice(d,i,p,t):
    if i==0 or i>=7:
        text(d,(510,500),'ICE / WATER',38,MUTED,anchor='mm')
        d.rounded_rectangle((245,620,775,1190),radius=40,outline=MUTED,width=6)
        d.rectangle((252,820,768,1180),fill='#193f57')
        y=(620+(805-620)*min(1,p*2)) if i==0 else 805+3*math.sin(t*2)
        d.rounded_rectangle((420,y,600,y+180),radius=18,fill='#8bdde6',outline=FG,width=4)
        d.line((252,820,768,820),fill=CYAN,width=5)
        text(d,(510,1250),'LESS DENSE → FLOATS',37,CYAN,bold=True,anchor='mm')
        return
    # Equal particle count, unchanged dot radius, expanded occupied volume.
    expand=min(1,max(0,(i-2+p)/2))
    text(d,(510,510),'SAME MASS. MORE SPACE.',42,GOLD,bold=True,anchor='mm')
    compact=[(-1.1,-.9),(-.2,-1.15),(.9,-.8),(-1,.1),(.1,-.1),(1.1,.2),(-.8,1.1),(.3,.9),(1.2,1.1)]
    opened=[(-1.45,-1.35),(0,-1.35),(1.45,-1.35),(-1.45,0),(0,0),(1.45,0),(-1.45,1.35),(0,1.35),(1.45,1.35)]
    scale=82
    for center,factor,name in [(285,0,'LIQUID'),(745,expand,'ICE')]:
        text(d,(center,650),name,36,FG,bold=True,anchor='mm')
        coords=[]
        for j,((a,b),(x,y)) in enumerate(zip(compact,opened)):
            x=(a*(1-factor)+x*factor)*scale+center
            y=(b*(1-factor)+y*factor)*scale+900
            if name=='LIQUID':
                x+=5*math.sin(t*2+j); y+=5*math.cos(t*1.7+j)
            coords.append((x,y))
        extent=128+factor*40
        d.rounded_rectangle((center-extent,900-extent,center+extent,900+extent),radius=25,outline='#456078',width=3)
        for x,y in coords: dot(d,x,y,19)
    text(d,(510,1190),'9 dots each = equal mass',30,MUTED,anchor='mm')
    text(d,(510,1240),'Each dot represents one molecule',28,MUTED,anchor='mm')
    text(d,(510,1290),'Arrangement only · not a crystal model',28,MUTED,anchor='mm')
    text(d,(510,1350),'DENSITY = MASS ÷ VOLUME',38,CYAN,bold=True,anchor='mm')


def sky(d,i,p,t):
    sunset=i>=6
    text(d,(510,510),'LONGER PATH' if sunset else 'FOLLOW THE LIGHT',42,GOLD,bold=True,anchor='mm')
    # Colors travel together as sunlight; colored lines are separated for explanation.
    sun=(150,730 if sunset else 620)
    dot(d,*sun,55,GOLD)
    d.rounded_rectangle((300,570,890,1090),radius=32,fill='#152b42',outline='#3b5973',width=3)
    for x,y in [(370,690),(520,760),(700,680),(790,890),(450,960),(640,1020)]: dot(d,x,y,8,MUTED)
    eye=(800,1060)
    hit=(510,730)
    # Short daytime beam versus extended, nearly horizontal sunset beam.
    if sunset:
        # A second, short path through the same schematic layer makes length explicit.
        arrow(d,(830,590),(830,720),GOLD,4)
        text(d,(780,555),'SHORT',24,MUTED,anchor='mm')
        for offset,col in [(-8,RED),(0,GOLD),(8,CYAN)]:
            arrow(d,(205,730+offset),(430,730+offset),col,5)
        arrow(d,(430,720),(835,720),RED,9)
        for x in (440,565,680):
            arrow(d,(x,730),(x+20,600),CYAN,5)
            phase=(t*.4+x*.001)%1
            dot(d,x+20*phase,730-130*phase,7,CYAN)
        text(d,(510,1170),'Blue redirected out of the direct beam',30,anchor='mm')
        text(d,(510,1220),'More red / orange reaches your eye',31,RED,anchor='mm')
        text(d,(850,770),'EYE',28,MUTED,anchor='mm')
        d.ellipse((815,700,855,740),outline=FG,width=3)
        dot(d,835,720,5,FG)
    else:
        for offset,col in [(-8,RED),(0,GOLD),(8,CYAN)]:
            arrow(d,(205,620+offset),(510,730+offset),col,5)
        arrow(d,(510,722),(820,834),RED,5)
        for end in [(350,890),(630,570),eye,(340,590)]: arrow(d,hit,end,CYAN,6)
        dot(d,*hit,12,MUTED)
        dot(d,hit[0]+(eye[0]-hit[0])*((t*.35)%1),hit[1]+(eye[1]-hit[1])*((t*.35)%1),12,CYAN)
        d.ellipse((765,1040,835,1080),outline=FG,width=4)
        dot(d,800,1060,9,FG)
        text(d,(510,1170),'BLUE: scattered more than red',34,CYAN,bold=True,anchor='mm')
        text(d,(510,1220),'Scattered sunlight reaches your eye',32,anchor='mm')
    text(d,(510,1310),'Rayleigh scattering · simplified paths',29,MUTED,anchor='mm')
    text(d,(510,1355),'Colors separated for explanation',29,MUTED,anchor='mm')


def space(d,i,p,t):
    radio=i>=5
    sound_inset=i==2
    label='RADIO → SPEAKER → SOUND' if i>=7 else ('RADIO CROSSES VACUUM' if radio else 'SOUND NEEDS MATTER')
    text(d,(510,510),label,42,GOLD,bold=True,anchor='mm')
    for x in (220,800):
        d.rounded_rectangle((x-60,830,x+60,1000),radius=24,fill='#c7d5de')
        d.ellipse((x-60,705,x+60,835),fill='#c7d5de')
        d.ellipse((x-43,725,x+43,795),fill='#29455b',outline=CYAN,width=3)
    if radio:
        # Radio is shown as a symbolic field line, never as moving air particles.
        points=[(x,840+32*math.sin((x-290)/35-t*4)) for x in range(290,731,3)]
        d.line(points,fill=GOLD,width=7)
        arrow(d,(330,925),(700,925),GOLD,5)
        text(d,(510,1030),'microphone → radio → speaker',30,anchor='mm')
        text(d,(510,1100),'ELECTROMAGNETIC WAVE',31,GOLD,bold=True,anchor='mm')
        if i>=7:
            d.rounded_rectangle((665,690,890,1020),radius=30,outline=CYAN,width=4)
            text(d,(800,650),'HELMET',28,MUTED,anchor='mm')
            d.rectangle((740,750,755,790),fill=GOLD)
            for x in (772,797,822): dot(d,x+3*math.sin(t*8),770,4,CYAN)
            d.arc((832,750,852,786),-100,110,fill=FG,width=4)
            text(d,(845,814),'EAR',22,FG,anchor='mm')
            text(d,(800,1060),'speaker → air → ear',23,CYAN,anchor='mm')
            text(d,(510,1170),'Local sound inside the helmet',31,CYAN,anchor='mm')
    elif sound_inset:
        text(d,(510,850),'VACUUM GAP',31,MUTED,bold=True,anchor='mm')
        d.rounded_rectangle((285,1070,740,1240),radius=20,outline=CYAN,width=3)
        text(d,(510,1040),'SEPARATE INSET: SOUND IN AIR',27,CYAN,anchor='mm')
        for row in range(4):
            for col in range(15):
                rest=310+col*28
                x=rest+9*math.sin((rest-50*t)/46)
                dot(d,x,1100+row*30,5,CYAN)
        arrow(d,(320,1260),(710,1260),CYAN)
        text(d,(510,1310),'Particles vibrate; the disturbance travels',28,anchor='mm')
    else:
        d.arc((250,720,360,930),-65,65,fill=RED,width=6)
        d.line((450,780,560,950),fill=RED,width=7)
        d.line((560,780,450,950),fill=RED,width=7)
        text(d,(510,1090),'NO SOUND PATH THROUGH VACUUM',30,RED,bold=True,anchor='mm')
    if not sound_inset:
        text(d,(510,1290),'Ideal vacuum gap · no shared solid path',30,CYAN,anchor='mm')
    text(d,(510,1350),'Schematic · no scales implied',29,MUTED,anchor='mm')


def frame(episode,timeline,n,profile):
    image=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(image)
    total=timeline[-1]['end']
    index=next((i for i,c in enumerate(timeline) if c['start']<=n<c['end']),0)
    cue=timeline[index]
    p=max(0,min(1,(n-cue['start'])/max(1,cue['end']-cue['start'])))
    d.rectangle((0,0,18,H),fill=CYAN)
    text(d,(85,160),'ONE QUESTION / ONE MINUTE',29,CYAN,bold=True)
    text(d,(85,230),{'ice':'Why does ice float?','sky':'Why is the sky blue?','space':'Can sound cross space?'}[episode['id']],55,bold=True)
    text(d,(85,320),episode['title_zh'],37,MUTED,zh=True)
    d.line((85,405,935,405),fill='#365069',width=2)
    {'ice':ice,'sky':sky,'space':space}[episode['id']](d,index,p,n/FPS)
    d.rounded_rectangle((70,1450,950,1710),radius=24,fill='#081320')
    if profile!='clean' and n>=cue['start']:
        paragraph(d,cue['zh'] if profile=='zh' else cue['en'],1480,profile)
    d.rounded_rectangle((85,1760,935,1768),radius=4,fill='#365069')
    d.rounded_rectangle((85,1760,85+850*(n+1)/total,1768),radius=4,fill=CYAN)
    text(d,(85,1805),'SCHEMATIC / NOT TO SCALE',25,MUTED)
    return image


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--tools',type=Path,required=True)
    parser.add_argument('--models',type=Path,required=True)
    parser.add_argument('--episode',choices=['ice','sky','space'])
    parser.add_argument('--reuse-audio',action='store_true')
    args=parser.parse_args()
    batch=args.batch.resolve(strict=True)
    scripts=batch/'scripts-final.json'
    gate=load(batch/'editorial-gate.json')
    script_hash=validate_gate(scripts,gate,batch/'reviews')
    helpers=shared()
    bindings=load(ROOT/'experiments/episode-02-73h/render-manifest.json')
    ffmpeg=(args.tools/'ffmpeg.exe').resolve(strict=True)
    ffprobe=(args.tools/'ffprobe.exe').resolve(strict=True)
    for name,path in [('ffmpeg',ffmpeg),('ffprobe',ffprobe)]: helpers.verify_file(path,**bindings[name])
    models=args.models.resolve(strict=True)
    for name in ['kokoro-v1.0.int8.onnx','voices-v1.0.bin']:
        helpers.verify_file(models/name,**bindings['inputs']['models/'+name])
    global Image,ImageDraw,font
    Image,ImageDraw,font=painter()
    for episode in load(scripts)['episodes']:
        if args.episode and episode['id']!=args.episode: continue
        output=(args.output/episode['id']).resolve()
        output.mkdir(parents=True,exist_ok=True)
        started=time.perf_counter()
        timeline=synthesize(episode,output,models,args.reuse_audio)
        captions(output,timeline,helpers)
        def execute(kind,argv,capture=False):
            path=ffmpeg if kind=='ffmpeg' else ffprobe
            helpers.verify_file(path,**bindings[kind])
            base=['-hide_banner','-loglevel','error','-nostdin','-y'] if kind=='ffmpeg' else []
            return subprocess.run([str(path),*base,*map(str,argv)],cwd=output,env=ENV,check=True,capture_output=capture,text=capture,encoding='utf-8' if capture else None)
        # One diagram render; language profiles burn subtitles from the same timing.
        helpers.verify_file(ffmpeg,**bindings['ffmpeg'])
        argv=[str(ffmpeg),'-hide_banner','-loglevel','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-i','narration.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','20','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-ar','48000','-b:a','128k','-movflags','+faststart','master.mp4']
        with subprocess.Popen(argv,stdin=subprocess.PIPE,cwd=output,env=ENV) as proc:
            try:
                for n in range(timeline[-1]['end']):
                    picture=frame(episode,timeline,n,'clean')
                    proc.stdin.write(picture.tobytes())
                    if n%300==0: print(f"{episode['id']} {n}/{timeline[-1]['end']} frames",flush=True)
                proc.stdin.close()
                if proc.wait(): raise RuntimeError('FFmpeg encode failed')
            except BaseException:
                proc.kill(); proc.wait(); raise
        # libass wraps the exact SRT text; separate English/Taiwanese profiles.
        for profile in ['zh','en']:
            filt=f'ass={profile}.ass'
            execute('ffmpeg',['-i','master.mp4','-vf',filt,'-c:v','libx264','-preset','veryfast','-crf','20','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',f'{episode["id"]}-{profile}.mp4'])
        execute('ffmpeg',['-i','master.mp4','-i','en.srt','-i','zh-Hant.srt','-map','0:v','-map','0:a','-map','1:s','-map','2:s','-c','copy','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata:s:s:1','language=zho','-disposition:s:0','0','-disposition:s:1','default','-movflags','+faststart',f'{episode["id"]}-selectable.mp4'])
        snapshots=[]
        for i,cue in enumerate(timeline):
            n=(cue['start']+cue['end'])//2
            pic=frame(episode,timeline,n,'zh')
            pic.save(output/f'cue-{i+1:02}.png')
            snapshots.append(pic.resize((270,480)))
        sheet=Image.new('RGB',(270*5,480*math.ceil(len(snapshots)/5)),BG)
        for i,pic in enumerate(snapshots): sheet.paste(pic,((i%5)*270,(i//5)*480))
        sheet.save(output/'storyboard-contact.png')
        media={}
        for path in sorted(output.glob('*.mp4')):
            result=execute('ffprobe',['-v','error','-show_streams','-show_format','-of','json',path.name],True)
            probe=json.loads(result.stdout)
            save(output/(path.stem+'.probe.json'),probe)
            execute('ffmpeg',['-v','error','-xerror','-i',path.name,'-map','0:v','-map','0:a','-f','null','NUL'])
            media[path.name]={'sha256':sha(path),'size':path.stat().st_size,'duration':probe['format']['duration']}
        save(output/'provenance.json',{'script_sha256':script_hash,'renderer_sha256':sha(Path(__file__)),'editorial_gate_sha256':sha(batch/'editorial-gate.json'),'models':bindings['inputs'],'ffmpeg':bindings['ffmpeg'],'voice':'am_michael','speed':.93,'frames':timeline[-1]['end'],'media':media,'render_seconds':round(time.perf_counter()-started,2),'paid_api_calls':0,'incremental_media_api_cost_usd':0,'unpriced':['existing subscription','human effort','compute/electricity'],'human_gate':'PENDING','market_gate':'PENDING'})
        print(f"DONE {episode['id']}: {timeline[-1]['end']/FPS:.2f}s",flush=True)


if __name__=='__main__': main()
