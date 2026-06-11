# -*- coding: utf-8 -*-
"""第73回(tp210416-06) cmap復元。数字は74回等と共通、括弧グリフが固有。
数字: \x02→2 \x04→1 \x05→5 \x06→3 \x07→4 ઄→2 / 記号: 庵→× 袷→＋ ï→梢 安→− 暗→＝
腿: ¹(AM)/｜(PM)→腿(大腿骨)
括弧: 午前 £→［ ¥→］・\x19→〈 \x1B→〉 / 午後 $→［ ( 文脈→］・½→〈 À→〉
全角括弧（→1 ）→3 は別冊参照のみ文脈復元。ASCII () は数式で実使用のため保持。
検証: 「令和\x06年\x02月18日」→令和3年2月18日(=2021), 「઄つ選べ/\x02つ選べ」→2つ選べ。
"""
import re, sys
DIGIT = {'\x04':'1','\x02':'2','\x06':'3','\x07':'4','\x05':'5','઄':'2','અ':'3','આ':'4','ઇ':'5'}

def fix(text, side):
    s = text
    for k,v in DIGIT.items(): s = s.replace(k,v)
    s = s.replace('ï','梢').replace('庵','×').replace('袷','＋')
    s = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ωβγδ｜])安', '−', s)
    s = re.sub(r'([0-9A-Za-z)）\]］])\s*暗\s*', r'\1＝', s)
    s = s.replace('大¹骨','大腿骨').replace('大｜骨','大腿骨').replace('大|骨','大腿骨')
    if side == 'AM':
        s = s.replace('£','［').replace('¥','］')
        s = s.replace('\x19','〈').replace('\x1b','〉')
    else:
        s = s.replace('½','〈').replace('\xc0','〉')   # À→〉
        s = re.sub(r'\$([^$\n（）]*?)\(', r'［\1］', s)   # ［単位］ ($...( )
        s = s.replace('$','［')                          # 残$は開き括弧
    s = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', s)  # 残存制御文字(注記バブル/脱落値)を除去
    # 別冊参照の全角括弧
    s = re.sub(r'1(別冊No[.．]?\s*)(\d+)3', r'（\1\2）', s)
    s = re.sub(r'1(令和[0-9年月日 ]+?)3', r'（\1）', s)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k73'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
