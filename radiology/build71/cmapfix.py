# -*- coding: utf-8 -*-
"""第71回(tp190415-06) cmap復元。数字共通、括弧グリフ固有。
数字 \\x02->2 \\x04->1 \\x05->5 \\x06->3 \\x07->4 guj->2 / 庵x 袷+ ï梢 安- 暗=
括弧: 午前 '...)->[ ] / ô-><  ö->> ; 午後 )...*->[ ] / \\x8b-><  \\x92->>
脱字: \\x10->扁(扁平骨) É->腿(大腿) à->腿(太腿) Ú->鞘(神経鞘腫)
検証 平成31年2月21日(=2019,第71回)。
"""
import re, sys
DIGIT = {'\x04':'1','\x02':'2','\x06':'3','\x07':'4','\x05':'5','઄':'2','અ':'3','આ':'4','ઇ':'5'}

def fix(text, side):
    s = text
    for k,v in DIGIT.items():
        s = s.replace(k,v)
    s = s.replace('ï','梢').replace('庵','×').replace('袷','＋')
    s = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω])安', '−', s)
    s = re.sub(r'([0-9A-Za-z)）\]］(（])\s*暗\s*', r'\1＝', s)
    s = s.replace('大É骨','大腿骨').replace('太à','太腿').replace('神経Ú腫','神経鞘腫')
    s = s.replace('\x10','扁')
    if side == 'AM':
        s = re.sub(r"'([A-Za-z0-9μ/･・°℃Ω％% ]{1,10}?)\)", r'［\1］', s)
        s = s.replace('ô','〈').replace('ö','〉')
    else:
        s = re.sub(r'\)([A-Za-z0-9μ/･・°℃Ω％% ]{1,10}?)\*', r'［\1］', s)
        s = s.replace('\x8b','〈').replace('\x92','〉')
    s = re.sub('[\ue000-\uf8ff]', '', s)  # PUA(数式記号)除去
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)
    s = re.sub(r'1(別冊No[.．]?\s*)(\d+)3', r'（\1\2）', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k71'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
