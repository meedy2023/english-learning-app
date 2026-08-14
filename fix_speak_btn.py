# -*- coding: utf-8 -*-
"""
修复 showLessonDetail 函数的结构问题
之前的 fix_lesson_button.py 破坏了函数结构，导致：
1. function backToLessonUnits() 关键字消失
2. 整篇朗读按钮的 onclick 绑定放在了函数外面（无效）

正确的结构应该是：
function showLessonDetail(unit) {
  ...
  area.innerHTML = `...`;
  // 在这里绑定按钮事件
  var btn = document.getElementById("lesson-full-speak-btn");
  if (btn) btn.onclick = function() { speakAllLessonLines(unit.content); };
}

function backToLessonUnits() { ... }
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

original = content

# 找到被破坏的结构
# 现状：
#   area.innerHTML = `...`;
# }
#     // 添加整篇朗读按钮的事件监听器
#     setTimeout(function() {
#       var btn = document.getElementById("lesson-full-speak-btn");
#       if (btn) {
#         btn.onclick = function() {
#           speakAllLessonLines(unit.content);
#         };
#       }
#     }, 100);
#   function backToLessonUnits() {

# 应该改为：
#   area.innerHTML = `...`;
#
#   // 绑定整篇朗读按钮
#   var btn = document.getElementById("lesson-full-speak-btn");
#   if (btn) btn.onclick = function() { speakAllLessonLines(unit.content); };
# }
#
# function backToLessonUnits() {

old_pattern = """    `;
  }
    

    // 添加整篇朗读按钮的事件监听器

    setTimeout(function() {

      var btn = document.getElementById("lesson-full-speak-btn");

      if (btn) {

        btn.onclick = function() {

          speakAllLessonLines(unit.content);

        };

      }

    }, 100);

  function backToLessonUnits() {"""

new_pattern = """    `;

    // 绑定整篇朗读按钮
    var fullSpeakBtn = document.getElementById("lesson-full-speak-btn");
    if (fullSpeakBtn) {
      fullSpeakBtn.onclick = function() {
        speakAllLessonLines(unit.content);
      };
    }
  }

  function backToLessonUnits() {"""

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("✓ 修复了函数结构")
else:
    print("⚠ 未找到旧模式，尝试替代方法...")
    # 用更灵活的正则
    pattern = re.compile(
        r"`;\s*\n\s*\}\s*\n\s*\n\s*// 添加整篇朗读按钮的事件监听器.*?function backToLessonUnits\(\)\s*\{",
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        content = pattern.sub(new_pattern, content)
        print("✓ 通过正则修复")
    else:
        print("✗ 完全未找到，需要手动检查")

if content != original:
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✓ 文件已保存")
else:
    print("无修改")