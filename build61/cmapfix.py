# -*- coding: utf-8 -*-
"""第61回(tp150511-05) cmap整形。平成27年(2015)。この回は本文フォントが正常で
括弧（）・別冊No.・数字はそのまま抽出できる。整形は改ページとごく一部の制御コードのみ。
検証: 巻末「2014/10/17」「TP07ct」フッタ。"""
import re
def fix(text):
    text = text.replace('\x0c','\n')
    text = text.replace('\x07',' ')   # 例示ボックス内の区切り（本問には出ない）
    # 注意事項・答案用紙グリッドの例示を除去（本文の数字が正常なため誤って問1に取り込まれる）
    text = re.sub(r'^.*以上解答した場合は誤りとする。', '', text, count=1, flags=re.S)
    # 透かし「別  冊 / No.X」を行ごと除去（本文の参照は（別冊 No.X）の形）
    text = re.sub(r'^\s*別\s+冊\s*$', '', text, flags=re.M)
    text = re.sub(r'^\s*No\.\s*\d+\s*[ＡＢAB]?\s*$', '', text, flags=re.M)
    # 参照の表記ゆれを正規化: 「別冊 No.」→「別冊No.」
    text = re.sub(r'別\s*冊\s*No', '別冊No', text)
    text = re.sub(r'×\s*10\s*(-?[1-9]\d*)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix61:', sys.argv[1],'->',sys.argv[2])
