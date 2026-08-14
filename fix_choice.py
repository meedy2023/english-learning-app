# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# === 替换顶部工具栏：加"选择学习"按钮 ===
old_bar = '<div id="quiz-toggle-bar" style="display:flex;gap:8px;margin-bottom:12px">\n      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="showWordList()">📖 单词表</button>\n      <button class="btn btn-primary btn-sm" style="flex:1;opacity:1" onclick="startQuiz()">✏️ 开始测验</button>\n    </div>'

new_bar = '<div id="quiz-toggle-bar" style="display:flex;gap:8px;margin-bottom:12px">\n      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="showWordList()">📖 单词表</button>\n      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="startChoiceLearn()">🎯 选择学习</button>\n      <button class="btn btn-primary btn-sm" style="flex:1" onclick="startQuiz()">✏️ 闯关测验</button>\n    </div>'

if old_bar in content:
    content = content.replace(old_bar, new_bar)
    print('Bar replaced OK')
else:
    print('Bar pattern NOT found')

# === 添加选择题区域 DOM ===
old_detail_area = '<div id="word-detail-area" style="display:none"></div>'
new_detail_area = '<div id="word-detail-area" style="display:none"></div>\n    <!-- 选择题学习区 -->\n    <div id="choice-learn-area" style="display:none"></div>'

if old_detail_area in content:
    content = content.replace(old_detail_area, new_detail_area)
    print('Choice area DOM added OK')
else:
    print('Detail area pattern NOT found')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('File written OK')
