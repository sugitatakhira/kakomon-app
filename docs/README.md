# 過去問活用ノート — スマホアプリ版（PWA）

この `docs/` フォルダ一式を **HTTPSのどこかに置く**と、スマホで「ホーム画面に追加」して
**アプリのように**（全画面・アイコン付き・オフライン可）使えます。iPhone / Android 両対応。

中身：
- `index.html` … アプリ本体（第63〜72回＝2000問＋別冊画像、約15MB）
- `manifest.webmanifest` … アプリ名・アイコン・全画面設定
- `sw.js` … Service Worker（オフライン用にキャッシュ）
- `icon-*.png` … アプリアイコン

## 置き方（どれか1つ。いちばん簡単なのは Netlify Drop）

### A. Netlify Drop（無料・登録ほぼ不要・いちばん簡単）
1. パソコンで <https://app.netlify.com/drop> を開く
2. この **`docs` フォルダごと**ページにドラッグ&ドロップ
3. `https://〇〇〇.netlify.app` というURLが発行される → それをスマホで開く

### B. GitHub Pages（無料。※privateリポジトリは要有料プラン）
1. この `docs/` を `main` ブランチに入れる（このブランチをmainにマージ）
2. リポジトリ Settings → Pages → Source を「Deploy from a branch」、Branch=`main` /`docs` に設定
3. 数分後 `https://sugitatakhira.github.io/kakomon-app/` で公開される

### C. Cloudflare Pages（無料）
- ダッシュボードで「Direct Upload」→ `docs` の中身をアップロード

## スマホでの「インストール」
- **iPhone(Safari)**: 公開URLを開く → 共有ボタン → **「ホーム画面に追加」**
- **Android(Chrome)**: 公開URLを開く → メニュー → **「アプリをインストール」/「ホーム画面に追加」**

一度開けば、次回からはオフライン（圏外・機内モード）でも起動します。
（※初回だけ約15MBのダウンロードが走ります。Wi-Fi推奨。）

## アプリを更新したとき
問題や機能を更新したら、`build71/gen_pwa.py` を実行して `docs/` を作り直し、
**`sw.js` の `CACHE = "kakomon-v1"` の番号を上げて**から再アップロードしてください
（番号を変えると、利用者の端末で古いキャッシュが破棄され新版に入れ替わります）。

## 再生成
リポジトリ直下で：
```
python3 build71/gen_all.py    # kakomon-webapp-all.html（統合版）を作る
python3 build71/gen_pwa.py    # それを docs/ にPWAとして展開
```
アイコンを作り直すには `build71/gen_icons.py` を実行。
