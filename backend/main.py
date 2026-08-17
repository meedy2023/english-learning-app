# -*- coding: utf-8 -*-
"""
英语学习 App 后端
运行方式: uvicorn main:app --reload --port 8080
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
from words_data import WORDS, get_words_by_module, search_words, get_all_modules, get_all_grades
from ket_data import KET_DATA

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- 静态文件 -----
import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# ----- 根路径 -----
@app.get("/")
def root():
    from fastapi.responses import FileResponse
    idx = os.path.join(frontend_dir, "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"message": "English Learning App Backend", "docs": "/docs"}


# ----- 进度存储 -----
class ProgressStore:
    def __init__(self):
        self._store = {}

    def mark(self, user_id, word_id, status):
        key = f"{user_id}:{word_id}"
        self._store[key] = status

    def get(self, user_id, word_id):
        return self._store.get(f"{user_id}:{word_id}", "new")

    def get_all_word_statuses(self, user_id, module=None, grade=None):
        statuses = {}
        for w in WORDS:
            if module and w["module"] != module:
                continue
            if grade and w.get("grade") != grade:
                continue
            statuses[w["id"]] = self.get(user_id, w["id"])
        return statuses

    def get_all_stats(self, user_id):
        stats = {}
        for w in WORDS:
            mod = w["module"]
            grade = w.get("grade", "三年级")
            key = f"{grade}/{mod}"
            if key not in stats:
                stats[key] = {"grade": grade, "module": mod, "total": 0, "learned": 0, "mastered": 0}
            stats[key]["total"] += 1
            st = self.get(user_id, w["id"])
            if st == "learned":
                stats[key]["learned"] += 1
            elif st == "mastered":
                stats[key]["learned"] += 1
                stats[key]["mastered"] += 1
        for v in stats.values():
            v["percent"] = round(v["learned"] / v["total"] * 100) if v["total"] > 0 else 0
        return stats

    def get_module_progress(self, user_id, module):
        words = [w for w in WORDS if w["module"] == module]
        total = len(words)
        learned = sum(1 for w in words if self.get(user_id, w["id"]) in ("learned", "mastered"))
        mastered = sum(1 for w in words if self.get(user_id, w["id"]) == "mastered")
        return {
            "total": total,
            "learned": learned,
            "mastered": mastered,
            "percent": round(learned / total * 100) if total > 0 else 0
        }


progress_store = ProgressStore()


# ========== 年级 API ==========

@app.get("/api/grades")
def list_grades():
    """获取所有年级列表"""
    return {"grades": get_all_grades()}


# ========== 课文 API ==========

@app.get("/api/textbook")
def get_textbook():
    """获取课文数据（支持所有年级）"""
    try:
        with open("textbook_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="课文数据文件未找到")


@app.get("/api/textbook/modules")
def get_textbook_modules(grade: Optional[str] = None):
    """获取课文模块列表（可按年级过滤）"""
    try:
        with open("textbook_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"modules": [], "grades": []}

    all_grades = list(data.get("外研社", {}).keys())
    modules = []
    for g in all_grades:
        if grade and g != grade:
            continue
        semesters = data["外研社"][g]
        for sem, mod_dict in semesters.items():
            for mod_name, units in mod_dict.items():
                modules.append({
                    "grade": g,
                    "semester": sem,
                    "module": mod_name,
                    "grade_label": g + sem,
                    "unit_count": len(units) if isinstance(units, list) else 0,
                })
    return {"modules": modules, "grades": all_grades}


@app.get("/api/textbook/{module_name}")
def get_textbook_module(module_name: str, grade_label: Optional[str] = None, semester: Optional[str] = None):
    """获取指定课文模块内容"""
    try:
        with open("textbook_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="课文数据文件未找到")

    # 精确匹配：遍历 (年级, 学期) 组合，用 grade_label = g+sem 来匹配
    for g, semesters in data.get("外研社", {}).items():
        for sem, mod_dict in semesters.items():
            if grade_label and (g + sem) != grade_label:
                continue
            if module_name in mod_dict:
                return {"grade": g, "semester": sem, "module": module_name, "units": mod_dict[module_name]}
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="未找到该课文模块")


@app.get("/api/textbook/grade/{word_module}")
def textbook_by_word_module(word_module: str):
    """根据单词模块找课文模块（如 '上1' → Module 1 三年级上册）"""
    mapping = WORD_TO_LESSON_MODULE.get(word_module)
    if not mapping:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="未找到映射")
    mod_name, semester = mapping
    return {"module": mod_name, "semester": semester}


# 单词模块 → 课文模块+学期
WORD_TO_LESSON_MODULE = {
    # 三年级
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
    # 四年级
    '四上1': ('Module 1', '四年级上册'), '四上2': ('Module 2', '四年级上册'),
    '四上3': ('Module 3', '四年级上册'), '四上4': ('Module 4', '四年级上册'),
    '四上5': ('Module 5', '四年级上册'), '四上6': ('Module 6', '四年级上册'),
    '四上7': ('Module 7', '四年级上册'), '四上8': ('Module 8', '四年级上册'),
    '四上9': ('Module 9', '四年级上册'), '四上10': ('Module 10', '四年级上册'),
    '四下1': ('Module 1', '四年级下册'), '四下2': ('Module 2', '四年级下册'),
    '四下3': ('Module 3', '四年级下册'), '四下4': ('Module 4', '四年级下册'),
    '四下5': ('Module 5', '四年级下册'), '四下6': ('Module 6', '四年级下册'),
    '四下7': ('Module 7', '四年级下册'), '四下8': ('Module 8', '四年级下册'),
    '四下9': ('Module 9', '四年级下册'), '四下10': ('Module 10', '四年级下册'),
    # 五年级
    '五上1': ('Module 1', '五年级上册'), '五上2': ('Module 2', '五年级上册'),
    '五上3': ('Module 3', '五年级上册'), '五上4': ('Module 4', '五年级上册'),
    '五上5': ('Module 5', '五年级上册'), '五上6': ('Module 6', '五年级上册'),
    '五上7': ('Module 7', '五年级上册'), '五上8': ('Module 8', '五年级上册'),
    '五上9': ('Module 9', '五年级上册'), '五上10': ('Module 10', '五年级上册'),
    '五下1': ('Module 1', '五年级下册'), '五下2': ('Module 2', '五年级下册'),
    '五下3': ('Module 3', '五年级下册'), '五下4': ('Module 4', '五年级下册'),
    '五下5': ('Module 5', '五年级下册'), '五下6': ('Module 6', '五年级下册'),
    '五下7': ('Module 7', '五年级下册'), '五下8': ('Module 8', '五年级下册'),
    '五下9': ('Module 9', '五年级下册'), '五下10': ('Module 10', '五年级下册'),
}


# ========== 单词 API ==========

class ModuleInfo(BaseModel):
    module: str
    grade: str
    count: int


class WordItem(BaseModel):
    id: int
    module: str
    grade: str
    word: str
    phonetic: str
    chinese: str
    type: str
    example_en: str
    example_cn: str


@app.get("/api/modules", response_model=List[ModuleInfo])
def list_modules(grade: Optional[str] = None):
    """列出所有模块（可按年级过滤）"""
    all_modules = get_all_modules(grade=grade)
    return all_modules


@app.get("/api/words")
def list_words(module: Optional[str] = None, grade: Optional[str] = None):
    """获取单词列表（可按模块/年级筛选）"""
    if module:
        words = get_words_by_module(module)
    elif grade:
        words = [w for w in WORDS if w.get("grade") == grade]
    else:
        words = WORDS
    return {"total": len(words), "words": words}


@app.get("/api/word/{word_id}", response_model=WordItem)
def get_word(word_id: int):
    """获取单个单词详情"""
    for w in WORDS:
        if w["id"] == word_id:
            return w
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="单词不存在")


@app.get("/api/search")
def search(q: str):
    """搜索单词"""
    results = search_words(q)
    return {"total": len(results), "words": results}


# ========== 进度 API ==========

@app.post("/api/progress/{user_id}/{word_id}")
def update_progress(user_id: str, word_id: int, status: str):
    """标记单词学习状态"""
    if status not in ("learned", "mastered"):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="status 必须是 learned 或 mastered")
    progress_store.mark(user_id, word_id, status)
    return {"ok": True, "word_id": word_id, "status": status}


@app.get("/api/progress/{user_id}")
def get_progress(user_id: str):
    """获取用户所有模块的学习进度"""
    return progress_store.get_all_stats(user_id)


@app.get("/api/progress/{user_id}/{module}")
def get_module_progress(user_id: str, module: str):
    """获取用户在指定模块的进度"""
    prog = progress_store.get_module_progress(user_id, module)
    prog["module"] = module
    return prog


@app.get("/api/word-status/{user_id}")
def get_word_statuses(user_id: str, module: Optional[str] = None, grade: Optional[str] = None):
    """获取用户指定模块或年级的单词状态"""
    statuses = progress_store.get_all_word_statuses(user_id, module=module, grade=grade)
    return statuses


# ========== 测试评分 API ==========

class ScoreRequest(BaseModel):
    user_answer: str
    correct_answer: str


def simple_score(user_answer: str, correct_answer: str) -> dict:
    u = user_answer.strip().lower()
    c = correct_answer.strip().lower()
    if u == c:
        return {"score": 100, "feedback": "太棒了！完全正确！🎉"}
    if not u:
        return {"score": 0, "feedback": "没有输入答案哦，再试一次！"}
    if c in u or u in c:
        return {"score": 80, "feedback": "很接近了！注意大小写和空格哦 💪"}
    if u[0] == c[0] and len(u) >= 2:
        return {"score": 70, "feedback": "开头对了！再仔细看看 ✨"}
    if abs(len(u) - len(c)) <= 2:
        return {"score": 50, "feedback": "差不多对了，再想想 🤔"}
    return {"score": 0, "feedback": "不对哦，再看看答案示例 🔍"}


@app.post("/api/score")
def score(req: ScoreRequest):
    result = simple_score(req.user_answer, req.correct_answer)
    result["correct_answer"] = req.correct_answer
    return result


# ========== KET API ==========

@app.get("/api/ket/categories")
def get_ket_categories():
    categories = []
    for cat_type, cat_data in KET_DATA.items():
        if cat_type == "词汇":
            for sub_cat in cat_data["分类"].keys():
                categories.append({
                    "type": "词汇", "category": sub_cat,
                    "count": len(cat_data["分类"][sub_cat])
                })
        elif cat_type in ["句型", "语法"]:
            for sub_cat in cat_data.keys():
                count = len(cat_data[sub_cat]) if isinstance(cat_data[sub_cat], list) else 1
                categories.append({
                    "type": cat_type, "category": sub_cat, "count": count
                })
    return {"categories": categories}


@app.get("/api/ket/words")
def get_ket_words(category: str):
    if "词汇" in KET_DATA and category in KET_DATA["词汇"]["分类"]:
        return {"words": KET_DATA["词汇"]["分类"][category]}
    return {"words": []}


@app.get("/api/ket/sentences")
def get_ket_sentences(category: str):
    if "句型" in KET_DATA and category in KET_DATA["句型"]:
        return {"sentences": KET_DATA["句型"][category]}
    return {"sentences": []}


@app.get("/api/ket/grammar")
def get_ket_grammar(category: str):
    if "语法" in KET_DATA and category in KET_DATA["语法"]:
        return {"grammar": KET_DATA["语法"][category]}
    return {"grammar": {}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
