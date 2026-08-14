# -*- coding: utf-8 -*-
"""
修复课文学习功能的脚本
"""
import re

# 读取 index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 修复 showChoiceSummary 中的转义问题
html = html.replace(
    "onclick=\"switchView('home'); loadModules()\"",
    "onclick=\\\"switchView('home'); loadModules()\\\""
)

# 写回文件
with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("修复完成")
