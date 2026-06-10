# -*- coding: utf-8 -*-
from PIL import Image, ImageChops
import os
ROT = {'eam':{3}, 'epm':{2,4}}
def autotrim(im, pad=8):
    g = im.convert('L'); bg = Image.new('L', g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda p: 255 if p > 12 else 0)
    bbox = diff.getbbox()
    if not bbox: return im
    l,t,r,b = bbox
    return im.crop((max(0,l-pad),max(0,t-pad),min(im.size[0],r+pad),min(im.size[1],b+pad)))
def process(srcdir, maxno, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no in range(1, maxno+1):
        page = no + 4
        im = Image.open('%s/p-%02d.png'%(srcdir,page)).convert('RGB')
        if no in ROT.get(outdir,set()):
            im = im.transpose(Image.ROTATE_270); rot=True
        else: rot=False
        w,h = im.size
        if rot: crop = im.crop((int(w*0.09), int(h*0.11), int(w*0.985), int(h*0.97)))
        else:   crop = im.crop((int(w*0.05), int(h*0.11), int(w*0.95), int(h*0.93)))
        crop = autotrim(crop)
        W,H = crop.size; ls=max(W,H)
        if ls>900: crop = crop.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
        crop.save('%s/no%02d.png'%(outdir,no))
    print(outdir,'done',maxno)
process('bam',14,'eam'); process('bpm',16,'epm')
