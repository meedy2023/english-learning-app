# -*- coding: utf-8 -*-
import json

with open('backend/textbook3_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("完整数据结构检查")
print("=" * 60)

# 顶层
for publisher in data:
    print(f"\n出版商: {publisher}")
    for grade in data[publisher]:
        print(f"\n  年级: {grade}")
        modules = data[publisher][grade]
        if isinstance(modules, dict):
            for mname, units in modules.items():
                if isinstance(units, list):
                    print(f"    {mname}: {len(units)} 个单元")
                    for i, u in enumerate(units):
                        unit_name = u.get('unit', '?') if isinstance(u, dict) else '?'
                        print(f"      [{i}] {unit_name}")
                else:
                    print(f"    {mname}: {type(units).__name__}")
        elif isinstance(modules, list):
            print(f"  类型: list, 长度: {len(modules)}")

# 单词模块映射检查
print("\n" + "=" * 60)
print("单词模块清单（words_data.py）")
print("=" * 60)
from words_data import WORDS
modules_in_words = set(w['module'] for w in WORDS)
for m in sorted(modules_in_words):
    count = sum(1 for w in WORDS if w['module'] == m)
    print(f"  {m}: {count} 个单词")