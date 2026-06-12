# -*- coding: utf-8 -*-
"""ホウゼミ(放射技術ゼミナール)PWA化: 統合版 radiology/kakomon-webapp-all.html に
manifest/Service Worker を組み込み docs/houzemi/ 配下にデプロイ一式を出力。
docs/ をHTTPSで公開(GitHub Pages)すれば https://<user>.github.io/kakomon-app/houzemi/ で
「ホーム画面に追加」してオフライン動作。SWキャッシュ名はindex.htmlの内容ハッシュに連動。
ケンゼミ(docs/直下)・道場(docs/dojo/)とは別サブパス・別キャッシュ・別DB(houzemi-db)。"""
import os, json, hashlib
HERE=os.path.dirname(os.path.abspath(__file__))            # radiology/
ROOT=os.path.join(HERE,'..')
DOCS=os.path.join(ROOT,'docs','houzemi')
os.makedirs(DOCS, exist_ok=True)
html=open(os.path.join(HERE,'kakomon-webapp-all.html'),encoding='utf-8').read()

# 1) <head> に PWA メタ/manifest/アイコンを差し込む(統合版の<title>の直後)
TITLE='<title>放射技術ゼミナール｜ホウゼミ</title>'
head_add=TITLE+'''
<meta name="theme-color" content="#4338ca">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ホウゼミ">'''
assert html.count(TITLE)==1, 'title anchor'
html=html.replace(TITLE, head_add)

# 2) Service Worker 登録を </body> 直前に
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
 "name":"放射技術ゼミナール｜ホウゼミ","short_name":"ホウゼミ",
 "description":"放射技術ゼミナール｜診療放射線技師国家試験 第64〜78回の過去問3000問(別冊・図画像つき)。検索・テスト編成・印刷ができる。",
 "id":"/kakomon-app/houzemi/","start_url":"./index.html","scope":"./","display":"standalone","orientation":"portrait",
 "background_color":"#1e1b4b","theme_color":"#4338ca","lang":"ja",
 "icons":[
   {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
   {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
   {"src":"icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"},
 ],
}
open(os.path.join(DOCS,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=2))

# 4) Service Worker。キャッシュ名は内容ハッシュ連動(houzemi専用)
CACHE_NAME="houzemi-"+hashlib.md5(html.encode('utf-8')).hexdigest()[:12]
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

for ic in ["icon-192.png","icon-512.png","icon-512-maskable.png","icon-180.png"]:
    if not os.path.exists(os.path.join(DOCS,ic)): print("  !! missing icon", ic)
print("wrote docs/houzemi/ : index.html(%.1fMB), manifest.webmanifest, sw.js  cache=%s" % (len(html)/1e6, CACHE_NAME))
