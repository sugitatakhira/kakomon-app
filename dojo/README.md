# 過去問道場（演習アプリ）

臨床検査技師 国家試験の過去問を**1問ずつ解いて即採点・解説・成績記録**できる、過去問道場ライクな自己学習アプリ。
既存の編集アプリ（`kakomon-webapp*.html` / `docs/`）とは**完全に独立**しており、そちらには一切手を加えていない。

## ファイル
- `../kakomon-dojo.html` … アプリ本体（**空テンプレ**。問題データは未投入）。これがソース。
- `../kakomon-dojo-all.html` … **全15回＝3000問を埋め込んだ配布版**（約24MB・単体HTML）。生徒に渡すのはこれ。
- `gen_dojo.py` … 各年度の単体HTML（`kakomon-webapp-NN.html`）に埋め込み済みの `KOKUSHI_NN` を取り出し、
  `assets/mascot/*.png` と一緒にテンプレへ注入して配布版を生成する。

## できること
- **出題範囲**：年度（第58〜72回）・科目（10科目）で絞り込み。
- **出題対象**：すべて／未挑戦のみ／間違えた問題（復習）。
- **出題順**：番号順／シャッフル。**問題数**：10/20/50/すべて。
- 1問ずつ選択肢をタップ → 「採点する」で○×・正解・解説・別冊図を表示 → 次へ。
- **複数正解「○つ選べ」**に対応（選択集合が正解と完全一致で正解）。
- **採点除外問題（公式に正答なし＝全員正解扱い。第72回午後B28・第65回午後B32の2問）も出題に含める**。
  「採点除外」と明示し、何を選んでも正解扱い（成績には正解として計上）。→ 出題プールは全3000問。
- **成績記録**：全体正答率・科目別正答率・挑戦数を記録。結果画面で「間違いだけもう一度」。

## データの持ち方
- **問題データはJSに埋め込み**（`KOKUSHI_SETS`）。起動時に `QUESTIONS` へフラット展開（メモリ上）。
  問題は端末に保存しない（ファイル自体がデータ）。→ IndexedDB 不要、オフライン動作。
- **成績だけ localStorage** に保存：`kakomon-dojo-progress`（科目別の正誤履歴）と
  `kakomon-dojo-session`（出題中セッション＝再読込で続きから）。容量はごく小さい。
  ※ 編集アプリのキー（`kakomon-app-data` / IndexedDB `kakomon-db`）とは別物で衝突しない。

## スマホアプリ版（PWA・GitHub Pages配信）
ケンゼミDB（`docs/`）と同じやり方で、過去問道場も **`docs/dojo/`** にPWAとして配信できる
（同じPagesサイトの `…/kakomon-app/dojo/` で開く。既存 `docs/` には触れない）。
```
python3 dojo/gen_icons_dojo.py  # docs/dojo/ のアイコン（過去問/道場）。初回のみでOK
python3 dojo/gen_pwa_dojo.py    # kakomon-dojo-all.html を docs/dojo/ にPWA展開
```
公開手順・スマホへの追加方法は `../docs/dojo/README.md` を参照。
**友達・生徒には、公開された URL を送るだけ**で渡せる（HTMLファイルを直接送る必要はない）。

## 再生成
```
python3 dojo/gen_dojo.py        # → kakomon-dojo-all.html を更新
python3 dojo/gen_pwa_dojo.py    # → docs/dojo/ のPWAも更新（配信している場合）
```
年度を増やしたら `gen_dojo.py` の `YEARS` に番号を足すだけ（対応する `kakomon-webapp-NN.html` が必要）。

## 動作確認
- `node --check`：HTML内の `<script>` を抜いて構文確認。
- jsdom：`QUESTIONS.length===3000`、年度15、`pool()` の採点除外除外、`grade()` の単一/複数正解判定、
  localStorage への成績/セッション保存 を確認済み。
