# -*- coding: utf-8 -*-
"""添加 KET 学习功能到前端"""

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. 更新 switchView 函数中的 titles
old_titles = '"📊 学习报告" };'
new_titles = '"📊 学习报告", ket: "📚 KET 学习" };'
if old_titles in content:
    content = content.replace(old_titles, new_titles)
    print("✓ 更新 switchView titles")
else:
    print("✗ 未找到 titles")

# 2. 更新 topbar-right 显示逻辑
old_display = '(name === "report") ? "none" : "";'
new_display = '(name === "report" || name === "ket") ? "none" : "";'
if old_display in content:
    content = content.replace(old_display, new_display)
    print("✓ 更新 topbar-right 显示逻辑")
else:
    print("✗ 未找到 display 逻辑")

# 3. 添加 KET 加载调用
old_report = 'if (name === "report") loadReport();'
new_report = 'if (name === "report") loadReport();\n      if (name === "ket") loadKetCategories();'
if old_report in content:
    content = content.replace(old_report, new_report)
    print("✓ 添加 KET 加载调用")
else:
    print("✗ 未找到 loadReport")

# 4. 更新底部导航激活状态更新
old_nav_update = "['home', 'learn', 'report'].forEach"
new_nav_update = "['home', 'learn', 'ket', 'report'].forEach"
if old_nav_update in content:
    content = content.replace(old_nav_update, new_nav_update)
    print("✓ 更新底部导航激活状态")
else:
    print("✗ 未找到 nav update")

# 保存
with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("\n✓ 前端更新完成")