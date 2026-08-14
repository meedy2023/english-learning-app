# -*- coding: utf-8 -*-
"""
修复课文学习功能的完整脚本
"""
import re

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 showLessonDetail 函数中添加整篇朗读按钮的位置
found = False
for i, line in enumerate(lines):
    if 'id="lesson-full-speak-btn"' in line:
        # 找到了按钮定义，现在需要在函数结束后添加事件监听器
        # 往后找到函数结束的位置（下一个函数开始）
        for j in range(i+1, len(lines)):
            if 'function backToLessonUnits()' in lines[j]:
                # 在 backToLessonUnits 函数之前添加事件监听器
                indent = '    '
                insert_lines = [
                    f'{indent}\n',
                    f'{indent}// 添加整篇朗读按钮的事件监听器\n',
                    f'{indent}setTimeout(function() {{\n',
                    f'{indent}  var btn = document.getElementById("lesson-full-speak-btn");\n',
                    f'{indent}  if (btn) {{\n',
                    f'{indent}    btn.onclick = function() {{\n',
                    f'{indent}      speakAllLessonLines(unit.content);\n',
                    f'{indent}    }};\n',
                    f'{indent}  }}\n',
                    f'{indent}}}, 100);\n',
                ]
                # 在当前函数结束大括号后插入
                # 找到上一个 }
                for k in range(j-1, i, -1):
                    if '}\n' in lines[k] and '}`;\n' not in lines[k]:
                        lines.insert(k+1, '\n'.join(insert_lines))
                        found = True
                        break
                break
        break

if found:
    # 写回文件
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("✓ 修复完成：添加了整篇朗读按钮的事件监听器")
else:
    print("✗ 未找到需要修复的位置，可能已经修复过或代码结构有变化")
