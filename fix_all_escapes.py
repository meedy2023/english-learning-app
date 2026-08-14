# -*- coding: utf-8 -*-
"""
修复所有 HTML 属性中 onclick 内的 \' 转义
这些转义在 JS 字符串中虽然合法但容易引起混淆
统一改为不带转义的版本
"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 第 549 行：在 JavaScript 字符串中
# onclick="switchView(\'home\')" 
# 这种实际上是字符串中的 onclick HTML 属性，应该用 \\\\' 转义双引号
# 但因为外面已经是单引号字符串，里面用单引号不需要转义

# 修复方式：直接去掉 \ 转义
fixes = [
    # 第 549 行：内嵌的 JS 中
    (
        '''onclick="switchView(\\'home\\')"''',
        '''onclick="switchView('home')"'''
    ),
    # 第 1155 行
    (
        '''onclick="switchView(\\'learn\\')"''',
        '''onclick="switchView('learn')"'''
    ),
    # 第 1156 行
    (
        '''onclick="switchView(\\'home\\'); loadModules()"''',
        '''onclick="switchView('home'); loadModules()"'''
    ),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ 修复: {old[:60]}...")
    else:
        print(f"⚠ 未找到: {old[:60]}...")

# 检查是否还有其他转义
import re
remaining = re.findall(r'\\\'[a-z]+\\', content)
if remaining:
    print(f"\n仍有 {len(remaining)} 处转义:")
    for r in remaining[:5]:
        print(f"  {r}")

# 写回文件
if content != original:
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n✓ 文件已更新")
else:
    print("\n无修改")