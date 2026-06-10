# -*- coding: utf-8 -*-
import json, os
HERE=os.path.dirname(__file__)
src=open(os.path.join(HERE,'..','kakomon-webapp.html'),encoding='utf-8').read()
data=json.load(open(os.path.join(HERE,'kokushi70.json'),encoding='utf-8'))
js=json.dumps(data,ensure_ascii=False)

# A) inject data
old_a='"use strict";\n\n// ===== 定数 ====='
new_a='"use strict";\n\nconst KOKUSHI_70 = '+js+';\n\n// ===== 定数 ====='
assert src.count(old_a)==1, 'A anchor'
src=src.replace(old_a,new_a)

# B) seed + loader
old_b='''      if (d.test && Array.isArray(d.test.items)) test = d.test;
    }
  } catch (e) {
    canStore = false;
    document.getElementById("storage-notice").style.display = "block";
  }
}'''
new_b='''      if (d.test && Array.isArray(d.test.items)) test = d.test;
    }
    const seeded = localStorage.getItem(STORAGE_KEY + "-seeded70");
    if (!raw && !seeded && typeof KOKUSHI_70 !== "undefined") {
      questions = KOKUSHI_70.map(q => ({ ...q }));
      localStorage.setItem(STORAGE_KEY + "-seeded70", "1");
      saveData();
    }
  } catch (e) {
    canStore = false;
    if (typeof KOKUSHI_70 !== "undefined" && questions.length === 0) {
      questions = KOKUSHI_70.map(q => ({ ...q }));
    }
    document.getElementById("storage-notice").style.display = "block";
  }
}

function loadKokushi70() {
  confirmAction("第70回(200問)を問題バンクに追加します。よろしいですか？", () => {
    const have = new Set(questions.map(q => q.id));
    const add = KOKUSHI_70.filter(q => !have.has(q.id)).map(q => ({ ...q }));
    questions = [...add, ...questions];
    saveData(); render();
    toast(add.length + "問を読み込みました");
  });
}'''
assert src.count(old_b)==1, 'B anchor'
src=src.replace(old_b,new_b)

# C) button
old_c='''  if (questions.length > 0) h += '<button class="btn btn-danger" onclick="clearAll()">全件削除</button>';'''
new_c=old_c+'''
  if (questions.length === 0) h += '<button class="btn btn-primary" onclick="loadKokushi70()">第70回を読み込む</button>';'''
assert src.count(old_c)==1, 'C anchor'
src=src.replace(old_c,new_c)

open(os.path.join(HERE,'..','kakomon-webapp-70.html'),'w',encoding='utf-8').write(src)
print('wrote kakomon-webapp-70.html', len(src), 'bytes')
