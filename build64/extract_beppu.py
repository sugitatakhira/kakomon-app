# -*- coding: utf-8 -*-
"""第64回 別冊抽出。a_02:午前(No.1-12,p5-16)/b_02:午後(No.1-12,p5-16)。page=No+4、余白なし。
回転(ROTATE_270): 線グラフ系＝午前No.2(左室圧容積)/No.3(心電図)/No.4(反応タイムコース)、午後No.2(心電図)/No.3(フローボリューム)。
午前No.12は連問(問題83,84)の蛍光抗体、午後No.12=12Ａ/Ｂ(問題88)。
"""
import os, subprocess
from PIL import Image, ImageChops
TMP='/tmp/k64'
AM_PDF=os.path.join(TMP,'tp180511-07a_02.pdf'); PM_PDF=os.path.join(TMP,'tp180511-07b_02.pdf')
AM_PAGES={n:n+4 for n in range(1,13)}; PM_PAGES={n:n+4 for n in range(1,13)}
AM_ROT={2,3,4}; PM_ROT={2,3}
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
