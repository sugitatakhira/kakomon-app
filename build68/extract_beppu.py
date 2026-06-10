# -*- coding: utf-8 -*-
"""第68回 別冊画像の抽出。
厚労省PDFの別冊(a_02:午前 / b_02:午後)は本文が画像のスキャン。
gsでページをラスタ化 → トンボ/No.ヘッダ/フッタをcrop → autotrim → 長辺900px → eam/epm に保存。

ページ対応(目視確認済み):
  午前 No.1-5 → PDF p5-9, No.6-17 → p11-22 （p10は「余白」白紙のため1ページずれる）
  午後 No.1-18 → PDF p5-22 （ずれ無し）
  回転(ROTATE_270): 午前 No.5(運動神経伝導波形)・No.6(脳波)。午後は無し。
"""
import os, subprocess
from PIL import Image, ImageChops

TMP = '/tmp/k68'
AM_PDF = os.path.join(TMP, 'tp220421-07a_02.pdf')
PM_PDF = os.path.join(TMP, 'tp220421-07b_02.pdf')

# No -> PDFページ番号
AM_PAGES = {1:5,2:6,3:7,4:8,5:9,6:11,7:12,8:13,9:14,10:15,
            11:16,12:17,13:18,14:19,15:20,16:21,17:22}
PM_PAGES = {n: n+4 for n in range(1,19)}   # No.1-18 → p5-22
AM_ROT = {5,6}
PM_ROT = set()

def autotrim(im, pad=10, thr=18):
    g = im.convert('L'); bg = Image.new('L', g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda p: 255 if p > thr else 0)
    bb = diff.getbbox()
    if not bb: return im
    l,t,r,b = bb
    return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))

def render(pdf, page, r=150):
    out = os.path.join(TMP, '_pg.png')
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r%d'%r,
                    '-dFirstPage=%d'%page,'-dLastPage=%d'%page,'-sOutputFile='+out,pdf],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Image.open(out).convert('RGB')

def extract(pdf, pages, rot, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no, page in pages.items():
        im = render(pdf, page)
        if no in rot:
            im = im.transpose(Image.ROTATE_270)
        w,h = im.size
        # No.ヘッダ(上)・フッタ/ページ番号(下)・トンボ(外周)を落とす
        im = im.crop((int(w*0.04), int(h*0.115), int(w*0.96), int(h*0.915)))
        im = autotrim(im)
        W,H = im.size; ls = max(W,H)
        if ls > 900:
            im = im.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
        im.save(os.path.join(outdir, 'no%02d.png' % no))
    print(outdir, 'done', len(pages))

if __name__ == '__main__':
    extract(AM_PDF, AM_PAGES, AM_ROT, os.path.join(TMP,'eam'))
    extract(PM_PDF, PM_PAGES, PM_ROT, os.path.join(TMP,'epm'))
