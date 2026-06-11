# -*- coding: utf-8 -*-
"""第61回 別冊抽出。午前 No.1-12=am_02(page=No+4)、午後 No.1-15=pm_02(page=No+4)。
心電図(午前No.3/午後No.3)は ROTATE_270。余白は自動トリム。"""
import os, subprocess
from PIL import Image, ImageChops
HERE=os.path.dirname(__file__); TMP='/tmp/k61'
AM=os.path.join(HERE,'am_02.pdf'); PM=os.path.join(HERE,'pm_02.pdf')
AM_PAGES={n:(AM,n+4) for n in range(1,13)}
PM_PAGES={n:(PM,n+4) for n in range(1,16)}
AM_ROT={3}; PM_ROT={3}
def autotrim(im,pad=10,thr=18):
    g=im.convert('L');bg=Image.new('L',g.size,255)
    diff=ImageChops.difference(g,bg).point(lambda p:255 if p>thr else 0);bb=diff.getbbox()
    if not bb:return im
    l,t,r,b=bb;return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))
def render(pdf,page,r=150):
    out=os.path.join(TMP,'_pg.png')
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r%d'%r,'-dFirstPage=%d'%page,'-dLastPage=%d'%page,'-sOutputFile='+out,pdf],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return Image.open(out).convert('RGB')
def extract(pages,rot,outdir):
    os.makedirs(outdir,exist_ok=True)
    for no,(pdf,page) in pages.items():
        im=render(pdf,page)
        if no in rot: im=im.transpose(Image.ROTATE_270)
        w,h=im.size; im=im.crop((int(w*0.04),int(h*0.115),int(w*0.96),int(h*0.915))); im=autotrim(im)
        W,H=im.size; ls=max(W,H)
        if ls>900: im=im.resize((round(W*900/ls),round(H*900/ls)),Image.LANCZOS)
        im.save(os.path.join(outdir,'no%02d.png'%no))
    print(outdir,'done',len(pages))
if __name__=='__main__':
    os.makedirs(TMP,exist_ok=True)
    extract(AM_PAGES,AM_ROT,os.path.join(TMP,'eam'))
    extract(PM_PAGES,PM_ROT,os.path.join(TMP,'epm'))
