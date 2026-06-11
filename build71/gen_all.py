# -*- coding: utf-8 -*-
import json, os, re, hashlib, base64
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..')
src=open(os.path.join(ROOT,'kakomon-webapp.html'),encoding='utf-8').read()

# 問題文先頭の通し番号表記を「午前15」「午後2」に統一する。
#   旧表記ゆれ: [A15] / [B02] / [午前A15] / [午後B2] / [午前81]（角括弧つき）など。
#   A=午前・B=午後。先頭ゼロは除去。すでに「午前15」（角括弧なし）になっている分は変化しない（冪等）。
#   重要: 午前/午後 か A/B の標識が必ず付くものだけを対象にする。
#   "answers":[4] のような数字だけの角括弧（解答配列）は絶対に書き換えない。
def normalize_prefix(s):
    def repl(m):
        ampm, letter, num = m.group(1), m.group(2), m.group(3)
        if not ampm and not letter:
            return m.group(0)  # [4] 等の数字のみは対象外（解答配列を壊さない）
        return (ampm or ('午前' if letter == 'A' else '午後')) + num
    return re.sub(r'\[(午前|午後)?([AB])?0*(\d+)\]', repl, s)

def extract(htmlname, const):
    h=open(os.path.join(ROOT,htmlname),encoding='utf-8').read()
    return normalize_prefix(re.search(r'const '+const+r' = (\[.*?\]);', h, re.S).group(1))

# 各年度の単体HTMLから埋め込み済みデータを取り出して合成（リポジトリ単体で再現可）
k72=extract('kakomon-webapp-72.html','KOKUSHI_72')
k71=extract('kakomon-webapp-71.html','KOKUSHI_71')
k70=extract('kakomon-webapp-70.html','KOKUSHI_70')
k69=extract('kakomon-webapp-69.html','KOKUSHI_69')
k68=extract('kakomon-webapp-68.html','KOKUSHI_68')
k67=extract('kakomon-webapp-67.html','KOKUSHI_67')
k66=extract('kakomon-webapp-66.html','KOKUSHI_66')
k65=extract('kakomon-webapp-65.html','KOKUSHI_65')
k64=extract('kakomon-webapp-64.html','KOKUSHI_64')
k63=extract('kakomon-webapp-63.html','KOKUSHI_63')
k62=extract('kakomon-webapp-62.html','KOKUSHI_62')
k61=extract('kakomon-webapp-61.html','KOKUSHI_61')
k60=extract('kakomon-webapp-60.html','KOKUSHI_60')
k59=extract('kakomon-webapp-59.html','KOKUSHI_59')
k58=extract('kakomon-webapp-58.html','KOKUSHI_58')

# 内容バージョン: 全問データのハッシュ。内容が変わった時だけ値が変わる
#   → 利用者端末では「公式問題だけ最新化(自作分は保持)」が走る(loadData内)。
KOKUSHI_VERSION=hashlib.md5((k72+k71+k70+k69+k68+k67+k66+k65+k64+k63+k62+k61+k60+k59+k58).encode('utf-8')).hexdigest()[:12]

# キャラクター画像(assets/mascot/*.png)をbase64で埋め込む
def _b64png(path): return "data:image/png;base64," + base64.b64encode(open(path,'rb').read()).decode()
MASCOTS = {n: _b64png(os.path.join(ROOT,'assets','mascot',n+'.png'))
           for n in ['upa_happy','upa_think','upa_smile','bear_point','bear_wow','bear_smile']}

# コアテスト（章→該当問題ID）。coretests/gen_coretests.py で生成した対応表を読み込む。
CORE_TESTS = json.load(open(os.path.join(ROOT,'coretests','coretests.json'),encoding='utf-8'))

# A) inject data + sets (newest first)
old_a='"use strict";\n\n// ===== 定数 ====='
inject=('"use strict";\n\n'
 'const KOKUSHI_VERSION = "'+KOKUSHI_VERSION+'";\n'
 'const MASCOTS = '+json.dumps(MASCOTS,ensure_ascii=False)+';\n'
 'const CORE_TESTS = '+json.dumps(CORE_TESTS,ensure_ascii=False)+';\n'
 'const KOKUSHI_72 = '+k72+';\n'
 'const KOKUSHI_71 = '+k71+';\n'
 'const KOKUSHI_70 = '+k70+';\n'
 'const KOKUSHI_69 = '+k69+';\n'
 'const KOKUSHI_68 = '+k68+';\n'
 'const KOKUSHI_67 = '+k67+';\n'
 'const KOKUSHI_66 = '+k66+';\n'
 'const KOKUSHI_65 = '+k65+';\n'
 'const KOKUSHI_64 = '+k64+';\n'
 'const KOKUSHI_63 = '+k63+';\n'
 'const KOKUSHI_62 = '+k62+';\n'
 'const KOKUSHI_61 = '+k61+';\n'
 'const KOKUSHI_60 = '+k60+';\n'
 'const KOKUSHI_59 = '+k59+';\n'
 'const KOKUSHI_58 = '+k58+';\n'
 'const KOKUSHI_SETS = [\n'
 '  { key: "72", label: "第72回", data: KOKUSHI_72 },\n'
 '  { key: "71", label: "第71回", data: KOKUSHI_71 },\n'
 '  { key: "70", label: "第70回", data: KOKUSHI_70 },\n'
 '  { key: "69", label: "第69回", data: KOKUSHI_69 },\n'
 '  { key: "68", label: "第68回", data: KOKUSHI_68 },\n'
 '  { key: "67", label: "第67回", data: KOKUSHI_67 },\n'
 '  { key: "66", label: "第66回", data: KOKUSHI_66 },\n'
 '  { key: "65", label: "第65回", data: KOKUSHI_65 },\n'
 '  { key: "64", label: "第64回", data: KOKUSHI_64 },\n'
 '  { key: "63", label: "第63回", data: KOKUSHI_63 },\n'
 '  { key: "62", label: "第62回", data: KOKUSHI_62 },\n'
 '  { key: "61", label: "第61回", data: KOKUSHI_61 },\n'
 '  { key: "60", label: "第60回", data: KOKUSHI_60 },\n'
 '  { key: "59", label: "第59回", data: KOKUSHI_59 },\n'
 '  { key: "58", label: "第58回", data: KOKUSHI_58 },\n'
 '];\n\n// ===== 定数 =====')
assert src.count(old_a)==1
src=src.replace(old_a,inject)

# B) 保存・読み込みを IndexedDB に置き換え（10回=2000問・画像込みで localStorage 上限を超えるため）。
#    旧 localStorage データは初回に一度だけ IndexedDB へ移行する。保存は test を常に書き、
#    questions は配列参照/長さが変わったとき（＝問題が増減・編集されたとき）だけ全置換する。
old_storage='''// ===== 保存・読み込み =====
function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const d = JSON.parse(raw);
      if (Array.isArray(d.questions)) questions = d.questions;
      if (d.test && Array.isArray(d.test.items)) test = d.test;
      if (Array.isArray(d.savedTests)) savedTests = d.savedTests;
    }
  } catch (e) {
    canStore = false;
    document.getElementById("storage-notice").style.display = "block";
  }
}
let saveTimer = null;
function saveData() {
  const el = document.getElementById("save-state");
  if (!canStore) return;
  el.textContent = "保存中…";
  el.classList.remove("error");
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ questions, test, savedTests }));
      el.textContent = "✓ 保存しました";
      setTimeout(() => { if (el.textContent === "✓ 保存しました") el.textContent = ""; }, 1500);
    } catch (e) {
      el.textContent = "保存に失敗しました（容量超過の可能性）";
      el.classList.add("error");
    }
  }, 400);
}'''
new_storage='''// ===== 保存・読み込み（IndexedDB） =====
const DB_NAME = "kakomon-db", DB_VER = 1;
let _db = null, _qSavedRef = null, _qSavedLen = -1;
function idbOpen() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(DB_NAME, DB_VER);
    r.onupgradeneeded = () => {
      const db = r.result;
      if (!db.objectStoreNames.contains("questions")) db.createObjectStore("questions", { keyPath: "id" });
      if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta", { keyPath: "k" });
    };
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
function idbReq(req) { return new Promise((res, rej) => { req.onsuccess = () => res(req.result); req.onerror = () => rej(req.error); }); }
function idbDone(tx) { return new Promise((res, rej) => { tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error); tx.onabort = () => rej(tx.error); }); }
function metaGet(k) { return idbReq(_db.transaction("meta", "readonly").objectStore("meta").get(k)).then(r => r ? r.v : undefined); }
function metaPut(k, v) { const tx = _db.transaction("meta", "readwrite"); tx.objectStore("meta").put({ k, v }); return idbDone(tx); }
function questionsGetAll() { return idbReq(_db.transaction("questions", "readonly").objectStore("questions").getAll()); }
async function questionsPutAll(arr) {
  await idbDone((function () { const tx = _db.transaction("questions", "readwrite"); tx.objectStore("questions").clear(); return tx; })());
  for (let i = 0; i < arr.length; i += 200) {
    const tx = _db.transaction("questions", "readwrite"); const st = tx.objectStore("questions");
    for (let j = i; j < Math.min(i + 200, arr.length); j++) st.put(arr[j]);
    await idbDone(tx);
  }
}
async function loadData() {
  try {
    _db = await idbOpen();
    // 旧 localStorage データを一度だけ IndexedDB へ移行
    if (!(await metaGet("migrated"))) {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const d = JSON.parse(raw);
          if (Array.isArray(d.questions) && d.questions.length) await questionsPutAll(d.questions);
          if (d.test && Array.isArray(d.test.items)) await metaPut("test", d.test);
        }
      } catch (e) {}
      await metaPut("migrated", 1);
      try { localStorage.removeItem(STORAGE_KEY); localStorage.removeItem(STORAGE_KEY + "-seededAll"); } catch (e) {}
    }
    const qs = await questionsGetAll();
    if (qs && qs.length) questions = qs;
    const t = await metaGet("test");
    if (t && Array.isArray(t.items)) test = t;
    const stv = await metaGet("savedTests");
    if (Array.isArray(stv)) savedTests = stv;
    // 公式問題は常に存在させる（消えていても復元）＋バージョンが上がれば内容更新。講師の自作分・テストは保持。
    if (typeof KOKUSHI_SETS !== "undefined" && typeof KOKUSHI_VERSION !== "undefined") {
      const official = KOKUSHI_SETS.flatMap(s => s.data);
      const officialIds = new Set(official.map(q => q.id));
      const have = new Set(questions.map(q => q.id));
      const versionChanged = (await metaGet("contentVersion")) !== KOKUSHI_VERSION;
      const missingOfficial = official.some(q => !have.has(q.id));
      if (versionChanged || missingOfficial) {
        const userAdded = questions.filter(q => !officialIds.has(q.id));
        questions = [...userAdded, ...official.map(q => ({ ...q }))];
        // 永続化はバックグラウンドで実行（初回描画＝スプラッシュ解除をブロックしない）。
        // メモリ上の questions は既に最新なので、画面はすぐ全問表示される。
        _qSavedRef = questions; _qSavedLen = questions.length;
        (async () => {
          try {
            await questionsPutAll(questions);
            await metaPut("contentVersion", KOKUSHI_VERSION);
            await metaPut("seededAll", 1);
          } catch (e) {}
        })();
        return;
      }
    }
    _qSavedRef = questions; _qSavedLen = questions.length;
  } catch (e) {
    // IndexedDB が使えない環境では、今セッションのみメモリ上に全問展開して閲覧可能にする
    canStore = false;
    if (typeof KOKUSHI_SETS !== "undefined" && questions.length === 0) {
      questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));
    }
    const sn = document.getElementById("storage-notice"); if (sn) sn.style.display = "block";
  }
}
let saveTimer = null;
function saveData() {
  const el = document.getElementById("save-state");
  if (!canStore || !_db) return;
  if (el) { el.textContent = "保存中…"; el.classList.remove("error"); }
  clearTimeout(saveTimer);
  saveTimer = setTimeout(async () => {
    try {
      await metaPut("test", test);
      await metaPut("savedTests", savedTests);
      if (questions !== _qSavedRef || questions.length !== _qSavedLen) {
        await questionsPutAll(questions);
        _qSavedRef = questions; _qSavedLen = questions.length;
      }
      if (el) { el.textContent = "✓ 保存しました"; setTimeout(() => { if (el.textContent === "✓ 保存しました") el.textContent = ""; }, 1500); }
    } catch (e) {
      if (el) { el.textContent = "保存に失敗しました"; el.classList.add("error"); }
    }
  }, 400);
}
function loadKokushi(key) {
  const set = KOKUSHI_SETS.find(s => s.key === key);
  if (!set) return;
  confirmAction(set.label + "(" + set.data.length + "問)を問題バンクに追加します。よろしいですか？", () => {
    const have = new Set(questions.map(q => q.id));
    const add = set.data.filter(q => !have.has(q.id)).map(q => ({ ...q }));
    questions = [...add, ...questions];
    saveData(); render();
    toast(add.length + "問を読み込みました");
  });
}
function seedAll() {
  if (typeof KOKUSHI_SETS === "undefined") return;
  const have = new Set(questions.map(q => q.id));
  const add = KOKUSHI_SETS.flatMap(s => s.data).filter(q => !have.has(q.id)).map(q => ({ ...q }));
  questions = [...questions, ...add];
  saveData(); render();
  toast(add.length + "問を読み込みました");
}'''
assert src.count(old_storage)==1
src=src.replace(old_storage,new_storage)


# D) 起動: まず埋め込みデータで即描画（スプラッシュをIndexedDB待ちにしない）→
#    その後バックグラウンドで保存データ(自作問題・テスト)を読み込んで再描画。
old_init='// ===== 起動 =====\nloadData();\nrender();'
new_init=('// ===== 起動 =====\n'
 '// 1) 埋め込み済みの公式データだけで即描画。IndexedDBを一切待たないのでスプラッシュは必ず解除される。\n'
 'try {\n'
 '  if (typeof KOKUSHI_SETS !== "undefined" && questions.length === 0) {\n'
 '    questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));\n'
 '  }\n'
 '  render();\n'
 '} catch (e) { try { hideSplash(); } catch (e2) {} }\n'
 '// 2) 保存データ(自作問題・テスト)をバックグラウンドで読み込み、整合できたら再描画。\n'
 '(async () => { try { await loadData(); render(); } catch (e) {} })();\n'
 '// 3) 安全網: 何があってもスプラッシュは一定時間で必ず解除する。\n'
 'setTimeout(() => { try { hideSplash(); } catch (e) {} }, 3000);')
assert src.count(old_init)==1
src=src.replace(old_init,new_init)

open(os.path.join(ROOT,'kakomon-webapp-all.html'),'w',encoding='utf-8').write(src)
print('wrote kakomon-webapp-all.html', len(src), 'bytes')
