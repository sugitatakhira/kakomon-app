# -*- coding: utf-8 -*-
"""第66回(tp200414) 専用 cmap破損の置換。第67/68回と同型だが別コード表。
検証: 「令和\x02年\x02月 19 日」→「令和2年2月19日」(=令和2年=2020=第66回)。
"""
import re

DIGIT = {
    '\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3','\x0f':'0',
    '઄':'2','ઃ':'3','આ':'4',
}
KANJI = {
    'æ':'梢',                       # 末梢血
    '\x0e':'扁',                    # 扁平上皮
    '\x10':'穿',                    # 穿刺
}
BRACKET = {
    '½':'〈','¿':'〉',             # 略号 〈RI〉〈ADA〉〈eGFR〉
    '¢':'［','¤':'］',             # 単位 ［nm］［Torr］［mmol/L］
}

def fix(text):
    text = text.replace('\x0c','\n')
    # 略号の山括弧（\x04…\x05 は午後で 略号 〈Vmax〉〈OC〉〈Hb〉等を囲む。数字1/5より先に処理）
    text = re.sub(r'\x04([A-Za-z][A-Za-z0-9/\-]*)\x05', r'〈\1〉', text)
    for k,v in {**DIGIT,**KANJI,**BRACKET}.items():
        text = text.replace(k,v)
    text = text.replace('袷','+')                       # イオン価・凝集判定の+
    text = re.sub(r'暗(?!号)','≒',text)                # ≒（「暗号」は保護）
    # 安→⁻（「安全/安定/安静/不安」等は保護。数字・ラテン・ギリシャ隣接時のみ）
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安','⁻',text)
    text = re.sub(r'安(?=[0-9A-Za-z])','⁻',text)
    # 別冊参照の全角括弧復元（改行で「別\n冊」に割れる場合に対応）
    def _beppu(m):
        import re as _r
        return '（別冊No. %s）' % _r.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _beppu, text)
    text = text.replace('0左2','（左）').replace('0右2','（右）')
    # 10のべき指数（負号対応）
    text = re.sub(r'×\s*10(-?\d+)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix66:', sys.argv[1],'->',sys.argv[2])
