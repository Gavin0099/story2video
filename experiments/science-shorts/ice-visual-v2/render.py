"""Isolated art-direction pilot. Reuses reviewed ice narration; never publishes.

Generated raster layers + deterministic camera/diagram animation. This is not
a production Remotion integration. Preview is available before the review gate;
encoding requires a new review bound to this renderer and the frozen inputs.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import time
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'artifacts/science-shorts/ice-visual-v2'
ORIGINAL = ROOT / 'artifacts/science-shorts/batch-20261121/ice'
BATCH = HERE.parent / 'batch-20261121'
W, H, FPS = 1080, 1920, 30
INK, SOFT, TEAL, ORANGE = '#163f49', '#55747a', '#087d88', '#d75132'
ENV = {k: v for k, v in os.environ.items() if k.upper() in {'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP'}}


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def verify(path, binding):
    path = Path(path)
    if not path.is_absolute() or path.resolve(strict=True) != path:
        raise ValueError('Noncanonical input')
    if path.stat().st_size != binding['size'] or sha(path) != binding['sha256']:
        raise ValueError(f'Frozen input differs: {path.name}')


def inputs(require_review=False):
    manifest = load(HERE/'inputs.json')
    for relative, binding in manifest['files'].items():
        verify((ROOT/relative).resolve(strict=True), binding)
    tools = ROOT/'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
    binaries = load(ROOT/'experiments/episode-02-73h/render-manifest.json')
    for name in ('ffmpeg', 'ffprobe'):
        verify((tools/(name+'.exe')).resolve(strict=True), binaries[name])
    timeline = load(ORIGINAL/'timeline.json')
    if timeline['audio_sha256'] != sha(ORIGINAL/'narration.wav'):
        raise ValueError('Audio/timeline mismatch')
    script = next(e for e in load(BATCH/'scripts-final.json')['episodes'] if e['id']=='ice')
    if len(script['cues']) != len(timeline['cues']):
        raise ValueError('Cue count differs')
    for source, timed in zip(script['cues'], timeline['cues']):
        for key in ('en', 'zh', 'claim_ids'):
            if source[key] != timed[key]:
                raise ValueError('Narration differs from reviewed script')
    gate = load(BATCH/'editorial-gate.json')
    if gate['status'] != 'PASS' or gate['script_sha256'] != sha(BATCH/'scripts-final.json'):
        raise ValueError('Original editorial gate differs')
    if require_review:
        review = load(HERE/'visual-review.json')
        if review.get('status') != 'PASS' or review.get('critical_defects'):
            raise ValueError('New scientific visual review has not passed')
        if review.get('renderer_sha256') != sha(Path(__file__)) or review.get('inputs_sha256') != sha(HERE/'inputs.json'):
            raise ValueError('Review does not cover current renderer/inputs')
    return timeline['cues'], tools, binaries


@lru_cache(maxsize=100)
def font(size, zh=False, bold=False):
    name = ('msjhbd.ttc' if bold else 'msjh.ttc') if zh else ('seguisb.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype('C:/Windows/Fonts/'+name, size)


def txt(d, pos, value, size=42, color=INK, zh=False, bold=False, anchor=None):
    d.text(pos, value, font=font(size, zh, bold), fill=color, anchor=anchor)


def ease(x):
    x = min(1, max(0, x))
    return x*x*(3-2*x)


def mix(a, b, p):
    return a+(b-a)*p


@lru_cache(maxsize=2)
def backdrop(dark=False):
    yy, xx = np.mgrid[0:H, 0:W]
    t = np.clip(yy/H*.65 + xx/W*.15, 0, 1)[..., None]
    a, b = ((19, 62, 72), (32, 103, 112)) if dark else ((255, 242, 224), (219, 241, 235))
    colors = np.array(a)*(1-t)+np.array(b)*t
    return Image.fromarray(colors.astype('uint8'))


@lru_cache(maxsize=1)
def assets():
    glass = Image.open(OUT/'assets/glass.png').convert('RGB')
    scale = max(W/glass.width, H/glass.height)
    glass = glass.resize((round(glass.width*scale), round(glass.height*scale)), Image.Resampling.LANCZOS)
    x, y = (glass.width-W)//2, (glass.height-H)//2
    glass = glass.crop((x,y,x+W,y+H))
    cube = Image.open(OUT/'assets/ice.png').convert('RGBA')
    if cube.getextrema()[3][0] != 0 or cube.getextrema()[3][1] != 255:
        raise ValueError('Ice asset must have genuine alpha')
    return glass, cube.crop(cube.getbbox())


def cube_layer(im, center, width, submerged_line=None):
    source = assets()[1]
    height = round(width*source.height/source.width)
    cube = source.resize((round(width), height), Image.Resampling.LANCZOS)
    x, y = round(center[0]-width/2), round(center[1]-height/2)
    if submerged_line is not None and submerged_line-y < height:
        tint = Image.new('RGBA', cube.size, (0,0,0,0))
        draw = ImageDraw.Draw(tint)
        draw.rectangle((0,max(0,submerged_line-y),cube.width,cube.height), fill=(7,112,123,90))
        tint.putalpha(Image.fromarray((np.asarray(tint.getchannel('A'),dtype=np.uint16)*np.asarray(cube.getchannel('A'),dtype=np.uint16)//255).astype('uint8')))
        cube = Image.alpha_composite(cube,tint)
    im.paste(cube, (x,y), cube)


def heading(im, number, chinese, english, dark=False):
    d = ImageDraw.Draw(im)
    color = '#f8f1dc' if dark else INK
    accent = '#87e5e0' if dark else TEAL
    txt(d,(80,110),f'{number:02}  /  EVERYDAY SCIENCE',27,accent,bold=True)
    txt(d,(80,190),chinese,62,color,zh=True,bold=True)
    txt(d,(83,286),english,30,accent)


@lru_cache(maxsize=4)
def ball(radius=30, warm=False):
    s = radius*2+4
    yy, xx = np.mgrid[0:s, 0:s]
    dist = np.sqrt((xx-s/2)**2+(yy-s/2)**2)/radius
    light = np.clip(1-np.sqrt((xx-s*.32)**2+(yy-s*.28)**2)/(radius*2.3),0,1)
    low, high = ((207,85,43),(255,211,143)) if warm else ((4,105,129),(184,255,243))
    rgb = np.array(low)[None,None,:]*(1-light[...,None])+np.array(high)[None,None,:]*light[...,None]
    rgba = np.dstack([rgb,np.where(dist<=1,255,0)]).astype('uint8')
    return Image.fromarray(rgba)


WATER = [(-.91,-.77),(-.34,-.91),(.34,-.75),(.87,-.94),(-.8,-.12),(-.26,-.21),(.4,-.07),(.94,-.23),(-.96,.72),(-.37,.8),(.29,.65),(.84,.85)]
ORDER = [(c*.55-.825+(r%2)*.10,r*.75-.75) for r in range(3) for c in range(4)]


def particles(im, center, sx, sy, t, ordered=0, radius=29, warm=False, highlight=False):
    d = ImageDraw.Draw(im)
    points=[]
    for i, ((wx,wy),(ix,iy)) in enumerate(zip(WATER,ORDER)):
        x = mix(wx,ix,ordered)*sx+center[0] + math.sin(t*1.8+i*2.1)*6*(1-ordered)
        y = mix(wy,iy,ordered)*sy+center[1] + math.cos(t*1.4+i*1.7)*6*(1-ordered)
        points.append((x,y))
    if highlight:
        for a,b in ((0,1),(1,2),(4,5),(5,6),(8,9),(9,10)):
            ax,ay=points[a]; bx,by=points[b]
            d.line((ax+radius+8,ay,bx-radius-8,by),fill='#e69754',width=5)
    for x,y in points:
        sphere=ball(radius,warm)
        im.paste(sphere,(round(x-radius-2),round(y-radius-2)),sphere)
    return points


def schematic(im, text='每顆球代表一個水分子；排列與體積變化僅為示意', dark=False):
    d=ImageDraw.Draw(im)
    txt(d,(540,1398),text,27,'#bfd7d2' if dark else SOFT,zh=True,anchor='mm')
    txt(d,(540,1442),'SCHEMATIC · NOT A CRYSTAL MODEL · NOT TO SCALE',21,'#bfd7d2' if dark else SOFT,anchor='mm')


def hero(n, end=False, card=True, chapter=8):
    t=n/FPS
    im=assets()[0].copy()
    # Layered object motion: cube falls, overshoots and settles; mostly submerged.
    water_y=865
    drop=ease((t-.1)/.9) if not end else 1
    bob=math.sin(max(0,t-1)*5)*9*math.exp(-max(0,t-1)*.7) if not end else math.sin(t*1.4)*3
    cy=mix(595,963,drop)+bob
    cube_layer(im,(540,cy),245,water_y)
    d=ImageDraw.Draw(im)
    # Local surface rings decay after impact, staying inside the glass.
    if 1<t<3.6:
        ripple=(t-1)/2.6
        ww=150+130*ripple
        d.arc((540-ww,water_y-18-12*ripple,540+ww,water_y+18+12*ripple),0,180,fill='#a6e3db',width=3)
    if end:
        heading(im,chapter,'所以，冰浮起來了。','LOWER DENSITY. SAME WATER.')
        if card:
            d.rounded_rectangle((110,1210,970,1360),radius=28,fill='#fff3de')
            txt(d,(540,1260),'排列較開放 → 密度較低',42,TEAL,zh=True,bold=True,anchor='mm')
            txt(d,(540,1320),'大部分冰塊，仍浸在水裡',30,SOFT,zh=True,anchor='mm')
    else:
        txt(d,(80,110),'ONE QUESTION / ONE MINUTE',28,TEAL,bold=True)
        txt(d,(80,195),'冰，為什麼',78,INK,zh=True,bold=True)
        txt(d,(80,300),'浮在水上？',96,INK,zh=True,bold=True)
        txt(d,(86,444),'WHY DOES ICE FLOAT?',32,TEAL,bold=True)
    # Gentle camera drift on the entire scene, rather than fixed slide framing.
    z=1+.018*math.sin(t*.4)
    nw,nh=round(W*z),round(H*z)
    if nw>=W and nh>=H:
        im=im.resize((nw,nh),Image.Resampling.BICUBIC).crop(((nw-W)//2,(nh-H)//2,(nw+W)//2,(nh+H)//2))
    return im


def macro(n, cue):
    p=ease((n-cue['start'])/(cue['end']-cue['start']))
    im=backdrop().copy()
    heading(im,2,'答案，藏在冰塊裡。','LOOK CLOSER. THE ARRANGEMENT CHANGES.')
    cube_layer(im,(490,840),660+50*p)
    # A growing magnification window links the same cube to the next diagram.
    radius=round(mix(90,250,p))
    center=(665,965)
    layer=Image.new('RGB',(W,H),'#e7f6ee')
    particles(layer,center,radius*.73,radius*.63,n/FPS,ease(p),max(13,round(radius*.085)))
    mask=Image.new('L',(W,H),0)
    ImageDraw.Draw(mask).ellipse((center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius),fill=255)
    im.paste(layer,(0,0),mask)
    d=ImageDraw.Draw(im)
    d.ellipse((center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius),outline='#fff7e6',width=12)
    txt(d,(540,1300),'結冰時，分子的排列改變了',43,TEAL,zh=True,bold=True,anchor='mm')
    schematic(im)
    return im


def comparison(n, index, cue):
    im=backdrop().copy()
    d=ImageDraw.Draw(im)
    titles={2:('先拿同樣多的水。','SAME NUMBER OF MOLECULES.'),3:('結冰，改變的是排列。','MORE OPEN. MORE ORDERED.'),5:('同樣的水，佔更多空間。','SAME MASS. LARGER VOLUME.')}
    title,subtitle=titles[index]
    heading(im,index+1,title,subtitle)
    if index==2:
        ordered=0
        expansion=0
    elif index==3:
        ordered=ease((n-cue['start'])/(cue['end']-cue['start'])*1.5)
        expansion=ordered
    else:
        ordered=1
        expansion=1
    for cx,ice in ((290,False),(790,True)):
        ex=expansion if ice else 0
        ww=360+45*ex
        hh=490+65*ex
        cy=864
        # Glassy panel with rim and offset shadow, leaving space for larger dots.
        d.rounded_rectangle((cx-ww/2+7,cy-hh/2+13,cx+ww/2+7,cy+hh/2+13),radius=42,fill='#c9dbd3')
        d.rounded_rectangle((cx-ww/2,cy-hh/2,cx+ww/2,cy+hh/2),radius=42,fill='#e8f8f4' if ice else '#ffead9',outline='#77ada8' if ice else '#e6b99a',width=3)
        txt(d,(cx,483),'冰' if ice else '水',58,INK,zh=True,bold=True,anchor='mm')
        txt(d,(cx,549),'ICE' if ice else 'LIQUID',27,TEAL,anchor='mm')
        particles(im,(cx,cy),140+18*ex,176+23*ex,n/FPS,ordered if ice else 0)
        txt(d,(cx,1230),'12 個水分子',34,TEAL,zh=True,bold=True,anchor='mm')
    d=ImageDraw.Draw(im)
    txt(d,(540,1305),'質量相同',43,ORANGE,zh=True,bold=True,anchor='mm')
    if index==5:
        d.line((605,1170,982,1170),fill=TEAL,width=4)
        d.polygon([(605,1170),(622,1160),(622,1180)],fill=TEAL)
        d.polygon([(982,1170),(965,1160),(965,1180)],fill=TEAL)
    schematic(im)
    return im


def spacing(n,cue):
    im=backdrop(True).copy()
    heading(im,5,'排列鬆開，空間就多了。','FOLLOW THE SPACE BETWEEN MOLECULES.',True)
    p=ease((n-cue['start'])/(cue['end']-cue['start']))
    points=particles(im,(540,860),360+16*p,330+12*p,n/FPS,1,48,highlight=True)
    d=ImageDraw.Draw(im)
    # Pulse in an empty gap, never changing molecule size or molecule count.
    x=(points[5][0]+points[6][0])/2
    y=(points[5][1]+points[6][1])/2
    r=24+9*math.sin(n/FPS*3)
    d.ellipse((x-r,y-r,x+r,y+r),outline='#f1bb75',width=4)
    txt(d,(540,1270),'更多分子間的空間',49,'#f8efdc',zh=True,bold=True,anchor='mm')
    schematic(im,dark=True)
    return im


def density(n,cue):
    im=backdrop(True).copy()
    heading(im,7,'所以，密度變低了。','DENSITY = MASS / VOLUME',True)
    d=ImageDraw.Draw(im)
    local=(n-cue['start'])/FPS
    rows=[(520,'同樣的質量','SAME MASS','#d9f2e9'),(760,'更大的體積','LARGER VOLUME','#a4e5de'),(1110,'更低的密度','LOWER DENSITY','#ffcb8f')]
    for i,(y,ch,en,col) in enumerate(rows):
        p=ease((local-i*.55)/.6)
        if p<=0: continue
        x=80+round((1-p)*130)
        txt(d,(x,y),ch,69,col,zh=True,bold=True)
        txt(d,(x+4,y+95),en,32,col)
        txt(d,(900,y+45),('=','↑','↓')[i],74,col,bold=True,anchor='mm')
    # Avoid presenting the three phrases as a literal chained equation.
    d.line((85,1000,970,1000),fill='#739f9e',width=3)
    return im


def takeaway(n,cue):
    im=hero(n,True,False,9)
    # Return to the same hero object, then reveal a separate explanatory inset.
    d=ImageDraw.Draw(im)
    p=ease((n-cue['start'])/30)
    if p>0:
        d.rounded_rectangle((120,1160,960,1400),radius=30,fill='#fff4e1')
        txt(d,(540,1210),'關鍵：水分子的排列',45,INK,zh=True,bold=True,anchor='mm')
        txt(d,(540,1280),'較開放 → 較低密度 → 浮起',35,TEAL,zh=True,bold=True,anchor='mm')
        txt(d,(540,1350),'圖像為示意，並非晶體結構模型',26,SOFT,zh=True,anchor='mm')
    return im


def shot(n,index,cues):
    cue=cues[index]
    if index==0: return hero(n)
    if index==1: return macro(n,cue)
    if index in (2,3,5): return comparison(n,index,cue)
    if index==4: return spacing(n,cue)
    if index==6: return density(n,cue)
    if index==7: return hero(n,True)
    return takeaway(n,cue)


def wrapped(value,language,max_width=850):
    size=48 if language=='zh' else 42
    face=font(size,language=='zh')
    units=list(value) if language=='zh' else value.split()
    join='' if language=='zh' else ' '
    lines=[]
    line=''
    for unit in units:
        candidate=line+join+unit if line else unit
        if face.getlength(candidate)>max_width and line:
            lines.append(line); line=unit
        else: line=candidate
    if line: lines.append(line)
    return lines,size


def caption(im,n,cues,language):
    if language=='clean': return
    cue=next((c for c in cues if c['start']<=n<c['end']),None)
    if not cue: return
    lines,size=wrapped(cue[language],language)
    line_h=size+21
    if len(lines)*line_h>250: raise ValueError('Caption exceeds reserved area')
    panel=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(panel)
    top=1540
    height=max(145,len(lines)*line_h+46)
    d.rounded_rectangle((65,top,1015,top+height),radius=28,fill=(255,249,232,240))
    for i,line in enumerate(lines):
        txt(d,(540,top+23+i*line_h),line,size,INK,zh=language=='zh',anchor='mt')
    im.paste(panel,(0,0),panel)


def frame(n,cues,language='zh'):
    index=next((i for i,c in enumerate(cues) if c['start']<=n<c['end']),0)
    im=shot(n,index,cues)
    # Brief dissolves connect scales; the diagram itself remains deterministic.
    transition=n-cues[index]['start']
    if index>0 and 0<=transition<12:
        previous=shot(cues[index]['start']-1,index-1,cues)
        im=Image.blend(previous,im,ease(transition/12))
    caption(im,n,cues,language)
    d=ImageDraw.Draw(im)
    y=1830
    d.rounded_rectangle((80,y,1000,y+5),radius=2,fill='#b0c4ba')
    d.rounded_rectangle((80,y,80+920*(n+1)/cues[-1]['end'],y+5),radius=2,fill=TEAL)
    return im


def srt_time(n):
    ms=round(n*1000/FPS)
    minutes,ms=divmod(ms,60000)
    seconds,ms=divmod(ms,1000)
    return f'00:{minutes:02}:{seconds:02},{ms:03}'


def preview(cues):
    dest=OUT/'preview'
    dest.mkdir(parents=True,exist_ok=True)
    shots=[]
    for i,c in enumerate(cues):
        n=(c['start']+c['end'])//2
        im=frame(n,cues)
        im.save(dest/f'shot-{i+1:02}.png')
        shots.append(im.resize((270,480),Image.Resampling.LANCZOS))
    contact=Image.new('RGB',(270*3,480*3),'#fff3de')
    for i,im in enumerate(shots): contact.paste(im,((i%3)*270,(i//3)*480))
    contact.save(dest/'contact.png')
    for n in (0,15,30,45,60,1440): frame(n,cues).save(dest/f'frame-{n:04}.png')
    save(dest/'timing.json',[{'shot':i+1,'start':c['start']/FPS,'end':c['end']/FPS} for i,c in enumerate(cues)])


def execute(name,argv,tools,bindings,capture=False):
    binary=(tools/(name+'.exe')).resolve(strict=True)
    verify(binary,bindings[name])
    base=['-hide_banner','-loglevel','error','-nostdin','-y'] if name=='ffmpeg' else []
    return subprocess.run([str(binary),*base,*map(str,argv)],cwd=OUT,env=ENV,check=True,capture_output=capture,text=capture,encoding='utf-8' if capture else None)


def render(cues,tools,bindings):
    start=time.perf_counter()
    total=cues[-1]['end']
    ffmpeg=(tools/'ffmpeg.exe').resolve(strict=True)
    verify(ffmpeg,bindings['ffmpeg'])
    argv=[str(ffmpeg),'-hide_banner','-loglevel','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(ORIGINAL/'narration.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-ar','48000','-b:a','160k','-movflags','+faststart','ice-v2-zh.mp4']
    with subprocess.Popen(argv,stdin=subprocess.PIPE,cwd=OUT,env=ENV) as proc:
        try:
            for n in range(total):
                proc.stdin.write(frame(n,cues).tobytes())
                if n%180==0: print(f'FRAME {n}/{total}',flush=True)
            proc.stdin.close()
            if proc.wait(): raise RuntimeError('Encoding failed')
        except BaseException:
            proc.kill(); proc.wait(); raise
    for lang,name in (('en','en.srt'),('zh','zh-Hant.srt')):
        entries=[f'{i}\n{srt_time(c["start"])} --> {srt_time(c["end"])}\n{c[lang]}' for i,c in enumerate(cues,1)]
        (OUT/name).write_text('\n\n'.join(entries)+'\n',encoding='utf-8')
    # First 11.6 seconds show both the scene and magnification transition.
    execute('ffmpeg',['-i','ice-v2-zh.mp4','-t','11.6','-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-c:a','aac','-movflags','+faststart','ice-v2-preview.mp4'],tools,bindings)
    save(OUT/'provenance.json',{'renderer_sha256':sha(Path(__file__)),'inputs_sha256':sha(HERE/'inputs.json'),'review_sha256':sha(HERE/'visual-review.json'),'audio_sha256':sha(ORIGINAL/'narration.wav'),'frames':total,'duration_seconds':total/FPS,'render_seconds':round(time.perf_counter()-start,2),'image_generation':{'mode':'built-in image_gen','calls':2,'metered_api_calls':0,'cash_cost':'not reported by built-in tool; subscription and compute unpriced'},'voice':'reused original Kokoro am_michael; same script and timing','engine':'Pillow layered compositor + FFmpeg; not production Remotion','human_acceptance':'PENDING','market_acceptance':'PENDING'})


def qa(cues,tools,bindings):
    reports={}
    samples=OUT/'actual-mp4'
    samples.mkdir(exist_ok=True)
    for name in ('ice-v2-zh.mp4','ice-v2-preview.mp4'):
        path=OUT/name
        data=json.loads(execute('ffprobe',['-v','error','-show_streams','-show_format','-of','json',name],tools,bindings,True).stdout)
        video=next(s for s in data['streams'] if s['codec_type']=='video')
        audio=next(s for s in data['streams'] if s['codec_type']=='audio')
        expected=cues[-1]['end']/FPS if name=='ice-v2-zh.mp4' else 11.6
        assert (video['width'],video['height'],video['avg_frame_rate'],video['pix_fmt'])==(W,H,'30/1','yuv420p')
        assert video['codec_name']=='h264' and audio['codec_name']=='aac'
        assert abs(float(data['format']['duration'])-expected)<.1
        execute('ffmpeg',['-v','error','-xerror','-i',name,'-map','0:v','-map','0:a','-f','null','NUL'],tools,bindings)
        detect=execute('ffmpeg',['-i',name,'-vf','blackdetect=d=0.15:pix_th=0.08','-af','silencedetect=n=-45dB:d=2,ebur128=peak=true','-f','null','NUL','-loglevel','info'],tools,bindings,True)
        (samples/(path.stem+'-analysis.txt')).write_text(detect.stderr,encoding='utf-8')
        assert 'black_start:' not in detect.stderr
        assert 'silence_start:' not in detect.stderr
        reports[name]={'sha256':sha(path),'bytes':path.stat().st_size,'duration':data['format']['duration'],'probe':data,'decode':'PASS','blackdetect':'PASS','silencedetect':'PASS'}
    shots=[]
    for i,c in enumerate(cues):
        second=(c['start']+c['end'])/2/FPS
        path=samples/f'shot-{i+1:02}.png'
        execute('ffmpeg',['-ss',second,'-i','ice-v2-zh.mp4','-frames:v','1',str(path)],tools,bindings)
        with Image.open(path) as im: shots.append(im.resize((270,480),Image.Resampling.LANCZOS))
    sheet=Image.new('RGB',(810,1440),'#fff3de')
    for i,pic in enumerate(shots): sheet.paste(pic,((i%3)*270,(i//3)*480))
    sheet.save(samples/'contact.png')
    for n in (0,15,30,45,60,1440):
        execute('ffmpeg',['-ss',n/FPS,'-i','ice-v2-zh.mp4','-frames:v','1',str(samples/f'frame-{n:04}.png')],tools,bindings)
    for lang in ('zh','en'):
        for cue in cues:
            lines,size=wrapped(cue[lang],lang)
            assert len(lines)*(size+21)<=250
            assert all(font(size,lang=='zh').getlength(line)<=850 for line in lines)
    save(OUT/'qa.json',{'status':'PASS','renderer_sha256':sha(Path(__file__)),'inputs_sha256':sha(HERE/'inputs.json'),'reports':reports,'caption_bounds':'PASS; measured glyph widths and reserved height','molecule_counts':{'liquid':len(WATER),'ice':len(ORDER)},'human_acceptance':'PENDING','market_acceptance':'PENDING'})
    print('QA PASS',flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['preview','render','qa'],required=True)
    args=parser.parse_args()
    cues,tools,bindings=inputs(require_review=args.mode!='preview')
    if args.mode=='preview': preview(cues)
    elif args.mode=='render': render(cues,tools,bindings)
    else: qa(cues,tools,bindings)


if __name__=='__main__': main()
