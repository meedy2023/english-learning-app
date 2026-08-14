# -*- coding: utf-8 -*-
"""修复例句点读：单词学习删除中文点读，KET学习添加例句点读"""

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

changes = 0

# 1. 删除单词学习例句的中文点读按钮
old_example = """        <div class="word-example">
          <div style="display:flex;align-items:center;gap:8px">
            <span style="flex:1">${capitalize(w.example_en)}</span>
            <button class="speak-btn" onclick="speakWord('${esc(w.example_en)}')" style="padding:4px 10px;font-size:12px;flex-shrink:0">🔊 例句</button>
          </div>
          <div class="word-example-cn" style="display:flex;align-items:center;gap:8px;margin-top:8px">
            <span style="flex:1">${w.example_cn}</span>
            <button class="speak-btn" onclick="speakChinese('${esc(w.example_cn)}')" style="padding:4px 10px;font-size:12px;flex-shrink:0">🔊 中文</button>
          </div>
        </div>"""

new_example = """        <div class="word-example">
          <div style="display:flex;align-items:center;gap:8px">
            <span style="flex:1">${capitalize(w.example_en)}</span>
            <button class="speak-btn" onclick="speakWord('${esc(w.example_en)}')" style="padding:4px 10px;font-size:12px;flex-shrink:0">🔊 例句</button>
          </div>
          <div class="word-example-cn">${w.example_cn}</div>
        </div>"""

if old_example in content:
    content = content.replace(old_example, new_example)
    changes += 1
    print("✓ 已删除单词学习的例句中文点读")
else:
    print("⚠ 未找到单词学习例句，需要手动检查")

# 2. KET词汇添加例句点读按钮
old_ket_word = """          <div style="font-size:13px;color:#999;font-style:italic">例：${w.example}</div>
        </div>
      `).join('');
    } else if (ketCurrentType === '句型')"""

new_ket_word = """          <div style="display:flex;align-items:center;gap:8px;margin-top:4px">
            <span style="font-size:13px;color:#999;font-style:italic;flex:1">例：${w.example}</span>
            <button class="speak-btn" onclick="speakWord('${w.example}')" style="padding:2px 8px;font-size:11px">🔊</button>
          </div>
        </div>
      `).join('');
    } else if (ketCurrentType === '句型')"""

if old_ket_word in content:
    content = content.replace(old_ket_word, new_ket_word)
    changes += 1
    print("✓ 已添加KET词汇例句点读")
else:
    print("⚠ 未找到KET词汇例句位置")

# 3. KET句型添加中文翻译点读
old_ket_sentence = """          <div style="font-size:12px;color:#999;background:#f0f4ff;padding:4px 8px;border-radius:4px;display:inline-block">用途：${s.usage}</div>
        </div>
      `).join('');
    }
  }

  async function openKetCategory"""

new_ket_sentence = """          <div style="display:flex;align-items:center;gap:8px;margin-top:4px">
            <span style="font-size:12px;color:#999;background:#f0f4ff;padding:4px 8px;border-radius:4px;display:inline-block">用途：${s.usage}</span>
            <button class="speak-btn" onclick="speakWord('${s.english}')" style="padding:2px 8px;font-size:11px">🔊 朗读</button>
          </div>
        </div>
      `).join('');
    }
  }

  async function openKetCategory"""

if old_ket_sentence in content:
    content = content.replace(old_ket_sentence, new_ket_sentence)
    changes += 1
    print("✓ 已添加KET句型朗读按钮")
else:
    print("⚠ 未找到KET句型位置")

with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print(f"\n完成，共 {changes} 处修改")
