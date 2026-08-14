# -*- coding: utf-8 -*-
"""
修复剩余的 onclick 转义问题
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查这些位置
# 这些实际上在 HTML 中是合法的 JavaScript 转义
# onclick="switchView('home')" 在 HTML 中是合法写法

# 第 549 行: onclick="switchView('home')" - 合法
# 第 1155 行: onclick="switchView('learn')" - 合法
# 第 1156 行: onclick="switchView('home'); loadModules()" - 合法

# 这些写法在 HTML 中完全合法，不会导致 JS 错误
# 之前的错误是因为反斜杠被错误地添加了

# 让我们确认一下
print("=== 检查 onclick 中的引号转义 ===")
pattern = re.compile(r'onclick="[^"]*switchView[^"]*"')
for match in pattern.finditer(content):
    pos = match.start()
    line_num = content[:pos].count('\n') + 1
    text = match.group(0)
    # 判断是否有 \'
    if "\\'" in text:
        print(f"Line {line_num}: [有转义] {text}")
    else:
        print(f"Line {line_num}: [正常]  {text}")

# 输出每一行的 onclick switchView 内容
print("\n=== switchView 调用位置 ===")
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'onclick=' in line and 'switchView' in line:
        print(f"Line {i}: {line.strip()}")