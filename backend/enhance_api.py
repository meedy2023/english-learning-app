# -*- coding: utf-8 -*-
"""
增强后端 API，支持下册课文
1. /api/textbook/modules 支持查询参数 ?grade=
2. /api/textbook/{module_name} 支持按学期查找
3. 增加下册映射: 下1→Module 1 (三年级下册), etc.
"""

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content

# ============================================================
# 改造 1: 修改 /api/textbook/modules 支持学期过滤
# ============================================================
old_modules_api = '''@app.get("/api/textbook/modules")
def get_textbook_modules():
    """获取所有课文模块列表"""
    try:
        with open("textbook3_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        modules = []
        # 提取三年级上册的所有模块
        if "外研社" in data and "三年级上册" in data["外研社"]:
            grade_data = data["外研社"]["三年级上册"]
            for module_name, units in grade_data.items():
                unit_count = len(units)
                modules.append({
                    "module": module_name,
                    "unit_count": unit_count,
                    "units": [u["unit"] for u in units]
                })
        return modules
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"获取模块列表失败: {str(e)}")


@app.get("/api/textbook/{module_name}")
def get_textbook_module(module_name: str):
    """获取指定模块的课文内容"""
    try:
        with open("textbook3_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if "外研社" in data and "三年级上册" in data["外研社"]:
            grade_data = data["外研社"]["三年级上册"]
            if module_name in grade_data:
                return {
                    "module": module_name,
                    "units": grade_data[module_name]
                }
        
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="模块不存在")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"获取课文内容失败: {str(e)}")'''

new_modules_api = '''# 单词模块到课文模块 + 学期的映射
# 上N → Module N (三年级上册)
# 下N → Module N (三年级下册)
WORD_TO_LESSON_MODULE = {
    '上1': ('Module 1', '三年级上册'), '上2': ('Module 2', '三年级上册'),
    '上3': ('Module 3', '三年级上册'), '上4': ('Module 4', '三年级上册'),
    '上5': ('Module 5', '三年级上册'), '上6': ('Module 6', '三年级上册'),
    '上7': ('Module 7', '三年级上册'), '上8': ('Module 8', '三年级上册'),
    '上9': ('Module 9', '三年级上册'), '上10': ('Module 10', '三年级上册'),
    '下1': ('Module 1', '三年级下册'), '下2': ('Module 2', '三年级下册'),
    '下3': ('Module 3', '三年级下册'), '下4': ('Module 4', '三年级下册'),
    '下5': ('Module 5', '三年级下册'), '下6': ('Module 6', '三年级下册'),
    '下7': ('Module 7', '三年级下册'), '下8': ('Module 8', '三年级下册'),
    '下9': ('Module 9', '三年级下册'), '下10': ('Module 10', '三年级下册'),
}


@app.get("/api/textbook/modules")
def get_textbook_modules(grade: Optional[str] = None):
    """获取所有课文模块列表
    参数:
        grade: 可选，按学期过滤（"三年级上册" 或 "三年级下册"），不传则返回所有
    """
    try:
        with open("textbook3_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        modules = []
        if "外研社" in data:
            grades_to_check = []
            if grade:
                grades_to_check = [grade]
            else:
                grades_to_check = list(data["外研社"].keys())

            for g in grades_to_check:
                if g not in data["外研社"]:
                    continue
                grade_data = data["外研社"][g]
                for module_name, units in grade_data.items():
                    if isinstance(units, list):
                        modules.append({
                            "module": module_name,
                            "grade": g,
                            "unit_count": len(units),
                            "units": [u["unit"] for u in units if isinstance(u, dict)]
                        })
        return modules
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"获取模块列表失败: {str(e)}")


@app.get("/api/textbook/grade/{word_module}")
def get_lesson_by_word_module(word_module: str):
    """根据单词模块（上N/下N）获取对应的课文模块名+学期"""
    result = WORD_TO_LESSON_MODULE.get(word_module)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"无对应课文: {word_module}")
    module_name, grade = result
    return {
        "word_module": word_module,
        "module": module_name,
        "grade": grade,
    }


@app.get("/api/textbook/{module_name}")
def get_textbook_module(module_name: str, grade: Optional[str] = None):
    """获取指定模块的课文内容
    参数:
        module_name: 模块名，如 "Module 1"
        grade: 可选，学期（"三年级上册" 或 "三年级下册"），不传则自动查找
    """
    try:
        with open("textbook3_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if "外研社" in data:
            # 优先用指定学期
            grades_to_check = []
            if grade:
                grades_to_check = [grade]
            else:
                grades_to_check = list(data["外研社"].keys())

            for g in grades_to_check:
                if g not in data["外研社"]:
                    continue
                grade_data = data["外研社"][g]
                if module_name in grade_data:
                    return {
                        "module": module_name,
                        "grade": g,
                        "units": grade_data[module_name]
                    }

        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"模块不存在: {module_name}")
    except HTTPException:
        raise
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"获取课文内容失败: {str(e)}")'''

if old_modules_api in content:
    content = content.replace(old_modules_api, new_modules_api)
    print("✓ 后端 API 已增强（支持学期参数 + 单词模块查询）")
else:
    print("✗ 未找到旧 API 代码")

if content != original_content:
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ main.py 已保存")
else:
    print("无修改")