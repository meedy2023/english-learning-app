# -*- coding: utf-8 -*-
"""验证 API 返回数据"""
import urllib.request
import json

url = 'http://127.0.0.1:8080/api/textbook/Module%201'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode('utf-8'))

print('Module:', data['module'])
print('Units:', len(data['units']))
print()
for unit in data['units']:
    print(f"Unit: {unit['unit']}")
    for line in unit['content']:
        print(f"  [{line['role']}] {line['text']}")
        print(f"          Translation: {line['translation']}")
    print()