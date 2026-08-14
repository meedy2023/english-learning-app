# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 找 showWordDetail 函数中 area.innerHTML = ` 那一段
marker_start = "  // ========== 单词详情 =========="
marker_end = "  // ========== 测验 =========="

idx_start = content.find(marker_start)
idx_end = content.find(marker_end)
if idx_start == -1 or idx_end == -1:
    print(f"Markers not found: start={idx_start}, end={idx_end}")
    exit(1)

before = content[:idx_start]
target = content[idx_start:idx_end]
after = content[idx_end:]

# 在 showWordDetail 里加 esc 函数，替换原来的 inline onclick
old_word_detail = target

# 新的 showWordDetail
new_word_detail = '''  // ========== 单词详情 ==========
  function showWordDetail(w) {
    document.getElementById("word-list").style.display = "none";
    document.getElementById("quiz-toggle-bar").style.display = "none";
    const area = document.getElementById("word-detail-area");
    area.style.display = "block";
    // 转义单引号，防止破坏 HTML onclick 属性的 JS 字符串
    const esc = s => (s || "").replace(/'/g, "\\\\'");
    area.innerHTML = `
      <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>
      <div class="word-detail-card">
        <div class="word-type-badge">${w.type}</div>
        <div class="word-text">${capitalize(w.word)}</div>
        <div class="word-phonetic">${w.phonetic}</div>
        <button class="speak-btn" onclick="speakWord('${esc(w.word)}')">🔊 听发音</button>
        <div class="word-chinese">${w.chinese}</div>
        <div class="word-example">
          <div>${capitalize(w.example_en)}</div>
          <div class="word-example-cn">${w.example_cn}</div>
        </div>
      </div>
      <button class="btn btn-primary" onclick="markWord('${w.id}', 'learned')">✓ 我学会了</button>
      <button class="btn btn-secondary" onclick="markWord('${w.id}', 'mastered')" style="margin-top:8px;width:100%">⭐ 我已掌握</button>
      <button class="btn btn-secondary" onclick="speakAll('${esc(w.word)}','${esc(w.chinese)}','${esc(w.example_en)}','${esc(w.example_cn)}')" style="margin-top:8px;width:100%">🔊 朗读全部</button>
    `;
  }

'''

if old_word_detail.strip() == new_word_detail.strip():
    print("Already up to date")
else:
    # 检查旧的 speakWord onclick 是否有转义
    if "speakWord('${w.word}')" in target and "\\'" not in target.split("speakWord('${w.word}')")[0][-5:]:
        print("Found inline speakWord with unescaped quotes, replacing...")
    elif "speakWord(\\'${w.word}\\')" in target:
        print("Found inline speakWord with escaped quotes")
    else:
        print("Pattern uncertain, checking...")

    content = before + new_word_detail + after
    print("Replacement done")

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print("File written successfully")
