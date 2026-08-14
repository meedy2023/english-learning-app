# -*- coding: utf-8 -*-
"""
全面修复 JS 字符串中的嵌套引号问题
这是真正的 root cause：
当用 '...' 包裹 HTML 字符串时，
HTML 属性中 onclick="switchView('home')" 的单引号会意外终止 JS 字符串

解决方案：
1. 把 onclick 改为不依赖引号的函数调用
2. 或把外层字符串改为反引号 `
3. 或把外层字符串改为双引号，内部 onclick 用 \"

最简单：所有 'home'、'learn'、'report' 等 onclick 都改为 backToHome/showWordList 等具名函数
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

original = content

# 找出所有在 JS 字符串中的 onclick="switchView('xxx')"
# 模式：在 outer='...' 内的 onclick="switchView('name')"

# 修复方式：将外层字符串改为反引号
# 找出模式：'<... onclick="switchView('home')">...</div>' +  ...
# 把这些行替换为 `<... onclick="switchView('home')">...</div>` + ...

# 行 549 例子：
# '<div ... onclick="switchView('home')">...</div>'
# 改为：
# `<div ... onclick="switchView('home')">...</div>`

# 简单做法：把这种内嵌的 onclick='switchView('...')' 改为调用函数
# 用反引号版本替换单引号版本

# Step 1: 找到所有这样的模式并改为反引号
# Pattern: innerHTML = '... onclick="switchView('home')" ...'
# Step: 改为 innerHTML = `... onclick="switchView('home')" ...`

# 实际上最简单的修复是：定义全局函数 loadHome() 替换 switchView('home') + loadModules()
# 定义 showLearn() 替换 switchView('learn') + 加载逻辑

# 添加新的辅助函数（在 backToHome 之后）
helper_funcs = '''
  function showLearn() {
    switchView('learn');
    if (typeof loadModules === 'function') {
      // 重新进入学习视图
    }
  }
'''

# 在文件开始处定义这些辅助函数
# 找到 backToHome 函数并在其后插入
backToHome_match = re.search(r'function backToHome\(\)\s*\{[^}]+\}', content)
if backToHome_match:
    insert_pos = backToHome_match.end()
    content = content[:insert_pos] + helper_funcs + content[insert_pos:]
    print("✓ 添加了辅助函数")

# Step 2: 修复所有 innerHTML 中的嵌套引号
# 找出所有有 innerHTML 赋值的行，检查是否有 onclick="switchView('xxx')"
lines = content.split('\n')
fixed_count = 0

for i, line in enumerate(lines):
    # 检查是否是 innerHTML 赋值且包含嵌套引号问题
    if 'innerHTML' in line and 'onclick="switchView(' in line:
        # 这种行需要修复：把整行的单引号字符串改为反引号字符串
        old_line = line
        # 把开头的 ' 改为 `，结尾的 ' 改为 `
        # 但是要小心：可能还有其他单引号
        
        # 简单方法：用反引号包整个字符串
        # 找出 innerHTML = ' ... ' 的边界
        match = re.search(r"(\.\s*innerHTML\s*=\s*)'(.*)'(\s*;?\s*)$", line)
        if match:
            prefix = match.group(1)
            html_content = match.group(2)
            suffix = match.group(3)
            new_line = f"{prefix}`{html_content}`{suffix}"
            lines[i] = new_line
            fixed_count += 1
            print(f"  ✓ Line {i+1}: 改为反引号")

content = '\n'.join(lines)

# Step 3: 修复多行 innerHTML（用 + 号连接）
# 模式：lines[1155] = '<button ... onclick="switchView('learn')">...</button>' +
# 模式：lines[1156] = '<button ... onclick="switchView('home'); loadModules()">...</button>' +

# 这些是单行，需要单独修复
fixed_lines = []
for i, line in enumerate(lines):
    if re.search(r"'\s*<[^']*onclick=\"switchView\('(home|learn|report)'\)\"", line):
        # 这是 JS 字符串 '<... onclick="switchView('home')">...</button>'
        # 把外层 ' 改为 `
        new_line = line.replace(
            "switchView('home')",
            "switchView('home')"  # 保持内容不变，只改外层引号
        )
        # 改用反引号：找到开头的 ' 和结尾的 ' 改为 `
        # 这种行是 '...' + 形式
        match = re.match(r"^(\s*)'(.*)'(\s*\+\s*)$", line)
        if match:
            indent = match.group(1)
            body = match.group(2)
            tail = match.group(3)
            new_line = f"{indent}`{body}`{tail}"
            fixed_lines.append((i+1, line, new_line))
            lines[i] = new_line

for line_num, old, new in fixed_lines:
    print(f"  ✓ Line {line_num}: 改为反引号")

# Step 4: 修复 line 549 等单行 innerHTML
# 直接替换具体的字符串
specific_fixes = [
    # Line 549
    (
        'document.getElementById("word-list").innerHTML = \'<div class="empty-state"><div class="empty-state-icon">📖</div><div>请先选择一个模块</div><button class="btn btn-primary" style="margin-top:16px" onclick="switchView(\'home\')">去首页选择</button></div>\';',
        'document.getElementById("word-list").innerHTML = \'<div class="empty-state"><div class="empty-state-icon">📖</div><div>请先选择一个模块</div><button class="btn btn-primary" style="margin-top:16px" onclick="backToHome()">去首页选择</button></div>\';'
    ),
]

for old, new in specific_fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"  ✓ 修复了具体的字符串")
    else:
        print(f"  ⚠ 未找到具体字符串")

# 写回文件
if content != original:
    # 保持 CRLF
    if '\r\n' in original:
        content = content.replace('\n', '\r\n')
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print(f"\n✓ 共修复 {fixed_count} 处，总计完成")
else:
    print("\n无修改")