# -*- coding: utf-8 -*-
"""第69回(tp170425-06) cmap復元。数字共通、括弧グリフ固有。
数字 \\x02->2 \\x04->1 \\x05->5 \\x06->3 \\x07->4 guj->2 / 庵x 袷+ ï梢 安- 暗=
括弧: 午前 ®...µ -> <...> (µは単位と衝突するため正規表現) / 午後 \\x1A-><  \\x1C->>
脱字: \\x14->穿(午前) \\x11->0 \\x9f->腿 神経Ç腫->神経鞘腫(午後)。PUA(数式)除去。
検証 平成29年2月23日(=2017,第69回)。
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
    if side == 'AM':
        s = re.sub(r'®([^®µ\n]{1,16}?)µ', r'〈\1〉', s)
        s = s.replace('\x14','穿')
    else:
        s = s.replace('\x1a','〈').replace('\x1c','〉')
        s = s.replace('\x11','0')
        s = s.replace('下\x9f','下腿').replace('\x9f','腿')
        s = s.replace('神経Ç腫','神経鞘腫').replace('末Ç','末梢').replace('Ç','梢')
    s = re.sub('[\ue000-\uf8ff]', '', s)              # PUA(数式記号)除去
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)
    s = re.sub(r'1(別冊No[.．]?\s*)(\d+)3', r'（\1\2）', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k69'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
