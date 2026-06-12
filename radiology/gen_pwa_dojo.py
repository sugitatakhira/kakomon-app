# -*- coding: utf-8 -*-
"""ホウゼミ過去問道場 PWA化: radiology/kakomon-dojo-all.html に manifest/Service Worker を
組み込み docs/houzemi-dojo/ 配下に出力。GitHub Pages 公開で
https://<user>.github.io/kakomon-app/houzemi-dojo/ から「ホーム画面に追加」→オフライン動作。
ケンゼミ(docs/)・道場(docs/dojo/)・ホウゼミ本体(docs/houzemi/)とは別サブパス・別キャッシュ・別保存。"""
import os, json, hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..')
DOCS=os.path.join(ROOT,'docs','houzemi-dojo'); os.makedirs(DOCS, exist_ok=True)
html=open(os.path.join(HERE,'kakomon-dojo-all.html'),encoding='utf-8').read()

TITLE='<title>放射技術ゼミナール 過去問道場｜ホウゼミ</title>'
head_add=TITLE+'''
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ホウゼミ道場">'''
assert html.count(TITLE)==1, 'title anchor'
html=html.replace(TITLE, head_add)

sw_reg='''<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
}
</script>
</body>'''
assert html.count('</body>')==1
html=html.replace('</body>', sw_reg)
open(os.path.join(DOCS,'index.html'),'w',encoding='utf-8').write(html)

manifest={
 "name":"放射技術ゼミナール 過去問道場","short_name":"ホウゼミ道場",
 "description":"診療放射線技師国家試験 第64〜78回の過去問3000問を1問ずつ解いて即採点・解説・成績記録。",
 "id":"/kakomon-app/houzemi-dojo/","start_url":"./index.html","scope":"./","display":"standalone","orientation":"portrait",
 "background_color":"#1e1b4b","theme_color":"#4338ca","lang":"ja",
 "icons":[
   {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
   {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
   {"src":"icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"},
 ],
}
open(os.path.join(DOCS,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=2))

CACHE_NAME="houzemi-dojo-"+hashlib.md5(html.encode('utf-8')).hexdigest()[:12]
sw='''const CACHE = "__CACHE_NAME__";
const ASSETS = ["./", "./index.html", "./manifest.webmanifest",
  "./icon-192.png", "./icon-512.png", "./icon-512-maskable.png", "./icon-180.png"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
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
print("wrote docs/houzemi-dojo/ : index.html(%.1fMB), manifest, sw.js  cache=%s" % (len(html)/1e6, CACHE_NAME))
