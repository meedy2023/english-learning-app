# -*- coding: utf-8 -*-
"""
简单直接的修复：
所有在 JS 单引号字符串内的 onclick="switchView('home')"
改为 onclick="backToHome()"
因为嵌套单引号会终止 JS 字符串字面量
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

original = content

# 关键修复：JS 字符串中嵌套引号问题
# '<...onclick="switchView('home')">...' 中，外层是 '...'，
# 内部的 'home' 中的单引号会终止外层字符串

# 解决方案：使用 backToHome() 等不带参数的函数
# 替换所有出现在单引号字符串内的 onclick="switchView('home')"

# 模式 1: '<... onclick="switchView('home')">...' + 或 ;
# 在单引号字符串中
fixes = [
    # 第 549 行: 整个字符串内嵌 onclick
    (
        """document.getElementById("word-list").innerHTML = '<div class="empty-state"><div class="empty-state-icon">📖</div><div>请先选择一个模块</div><button class="btn btn-primary" style="margin-top:16px" onclick="switchView('home')">去首页选择</button></div>';""",
        """document.getElementById("word-list").innerHTML = `<div class="empty-state"><div class="empty-state-icon">📖</div><div>请先选择一个模块</div><button class="btn btn-primary" style="margin-top:16px" onclick="backToHome()">去首页选择</button></div>`;"""
    ),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ 修复了第 549 行")
    else:
        print(f"⚠ 未找到第 549 行")

# 第 1155, 1156 行：多行 innerHTML
# 模式：'<button ... onclick="switchView('learn')">...</button>' +
# 这两行是 innerHTML + 拼接

line_1155 = "'<button class=\"btn btn-secondary\" style=\"width:100%;margin-bottom:8px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;display:flex;align-items:center;justify-content:center;gap:6px\" onclick=\"switchView('learn')\">← 返回单词表</button>' +"

new_line_1155 = '`<button class="btn btn-secondary" style="width:100%;margin-bottom:8px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;display:flex;align-items:center;justify-content:center;gap:6px" onclick="switchView(\'learn\')">← 返回单词表</button>` +'

if line_1155 in content:
    content = content.replace(line_1155, new_line_1155)
    print("✓ 修复了第 1155 行")
else:
    print("⚠ 未找到第 1155 行")

line_1156 = "'<button class=\"btn btn-secondary\" style=\"width:100%;background:#f0f4ff;border:1px solid #d0d8ff;color:#6c63ff;display:flex;align-items:center;justify-content:center;gap:6px\" onclick=\"switchView('home'); loadModules()\">🏠 返回首页</button>' +"

new_line_1156 = '`<button class="btn btn-secondary" style="width:100%;background:#f0f4ff;border:1px solid #d0d8ff;color:#6c63ff;display:flex;align-items:center;justify-content:center;gap:6px" onclick="backToHome()">🏠 返回首页</button>` +'

if line_1156 in content:
    content = content.replace(line_1156, new_line_1156)
    print("✓ 修复了第 1156 行")
else:
    print("⚠ 未找到第 1156 行")

# 写回
if content != original:
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("\n✓ 文件已更新")