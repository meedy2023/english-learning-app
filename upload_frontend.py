# -*- coding: utf-8 -*-
"""部署前端到 GitHub Pages"""
import os

# 创建一个简化的 index.html，云端 API 地址
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("✓ 当前 index.html 大小:", len(html), "字节")
print("✓ 包含 API_BASE 的位置:")
import re
matches = re.findall(r'API_BASE\s*=\s*["\']([^"\']+)["\']', html)
print(matches)