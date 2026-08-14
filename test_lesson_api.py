# -*- coding: utf-8 -*-
"""
测试课文学习 API
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_apis():
    print("=== 测试课文学习 API ===\n")
    
    # 测试1: 获取课文数据
    print("1. 测试获取课文数据...")
    try:
        resp = requests.get(f"{BASE_URL}/api/textbook")
        print(f"   状态码: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ 成功获取课文数据")
            print(f"   包含出版社: {list(data.keys())}")
        else:
            print(f"   ✗ 失败: {resp.text}")
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
    
    # 测试2: 获取模块列表
    print("\n2. 测试获取模块列表...")
    try:
        resp = requests.get(f"{BASE_URL}/api/textbook/modules")
        print(f"   状态码: {resp.status_code}")
        if resp.status_code == 200:
            modules = resp.json()
            print(f"   ✓ 成功获取 {len(modules)} 个模块")
            for m in modules[:3]:
                print(f"     - {m['module']}: {m['unit_count']} 个单元")
        else:
            print(f"   ✗ 失败: {resp.text}")
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
    
    # 测试3: 获取指定模块内容
    print("\n3. 测试获取 Module 1 内容...")
    try:
        resp = requests.get(f"{BASE_URL}/api/textbook/Module 1")
        print(f"   状态码: {resp.status_code}")
        if resp.status_code == 200:
            module_data = resp.json()
            print(f"   ✓ 成功获取 {module_data['module']}")
            print(f"   包含 {len(module_data['units'])} 个单元")
            for unit in module_data['units'][:1]:
                print(f"     单元: {unit['unit']}")
                print(f"     对话: {len(unit['content'])} 句")
                for line in unit['content'][:2]:
                    print(f"       - {line['role']}: {line['text']}")
        else:
            print(f"   ✗ 失败: {resp.text}")
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_apis()
