# -*- coding: utf-8 -*-
"""第59回(tp130422-05) 専用 cmap破損の置換。平成25年(2013)。62/63と同系統。
数字: \\x02=2,\\x04=1,\\x05=5,\\x06=4,\\x08=3,઄=2。
括弧: 午前 Ý…à / 午後 u…\\x7f / 0…2 → すべて（…）。
梢=¦、扁=\\x10、＋上付き=袷、−=安。
注: é 等の欧字は正規 → 触らない。検証「平成 25 年」。"""
import re
DIGIT = {'\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3','઄':'2','ઃ':'3','આ':'4'}

def fix(text):
    text = text.replace('\x0c','\n')
    text = text.replace('¦','梢').replace('\x10','扁')
    # 透かし「別 冊 / No.N」を除去（本文の参照は（別冊No.X）の形で別にある）
    text = re.sub(r'^\s*別\s+冊\s*$', '', text, flags=re.M)
    text = re.sub(r'^\s*No\.\s*\d+\s*[ＡＢAB]?\s*$', '', text, flags=re.M)
    for k,v in DIGIT.items(): text = text.replace(k,v)
    text = text.replace('袷','⁺')
    text = text.replace('庵','×')
    # 別冊（0…2の特例）
    def _b(m):
        return '（別冊No. %s）' % re.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _b, text)
    # 括弧: 午前 Ý…à / 午後 u…\x7f
    text = re.sub(r'Ý([^Ýà\n]{1,24}?)à', r'（\1）', text)
    text = re.sub(r'u([^\x7f\n]{1,20}?)\x7f', r'（\1）', text)
    text = text.replace('0左2','（左）').replace('0右2','（右）').replace('0例2','（例）')
    text = re.sub(r'0([A-Za-zぁ-ヿ一-鿿（][^\n]{0,14}?)2', r'（\1）', text)
    # −（A 安 B のような式中のみ）
    text = re.sub(r'([0-9A-Za-zα-ωΑ-Ω）βμ])\s*安\s*([0-9A-Za-zα-ωΑ-Ω（β])', r'\1−\2', text)
    text = re.sub(r'×\s*10\s*(-?[1-9]\d*)', r'×10^\1', text)
    # 取りこぼした閉じDEL
    text = text.replace('\x7f','')
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix59:', sys.argv[1],'->',sys.argv[2])
