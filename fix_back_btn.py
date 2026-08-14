# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

old = '''  async function showWordList() {
    document.getElementById("word-detail-area").style.display = "none";
    document.getElementById("word-list").style.display = "block";
    document.getElementById("quiz-toggle-bar").style.display = "flex";'''

new = '''  async function showWordList() {
    // 隐藏所有学习子视图
    document.getElementById("word-detail-area").style.display = "none";
    document.getElementById("choice-learn-area").style.display = "none";
    document.getElementById("view-quiz").classList.remove("active");
    document.getElementById("word-list").style.display = "block";
    document.getElementById("quiz-toggle-bar").style.display = "flex";'''

if old in content:
    content = content.replace(old, new)
    print('Replaced OK')
else:
    print('Pattern not found')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('Written OK')
