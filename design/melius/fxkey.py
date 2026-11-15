import numpy as np, json, glob, sys, os
from PIL import Image, ImageSequence
OUT='../../assets/fx'
NAMES={1:'play-shockwave',2:'pause-cracks',3:'seek-comet',4:'slot-pop',5:'scrub-spatter',6:'volume-ripples',7:'mute-blot',8:'wheel-bloom',9:'card-dissolve',10:'paused-smoke'}
LOOP={5,6,10}
def key(a):
    R,G,B=a[...,0],a[...,1],a[...,2]
    m=np.minimum(R,B)-G
    cm=np.concatenate([m[:12,:12].ravel(),m[-12:,-12:].ravel()])
    mbg=np.median(cm)
    bgc=np.median(np.concatenate([a[:12,:12].reshape(-1,3),a[-12:,-12:].reshape(-1,3)]),axis=0)
    lo,hi=40.0,mbg-30
    al=np.clip((hi-m)/(hi-lo),0,1)
    safe=np.maximum(al,0.06)[...,None]
    c=np.clip((a-(1-safe)*bgc)/safe,0,255)
    # kill any magenta/purple residue, keep vermillion (low blue)
    r,g,b=c[...,0],c[...,1],c[...,2]
    purple=(b>g+18)&(r>g+18)
    grey=(r+g+b)/3
    for ch in range(3): c[...,ch]=np.where(purple,grey*0.85,c[...,ch])
    return np.dstack([c,al*255])
meta=json.load(open(f'{OUT}/fx.json')) if os.path.exists(f'{OUT}/fx.json') else {}
for n,name in NAMES.items():
    if str(n) not in sys.argv[1:]: continue
    im=Image.open(f'rawfx/fx{n:02d}.gif')
    frames=[];durs=[]
    for i,fr in enumerate(ImageSequence.Iterator(im)):
        a=np.asarray(fr.convert('RGB')).astype(np.float32)
        k=key(a)
        if n==1 and i>=2:
            h,w=k.shape[:2]; yy,xx=np.mgrid[:h,:w]
            k[...,3][(yy-h/2)**2+(xx-w/2)**2<38**2]=0
        frames.append(Image.fromarray(k.astype(np.uint8),'RGBA'))
        durs.append(fr.info.get('duration',im.info.get('duration',60)))
    w,h=frames[0].size
    frames[0].save(f'{OUT}/{name}.webp',save_all=True,append_images=frames[1:],duration=durs,loop=0 if n in LOOP else 1,lossless=False,quality=90,method=2)
    sheet=Image.new('RGBA',(w*len(frames),h),(0,0,0,0))
    for i,f in enumerate(frames): sheet.paste(f,(i*w,0))
    sheet.save(f'{OUT}/{name}-sheet.webp',quality=90,method=2)
    meta[name]={'frames':len(frames),'frameWidth':w,'frameHeight':h,'durationsMs':durs,'loop':n in LOOP,'sheet':f'{name}-sheet.webp','animated':f'{name}.webp'}
    print(name,len(frames),durs[:3])
    json.dump(meta,open(f'{OUT}/fx.json','w'),indent=1)
json.dump(meta,open(f'{OUT}/fx.json','w'),indent=1)
