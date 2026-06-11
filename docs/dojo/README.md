# 過去問道場（演習アプリ）— スマホアプリ版（PWA）

この `docs/dojo/` フォルダ一式を **HTTPSのどこかに置く**と、スマホで「ホーム画面に追加」して
**アプリのように**（全画面・アイコン付き・オフライン可）使えます。iPhone / Android 両対応。
**友達・生徒には、できあがった URL を送るだけ**でOK（HTMLファイルそのものを送る必要はありません）。

中身：
- `index.html` … 演習アプリ本体（第58〜72回＝3000問＋別冊画像、約24MB）
- `manifest.webmanifest` … アプリ名「過去問道場」・アイコン・全画面設定
- `sw.js` … Service Worker（オフライン用にキャッシュ）
- `icon-*.png` … アプリアイコン（過去問／道場）

> 既存の「ケンゼミ過去問データベース」（`docs/` 直下）とは**別フォルダ**なので共存します。
> 同じ GitHub Pages サイトなら、道場は **`…/kakomon-app/dojo/`** のURLで開きます。

## 置き方（どれか1つ）

### A. GitHub Pages（ケンゼミDBと同じやり方。※privateリポは要有料プラン）
1. このブランチを `main` にマージ（`docs/` 全体が main に入る）
2. すでに Pages が `main` /`docs` で公開設定済みなら、追加設定は不要
3. 数分後、過去問道場は **`https://sugitatakhira.github.io/kakomon-app/dojo/`** で公開される
   （ケンゼミDBは従来どおり `https://sugitatakhira.github.io/kakomon-app/`）
4. その `…/dojo/` のURLを友達に送る ✅

### B. Netlify Drop（無料・いちばん簡単）
1. パソコンで <https://app.netlify.com/drop> を開く
2. この **`dojo` フォルダごと**ページにドラッグ&ドロップ
3. `https://〇〇〇.netlify.app` というURLが発行される → それを送る

### C. Cloudflare Pages（無料）
- ダッシュボードで「Direct Upload」→ `dojo` の中身をアップロード

## スマホでの「インストール」
- **iPhone(Safari)**: URLを開く → 共有ボタン → **「ホーム画面に追加」**
- **Android(Chrome)**: URLを開く → メニュー → **「アプリをインストール」/「ホーム画面に追加」**

一度開けば、次回からはオフラインでも起動。成績はその端末・そのサイト単位で自動保存されます。
（※初回だけ約24MBのダウンロード。Wi-Fi推奨。）

## 再生成
リポジトリ直下で：
```
python3 dojo/gen_dojo.py        # kakomon-dojo-all.html（3000問の配布版）を作る
python3 dojo/gen_icons_dojo.py  # docs/dojo/ のアイコンを作る（初回のみでOK）
python3 dojo/gen_pwa_dojo.py    # それを docs/dojo/ にPWAとして展開
```
`sw.js` のキャッシュ名は内容ハッシュに自動連動するので、更新しても番号の手上げは不要
（内容が変われば利用者端末で自動的に新版へ入れ替わります）。
