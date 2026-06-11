# -*- coding: utf-8 -*-
"""第72回(tp200414-06) cmap復元。数字共通、括弧グリフ固有。
数字: \\x02->2 \\x04->1 \\x05->5 \\x06->3 \\x07->4 guj->2 / 庵->x 袷->+ ï->梢 安->- 暗->=
括弧: 午前 @->[ A->] (@...A) / Û->< Ü->>  ; 午後 z->[ {->] / á->< å->>
PUA(私用領域)=数式記号は当該設問を図添付で担保し除去。全角括弧(->1 )->3 は別冊参照のみ。
検証: 令和2年2月20日(=2020,第72回)。
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
    s = s.replace('大¹骨','大腿骨').replace('大²骨','大腿骨')
    if side == 'AM':
        s = re.sub(r'@([^@A\n]{1,12}?)A', r'［\1］', s)
        s = s.replace('Û','〈').replace('Ü','〉')
    else:
        s = re.sub(r'z([A-Za-z0-9/･・°℃Ω％% ]{1,7}?)\{', r'［\1］', s)
        s = s.replace('á','〈').replace('å','〉')
    s = re.sub('[-]', '', s)                 # PUA(数式記号)除去
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)        # 残存制御文字
    s = re.sub(r'1(別冊No[.．]?\s*)(\d+)3', r'（\1\2）', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k72'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
