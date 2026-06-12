# -*- coding: utf-8 -*-
"""PWA(ホーム画面アプリ)化: 統合版 kakomon-webapp-all.html に manifest/Service Worker を組み込み
docs/ 配下にデプロイ一式を出力する。docs/ をHTTPSで公開(GitHub Pages/Netlify等)すれば
スマホで「ホーム画面に追加」してアプリのように使える(オフライン可)。

【重要】問題データ(約24MB)は index.html にインラインせず、kakomon-data.json に分離して
ランタイムで fetch する。インラインだと端末は全24MBをDL＋JSパースし終えるまで何も実行できず
スプラッシュで固まるため。外部JSONなら gzip 転送＋ネイティブ JSON.parse＋非同期なので、
軽量シェルが即描画され、フリーズしない。
SWのキャッシュ名は index.html＋data.json の内容ハッシュに連動 → 変更時だけ自動で新版に差し替わる。"""
import os, re, json, hashlib, subprocess, base64, shutil
# 出力先は docs/db/（DBアプリ専用サブディレクトリ）。ルート docs/ は4アプリのランチャー
# (docs/index.html)で、DBの scope(/kakomon-app/db/) が他アプリ(dojo/houzemi…)のサブパスを
# 内包しないようにしている。ルートにPWAを置くと配下URLを全部吸い込みアイコンが取り違う。
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..'); DOCS=os.path.join(ROOT,'docs','db')
os.makedirs(DOCS, exist_ok=True)
html=open(os.path.join(ROOT,'kakomon-webapp-all.html'),encoding='utf-8').read()

# 1) <head> に PWA メタ/manifest/アイコン を差し込む
head_add='''<title>ケンゼミ過去問データベース</title>
<meta name="theme-color" content="#0e7490">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ケンゼミ過去問">'''
assert html.count('<title>ケンゼミ過去問データベース</title>')==1
html=html.replace('<title>ケンゼミ過去問データベース</title>', head_add)

# 2) 大きなデータ定数を外部 JSON(kakomon-data.json)へ分離し、HTMLは軽量シェルにする。
#    2-a) データ定数ブロック(KOKUSHI_VERSION〜KOKUSHI_SETS)を抜き出す
m=re.search(r'\nconst KOKUSHI_VERSION = .*?\nconst KOKUSHI_SETS = \[.*?\n\];\n', html, re.S)
assert m, "data block not found"
data_block=m.group(0)
#    2-b) node で評価して JSON 化（JSエンジンに解釈させるのが最も安全・確実）
node_src=('"use strict";\n'+data_block+
  '\nprocess.stdout.write(JSON.stringify({version:KOKUSHI_VERSION,mascots:MASCOTS,coreTests:CORE_TESTS,sets:KOKUSHI_SETS}));\n')
_tmp=os.path.join(HERE,'_data_tmp.js')
open(_tmp,'w',encoding='utf-8').write(node_src)
try:
    data_json=subprocess.check_output(['node',_tmp]).decode('utf-8')
finally:
    os.remove(_tmp)
data=json.loads(data_json)  # 妥当性チェック
#    2-b') 別冊画像(base64)を img/ に実ファイルとして書き出し、data.json からは
#          URLパス参照に置換する。画像は遅延読込＋表示時にSWが都度キャッシュ。
#          これで data.json は本文のみ(約1MB)になり初回読込が軽くなる。
imgdir=os.path.join(DOCS,'img')
if os.path.isdir(imgdir): shutil.rmtree(imgdir)
os.makedirs(imgdir, exist_ok=True)
_EXT={'image/jpeg':'jpg','image/jpg':'jpg','image/png':'png','image/webp':'webp','image/gif':'gif'}
def _safe_id(qid): return qid.replace('午前','a').replace('午後','p')
_nimg=0; _ibytes=0
for _s in data['sets']:
    for _q in _s['data']:
        _du=_q.get('image')
        if not _du: continue
        _m=re.match(r'data:(image/[^;]+);base64,(.*)$', _du, re.S)
        if not _m: continue
        _mime,_b64=_m.group(1),_m.group(2)
        _ext=_EXT.get(_mime,'jpg')
        _fn='img/%s.%s'%(_safe_id(_q['id']),_ext)
        with open(os.path.join(DOCS,_fn),'wb') as _f:
            _raw=base64.b64decode(_b64); _f.write(_raw)
        _q['image']=_fn; _nimg+=1; _ibytes+=len(_raw)
data_json=json.dumps(data, ensure_ascii=False, separators=(',',':'))
json.loads(data_json)
open(os.path.join(DOCS,'kakomon-data.json'),'w',encoding='utf-8').write(data_json)
print("externalized %d images (%.1fMB) -> docs/img/" % (_nimg,_ibytes/1e6))
#    2-c) インライン定数を「空の可変グローバル＋適用関数」に置換
boot_decl=('\nlet KOKUSHI_VERSION = "", MASCOTS = {}, CORE_TESTS = [], KOKUSHI_SETS = [];\n'
  'function applyDB(d){ KOKUSHI_VERSION = d.version; MASCOTS = d.mascots || {}; CORE_TESTS = d.coreTests || []; KOKUSHI_SETS = d.sets || []; }\n')
html=html.replace(data_block, boot_decl)
#    2-d) 起動処理を「JSONをfetch→適用→描画」に差し替え
old_init='''// ===== 起動 =====
// 1) 埋め込み済みの公式データだけで即描画。IndexedDBを一切待たないのでスプラッシュは必ず解除される。
try {
  if (typeof KOKUSHI_SETS !== "undefined" && questions.length === 0) {
    questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));
  }
  render();
} catch (e) { try { hideSplash(); } catch (e2) {} }
// 2) 保存データ(自作問題・テスト)をバックグラウンドで読み込み、整合できたら再描画。
(async () => { try { await loadData(); render(); } catch (e) {} })();
// 3) 安全網: 何があってもスプラッシュは一定時間で必ず解除する。
setTimeout(() => { try { hideSplash(); } catch (e) {} }, 3000);'''
new_init='''// ===== 起動 =====
// 問題データは外部JSON(kakomon-data.json)を非同期取得（gzip転送＋ネイティブJSON.parseで高速）。
// 軽量シェルなのでJSは即実行され、データ到着後すぐ描画してスプラッシュを解除する。
function _startApp() {
  try {
    if (KOKUSHI_SETS.length && questions.length === 0) {
      questions = KOKUSHI_SETS.flatMap(function (s) { return s.data; }).map(function (q) { return Object.assign({}, q); });
    }
    render();
  } catch (e) { try { hideSplash(); } catch (e2) {} }
  (async function () { try { await loadData(); render(); } catch (e) {} })();
}
fetch("kakomon-data.json").then(function (r) { return r.json(); })
  .then(function (d) { applyDB(d); _startApp(); })
  .catch(function () { _startApp(); });
// 安全網: 何があってもスプラッシュは一定時間で必ず解除する。
setTimeout(function () { try { hideSplash(); } catch (e) {} }, 8000);'''
assert html.count(old_init)==1
html=html.replace(old_init, new_init)

# 3) Service Worker 登録を </body> 直前に差し込む（新版検出で自動更新）
sw_reg='''<script>
if ("serviceWorker" in navigator) {
  var _swRefreshing = false;
  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (_swRefreshing) return; _swRefreshing = true; location.reload();
  });
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").then(function (reg) {
      if (reg && reg.update) { try { reg.update(); } catch (e) {} }
    }).catch(function () {});
  });
}
</script>
</body>'''
assert html.count('</body>')==1
html=html.replace('</body>', sw_reg)
open(os.path.join(DOCS,'index.html'),'w',encoding='utf-8').write(html)

# 4) manifest
manifest={
 "name":"ケンゼミ過去問データベース","short_name":"ケンゼミ過去問",
 "description":"検査技術ゼミナール｜臨床検査技師国家試験 第58〜72回の過去問3000問(別冊画像つき)。検索・テスト編成・印刷ができる。",
 "id":"/kakomon-app/db/","start_url":"./index.html","scope":"./","display":"standalone","orientation":"portrait",
 "background_color":"#0f766e","theme_color":"#0e7490","lang":"ja",
 "icons":[
   {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
   {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
   {"src":"icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"},
 ],
}
open(os.path.join(DOCS,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=2))

# 5) Service Worker(アプリシェル＋データをキャッシュ→オフライン動作)。
#    CACHE 名は index.html＋data.json の内容ハッシュに連動 → 内容/コードが変わると自動で新版に。
CACHE_NAME="kakomon-"+hashlib.md5((html+data_json).encode('utf-8')).hexdigest()[:12]
sw='''const CACHE = "__CACHE_NAME__";
const ASSETS = ["./", "./index.html", "./kakomon-data.json", "./manifest.webmanifest",
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

# 6) アイコンは docs/ に生成済み(gen_icons相当)。無ければ警告。
for ic in ["icon-192.png","icon-512.png","icon-512-maskable.png","icon-180.png"]:
    if not os.path.exists(os.path.join(DOCS,ic)): print("  !! missing icon", ic)

print("wrote docs/ : index.html(%.2fMB shell), kakomon-data.json(%.1fMB), manifest, sw.js"
      % (len(html)/1e6, len(data_json)/1e6))
