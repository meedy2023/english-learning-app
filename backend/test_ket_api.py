# -*- coding: utf-8 -*-
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# 测试获取分类
r = client.get('/api/ket/categories')
print('分类API:', r.status_code)
data = r.json()
print('分类数量:', len(data['categories']))

# 测试获取词汇
r = client.get('/api/ket/words?category=个人信息')
print('词汇API:', r.status_code)
print('词汇数量:', len(r.json()['words']))

# 测试获取句型
r = client.get('/api/ket/sentences?category=自我介绍')
print('句型API:', r.status_code)
print('句型数量:', len(r.json()['sentences']))

# 测试获取语法
r = client.get('/api/ket/grammar?category=be动词')
print('语法API:', r.status_code)
print('语法规则:', r.json()['grammar'].get('规则', 'N/A'))