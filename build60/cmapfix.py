# -*- coding: utf-8 -*-
"""第60回(tp140512-05) cmap整形。平成26年(2014)。本文フォントはほぼ正常。
・括弧は半角 ( ) → 全角（）に統一
・組合せの区切りは長い罫線 ―――― → 単一の ―
・「末  血/末  神」は梢が脱落 → 末梢血/末梢神経 に復元
・透かし「別 冊 / No.N」、ページ番号「― N ―」、フッタ「HAP07ct-…」を除去
検証: フッタ HAP07ct / 「平成26年」。"""
import re
def fix(text):
    text = text.replace('\x0c','\n')
    # フッタ・ページ番号・透かしを行ごと除去
    text = re.sub(r'^.*HAP\w.*$', '', text, flags=re.M)
    text = re.sub(r'^\s*―\s*\d+\s*―\s*$', '', text, flags=re.M)
    text = re.sub(r'^\s*別\s+冊\s*$', '', text, flags=re.M)
    text = re.sub(r'^\s*No\.\s*\d+\s*[ＡＢAB]?\s*$', '', text, flags=re.M)
    # 注意事項の例示ブロックを除去（数字が正常で誤って問1に取り込まれるのを防ぐ）
    text = re.sub(r'^.*以上解答した場合は誤りとする。', '', text, count=1, flags=re.S)
    # 梢の脱落を復元
    text = re.sub(r'末\s{2,}(血|神)', r'末梢\1', text)
    # 括弧 半角→全角
    text = text.replace('(', '（').replace(')', '）')
    # 別冊 No. の表記ゆれ
    text = re.sub(r'別\s*冊\s*No', '別冊No', text)
    # 組合せの区切り（長い罫線/ダッシュの連なり）→ 単一の ―
    text = re.sub(r'\s*[―─—\-]{2,}\s*', ' ― ', text)
    text = re.sub(r'×\s*10\s*(-?[1-9]\d*)', r'×10^\1', text)
    return text

if __name__ == '__main__':
    import sys
    open(sys.argv[2],'w',encoding='utf-8').write(fix(open(sys.argv[1],encoding='utf-8').read()))
    print('cmapfix60:', sys.argv[1],'->',sys.argv[2])
