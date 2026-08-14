# -*- coding: utf-8 -*-
"""
检查 index.html 中所有 JavaScript 语法错误
特别是 onclick 中的转义问题
"""

import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查所有 onclick 属性中的可疑反斜杠
print("=== 检查 onclick 中的转义问题 ===")
# 匹配 onclick="..." 或 onclick=\"...\"
patterns = [
    (r'onclick=\\"', '错误的反斜杠转义 (onclick=\\")'),
    (r'onclick=\\\'', '错误的反斜杠转义 (onclick=\\\')'),
]

for pattern, desc in patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"⚠ 发现 {len(matches)} 处: {desc}")
        # 找出这些匹配的位置
        for m in re.finditer(pattern, content):
            pos = m.start()
            line_num = content[:pos].count('\n') + 1
            line_start = content.rfind('\n', 0, pos) + 1
            line_end = content.find('\n', pos)
            if line_end == -1:
                line_end = len(content)
            line_content = content[line_start:line_end]
            print(f"  第 {line_num} 行: {line_content[:120]}...")
    else:
        print(f"✓ 未发现: {desc}")

# 检查所有 onclick="..." 中是否有不平衡的引号
print("\n=== 检查 onclick 属性的引号平衡 ===")
onclick_pattern = re.compile(r'onclick=(["\']).*?\1', re.DOTALL)
bad_onclick = []
for m in onclick_pattern.finditer(content):
    text = m.group(0)
    # 计算字符串字面量中的 'home' 或 'learn' 等是否被错误转义
    if '\\' in text and ('switchView' in text or 'loadModules' in text):
        bad_onclick.append((m.start(), text[:200]))

if bad_onclick:
    print(f"⚠ 发现 {len(bad_onclick)} 处可疑的 onclick:")
    for pos, text in bad_onclick:
        line_num = content[:pos].count('\n') + 1
        print(f"  第 {line_num} 行: {text}")
else:
    print("✓ 所有 onclick 属性看起来正常")

# 简单的 JavaScript 语法检查
print("\n=== 简单语法检查 ===")
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if script_match:
    script = script_match.group(1)
    print(f"  脚本长度: {len(script)} 字符")
    
    # 检查常见语法问题
    issues = []
    
    # 检查函数定义
    func_count = script.count('function ')
    print(f"  函数数量: {func_count}")
    
    # 检查未闭合的引号（简单检查）
    single_quotes = script.count("'")
    double_quotes = script.count('"')
    backticks = script.count('`')
    print(f"  单引号: {single_quotes} (应为偶数)")
    print(f"  双引号: {double_quotes} (应为偶数)")
    print(f"  反引号: {backticks} (应为偶数)")
    
    if single_quotes % 2 != 0:
        issues.append(f"单引号数量为奇数 ({single_quotes})")
    if double_quotes % 2 != 0:
        issues.append(f"双引号数量为奇数 ({double_quotes})")
    if backticks % 2 != 0:
        issues.append(f"反引号数量为奇数 ({backticks})")
    
    if issues:
        print(f"  ⚠ 发现问题: {', '.join(issues)}")
    else:
        print(f"  ✓ 引号平衡")

print("\n=== 检查完成 ===")