# -*- coding: utf-8 -*-
"""第64回(tp_siken_64_rad) cmap復元。98/102問。最古層。数字共通、括弧固有、脱字多い。
数字 \\x02->2 \\x04->1 \\x05->5 \\x07->4 guj->2 / 庵x 袷+ ï梢 安- 暗=
文脈脱字: \\x08平->扁平 \\x0f孔->穿孔 \\x18->腿(下腿) \\x10進->10進。残脱字コードは除去(該当少数)。
括弧: 午前 Æ->[ Ç->] / \\x97-><  \\x99->> ; 全角括弧 午前(→1)→3 午後(→2)→4(別冊参照)。
PUA(数式)除去。検証 平成24年2月23日(=2012)。
"""
import re, sys
DIGIT = {'\x04':'1','\x02':'2','\x05':'5','\x07':'4','઄':'2','અ':'3','આ':'4','ઇ':'5'}

def fix(text, side):
    s = text
    # 文脈脱字(数字置換の前に)
    s = s.replace('\x08平','扁平').replace('\x0f孔','穿孔').replace('\x18','腿').replace('\x10進','10進')
    for k,v in DIGIT.items():
        s = s.replace(k,v)
    s = s.replace('ï','梢').replace('庵','×').replace('袷','＋')
    s = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω])安', '−', s)
    s = re.sub(r'([0-9A-Za-z)）\]］(（])\s*暗\s*', r'\1＝', s)
    if side == 'AM':
        s = s.replace('Æ','［').replace('Ç','］')
        s = s.replace('\x97','〈').replace('\x99','〉')
        s = re.sub(r'1(別冊No[.．]?\s*)(\d+[ＡＢAB]?)3', r'（\1\2）', s)
    else:
        s = re.sub(r'2(別冊No[.．]?\s*)(\d+[ＡＢAB]?)4', r'（\1\2）', s)
    s = re.sub('[\ue000-\uf8ff]', '', s)             # PUA(数式記号)除去
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k64'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
