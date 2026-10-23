import numpy as np
from PIL import Image
src='/root/.claude/uploads/7db5e8a6-d495-596a-8941-a726d2c69b08/f163953e-image.png'
A=np.asarray(Image.open(src).convert('RGB')).astype(float)
H,W,_=A.shape; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W]; r=np.hypot(yy-cy,xx-cx)
R,G,B=A[...,0],A[...,1],A[...,2]
bgm=(R<60)&(B>R+20)&(G<80)
# find center of radial gradient: use brightness-weighted centroid of bg pixels
w=(B*bgm)**4; ccy=(yy*w).sum()/w.sum(); ccx=(xx*w).sum()/w.sum(); print('center',ccy,ccx)
r=np.hypot(yy-ccy,xx-ccx)
nb=int(r.max())+2; prof=np.zeros((nb,3)); cnt=np.zeros(nb)
ri=r.astype(int)
for c in range(3): np.add.at(prof[:,c],ri[bgm],A[...,c][bgm])
np.add.at(cnt,ri[bgm],1)
ok=cnt>20; idx=np.arange(nb)
P=np.stack([np.interp(idx,idx[ok],prof[ok,c]/cnt[ok]) for c in range(3)],1)
# smooth
k=np.ones(15)/15; P=np.stack([np.convolve(np.pad(P[:,c],7,mode='edge'),k,'valid') for c in range(3)],1)
def bgimg(h,w,cy,cx,scale):
    yy,xx=np.mgrid[0:h,0:w]; rr=np.hypot(yy-cy,xx-cx)/scale
    rr=np.clip(rr,0,nb-1); i=rr.astype(int); f=(rr-i)[...,None]; j=np.minimum(i+1,nb-1)
    return P[i]*(1-f)+P[j]*f
BG=bgimg(H,W,ccy,ccx,1.0)
d=A-BG
aR=(R-BG[...,0])/np.maximum(235-BG[...,0],1)
aS=((R-B)-(BG[...,0]-BG[...,2]))/150
a=np.clip(np.maximum(aR,aS),0,1)
a[a<0.04]=0
Fc=np.clip((A-(1-a[...,None])*BG)/np.maximum(a[...,None],1e-3),0,255)
fg=np.dstack([Fc,a*255]).astype(np.uint8)
FG=Image.fromarray(fg,'RGBA')
bb=FG.getbbox(); print('bbox',bb)
# check recomposite error
rec=Fc*a[...,None]+BG*(1-a[...,None]); print('err',np.abs(rec-A).mean())
out='/home/claude/apk/assets/'
Image.open(src).convert('RGB').save(out+'icon-only.png')
Image.fromarray(BG.astype(np.uint8)).save(out+'icon-background.png')
crop=FG.crop(bb); cw,ch=crop.size
# foreground: content fits within 62% width of 1024 (safe zone 66%)
s=0.62*1024/max(cw,ch); c2=crop.resize((round(cw*s),round(ch*s)),Image.LANCZOS)
fgc=Image.new('RGBA',(1024,1024),(0,0,0,0)); fgc.paste(c2,((1024-c2.width)//2,(1024-c2.height)//2),c2); fgc.save(out+'icon-foreground.png')
# splash 2732: logo content ~ 1100px wide
S=2732; sc=1100/cw
sbg=bgimg(S,S,S/2,S/2,sc*1.6)
sp=Image.fromarray(sbg.astype(np.uint8)).convert('RGBA')
c3=crop.resize((round(cw*sc),round(ch*sc)),Image.LANCZOS)
sp.paste(c3,((S-c3.width)//2,(S-c3.height)//2),c3); sp=sp.convert('RGB'); sp.save(out+'splash.png'); sp.save(out+'splash-dark.png')
# preview
pv=Image.new('RGB',(1300,440),(255,255,255))
icon=Image.alpha_composite(Image.fromarray(BG.astype(np.uint8)).convert('RGBA'),fgc).resize((400,400),Image.LANCZOS)
from PIL import ImageDraw
m=Image.new('L',(400,400),0); ImageDraw.Draw(m).ellipse((0,0,399,399),fill=255); pv.paste(icon,(20,20),m)
m2=Image.new('L',(400,400),0); ImageDraw.Draw(m2).rounded_rectangle((0,0,399,399),90,fill=255); pv.paste(icon,(450,20),m2)
pv.paste(sp.resize((400,400)),(880,20)); pv.save('/home/claude/apk/icon_preview.png')
