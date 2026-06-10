# -*- coding: utf-8 -*-
"""第65回(tp190415) 専用 cmap破損の置換。平成31年(2019)。
66〜68と違い破損は軽微（本文digitは正常、前文のみdrop）。略号/単位の括弧・末梢/扁平/穿刺の脱落グリフを復元。
"""
import re

DIGIT = {  # 本文digitは正常。念のため標準セット＋前文の઄ઃઆ
    '\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3',
    '઄':'2','ઃ':'3','આ':'4',
}
BRACKET = {  # 略号=〈〉 / 単位=［］（66〜68の慣例どおり）
    '\x7f':'〈','\x80':'〉',        # 午前 略号 〈感染症法〉〈SIADH〉〈MGL法〉
    '\x98':'［','\x99':'］',        # 午前 単位 ［mg/dL］［mmHg］［％］
    'Ò':'［','Ó':'］',             # 午後 単位 ［m/s］［U/L］
}

def fix(text):
    text = text.replace('\x0c','\n')
    # 午後の略号括弧 N…Q（=〈…〉）。内部にN/Qを含む略号(BNP/NTX)対応のASCII版＋漢字/カナ版。
    # Q(?![A-Za-z]) で QRS/QT 等の実在Qを除外（午前は該当無し）。
    text = re.sub(r'N([A-Za-z0-9/\- ]{1,24}?)Q(?![A-Za-z])', r'〈\1〉', text)
    text = re.sub(r'N([ぁ-んァ-ヶー一-龠][^NQ\n]{0,18}?)Q(?![A-Za-z])', r'〈\1〉', text)
    for k,v in {**DIGIT,**BRACKET}.items():
        text = text.replace(k,v)
    # 脱落/誤マップ漢字の復元
    text = text.replace('末)','末梢').replace('末r','末梢')   # 梢（午前=) 午後=r）
    text = text.replace('平上皮','扁平上皮')                  # 扁（空白脱落）
    text = text.replace('刺液','穿刺液')                      # 穿（空白脱落）
    # 記号
    text = text.replace('袷','+')                            # イオン価・凝集判定
    text = re.sub(r'(?<=\d)暗(?=\d)','≒',text)             # log2≒0.301（暗紫色等の実字は保護）
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安','⁻',text)   # HCO3⁻ Cl⁻（安全/安定は保護）
    text = re.sub(r'安(?=[0-9A-Za-z])','⁻',text)
    # 別冊参照の全角括弧復元（改行割れ対応）
    def _beppu(m):
        import re as _r
        return '（別冊No. %s）' % _r.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _beppu, text)
    text = text.replace('0左2','（左）').replace('0右2','（右）')
    text = re.sub(r'×\s*10(-?\d+)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix65:', sys.argv[1],'->',sys.argv[2])
