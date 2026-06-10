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

# A) inject data + sets (newest first)
old_a='"use strict";\n\n// ===== 定数 ====='
inject=('"use strict";\n\n'
 'const KOKUSHI_72 = '+k72+';\n'
 'const KOKUSHI_71 = '+k71+';\n'
 'const KOKUSHI_SETS = [\n'
 '  { key: "72", label: "第72回", data: KOKUSHI_72 },\n'
 '  { key: "71", label: "第71回", data: KOKUSHI_71 },\n'
 '];\n\n// ===== 定数 =====')
assert src.count(old_a)==1
src=src.replace(old_a,inject)

# B) seed all (robust: flag only set if persist succeeds) + generic loader
old_b='''      if (d.test && Array.isArray(d.test.items)) test = d.test;
    }
  } catch (e) {
    canStore = false;
    document.getElementById("storage-notice").style.display = "block";
  }
}'''
new_b='''      if (d.test && Array.isArray(d.test.items)) test = d.test;
    }
    const seeded = localStorage.getItem(STORAGE_KEY + "-seededAll");
    if (!raw && !seeded && typeof KOKUSHI_SETS !== "undefined") {
      questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ questions, test }));
        localStorage.setItem(STORAGE_KEY + "-seededAll", "1");
      } catch (e2) {
        // 画像込みで容量超過の可能性。今セッションはメモリ上で全問表示する。
        document.getElementById("storage-notice").style.display = "block";
      }
    }
  } catch (e) {
    canStore = false;
    if (typeof KOKUSHI_SETS !== "undefined" && questions.length === 0) {
      questions = KOKUSHI_SETS.flatMap(s => s.data).map(q => ({ ...q }));
    }
    document.getElementById("storage-notice").style.display = "block";
  }
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
assert src.count(old_b)==1
src=src.replace(old_b,new_b)

# C) buttons per set (when empty)
old_c='''  if (questions.length > 0) h += '<button class="btn btn-danger" onclick="clearAll()">全件削除</button>';'''
new_c=old_c+'''
  if (questions.length === 0 && typeof KOKUSHI_SETS !== "undefined") h += KOKUSHI_SETS.map(s => '<button class="btn btn-primary" onclick="loadKokushi(\\'' + s.key + '\\')">' + s.label + 'を読み込む</button>').join('');'''
assert src.count(old_c)==1
src=src.replace(old_c,new_c)

open(os.path.join(ROOT,'kakomon-webapp-all.html'),'w',encoding='utf-8').write(src)
print('wrote kakomon-webapp-all.html', len(src), 'bytes')
