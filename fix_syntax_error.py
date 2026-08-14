# -*- coding: utf-8 -*-
"""
修复 JavaScript 语法错误
问题：第 1406 行的 onclick 中有错误的转义符
错误：onclick=\"switchView('home'); loadModules()\"
正确：onclick="backToHome()"
"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复错误的转义
bad_str = "onclick=\\\"switchView('home'); loadModules()\\\">"
good_str = 'onclick="backToHome()">'

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 修复成功：移除了错误的反斜杠转义")
else:
    print("⚠ 未找到错误字符串，尝试其他匹配...")
    # 尝试另一种匹配方式
    import re
    pattern = r'onclick=\\\"switchView\(.home.\); loadModules\(\)\\\"'
    matches = re.findall(pattern, content)
    print(f"找到 {len(matches)} 处匹配")
    if matches:
        content = re.sub(pattern, 'onclick="backToHome()"', content)
        with open('frontend/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ 通过正则修复成功")