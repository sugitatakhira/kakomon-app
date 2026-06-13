# -*- coding: utf-8 -*-
"""コウゼミ(工学技術ゼミナール)PWA化: 統合版 engineering/kakomon-webapp-all.html に
manifest/Service Worker を組み込み docs/kouzemi/ 配下にデプロイ一式を出力。
docs/ をHTTPSで公開(GitHub Pages)すれば https://<user>.github.io/kakomon-app/kouzemi/ で
「ホーム画面に追加」してオフライン動作。SWキャッシュ名は index.html の内容ハッシュに連動。
ケンゼミ(docs/直下)・ケンゼミ道場(docs/dojo/)・ホウゼミ(docs/houzemi*) とは別サブパス・別キャッシュ・別DB(kouzemi-db)。配色グリーン。"""
import os, json, hashlib
HERE=os.path.dirname(os.path.abspath(__file__))            # engineering/
ROOT=os.path.join(HERE,'..')
DOCS=os.path.join(ROOT,'docs','kouzemi')
os.makedirs(DOCS, exist_ok=True)
html=open(os.path.join(HERE,'kakomon-webapp-all.html'),encoding='utf-8').read()

# 1) <head> に PWA メタ/manifest/アイコンを差し込む(統合版の<title>の直後)
TITLE='<title>工学技術ゼミナール｜コウゼミ過去問データベース</title>'
head_add=TITLE+'''
<meta name="theme-color" content="#16a34a">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="コウゼミ">'''
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
 "name":"工学技術ゼミナール｜コウゼミ","short_name":"コウゼミ",
 "description":"工学技術ゼミナール｜臨床工学技士国家試験の過去問データベース。検索・テスト編成・印刷ができる。",
 "id":"/kakomon-app/kouzemi/","start_url":"./index.html","scope":"./","display":"standalone","orientation":"portrait",
 "background_color":"#052e16","theme_color":"#16a34a","lang":"ja",
 "icons":[
   {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
   {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
   {"src":"icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"},
 ],
}
open(os.path.join(DOCS,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=2))

# 4) Service Worker。キャッシュ名は内容ハッシュ連動(kouzemi専用)
CACHE_NAME="kouzemi-"+hashlib.md5(html.encode('utf-8')).hexdigest()[:12]
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
print("wrote docs/kouzemi/ : index.html(%.1fMB), manifest.webmanifest, sw.js  cache=%s" % (len(html)/1e6, CACHE_NAME))
