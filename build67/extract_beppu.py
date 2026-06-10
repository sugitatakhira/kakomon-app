# -*- coding: utf-8 -*-
"""第67回 別冊画像の抽出。a_02:午前 / b_02:午後 のスキャンPDF。
ページ対応(目視確認済み): 午前・午後とも No.1-13 → PDF p5-17（page=No+4。68と違い余白ページ無し、p18以降は裏表紙等の白紙）。
回転: 67には脳波/運動神経伝導の別冊が無く、心電図・フローボリューム等はすべて正立 → 回転なし。
午前No.10=10Ａ/Ｂ、午後No.13=13Ａ/Ｂは1ページに両図（そのまま使用）。
"""
import os, subprocess
from PIL import Image, ImageChops

TMP = '/tmp/k67'
AM_PDF = os.path.join(TMP,'tp210416-07a_02.pdf')
PM_PDF = os.path.join(TMP,'tp210416-07b_02.pdf')
AM_PAGES = {n: n+4 for n in range(1,14)}   # No.1-13 → p5-17
PM_PAGES = {n: n+4 for n in range(1,14)}
AM_ROT = set(); PM_ROT = set()

def autotrim(im, pad=10, thr=18):
    g=im.convert('L'); bg=Image.new('L',g.size,255)
    diff=ImageChops.difference(g,bg).point(lambda p:255 if p>thr else 0); bb=diff.getbbox()
    if not bb: return im
    l,t,r,b=bb
    return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))

def render(pdf, page, r=150):
    out=os.path.join(TMP,'_pg.png')
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r%d'%r,
                    '-dFirstPage=%d'%page,'-dLastPage=%d'%page,'-sOutputFile='+out,pdf],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Image.open(out).convert('RGB')

def extract(pdf, pages, rot, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no,page in pages.items():
        im=render(pdf,page)
        if no in rot: im=im.transpose(Image.ROTATE_270)
        w,h=im.size
        im=im.crop((int(w*0.04),int(h*0.115),int(w*0.96),int(h*0.915)))
        im=autotrim(im)
        W,H=im.size; ls=max(W,H)
        if ls>900: im=im.resize((round(W*900/ls),round(H*900/ls)),Image.LANCZOS)
        im.save(os.path.join(outdir,'no%02d.png'%no))
    print(outdir,'done',len(pages))

if __name__=='__main__':
    extract(AM_PDF, AM_PAGES, AM_ROT, os.path.join(TMP,'eam'))
    extract(PM_PDF, PM_PAGES, PM_ROT, os.path.join(TMP,'epm'))
