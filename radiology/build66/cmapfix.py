# -*- coding: utf-8 -*-
"""第66回(tp140512-04) は本文がほぼ正常(ASCII括弧[kV]・数字OK)。
別冊参照のスペース正規化(別冊 No→別冊No)・ページフッタ(HAP06)・制御文字のみ除去。98/102問。"""
import re, sys
def fix(text, side):
    s = re.sub(r'別\s*冊\s*No','別冊No',text)
    s = re.sub(r'\s*[0-9]*\s*HAP06\w+-\w+','',s)
    s = re.sub(r'\s*―\s*\d+\s*―\s*-?\d*','',s)  # ページフッタ ― N ―-NN
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]','',s)
    return s
if __name__=='__main__':
    tmp=sys.argv[1] if len(sys.argv)>1 else '/tmp/k66'
    for side,i,o in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(o,'w',encoding='utf-8').write(fix(open(i,encoding='utf-8').read(),side)); print('fixed',o)
