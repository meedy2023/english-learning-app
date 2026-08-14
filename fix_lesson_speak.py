# -*- coding: utf-8 -*-
"""
修复课文朗读按钮功能
"""
import re

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 showLessonDetail 函数的结束位置并添加事件监听器
# 查找模式：在函数结束前添加代码
pattern = r"(function showLessonDetail\(unit\) \{.*?)('</div>'\s*\+\s*'`\s*;\s*}\s*function backToLessonUnits)"

replacement = r"\1'</div>' +\n    '`;\n    \n    // 添加整篇朗读按钮的事件监听器\n    var fullSpeakBtn = document.getElementById('lesson-full-speak-btn');\n    if (fullSpeakBtn) {\n      fullSpeakBtn.addEventListener('click', function() {\n        speakAllLessonLines(unit.content);\n      });\n    }\n  }\n\n  function backToLessonUnits"

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 写回文件
with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成：添加了整篇朗读按钮的事件监听器")
