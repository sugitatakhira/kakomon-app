# -*- coding: utf-8 -*-
"""第64回(tp180511) 専用 cmap破損の置換。平成30年(2018)。66〜68と同型・別コード表。
検証: 「平成30年\x02月21日」→「平成30年2月21日」(=2018=第64回)。
"""
import re

DIGIT = {
    '\x02':'2','\x04':'1','\x05':'5','\x06':'4','\x08':'3',
    '\x0e':'8',                    # 「8bit のAD変換器」「LD1半減期約8時間」(画像確認)
    '઄':'2','ઃ':'3','આ':'4',
}
KANJI = {'Ö':'梢','\x8d':'梢'}      # 末梢（午前=Ö 午後=\x8d）
BRACKET = {'ù':'〈','þ':'〉'}        # 午後 略号 〈Dittrich〉〈Curschmann〉〈Charcot-Leyden〉

def fix(text):
    text = text.replace('\x0c','\n')
    # 午前の略号/グルーピング括弧 @…A・q…r（=〈…〉）。@/qは他用途で出現せず安全(pmに該当無し)
    # ①ASCII略号(内部にA含むTACO/TRALI等。貪欲で最後のAを閉じに) ②漢字/アクセント/+含む内容(A無し。非貪欲)
    text = re.sub(r'@([A-Za-z0-9/\-]{1,14})A', r'〈\1〉', text)
    text = re.sub(r'@([^@A\n]{1,24}?)A', r'〈\1〉', text)
    text = re.sub(r'q([^qr\n]{1,30}?)r', r'〈\1〉', text)
    for k,v in {**DIGIT,**KANJI,**BRACKET}.items():
        text = text.replace(k,v)
    text = text.replace('平上皮','扁平上皮').replace('刺液','穿刺液')  # 扁/穿の空白脱落
    text = text.replace('袷','+')
    text = text.replace('庵','×')
    text = re.sub(r'暗(?!号|紫)','≒',text)
    text = re.sub(r'(?<=[0-9A-Za-zα-ωΑ-Ω℃])安','⁻',text)
    text = re.sub(r'安(?=[0-9A-Za-z])','⁻',text)
    def _beppu(m):
        import re as _r
        return '（別冊No. %s）' % _r.sub(r'\s+','',m.group(1))
    text = re.sub(r'0\s*別\s*冊\s*No\.?\s*([0-9０-９]+\s*[ＡＢ]?)\s*2', _beppu, text)
    text = text.replace('0左2','（左）').replace('0右2','（右）')
    text = text.replace('01気圧2','（1気圧）')                              # PM20
    text = re.sub(r'0(\d+\s*℃、\d+分処理済)2', r'（\1）', text)            # AM81補体
    text = re.sub(r'×\s*10(-?\d+)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix64:', sys.argv[1],'->',sys.argv[2])
