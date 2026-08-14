# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 1. 学习页顶部返回按钮美化
old1 = '''    <button class="btn btn-secondary btn-sm" onclick="switchView('home')" style="margin-bottom:8px">← 返回</button>'''
new1 = '''    <button class="btn btn-secondary" onclick="switchView('home')" style="margin-bottom:12px;display:flex;align-items:center;gap:6px;padding:10px 16px;font-size:14px;border-radius:10px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;font-weight:500"><span style="font-size:16px">←</span> 返回首页</button>'''
if old1 in content:
    content = content.replace(old1, new1)
    print('Home return button updated')

# 2. 单词详情页返回按钮美化 + 按钮重新布局
old2 = '''      <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>
      <div class="word-detail-card">'''
new2 = '''      <button class="btn btn-secondary" onclick="showWordList()" style="margin-bottom:16px;display:flex;align-items:center;gap:6px;padding:10px 16px;font-size:14px;border-radius:10px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;font-weight:500"><span style="font-size:16px">←</span> 返回单词表</button>
      <div class="word-detail-card">'''
if old2 in content:
    content = content.replace(old2, new2)
    print('Detail return button updated')

# 3. 单词详情页底部按钮美化（横向布局）
old3 = '''      <button class="btn btn-primary" onclick="markWord('${w.id}', 'learned')">✓ 我学会了</button>
      <button class="btn btn-secondary" onclick="markWord('${w.id}', 'mastered')" style="margin-top:8px;width:100%">⭐ 我已掌握</button>
      <button class="btn btn-secondary" onclick="speakAll('${esc(w.word)}','${esc(w.chinese)}','${esc(w.example_en)}','${esc(w.example_cn)}')" style="margin-top:8px;width:100%">🔊 朗读全部</button>
    `;'''
new3 = '''      <div style="display:flex;gap:10px;margin-top:16px">
        <button class="btn btn-primary" onclick="markWord('${w.id}', 'learned')" style="flex:1">✓ 我学会了</button>
        <button class="btn btn-secondary" onclick="markWord('${w.id}', 'mastered')" style="flex:1;background:linear-gradient(135deg,#ffd700 0%,#ffb700 100%);border:none;color:#fff;font-weight:600">⭐ 已掌握</button>
      </div>
      <button class="btn btn-secondary" onclick="speakAll('${esc(w.word)}','${esc(w.chinese)}','${esc(w.example_en)}','${esc(w.example_cn)}')" style="margin-top:10px;width:100%;background:#f0f4ff;border:1px solid #d0d8ff;color:#6c63ff;display:flex;align-items:center;justify-content:center;gap:6px">🔊 朗读全部</button>
    `;'''
if old3 in content:
    content = content.replace(old3, new3)
    print('Detail bottom buttons updated')

# 4. 测验页返回按钮美化
old4 = '''  <!-- ======= 测验 ======= -->
  <div id="view-quiz" class="view">
    <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>'''
new4 = '''  <!-- ======= 测验 ======= -->
  <div id="view-quiz" class="view">
    <button class="btn btn-secondary" onclick="showWordList()" style="margin-bottom:16px;display:flex;align-items:center;gap:6px;padding:10px 16px;font-size:14px;border-radius:10px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;font-weight:500"><span style="font-size:16px">←</span> 返回单词表</button>'''
if old4 in content:
    content = content.replace(old4, new4)
    print('Quiz return button updated')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('All done!')
