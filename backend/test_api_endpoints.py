# -*- coding: utf-8 -*-
"""测试后端 API 真实行为"""
import urllib.request
import urllib.parse
import json

BASE = "http://localhost:8080"

def get(path, params=None):
    # 注意：path 中的空格需要 encode
    url = BASE + urllib.parse.quote(path)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    print(f"GET {url}")
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode('utf-8'))

print("=== Test 1: /api/textbook/modules (no filter) ===")
data = get('/api/textbook/modules')
print(f"Total: {len(data)}")
for m in data[:3]:
    print(f"  {m['module']} ({m.get('grade', '?')}): {m['unit_count']} units")
print(f"  ...")
for m in data[-3:]:
    print(f"  {m['module']} ({m.get('grade', '?')}): {m['unit_count']} units")

print("\n=== Test 2: /api/textbook/modules?grade=三年级上册 ===")
data = get('/api/textbook/modules', {'grade': '三年级上册'})
print(f"Total: {len(data)}")
for m in data[:3]:
    print(f"  {m['module']} ({m.get('grade', '?')})")

print("\n=== Test 3: /api/textbook/modules?grade=三年级下册 ===")
data = get('/api/textbook/modules', {'grade': '三年级下册'})
print(f"Total: {len(data)}")
for m in data[:3]:
    print(f"  {m['module']} ({m.get('grade', '?')})")

print("\n=== Test 4: /api/textbook/Module 1?grade=三年级下册 ===")
data = get('/api/textbook/Module 1', {'grade': '三年级下册'})
print(f"Module: {data['module']}, Grade: {data['grade']}, Units: {len(data['units'])}")
unit = data['units'][0]
print(f"  Unit: {unit['unit']}")
print(f"  Lines: {len(unit['content'])}")
print(f"  First line: {unit['content'][0]['role']}: {unit['content'][0]['text']}")
print(f"  Translation: {unit['content'][0]['translation']}")

print("\n=== Test 5: /api/textbook/grade/下1 ===")
data = get('/api/textbook/grade/下1')
print(f"Word module: {data['word_module']}")
print(f"  → Lesson: {data['module']}, Grade: {data['grade']}")

print("\n=== Test 6: /api/textbook/grade/下5 ===")
data = get('/api/textbook/grade/下5')
print(f"Word module: {data['word_module']}")
print(f"  → Lesson: {data['module']}, Grade: {data['grade']}")

print("\n=== Test 7: /api/textbook/Module 1 (no grade) - 默认返回上册 ===")
data = get('/api/textbook/Module 1')
print(f"Module: {data['module']}, Grade: {data['grade']}")

print("\n=== All tests passed! ===")