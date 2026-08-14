# -*- coding: utf-8 -*-
import json

with open('backend/textbook3_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Top level:", list(data.keys()))
top = data[list(data.keys())[0]]
print("Second level:", list(top.keys()))
sub = top[list(top.keys())[0]]
print("Type of third level:", type(sub))
print("Third level sample:", str(sub)[:200] if not isinstance(sub, list) else f"list with {len(sub)} items")

if isinstance(sub, list):
    for i, item in enumerate(sub):
        print(f"  [{i}]", list(item.keys()) if isinstance(item, dict) else type(item))
        if i >= 2:
            break
elif isinstance(sub, dict):
    for k in list(sub.keys())[:5]:
        print(f"  Key: {k}, Type: {type(sub[k])}")