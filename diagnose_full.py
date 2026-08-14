# -*- coding: utf-8 -*-
"""
全面诊断 index.html 的所有 JS 错误
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# 扫描每一行，找所有 onclick 和 HTML 字符串
print("=== 完整扫描所有 HTML 字符串和 onclick ===")
print(f"总行数: {len(lines)}")
print()

# 找出所有 innerHTML 赋值
for i, line in enumerate(lines, 1):
    if 'innerHTML' in line and ('switchView' in line or 'loadModules' in line or 'backToHome' in line or 'showLessonList' in line):
        # 检查转义
        has_escape = "\\'" in line
        marker = "⚠ [有转义]" if has_escape else "✓ [正常]"
        print(f"{marker} Line {i}: {line.strip()[:150]}...")

print()
print("=== 检查所有 switchView 调用 ===")
for i, line in enumerate(lines, 1):
    if 'switchView(' in line:
        # 提取 switchView 调用
        match = re.search(r'switchView\([^)]*\)', line)
        if match:
            print(f"Line {i}: {match.group(0)}")
            # 检查是否在字符串中
            if "\\'" in line:
                print(f"   ⚠ 包含 \\' 转义")

print()
print("=== 文件编码检查 ===")
# 检查 BOM
if content.startswith('\ufeff'):
    print("⚠ 文件以 BOM 开头")
else:
    print("✓ 文件无 BOM")

# 检查编码
import codecs
with open('frontend/index.html', 'rb') as f:
    raw = f.read()
print(f"原始字节数: {len(raw)}")
print(f"UTF-8 解码: {'✓' if raw.decode('utf-8', errors='strict') == content else '⚠'}")

# 检查 CRLF
crlf_count = raw.count(b'\r\n')
lf_only_count = raw.count(b'\n') - crlf_count
print(f"CRLF 行数: {crlf_count}")
print(f"LF 行数: {lf_only_count}")