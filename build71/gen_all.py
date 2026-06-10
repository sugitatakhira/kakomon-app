# -*- coding: utf-8 -*-
import json, os, re
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..')
src=open(os.path.join(ROOT,'kakomon-webapp.html'),encoding='utf-8').read()

def extract(htmlname, const):
    h=open(os.path.join(ROOT,htmlname),encoding='utf-8').read()
    return re.search(r'const '+const+r' = (\[.*?\]);', h, re.S).group(1)

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

# A) inject data + sets (newest first)
old_a='"use strict";\n\n// ===== 定数 ====='
inject=('"use strict";\n\n'
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
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ questions, test }));
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
function questionsPutAll(arr) {
  const tx = _db.transaction("questions", "readwrite"); const st = tx.objectStore("questions");
  st.clear(); for (const q of arr) st.put(q);
  return idbDone(tx);
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
    // 初回シード（全年度データがあり、未シードかつ空のとき）
    if (questions.length === 0 && !(await metaGet("seededAll")) && typeof KOKUSHI_SETS !== "undefined") {
      questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));
      await questionsPutAll(questions);
      await metaPut("seededAll", 1);
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
}'''
assert src.count(old_storage)==1
src=src.replace(old_storage,new_storage)

# C) buttons per set: まだ未取込（一部でも欠けている）年度のボタンを常に表示する
old_c='''  if (questions.length > 0) h += '<button class="btn btn-danger" onclick="clearAll()">全件削除</button>';'''
new_c=old_c+'''
  if (typeof KOKUSHI_SETS !== "undefined") {
    const have = new Set(questions.map(q => q.id));
    h += KOKUSHI_SETS.filter(s => s.data.some(q => !have.has(q.id)))
      .map(s => '<button class="btn btn-primary" onclick="loadKokushi(\\'' + s.key + '\\')">' + s.label + 'を読み込む</button>').join('');
  }'''
assert src.count(old_c)==1
src=src.replace(old_c,new_c)

# D) 起動を非同期化（loadData が IndexedDB なので await してから描画）
old_init='// ===== 起動 =====\nloadData();\nrender();'
new_init='// ===== 起動 =====\n(async () => { await loadData(); render(); })();'
assert src.count(old_init)==1
src=src.replace(old_init,new_init)

open(os.path.join(ROOT,'kakomon-webapp-all.html'),'w',encoding='utf-8').write(src)
print('wrote kakomon-webapp-all.html', len(src), 'bytes')
