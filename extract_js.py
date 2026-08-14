# -*- coding: utf-8 -*-
"""提取 JS 脚本部分"""
import re

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 提取 script 内容
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if match:
    script = match.group(1)
    with open('frontend/test_script.js', 'w', encoding='utf-8') as f:
        f.write(script)
    print(f"Script extracted: {len(script)} chars")