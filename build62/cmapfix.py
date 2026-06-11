# -*- coding: utf-8 -*-
"""第62回(tp160411-05) 専用 cmap破損の置換。平成28年(2016)。
検証: 「平成 28 年... 24 日」→2016=第62回。
数字の制御コードは第63回と同型 (\\x02=2,\\x04=1,\\x05=5,\\x06=4,\\x08=3,઄=2)。
括弧は文脈ごとに別グリフ: 午前 ¨…ª / Ï…Ð / 0…2、午後 j…l / 0…2。
梢: 午前 ù(U+00F9) / 午後 Ø(U+00D8)。＋上付き: 袷。× : 庵。− : 安。
注: é ö ü は正規の欧字 (Sjögren, Barré, Klüver) → 触らない。
"""
import re
DIGIT = {'\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3','઄':'2','ઃ':'3','આ':'4'}

def fix(text):
    text = text.replace('\x0c','\n')
    # 梢（午前 ù / 午後 Ø。ここでは梢以外の用法なし）
    text = text.replace('ù','梢').replace('Ø','梢')
    # 数字（制御コード）
    for k,v in DIGIT.items(): text = text.replace(k,v)
    # 記号
    text = text.replace('袷','⁺')                      # Na⁺ K⁺ Fe²⁺
    text = text.replace('庵','×')                       # A×B, ×10^n
    # 別冊（括弧0…2の特例。数字フォントの 0=（ 2=））
    def _b(m):
        return '（別冊No. %s）' % re.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _b, text)
    # 括弧（略号など）。文脈ごとの別グリフをすべて（…）へ
    text = re.sub(r'¨([^¨ª\n]{1,14}?)ª', r'（\1）', text)
    text = re.sub(r'Ï([^ÏÐ\n]{1,12}?)Ð', r'（\1）', text)
    text = re.sub(r'j([^jl\n\s]{1,12}?)l', r'（\1）', text)
    text = text.replace('0左2','（左）').replace('0右2','（右）').replace('0例2','（例）')
    # 0…2 括弧（中身が英字/かな漢字/（で始まるものだけ。小数 0.9 等は除外）
    text = re.sub(r'0([A-Za-zぁ-ヿ一-鿿（][^\n]{0,14}?)2', r'（\1）', text)
    # − （A 安 B のような式中のみ。安静/暗 等の正規漢字は対象外）
    text = re.sub(r'([0-9A-Za-zα-ωΑ-Ω）βμ])\s*安\s*([0-9A-Za-zα-ωΑ-Ω（β])', r'\1−\2', text)
    # ×10^n
    text = re.sub(r'×\s*10\s*(-?[1-9]\d*)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix62:', sys.argv[1],'->',sys.argv[2])
