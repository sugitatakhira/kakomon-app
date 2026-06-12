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
| 1 | 臨床検査技師 過去問DB | **ケンゼミ**（検査技術ゼミナール） | リポジトリ直下＋`docs/`(PWA) | `main` 等 | 第58〜72回=15回3000問 完成 |
| 2 | 診療放射線技師 過去問DB | **ホウゼミ**（放射技術ゼミナール） | **`radiology/`** | `claude/radiologic-tech-exam-db-dw7ipa` | 第64〜78回=15回3000問 完成（統合版あり）|
| 3 | 演習/クイズモード | **道場**（dojo） | 別ブランチ（要記入）| 別セッション | PR #2 進行中（`/kakomon-app/dojo/` に配信）|
| 4 | ECG（心電図）練習 | ECG | 別ブランチ（要記入）| 別セッション | 進行中 |

> #3・#4 は別セッションが作業中で、このファイル作成時点では `main`／本ブランチから
> 内容が見えない。**各担当セッションがこの表の自分の行を追記・更新すること。**

## 絶対に守るルール（混ぜない）
- **ケンゼミ（臨床検査技師）とホウゼミ（放射線技師）は完全に別物**。予備校も別。
  - 互いのファイルを参照・編集・統合しない。
  - 保存先も分離済み：ケンゼミ=IndexedDB `kakomon-db` / localStorage `kakomon-app-data`、
    ホウゼミ=IndexedDB `houzemi-db` / localStorage `houzemi-app-data`。
  - 配色も分離：ケンゼミ=ティール、**ホウゼミ=インディゴ（青紫）**。
- 自分の担当アプリのディレクトリ外には手を出さない。

## 各アプリの詳細ドキュメント
- ケンゼミ（臨床検査技師）… `HANDOFF.md`
- ホウゼミ（放射線技師）… `radiology/HANDOFF.md`（下記参照）
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
- **過去問道場(演習版)も有り**：`radiology/kakomon-dojo-all.html`（1問ずつ即採点・解説・成績記録）。
  PWA配信 `docs/houzemi-dojo/`（`https://<user>.github.io/kakomon-app/houzemi-dojo/`）。
  再生成：`radiology/gen_dojo.py`→`gen_icons_dojo.py`→`gen_pwa_dojo.py`。保存 `houzemi-dojo-progress/session`。
