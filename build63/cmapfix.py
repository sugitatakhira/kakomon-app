# -*- coding: utf-8 -*-
"""第63回(tp170425) 専用 cmap破損の置換。平成29年(2017)。66〜68同型・別コード表。
検証: 「平成29年\x02月22日」→2017=第63回。
注意: É(U+00C9,午前)・ñ(U+00F1,午後) は「末梢の梢」と「閉じ括弧」の二役 → 末梢を先に確定。
"""
import re
DIGIT = {'\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3','઄':'2','ઃ':'3','આ':'4'}

def fix(text):
    text = text.replace('\x0c','\n')
    # 末梢を先に確定（É/ñ の梢用法）
    text = text.replace('末É','末梢').replace('末ñ','末梢')
    for k,v in DIGIT.items(): text = text.replace(k,v)
    text = text.replace('Ý','腿')                       # 大腿骨
    text = text.replace('平上皮','扁平上皮').replace('刺液','穿刺液')
    # 括弧: 午前 単位 Ç…É→［…］ / 午後 略号 ð…ñ→〈…〉
    text = re.sub(r'Ç([^ÇÉ\n]{1,16})É', r'［\1］', text)
    text = re.sub(r'ð([^ðñ\n]{1,20}?)ñ', r'〈\1〉', text)
    # 記号
    text = text.replace('庵','×')
    text = re.sub(r'暗(?!号|紫)','≒',text)
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安','⁻',text)
    text = re.sub(r'安(?=[0-9A-Za-z])','⁻',text)
    # 全角括弧
    def _b(m):
        import re as _r
        return '（別冊No. %s）' % _r.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _b, text)
    text = text.replace('0左2','（左）').replace('0右2','（右）')
    text = re.sub(r'×\s*10(-?[1-9]\d*)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix63:', sys.argv[1],'->',sys.argv[2])
