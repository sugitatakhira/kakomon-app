# -*- coding: utf-8 -*-
"""第74回(tp220421-06) cmap破損の復元。臨床検査技師 第68回(同tp220421-07)と同種だが別コード表。
数字(別フォント=制御文字/Gujarati): \x04→1 \x02→2 \x06→3 \x07→4 \x05→5 ઄→2 અ→3 આ→4 ઇ→5
  \x10→6 \x11→0 (図問題AM76/PMコンデンサの選択肢。当該は図添付で担保)
記号: ï→梢 庵→× 袷→＋ 安→−(英数/ギリシャ隣接時のみ。安全/安定等は保護)
括弧: 午前 ［→L ］→M / 午後 ［→¥ ］→¦ / 全角括弧 （→1 ）→3(別冊・半影のみ文脈復元)
検証: 「令和\x07年\x02月17日」→令和4年2月17日, 「઄つ選べ」→2つ選べ, 「512庵512」→512×512。
"""
import re, sys

DIGIT = {'\x04':'1','\x02':'2','\x06':'3','\x07':'4','\x05':'5',
         '઄':'2','અ':'3','આ':'4','ઇ':'5','\x10':'6','\x11':'0'}

def fix(text, side):
    s = text
    # 1) 数字フォント
    for k,v in DIGIT.items():
        s = s.replace(k, v)
    # 2) 記号
    s = s.replace('ï','梢').replace('庵','×').replace('袷','＋')
    # 安→−（英数・ギリシャ・βに隣接する連結子のみ。安全/安定/安静/不安等は保護）
    s = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ωβγδ｜])安', '−', s)
    # 暗→＝（英数隣接時のみ＝記号。空白を挟む場合あり。明暗/暗号等の漢字は保護）
    s = re.sub(r'([0-9A-Za-z])\s*暗\s*', r'\1＝', s)
    # 3) 括弧(単位)
    if side == 'AM':
        s = re.sub(r'L([A-Za-zμΩ℃°/･・％%0-9]{1,6}?)M', r'［\1］', s)
        s = re.sub(r'>([^>?\n]{1,18}?)\?', r'〈\1〉', s)   # 〈略号/読み〉(IMRT/ラーモア/センチ等)
    else:
        s = s.replace('¥','［').replace('¦','］')
    # 4) 全角括弧（→1 ）→3 は実数字と衝突。高信頼の文脈のみ復元。
    s = re.sub(r'1(別冊No[.．]?\s*)(\d+)3', r'（\1\2）', s)   # 別冊参照
    s = re.sub(r'1(半影)3', r'（\1）', s)                        # （半影）
    s = re.sub(r'1(令和[0-9年月日 ]+?)3', r'（\1）', s)          # 日付(注記)
    return s

if __name__ == '__main__':
    tmp = sys.argv[1] if len(sys.argv)>1 else '/tmp/k74'
    for side,inp,out in [('AM',f'{tmp}/am.txt',f'{tmp}/am_fixed.txt'),
                         ('PM',f'{tmp}/pm.txt',f'{tmp}/pm_fixed.txt')]:
        open(out,'w',encoding='utf-8').write(fix(open(inp,encoding='utf-8').read(), side))
        print('fixed', out)
