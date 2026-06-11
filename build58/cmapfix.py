# -*- coding: utf-8 -*-
"""第58回(tp_siken_58) 専用 cmap破損の置換。平成24年(2012)。62/63/59と同系統。
数字: \\x02=2,\\x04=1,\\x05=5,\\x06=4,\\x08=3,઄=2。
括弧: ì…ð / \\x1b…\\x1f / 0…2 → すべて（…）。
梢=ù・Ò、扁=\\x11、第Ⅷ因子=\\x12。−/⁻=安（安全・安定等の語は保持）。
注: é ö 等の欧字は正規。検証「平成 24 年」。"""
import re
DIGIT = {'\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3','઄':'2','ઃ':'3','આ':'4'}

def fix(text):
    text = text.replace('\x0c','\n')
    text = text.replace('ù','梢').replace('Ò','梢')
    text = text.replace('\x11','扁').replace('\x12','Ⅷ')
    # 透かし「別 冊 / No.N」を除去
    text = re.sub(r'^\s*別\s+冊\s*$', '', text, flags=re.M)
    text = re.sub(r'^\s*No\.\s*\d+\s*[ＡＢAB]?\s*$', '', text, flags=re.M)
    for k,v in DIGIT.items(): text = text.replace(k,v)
    text = text.replace('袷','⁺').replace('庵','×')
    # 別冊（0…2の特例）
    def _b(m):
        return '（別冊No. %s）' % re.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _b, text)
    # 括弧
    text = re.sub(r'ì([^ìð\n]{1,48}?)ð', r'（\1）', text)
    text = re.sub(r'\x1b([^\x1b\x1f\n]{1,24}?)\x1f', r'（\1）', text)
    text = text.replace('0左2','（左）').replace('0右2','（右）').replace('0例2','（例）')
    text = re.sub(r'0([A-Za-zぁ-ヿ一-鿿（][^\n]{0,14}?)2', r'（\1）', text)
    # 安 → −/⁻（安全・安定・安価・不安 等は保持）
    text = re.sub(r'安(?=[0-9])', '−', text)
    text = re.sub(r'(?<=[0-9A-Za-z）])安', '⁻', text)
    text = re.sub(r'×\s*10\s*(-?[1-9]\d*)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix58:', sys.argv[1],'->',sys.argv[2])
