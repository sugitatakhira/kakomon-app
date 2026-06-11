# -*- coding: utf-8 -*-
"""第64回 別冊抽出。ink解析で内容頁が連続・回転なし→ page=No+4。
午前 No.1-9=p5-13、午後 No.1-10=p5-14。出力 eam/epm の noNN.png(長辺900px)。"""
from PIL import Image, ImageChops
import os, sys
AM_MAP = {n:[n+4] for n in range(1,10+1)}
PM_MAP = {n:[n+4] for n in range(1,7+1)}
ROT = {'eam': set(), 'epm': set()}
def autotrim(im, pad=8):
    g=im.convert('L'); diff=ImageChops.difference(g,Image.new('L',g.size,255)).point(lambda p:255 if p>12 else 0)
    bb=diff.getbbox()
    if not bb: return im
    l,t,r,b=bb; return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))
def load_trim(srcdir,page,rot):
    im=Image.open('%s/p-%02d.png'%(srcdir,page)).convert('RGB')
    if rot: im=im.transpose(Image.ROTATE_270)
    w,h=im.size; return autotrim(im.crop((int(w*0.05),int(h*0.07),int(w*0.95),int(h*0.95))))
def hcat(ims,gap=12):
    H=max(i.size[1] for i in ims); W=sum(i.size[0] for i in ims)+gap*(len(ims)-1)
    out=Image.new('RGB',(W,H),(255,255,255)); x=0
    for i in ims: out.paste(i,(x,(H-i.size[1])//2)); x+=i.size[0]+gap
    return out
def process(srcdir,pmap,outdir):
    os.makedirs(outdir,exist_ok=True)
    for no,pages in sorted(pmap.items()):
        rot=no in ROT.get(os.path.basename(outdir),set())
        tiles=[load_trim(srcdir,p,rot) for p in pages]
        im=tiles[0] if len(tiles)==1 else hcat(tiles)
        W,H=im.size; ls=max(W,H)
        if ls>900: im=im.resize((round(W*900/ls),round(H*900/ls)),Image.LANCZOS)
        im.save('%s/no%02d.png'%(outdir,no))
    print(outdir,'done',len(pmap))
if __name__=='__main__':
    TMP=sys.argv[1] if len(sys.argv)>1 else '/tmp/k64'
    process(os.path.join(TMP,'bam'),AM_MAP,os.path.join(TMP,'eam'))
    process(os.path.join(TMP,'bpm'),PM_MAP,os.path.join(TMP,'epm'))
