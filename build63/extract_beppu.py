# -*- coding: utf-8 -*-
"""第63回 別冊抽出。a_02:午前(No.1-16,p5-20)/b_02:午後(No.1-15,p5-19)。page=No+4、余白なし。
回転(ROTATE_270): 午前No.3(Holter心電図)/No.4(スパイログラム)/No.5(フローボリューム)、午後No.2(心電図)/No.3(単一窒素呼出曲線)。
"""
import os, subprocess
from PIL import Image, ImageChops
TMP='/tmp/k63'
AM_PDF=os.path.join(TMP,'tp170425-07a_02.pdf'); PM_PDF=os.path.join(TMP,'tp170425-07b_02.pdf')
AM_PAGES={n:n+4 for n in range(1,17)}; PM_PAGES={n:n+4 for n in range(1,16)}
AM_ROT={3,4,5}; PM_ROT={2,3}
def autotrim(im,pad=10,thr=18):
    g=im.convert('L');bg=Image.new('L',g.size,255)
    diff=ImageChops.difference(g,bg).point(lambda p:255 if p>thr else 0);bb=diff.getbbox()
    if not bb:return im
    l,t,r,b=bb;return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))
def render(pdf,page,r=150):
    out=os.path.join(TMP,'_pg.png')
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r%d'%r,'-dFirstPage=%d'%page,'-dLastPage=%d'%page,'-sOutputFile='+out,pdf],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return Image.open(out).convert('RGB')
def extract(pdf,pages,rot,outdir):
    os.makedirs(outdir,exist_ok=True)
    for no,page in pages.items():
        im=render(pdf,page)
        if no in rot: im=im.transpose(Image.ROTATE_270)
        w,h=im.size; im=im.crop((int(w*0.04),int(h*0.115),int(w*0.96),int(h*0.915))); im=autotrim(im)
        W,H=im.size; ls=max(W,H)
        if ls>900: im=im.resize((round(W*900/ls),round(H*900/ls)),Image.LANCZOS)
        im.save(os.path.join(outdir,'no%02d.png'%no))
    print(outdir,'done',len(pages))
if __name__=='__main__':
    extract(AM_PDF,AM_PAGES,AM_ROT,os.path.join(TMP,'eam'))
    extract(PM_PDF,PM_PAGES,PM_ROT,os.path.join(TMP,'epm'))
