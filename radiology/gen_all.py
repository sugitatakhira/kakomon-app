# -*- coding: utf-8 -*-
"""診療放射線技師 統合版 kakomon-webapp-all.html を生成。
第64〜78回(全15回3000問)を1ファイルに合成。保存は IndexedDB(臨床検査技師版と別DB名で非衝突)。
ブランディング: 放射技術ゼミナール / ホウゼミ。マスコット・コアテストは持たない(typeofガードで無害)。"""
import json, os, re, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))   # radiology/
src = open(os.path.join(HERE, 'kakomon-webapp.html'), encoding='utf-8').read()

ROUNDS = list(range(78, 63, -1))   # 78..64 (newest first)
YEARS = {78:2026,77:2025,76:2024,75:2023,74:2022,73:2021,72:2020,71:2019,70:2018,
         69:2017,68:2016,67:2015,66:2014,65:2013,64:2012}

def extract(nn):
    h = open(os.path.join(HERE, f'kakomon-webapp-{nn}.html'), encoding='utf-8').read()
    return re.search(r'const KOKUSHI_%d = (\[.*?\]);' % nn, h, re.S).group(1)

data = {nn: extract(nn) for nn in ROUNDS}
KOKUSHI_VERSION = hashlib.md5(''.join(data[nn] for nn in ROUNDS).encode('utf-8')).hexdigest()[:12]

# A) データ + KOKUSHI_SETS を注入
consts = ''.join('const KOKUSHI_%d = %s;\n' % (nn, data[nn]) for nn in ROUNDS)
sets = 'const KOKUSHI_SETS = [\n' + ''.join(
    '  { key: "%d", label: "第%d回(%d)", data: KOKUSHI_%d },\n' % (nn, nn, YEARS[nn], nn) for nn in ROUNDS
) + '];\n'
old_a = '"use strict";\n\n// ===== 定数 ====='
inject = ('"use strict";\n\n'
          'const KOKUSHI_VERSION = "' + KOKUSHI_VERSION + '";\n'
          + consts + sets + '\n// ===== 定数 =====')
assert src.count(old_a) == 1, 'A anchor'
src = src.replace(old_a, inject)

# 保存キーを放射線版専用に(臨床検査技師の localStorage を読まない)
src = src.replace('const STORAGE_KEY = "kakomon-app-data";',
                  'const STORAGE_KEY = "houzemi-app-data";')

# B) 保存・読み込みを IndexedDB へ(3000問+画像で localStorage 上限超過のため)。DB名は放射線版専用。
old_storage = '''// ===== 保存・読み込み =====
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
new_storage = '''// ===== 保存・読み込み（IndexedDB／放射技術ゼミナール専用DB） =====
const DB_NAME = "houzemi-db", DB_VER = 1;
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
    const qs = await questionsGetAll();
    if (qs && qs.length) questions = qs;
    const t = await metaGet("test");
    if (t && Array.isArray(t.items)) test = t;
    const stv = await metaGet("savedTests");
    if (Array.isArray(stv)) savedTests = stv;
    // 公式問題は常に存在させる（消えていても復元）＋バージョンが上がれば内容更新。自作分・テストは保持。
    if (typeof KOKUSHI_SETS !== "undefined" && typeof KOKUSHI_VERSION !== "undefined") {
      const official = KOKUSHI_SETS.flatMap(s => s.data);
      const officialIds = new Set(official.map(q => q.id));
      const have = new Set(questions.map(q => q.id));
      const versionChanged = (await metaGet("contentVersion")) !== KOKUSHI_VERSION;
      const missingOfficial = official.some(q => !have.has(q.id));
      if (versionChanged || missingOfficial) {
        const userAdded = questions.filter(q => !officialIds.has(q.id));
        questions = [...userAdded, ...official.map(q => ({ ...q }))];
        await questionsPutAll(questions);
        await metaPut("contentVersion", KOKUSHI_VERSION);
      }
    }
    _qSavedRef = questions; _qSavedLen = questions.length;
  } catch (e) {
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
}'''
assert src.count(old_storage) == 1, 'storage anchor'
src = src.replace(old_storage, new_storage)

# C) 起動を非同期化
old_init = '// ===== 起動 =====\nloadData();\nrender();'
new_init = '// ===== 起動 =====\n(async () => { await loadData(); render(); })();'
assert src.count(old_init) == 1, 'init anchor'
src = src.replace(old_init, new_init)

# D) ブランディング: 放射技術ゼミナール / ホウゼミ過去問データベース
src = src.replace('<title>ケンゼミ過去問データベース</title>', '<title>放射技術ゼミナール｜ホウゼミ過去問データベース</title>')
src = src.replace('<div class="s-eyebrow">検査技術ゼミナール</div>', '<div class="s-eyebrow">放射技術ゼミナール</div>')
src = src.replace('<div class="s-title">過去問データベース</div>', '<div class="s-title">ホウゼミ過去問データベース</div>')
src = src.replace('<div class="eyebrow">検査技術ゼミナール</div>', '<div class="eyebrow">放射技術ゼミナール</div>')
src = src.replace('<h1 class="app-title">ケンゼミ過去問データベース</h1>', '<h1 class="app-title">ホウゼミ過去問データベース</h1>')
src = src.replace('alt="ケンゼミ博士"', 'alt="ホウゼミ"')

open(os.path.join(HERE, 'kakomon-webapp-all.html'), 'w', encoding='utf-8').write(src)
print('wrote radiology/kakomon-webapp-all.html', len(src), 'bytes; version', KOKUSHI_VERSION)
