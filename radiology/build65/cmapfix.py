# -*- coding: utf-8 -*-
"""第65回(tp130422-04) cmap復元。98/102問。数字共通+\\x08->9。括弧固有。
数字 \\x02->2 \\x04->1 \\x05->5 \\x06->3 \\x08->9 guj->2 / 庵x 袷+ ï梢 安- 暗=
括弧: 午前 ±...² -> [...] ; 午後 ô->[ õ->]
PUA(数式)除去。脱落数字 \\x0e \\x13 \\x14 は除去(該当3問のみ軽微)。検証 平成25年2月21日(=2013)。
"""
import re, sys
DIGIT = {'\x04':'1','\x02':'2','\x06':'3','\x05':'5','\x08':'9','઄':'2','અ':'3','આ':'4','ઇ':'5','\x07':'4'}

def fix(text, side):
    s = text
    for k,v in DIGIT.items():
        s = s.replace(k,v)
    s = s.replace('ï','梢').replace('庵','×').replace('袷','＋')
    s = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω])安', '−', s)
    s = re.sub(r'([0-9A-Za-z)）\]］(（])\s*暗\s*', r'\1＝', s)
    if side == 'AM':
        s = re.sub(r'±([A-Za-z0-9μ/･・°℃Ω％% ]{1,8}?)²', r'［\1］', s)
    else:
        s = s.replace('ô','［').replace('õ','］')
    s = re.sub('[\ue000-\uf8ff]', '', s)             # PUA(数式記号)除去
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)
    if side == 'AM':
        s = re.sub(r'1(別冊No[.．]?\s*)(\d+[ＡＢAB]?)3', r'（\1\2）', s)
    else:
        s = re.sub(r'2(別冊No[.．]?\s*)(\d+[ＡＢAB]?)4', r'（\1\2）', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k65'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
