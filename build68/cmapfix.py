# -*- coding: utf-8 -*-
"""第68回(tp220421) 専用 cmap破損の置換。
本文PDF(a_01/b_01)を pdftotext -layout で抽出したテキストは一部グリフが誤マップされる。
HANDOFFの確定置換表に基づき復元する。検証: 「令和\x06年\x02月」→「令和4年2月」(=令和4年=2022=第68回)。
"""
import re

# 数字（制御文字 / グジャラート文字に誤マップ。bold体は別コード）
DIGIT = {
    '\x02': '2', '\x04': '1', '\x05': '5', '\x06': '4', '\x08': '3',
    '\x17': '1',            # bold 1
    '઄': '2',          # ઄
    'ઃ': '3',          # ઃ (前文の例)
    'આ': '4',          # આ (前文の例)
}
# 括弧類
BRACKET = {
    '\x13': '〈', '\x14': '〉',   # 略号の山括弧
    '»': '〈', '¼': '〉',
    '\x8b': '［', '\x8c': '］',   # 単位の角括弧 [dB] 等
}
# 記号（漢字に化けたもの。文脈限定で置換）
#   º→梢(末梢)  \x19→穿(穿刺)  暗→≒  庵→×  安→⁻
SIMPLE = {
    'º': '梢', '\x19': '穿', '暗': '≒',
}

def fix(text):
    text = text.replace('\x0c', '\n')   # 改ページ(FF)は改行に
    # 1) 数字・括弧・単純記号
    for k, v in {**DIGIT, **BRACKET, **SIMPLE}.items():
        text = text.replace(k, v)
    # 2) 末梢・穿刺の語確定（念のため）
    text = text.replace('末梢血', '末梢血')
    # 3) 庵→×（数式の乗算記号。数字に隣接する庵のみ）
    text = re.sub(r'庵', '×', text)  # 第68回に実在の「庵」は無い（全て乗算記号）
    # 4) 安→⁻（数式/略号。ただし「安全」「医療安全」等の実在語は保護）
    text = text.replace('量安反応', '量-反応')          # 量-反応関係（疫学）
    # 安は「安全/医療安全」が大半。数字・ラテン・ギリシャ文字に隣接する安のみ ⁻ に。
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安', '⁻', text)
    text = re.sub(r'安(?=[0-9A-Za-z])', '⁻', text)
    # 5) 略号の丸括弧（（→*, ）→-）: 「*SLE-」→「（SLE）」
    text = re.sub(r'\*([A-Za-z0-9]+)-', r'（\1）', text)
    # 6) 袷→＋（イオン価・凝集判定の+）: 「Mg2袷」→「Mg2+」「4袷」→「4+」
    text = text.replace('袷', '+')
    # 7) 全角括弧（（→0, ）→2）の復元: 別冊参照を確実に復元
    #    例「標本0別冊No. 12を」→「標本（別冊No. 1）を」
    text = re.sub(r'0(別冊No\.?\s*[0-9０-９]+[ＡＢ]?)2', r'（\1）', text)
    # 8) 個別の内側括弧復元（0=（,2=） が数字と衝突するため固有名を直指定）
    text = text.replace('NAD0P2H', 'NAD（P）H')
    text = text.replace('ERBB20HER22', 'ERBB2（HER2）')
    # 9) 10のべき指数が脱落した科学表記: 「× 103」→「×10^3」
    text = re.sub(r'×\s*10(\d+)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    src = open(sys.argv[1], encoding='utf-8').read()
    out = fix(src)
    open(sys.argv[2], 'w', encoding='utf-8').write(out)
    print('cmapfix:', sys.argv[1], '->', sys.argv[2], len(out), 'chars')
