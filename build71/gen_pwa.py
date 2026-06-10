# -*- coding: utf-8 -*-
"""PWA(ホーム画面アプリ)化: 統合版 kakomon-webapp-all.html に manifest/Service Worker を組み込み
docs/ 配下にデプロイ一式を出力する。docs/ をHTTPSで公開(GitHub Pages/Netlify等)すれば
スマホで「ホーム画面に追加」してアプリのように使える(オフライン可)。
SWのキャッシュ名は index.html の内容ハッシュに連動 → 変更があれば自動で新版に差し替わる(手動の番号上げ不要)。"""
import os, shutil, json, hashlib
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..'); DOCS=os.path.join(ROOT,'docs')
os.makedirs(DOCS, exist_ok=True)
html=open(os.path.join(ROOT,'kakomon-webapp-all.html'),encoding='utf-8').read()

# 1) <head> に PWA メタ/manifest/アイコン を差し込む
head_add='''<title>過去問活用ノート</title>
<meta name="theme-color" content="#0e7490">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="過去問ノート">'''
assert html.count('<title>過去問活用ノート</title>')==1
html=html.replace('<title>過去問活用ノート</title>', head_add)

# 2) Service Worker 登録を </body> 直前に差し込む
sw_reg='''<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  });
}
</script>
</body>'''
assert html.count('</body>')==1
html=html.replace('</body>', sw_reg)
open(os.path.join(DOCS,'index.html'),'w',encoding='utf-8').write(html)

# 3) manifest
manifest={
 "name":"臨床検査技師 過去問ノート","short_name":"過去問ノート",
 "description":"臨床検査技師国家試験 第63〜72回の過去問2000問(別冊画像つき)。検索・テスト編成・印刷ができる。",
 "start_url":"./index.html","scope":"./","display":"standalone","orientation":"portrait",
 "background_color":"#f5f5f4","theme_color":"#0e7490","lang":"ja",
 "icons":[
   {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
   {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
   {"src":"icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"},
 ],
}
open(os.path.join(DOCS,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=2))

# 4) Service Worker(アプリシェルをキャッシュ→オフライン動作)。
#    CACHE 名は index.html の内容ハッシュに連動 → 内容/コードが変わると自動で新版に入れ替わる。
CACHE_NAME="kakomon-"+hashlib.md5(html.encode('utf-8')).hexdigest()[:12]
sw='''const CACHE = "__CACHE_NAME__";
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
open(os.path.join(DOCS,'sw.js'),'w',encoding='utf-8').write(sw.replace("__CACHE_NAME__", CACHE_NAME))

# 5) アイコンは docs/ に生成済み(gen_icons相当)。無ければ警告。
for ic in ["icon-192.png","icon-512.png","icon-512-maskable.png","icon-180.png"]:
    if not os.path.exists(os.path.join(DOCS,ic)): print("  !! missing icon", ic)

print("wrote docs/ : index.html(%.1fMB), manifest.webmanifest, sw.js" % (len(html)/1e6))
