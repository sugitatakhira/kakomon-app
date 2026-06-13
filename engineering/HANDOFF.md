# コウゼミ（臨床工学技士 過去問DB）引き継ぎ書

> まず **リポジトリ直下 `CLAUDE.md`** を読むこと。本書はコウゼミ（`engineering/`）専用の詳細。
> ケンゼミ（臨床検査技師＝リポジトリ直下・`dojo/`・`docs/db|dojo/`）と
> ホウゼミ（放射線技師＝`radiology/`・`docs/houzemi*`）には**触れない**。

## これは何か
臨床工学技士 国家試験の過去問を登録・検索・テスト編成・印刷できる **1ファイル完結HTML Webアプリ**＋
1問ずつ演習できる **道場**。ケンゼミ／ホウゼミと**同じ鋳型**から派生させた臨床工学技士版。

- ブランド：**工学技術ゼミナール ／ コウゼミ**。職種ラベル＝**臨床工学技士**。
- **配色グリーン**（職種＝1色。ケンゼミ=ティール、ホウゼミ=インディゴ、コウゼミ=グリーン）。
- 国家試験は **午前90＋午後90＝180問/回**（臨床検査技師の 200/回、放射線の 200/回 とは違う）。

## 現状（2026-06）
**土台一式のみ完成。問題データは未投入。**
- `engineering/kakomon-webapp.html` … 空アプリ本体（緑）。問題の登録/編集/画像添付/CSV入出力/テスト編成/印刷ができる。
- `engineering/kakomon-webapp-all.html` … 統合版（**現状は中身ゼロ**＝各回HTMLがまだ無い）。CSV取込・手入力は可能。
- `engineering/kakomon-dojo.html` … 道場の空テンプレ（緑・コウゼミ改名済み）。
- `engineering/kouzemi-dojo-all.html` … 道場の配布版（**現状は問題ゼロ**）。
- `docs/kouzemi/` `docs/kouzemi-dojo/` … PWA配信一式（緑アイコン・manifest・SW）。
- まだ `engineering/kakomon-webapp-NN.html`（各回の問題）が無いので、統合版・道場ともに空。

## 保存先・キー（衝突回避）
- DB：IndexedDB `kouzemi-db`（v1, store `questions`/`meta`）／ localStorage `kouzemi-app-data`（空アプリ本体）。
- 道場：localStorage `kouzemi-dojo-progress` / `kouzemi-dojo-session`。
- いずれもケンゼミ（`kakomon-*`）・ホウゼミ（`houzemi-*`）と非衝突。

## 配色（ティール→グリーンの対応表）
空テンプレ `engineering/kakomon-webapp.html` は、ルートのケンゼミ空アプリ（ティール）を以下で緑化したもの。
ブランド文字（ケンゼミ等）は残してあり、`gen_all.py` 側でコウゼミへ置換する（ホウゼミと同方式）。

| ティール（ケンゼミ） | グリーン（コウゼミ） | 用途 |
|---|---|---|
| `#0d9488` | `#16a34a` | 明アクセント／グラデ始点 |
| `#0f766e` | `#15803d` | 暗アクセント／グラデ中間 |
| `#0e7490` | `#15803d` | シアン系アクセント→緑700に統合 |
| `#082f49` | `#052e16` | グラデ終端（紺→濃緑） |
| `#f0fdfa` | `#f0fdf4` | 最薄（green-50） |
| `#eef3f3` | `#ecfdf5` | 中性薄→emerald-50 |
| `#99f6e4` | `#86efac` | スプラッシュ見出し（green-300） |
| `#99d6cf` | `#a7d4b0` | やわらか緑 |
| `rgba(13,148,136,*)` | `rgba(22,163,74,*)` | 影など |
| `rgba(15,118,110,*)` | `rgba(21,128,61,*)` | 影など |

道場テンプレ `engineering/kakomon-dojo.html` は CSS変数 `--teal:#16a34a` / `--teal-d:#15803d`（変数名はそのまま値だけ緑）、
theme-color `#16a34a`、`rgba(13,148,136,*)→rgba(22,163,74,*)` を置換。`#047857`(正答)・`#dcfce7`/`#166534`(○表示)等は意味色なので据え置き。

## ビルド／再生成
```
python3 engineering/gen_all.py          # 各回HTMLを自動検出→統合版 kakomon-webapp-all.html（IndexedDB化・コウゼミ改名）
python3 engineering/gen_icons.py        # docs/kouzemi/icon-*.png（緑・コウゼミ/過去問/国試）  ※要 Pillow
python3 engineering/gen_pwa.py          # docs/kouzemi/（index.html+manifest+sw.js）
python3 engineering/dojo/gen_dojo.py    # 道場配布版 kouzemi-dojo-all.html
python3 engineering/dojo/gen_icons_dojo.py
python3 engineering/dojo/gen_pwa_dojo.py
```
- `gen_all.py`/`gen_dojo.py` は `engineering/kakomon-webapp-*.html` を **glob で自動検出**（新しい回が先）。回を増やしたらファイルを置いて再実行するだけ。
- 実施年は `year = 1987 + N`（第1回=1988、第38回=2025）で自動。
- SWキャッシュ名は index.html の内容ハッシュに連動（`kouzemi-…` / `kouzemi-dojo-…`）→ 変更で端末側が自動入替。
- Pillow が無い環境では `pip install Pillow`（アイコン生成のみで使用。HTML/PWA生成には不要）。

## 問題データの追加（次にやること）
ケンゼミ／ホウゼミと同手順。回ごとに：
1. 厚労省PDF（臨床工学技士国家試験の問題・正答）から本文・選択肢・正答を抽出。
   ※ MHLW のファイル名・cmap破損は回ごとに異なる。各回 `engineering/buildNN/` を作って素材・スクリプトを置く。
2. データモデル（ケンゼミと同じ）でリストを作り、各回単体HTML `engineering/kakomon-webapp-NN.html` に
   `const KOKUSHI_NN = [...]` を埋め込む（`KOKUSHI_NN` 名は回番号）。
3. 上の再生成コマンドを流す（統合版・道場・PWAが自動で当該回を取り込む）。

### データモデル（問題1件・ケンゼミ準拠）
```js
{ id:"k38午前A001", text:"…", choices:["…",…], answers:[1],  // 0始まりの正解インデックス配列。採点除外は []
  explanation:"", field:"医用電気電子工学", year:"第38回(2025)", difficulty:"普通", image:"data:image/jpeg;base64,…"(任意) }
```
CSV列：設問 / 選択肢1〜5 / 正解番号(1始まり,例「3,4」) / 解説 / 分野 / 年度 / 難易度。

### 臨床工学技士 国家試験の出題科目（field の候補）
医学概論／臨床医学総論／医用電気電子工学／医用機械工学／生体物性材料工学／
生体計測装置学／医用治療機器学／生体機能代行装置学（呼吸療法・体外循環・血液浄化）／医用機器安全管理学。
※ 臨床検査技師のような厳密な「問題番号＝科目」の固定ブロックではない。当面 `field` は問題ごとに付与する。

## 動作確認
HTML内の `<script>` を取り出して `node --check` で構文確認できる（本土台では全ブロック OK 済み）。
問題投入後は 問題数=180×回数 / 複数正解・採点除外の件数 / 別冊画像の対応を点検する。
