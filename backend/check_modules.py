# -*- coding: utf-8 -*-
import re

with open('words_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

modules = set(re.findall(r'"module":\s*"([^"]+)"', content))
print("单词模块列表：")
for m in sorted(modules):
    print(f'  {m}')

print("\n下册模块：")
xia = [m for m in modules if m.startswith('下')]
for m in sorted(xia):
    print(f'  {m}')