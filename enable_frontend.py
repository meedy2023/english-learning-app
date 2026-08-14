# -*- coding: utf-8 -*-
"""给后端添加静态文件托管，让 http://localhost:8080 直接访问前端"""

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加 import
if 'from fastapi.staticfiles import StaticFiles' not in content:
    content = content.replace(
        'from fastapi import FastAPI',
        'from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles'
    )

# 2. 在 app 创建后添加静态文件挂载
if 'app.mount("/static", StaticFiles(directory=' not in content:
    # 在 CORS middleware 之后添加
    insert_marker = "allow_headers=['*'],\n)"
    insert_code = """allow_headers=['*'],
)

# 托管前端静态文件（支持 http://localhost:8080 直接访问）
import os
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_path):
    app.mount('/static', StaticFiles(directory=frontend_path, html=True), name='frontend')

@app.get('/')
async def root():
    \"\"\"根路径返回前端页面\"\"\"
    from fastapi.responses import FileResponse
    index_path = os.path.join(frontend_path, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {'message': 'English Learning App API', 'docs': '/docs'}
"""
    content = content.replace(insert_marker, insert_code)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 已添加静态文件托管")
print("✓ 现在 http://localhost:8080 可直接访问前端页面")
