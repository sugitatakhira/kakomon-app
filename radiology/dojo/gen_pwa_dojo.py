# -*- coding: utf-8 -*-
"""過去問道場（診療放射線技師＝ホウゼミ 演習アプリ）のPWA化: 配布版 houzemi-dojo-all.html に
manifest/Service Worker を組み込み、docs/houzemi-dojo/ 配下にデプロイ一式を出力する。
既存の docs/dojo/(ケンゼミ道場)・docs/houzemi/(ホウゼミDB) とは別フォルダなので共存できる
(同じGitHub Pagesサイトの /houzemi-dojo/ で配信)。
SWのキャッシュ名は index.html の内容ハッシュに連動 → 変更があれば自動で新版に差し替わる。"""
import os, json, hashlib
HERE = os.path.dirname(__file__); RAD = os.path.join(HERE, '..'); ROOT = os.path.join(RAD, '..')
DOCS = os.path.join(ROOT, 'docs', 'houzemi-dojo')
os.makedirs(DOCS, exist_ok=True)
html = open(os.path.join(RAD, 'houzemi-dojo-all.html'), encoding='utf-8').read()

# 1) <head> に PWA メタ/manifest/アイコン を差し込む（テンプレ既存の theme-color はそのまま）
head_add = '''<title>診療放射線技師 過去問道場</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="過去問道場">'''
assert html.count('<title>診療放射線技師 過去問道場</title>') == 1
html = html.replace('<title>診療放射線技師 過去問道場</title>', head_add)

# 2) Service Worker 登録を </body> 直前に差し込む
sw_reg = '''<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  });
}
</script>
</body>'''
assert html.count('</body>') == 1
html = html.replace('</body>', sw_reg)
open(os.path.join(DOCS, 'index.html'), 'w', encoding='utf-8').write(html)

# 3) manifest
manifest = {
    "name": "診療放射線技師 過去問道場", "short_name": "過去問道場",
    "description": "診療放射線技師 国家試験 第64〜78回の過去問3000問を1問ずつ解いて即採点・解説・成績記録できる演習アプリ。",
    "start_url": "./index.html", "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": "#3730a3", "theme_color": "#4f46e5", "lang": "ja",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
open(os.path.join(DOCS, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest, ensure_ascii=False, indent=2))

# 4) Service Worker(アプリシェルをキャッシュ→オフライン動作)。CACHE 名は index.html の内容ハッシュに連動。
CACHE_NAME = "houzemi-dojo-" + hashlib.md5(html.encode('utf-8')).hexdigest()[:12]
sw = '''const CACHE = "__CACHE_NAME__";
const ASSETS = ["./", "./index.html", "./manifest.webmanifest",
  "./icon-192.png", "./icon-512.png", "./icon-512-maskable.png", "./icon-180.png"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); })
    .then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; })
      .map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request).then(function (hit) {
    return hit || fetch(e.request).then(function (res) {
      if (res && res.ok && new URL(e.request.url).origin === location.origin) {
        var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
      }
      return res;
    }).catch(function () { return caches.match("./index.html"); });
  }));
});
'''
open(os.path.join(DOCS, 'sw.js'), 'w', encoding='utf-8').write(sw.replace("__CACHE_NAME__", CACHE_NAME))

for ic in ["icon-192.png", "icon-512.png", "icon-512-maskable.png", "icon-180.png"]:
    if not os.path.exists(os.path.join(DOCS, ic)):
        print("  !! missing icon", ic, "→ 先に gen_icons_dojo.py を実行してください")

print("wrote docs/houzemi-dojo/ : index.html(%.1fMB), manifest.webmanifest, sw.js" % (len(html) / 1e6))
