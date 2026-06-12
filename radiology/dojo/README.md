# 過去問道場（診療放射線技師＝ホウゼミ 演習アプリ）

診療放射線技師 国家試験の過去問を**1問ずつ解いて即採点・解説・成績記録**できる、過去問道場ライクな自己学習アプリ。
臨床検査技師（ケンゼミ）版の道場（リポジトリ直下 `dojo/`・`docs/dojo/`）と**同じレイアウト／UI**だが、
**配色はインディゴ（青紫）**・保存キーも専用にして完全に分離している。
既存の編集アプリ（`radiology/kakomon-webapp*.html` / `docs/houzemi/`）には**一切手を加えていない**。

## ファイル
- `../kakomon-dojo.html` … アプリ本体（**空テンプレ**。問題データは未投入）。これがソース。
- `../houzemi-dojo-all.html` … **全15回＝3000問を埋め込んだ配布版**（約19MB・単体HTML）。生徒に渡すのはこれ。
- `gen_dojo.py` … 各年度の単体HTML（`radiology/kakomon-webapp-NN.html`）に埋め込み済みの `KOKUSHI_NN` を
  取り出してテンプレへ注入し、配布版を生成する。
- `gen_icons_dojo.py` / `gen_pwa_dojo.py` … PWA（`docs/houzemi-dojo/`）のアイコン・配信一式を生成。

## できること（ケンゼミ道場と同一）
- **出題範囲**：年度（第64〜78回）・科目（13科目）で絞り込み。
- **出題対象**：すべて／未挑戦のみ／間違えた問題（復習）。
- **出題順**：番号順／シャッフル。**問題数**：10/20/50/すべて。
- 1問ずつ選択肢をタップ → 「採点する」で○×・正解・解説・別冊図を表示 → 次へ。
- **複数正解「○つ選べ」**に対応（選択集合が正解と完全一致で正解）。
- **採点除外問題（公式に正答なし＝全員正解扱い）も出題に含める**。出題プールは全3000問。
- **成績記録**：全体正答率・科目別正答率・挑戦数を記録。結果画面で「間違いだけもう一度」。

## データ／保存（ケンゼミと衝突しない）
- **問題データはJSに埋め込み**（`KOKUSHI_SETS`）。起動時に `QUESTIONS` へフラット展開（メモリ上）。
  端末には保存しない（ファイル自体がデータ）。→ IndexedDB 不要・オフライン動作。
- **成績だけ localStorage** に保存：`houzemi-dojo-progress`（科目別の正誤履歴）と
  `houzemi-dojo-session`（出題中セッション＝再読込で続きから）。
  ※ ケンゼミ道場のキー（`kakomon-dojo-*`）・ホウゼミDB（`houzemi-app-data` / IndexedDB `houzemi-db`）の
    いずれとも別物で衝突しない。

## スマホアプリ版（PWA・GitHub Pages配信）
ホウゼミDB（`docs/houzemi/`）・ケンゼミ道場（`docs/dojo/`）とは**別フォルダ** `docs/houzemi-dojo/` に配信。
同じPagesサイトの `…/kakomon-app/houzemi-dojo/` で開く。既存フォルダには触れない。
```
python3 radiology/dojo/gen_icons_dojo.py  # docs/houzemi-dojo/ のアイコン（過去問/道場・インディゴ）。初回のみでOK
python3 radiology/dojo/gen_pwa_dojo.py    # houzemi-dojo-all.html を docs/houzemi-dojo/ にPWA展開
```
**友達・生徒には、公開された URL を送るだけ**で渡せる（HTMLファイルを直接送る必要はない）。

## 再生成
```
python3 radiology/dojo/gen_dojo.py        # → houzemi-dojo-all.html を更新
python3 radiology/dojo/gen_pwa_dojo.py    # → docs/houzemi-dojo/ のPWAも更新（配信している場合）
```
年度を増やしたら `gen_dojo.py` の `YEARS` に番号を足すだけ（対応する `kakomon-webapp-NN.html` が必要）。
