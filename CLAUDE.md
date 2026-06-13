# CLAUDE.md — このリポジトリの取扱い（全セッション共通の入口）

> **新しいセッションへ：まずこのファイルを読むこと。** このリポジトリには
> **複数の独立した学習アプリ**が同居している。自分が担当するアプリの
> ディレクトリ／ブランチだけを触り、他アプリのファイルは変更しない。

## セッション間で状況を共有する仕組み
- Claude の各セッションは**会話（メモリ）を共有しない**。状況共有は
  **このリポジトリ内のドキュメント経由**でのみ可能。
- このファイル（`CLAUDE.md`、リポジトリ直下）は**全セッションが起動時に自動で読む**。
  → ここを「状況の唯一の真実」にする。**作業を始める前に各アプリのHANDOFFも読む**。
- 各セッションは**別ブランチ**で作業し `main` から分岐する。よって**他セッションの成果は
  `main` にマージされて初めて見える**。完成したらブランチを `main` に取り込むこと。

## このリポジトリに同居するアプリ一覧

| # | アプリ | 通称 | 場所 | 主担当ブランチ | 状態 |
|---|---|---|---|---|---|
| 1 | 臨床検査技師 過去問DB | **ケンゼミ**（検査技術ゼミナール） | リポジトリ直下＋`docs/db/`(PWA) | `main` 等 | 第58〜72回=15回3000問 完成（`/kakomon-app/db/` に配信）|
| 2 | 診療放射線技師 過去問DB | **ホウゼミ**（放射技術ゼミナール） | **`radiology/`** | `claude/radiologic-tech-exam-db-dw7ipa` | 第64〜78回=15回3000問 完成（統合版あり）|
| 3 | 演習/クイズモード（臨床検査技師） | **道場**（dojo） | リポジトリ直下＋`dojo/`＋`docs/dojo/`(PWA) | `main` 等 | 全15回3000問 完成（`/kakomon-app/dojo/` に配信）|
| 4 | ECG（心電図）練習 | ECG | 別ブランチ（要記入）| 別セッション | 進行中 |
| 5 | 演習/クイズモード（放射線技師） | **ホウゼミ道場** | **`radiology/`＋`radiology/dojo/`＋`docs/houzemi-dojo/`**(PWA) | `claude/clinical-lab-tech-questions-phh7mh` | 全15回3000問 完成（`/kakomon-app/houzemi-dojo/` に配信）|
| 6 | 臨床工学技士 過去問DB | **コウゼミ**（工学技術ゼミナール） | **`engineering/`＋`docs/kouzemi/`**(PWA) | `claude/clinical-engineering-exam-db-31kp2u` | 土台一式 完成（空アプリ＋ビルド＋PWA）。**問題データは未投入**（回ごとに追加予定）|
| 7 | 演習/クイズモード（臨床工学技士） | **コウゼミ道場** | **`engineering/`＋`engineering/dojo/`＋`docs/kouzemi-dojo/`**(PWA) | `claude/clinical-engineering-exam-db-31kp2u` | 土台一式 完成（空テンプレ＋ビルド＋PWA）。問題データは未投入 |

> #3・#4 は別セッションが作業中で、このファイル作成時点では `main`／本ブランチから
> 内容が見えない。**各担当セッションがこの表の自分の行を追記・更新すること。**

> **PWA配置の鉄則（Androidのアイコン取り違え対策）**：各アプリは `docs/` 直下の
> **入れ子にならない兄弟ディレクトリ** `db/` `dojo/` `houzemi/` `houzemi-dojo/` `kouzemi/` `kouzemi-dojo/` に置く。
> ルート `docs/index.html` は**PWA化しないランチャー**（各アプリへのリンクのみ）。
> ルートにPWA（manifest/SW）を置くと scope `/kakomon-app/` が配下URLを全部飲み込み、
> ホーム画面の別アイコンから開いても同じアプリで開いてしまう。各 manifest の `id` も
> 配信パスに一致させて個別化する（例 `/kakomon-app/db/`）。

## 絶対に守るルール（混ぜない）
- **ケンゼミ（臨床検査技師）とホウゼミ（放射線技師）とコウゼミ（臨床工学技士）は完全に別物**。予備校も別。
  - 互いのファイルを参照・編集・統合しない。
  - 保存先も分離済み：ケンゼミ=IndexedDB `kakomon-db` / localStorage `kakomon-app-data`、
    ホウゼミ=IndexedDB `houzemi-db` / localStorage `houzemi-app-data`、
    コウゼミ=IndexedDB `kouzemi-db` / localStorage `kouzemi-app-data`。
  - 道場の保存キーも別：ケンゼミ道場=`kakomon-dojo-*`、ホウゼミ道場=`houzemi-dojo-*`、コウゼミ道場=`kouzemi-dojo-*`。
  - **配色は職種ごとに1色**（DBと道場で統一）：**ケンゼミ=ティール**、**ホウゼミ=インディゴ（青紫）**、**コウゼミ=グリーン**。
    （2026-06 にケンゼミ道場のグラデーションをケンゼミDB（紺終端の3段グラデ）に揃え、職種＝1色へ統一済み。）
- 自分の担当アプリのディレクトリ外には手を出さない。

## 各アプリの詳細ドキュメント
- ケンゼミ（臨床検査技師）… `HANDOFF.md`
- ホウゼミ（放射線技師）… `radiology/HANDOFF.md`（下記参照）
- コウゼミ（臨床工学技士）… `engineering/HANDOFF.md`（下記参照）
- 道場 / ECG … 各担当が追記

## ホウゼミ（`radiology/`）の要点
- 厚労省PDF（`tpYYMMDD-06` ほか）から半自動構築。第64〜67回は **午前98/午後102問**、
  第68〜78回は 100/100問。
- 古い回（第64〜74回）はPDFのcmap破損を各回 `radiology/buildNN/cmapfix.py` で復元。
- 生成物：`radiology/診療放射線技師_第NN回.csv`・`imagesNN.json`・`kakomon-webapp-NN.html`、
  統合版 `radiology/kakomon-webapp-all.html`（全15回3000問・タイトル「放射技術ゼミナール／ホウゼミ」）。
- 再生成：各 `radiology/buildNN/`（cmapfix→parse→extract_beppu→buildNN.py→gen_html.py）→
  `radiology/gen_all.py`（統合版）。
- **PWA配信済み**：`docs/houzemi/`（GitHub Pages公開で `https://<user>.github.io/kakomon-app/houzemi/`）。
  再生成：`radiology/gen_all.py`→`gen_icons.py`→`gen_pwa.py`。配色インディゴ・保存 `houzemi-db`。

## ホウゼミ道場（`radiology/dojo/`）の要点
- ケンゼミ道場（`dojo/`）と**同じレイアウト／UIの演習アプリ**の放射線技師版。1問ずつ即採点・解説・成績記録。
- **配色インディゴ**・保存キーは専用（localStorage `houzemi-dojo-progress` / `houzemi-dojo-session`）で、
  ケンゼミ道場（`kakomon-dojo-*`）ともホウゼミDB（`houzemi-db` / `houzemi-app-data`）とも衝突しない。
- ソース：`radiology/kakomon-dojo.html`（空テンプレ）。配布版：`radiology/houzemi-dojo-all.html`（全15回3000問・約19MB単体HTML）。
- 再生成：`radiology/dojo/gen_dojo.py`（各 `kakomon-webapp-NN.html` の `KOKUSHI_NN` を注入）→
  `gen_icons_dojo.py`→`gen_pwa_dojo.py`。
- **PWA配信**：`docs/houzemi-dojo/`（`https://<user>.github.io/kakomon-app/houzemi-dojo/`）。詳細は `radiology/dojo/README.md`。

## コウゼミ（`engineering/`）の要点（2026-06 土台を新規作成）
- 臨床工学技士 国家試験（**午前90＋午後90＝180問/回**）の過去問DB。ケンゼミ／ホウゼミと**同じ作り**の鋳型から派生。
- **配色グリーン**（`#16a34a`/`#15803d`、紺終端 `#052e16`）。保存＝IndexedDB `kouzemi-db` / localStorage `kouzemi-app-data`。
- **現状＝土台のみ。問題データは未投入**（`engineering/kakomon-webapp-NN.html` が無いので統合版は中身ゼロ＝CSV取込・手入力は可能）。
  回を追加するときは ①各回 `engineering/kakomon-webapp-NN.html`（`const KOKUSHI_NN = [...]`）を作る → ②再生成、の順。
- ファイル：`engineering/kakomon-webapp.html`（空テンプレ・緑・ブランド文字はケンゼミのまま＝gen_all が置換）、
  `engineering/gen_all.py`（各回検出→統合版 `kakomon-webapp-all.html`・IndexedDB化・コウゼミへ改名）、
  `engineering/gen_icons.py`／`gen_pwa.py`（→`docs/kouzemi/`）。
- 再生成：`python3 engineering/gen_all.py`→`gen_icons.py`→`gen_pwa.py`。年は `1987+N`（第38回=2025）で自動。
- 詳細は `engineering/HANDOFF.md`。

## コウゼミ道場（`engineering/dojo/`）の要点（2026-06 土台を新規作成）
- ケンゼミ道場（`dojo/`）と同じレイアウト／UIの演習アプリの臨床工学技士版。**配色グリーン**。
- 保存キー専用：localStorage `kouzemi-dojo-progress` / `kouzemi-dojo-session`（他アプリと非衝突）。
- ソース：`engineering/kakomon-dojo.html`（空テンプレ・緑・コウゼミ改名済み）。配布版：`engineering/kouzemi-dojo-all.html`。
- 再生成：`engineering/dojo/gen_dojo.py`（各 `engineering/kakomon-webapp-NN.html` の `KOKUSHI_NN` を注入）→
  `gen_icons_dojo.py`→`gen_pwa_dojo.py`。**PWA配信**：`docs/kouzemi-dojo/`。
