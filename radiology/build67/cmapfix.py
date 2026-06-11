# -*- coding: utf-8 -*-
"""第67回(tp150511-04) は本文がほぼ正常(括弧・数字・漢字OK)。
注記領域の制御文字(\x07/\x08)と特殊空白のみ除去。98/102問構成。"""
import re, sys
def fix(text, side):
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', text)
    s = re.sub(r'\s*[0-9]*\s*TP06mr-\w+-\d+', '', s)  # ページフッタ除去
    s = s.replace(' ','').replace(' ','')
    return s
if __name__=='__main__':
    tmp=sys.argv[1] if len(sys.argv)>1 else '/tmp/k67'
    for side,i,o in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(o,'w',encoding='utf-8').write(fix(open(i,encoding='utf-8').read(),side)); print('fixed',o)
