# -*- coding: utf-8 -*-
import json

with open('textbook3_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== 模拟后端 /api/textbook/modules ===')
print('所有学期:', list(data['外研社'].keys()))

modules_up = []
grade_data = data['外研社']['三年级上册']
for mname, units in grade_data.items():
    modules_up.append({'module': mname, 'grade': '三年级上册', 'unit_count': len(units)})
print(f'\n上册模块数: {len(modules_up)}')
print(f'  示例: {modules_up[0]}')

modules_down = []
if '三年级下册' in data['外研社']:
    grade_data = data['外研社']['三年级下册']
    for mname, units in grade_data.items():
        modules_down.append({'module': mname, 'grade': '三年级下册', 'unit_count': len(units)})
print(f'\n下册模块数: {len(modules_down)}')
print(f'  示例: {modules_down[0]}')

print('\n=== 模拟 /api/textbook/Module 1?grade=三年级下册 ===')
result = data['外研社']['三年级下册']['Module 1']
print(f'找到: Module 1 (三年级下册), {len(result)} 个单元')
print(f'  示例单元: {result[0]["unit"]}')
print(f'  示例对话: {result[0]["content"][0]["role"]}: {result[0]["content"][0]["text"]}')

print('\n=== 模拟 /api/textbook/Module 5?grade=三年级上册 ===')
result = data['外研社']['三年级上册']['Module 5']
print(f'找到: Module 5 (三年级上册), {len(result)} 个单元')

print('\n=== 模拟不带 grade 参数 ===')
# 应该从上册开始找
for grade in data['外研社']:
    if 'Module 1' in data['外研社'][grade]:
        print(f'  默认找到: {grade}/Module 1')
        break