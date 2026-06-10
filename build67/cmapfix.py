# -*- coding: utf-8 -*-
"""第67回(tp210416) 専用 cmap破損の置換。第68回(cmapfix.py)と同型だが別コード表。
検証: 「令和\x08年\x02月 17 日」→「令和3年2月17日」(=令和3年=2021=第67回)。
"""
import re

# 数字（制御文字/グジャラート文字に誤マップ）
DIGIT = {
    '\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3',
    '\x11':'0','\x12':'8',        # bold体: クロスミキシング比 10:0,8:2,5:5,2:8,0:10 で確定
    '\x14':'6',                    # 「6塩基の繰り返しDNA配列」(テロメアTTAGGG=6bp。B8選択肢5=誤答)
    '\x1e':'1',                    # 「総赤血球数の約1%」(網赤血球。B65選択肢3=誤答)
    '઄':'2','ઃ':'3','આ':'4',
}
# 記号→漢字に化けたもの
KANJI = {
    '\x0e':'梢','\x96':'梢',       # 末梢血
    '\x1c':'穿',                    # 穿刺
    '\x10':'扁',                    # 扁平上皮
}
# 括弧（第68回の慣例に合わせ 略号=〈〉 / 単位・変数=［］）
BRACKET = {
    '\x95':'〈','§':'〉',          # 略号展開 APACHE〈...〉
    'õ':'〈','ø':'〉',             # 略号 〈FITC〉〈感染症法〉
    '\x1a':'［','\x1b':'］',        # 変数/単位 ［S］［U/L］
    '¯':'［','°':'］',             # 単位 ［mmHg］［g/dL］［mL］［kg］
}

def fix(text):
    text = text.replace('\x0c','\n')
    for k,v in {**DIGIT,**KANJI,**BRACKET}.items():
        text = text.replace(k,v)
    text = text.replace('庵','×')                       # 乗算記号（実在の庵なし）
    text = text.replace('袷','+')                       # イオン価・凝集判定の+
    text = re.sub(r'暗(?!号)','≒',text)                # ≒（ただし「暗号」は保護）
    # 安→⁻（「安全/安定/安静/不安」等は保護。数字・ラテン・ギリシャ隣接時のみ）
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安','⁻',text)
    text = re.sub(r'安(?=[0-9A-Za-z])','⁻',text)
    # 別冊参照の全角括弧復元（（→0,）→2）。改行で「別\n冊」に割れる場合に対応
    def _beppu(m):
        import re as _r
        return '（別冊No. %s）' % _r.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _beppu, text)
    # その他の全角括弧（単一語）: （左）（右）
    text = text.replace('0左2','（左）').replace('0右2','（右）')
    # 10のべき指数（負号対応）: 「× 10-8」→「×10^-8」
    text = re.sub(r'×\s*10(-?\d+)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix67:', sys.argv[1],'->',sys.argv[2])
