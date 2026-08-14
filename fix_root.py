# -*- coding: utf-8 -*-
"""修复 root() 函数返回前端页面"""

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_root = '''@app.get("/")
def root():
    return {"msg": "英语学习 App API 正常运行", "docs": "/docs"}'''

new_root = '''@app.get("/")
async def root():
    """根路径返回前端页面"""
    from fastapi.responses import FileResponse
    import os
    index_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"msg": "英语学习 App API", "docs": "/docs"}'''

if old_root in content:
    content = content.replace(old_root, new_root)
    print("✓ root() 已修复")
else:
    print("✗ 未找到需要修复的 root() 函数")
    # 尝试其他模式
    if '@app.get("/")' in content:
        print("  - 找到 @app.get('/')，尝试模糊匹配...")
        import re
        pattern = r'@app\.get\("/"\)\s*\ndef root\(\):\s*return.*?(?=\n@app|\Z)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_root, content, flags=re.DOTALL)
            print("✓ root() 已修复（模糊匹配）")

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("完成")
