# -*- coding: utf-8 -*-
"""
英语学习 App 后端
运行方式: uvicorn main:app --reload --port 8080
访问文档: http://localhost:8080/docs
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
from words_data import WORDS, get_words_by_module, search_words, get_all_modules
from ket_data import KET_DATA

app = FastAPI(
    title="英语学习 App API",
    description="外研社三年级英语学习平台",
    version="1.0.0"
)

# 允许前端跨域访问（开发时放开）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 生产环境改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====================== 数据模型 ======================

class WordItem(BaseModel):
    id: int
    module: str
    word: str
    phonetic: str
    chinese: str
    type: str
    example_en: str
    example_cn: str


class ModuleInfo(BaseModel):
    module: str
    count: int


# ====================== 学习进度（内存版） ======================
# 后续可以换成 MySQL / SQLite 持久化
class ProgressStore:
    """简单内存存储：user_id -> {word_id -> 'learned'/'mastered'}"""

    def __init__(self):
        self._store: dict[str, dict[int, str]] = {}

    def mark(self, user_id: str, word_id: int, status: str):
        if user_id not in self._store:
            self._store[user_id] = {}
        # mastered 覆盖 learned，learned 覆盖 new
        current = self._store[user_id].get(word_id, "new")
        rank = {"new": 0, "learned": 1, "mastered": 2}
        if rank.get(status, 0) >= rank.get(current, 0):
            self._store[user_id][word_id] = status

    def get_word_status(self, user_id: str, word_id: int) -> str:
        return self._store.get(user_id, {}).get(word_id, "new")

    def get_all_word_statuses(self, user_id: str, module: str) -> dict[int, str]:
        """返回该用户在该模块下所有单词的状态 dict{word_id: status}"""
        return self._store.get(user_id, {})

    def get_module_progress(self, user_id: str, module: str) -> dict:
        module_words = get_words_by_module(module)
        total = len(module_words)
        if total == 0:
            return {"total": 0, "learned": 0, "mastered": 0, "percent": 0}
        learned = sum(
            1 for w in module_words
            if self.get_word_status(user_id, w["id"]) in ("learned", "mastered")
        )
        mastered = sum(
            1 for w in module_words
            if self.get_word_status(user_id, w["id"]) == "mastered"
        )
        return {
            "total": total,
            "learned": learned,
            "mastered": mastered,
            "percent": round(learned / total * 100)
        }

    def get_all_stats(self, user_id: str) -> dict:
        all_modules = get_all_modules()
        result = {}
        total_words = 0
        total_learned = 0
        total_mastered = 0
        for m in all_modules:
            prog = self.get_module_progress(user_id, m)
            result[m] = prog
            total_words += prog["total"]
            total_learned += prog["learned"]
            total_mastered += prog["mastered"]
        result["_total"] = {
            "total": total_words,
            "learned": total_learned,
            "mastered": total_mastered,
            "percent": round(total_learned / total_words * 100) if total_words else 0
        }
        return result


progress_store = ProgressStore()


# ====================== API 接口 ======================

@app.get("/")
async def root():
    """根路径返回前端页面"""
    from fastapi.responses import FileResponse
    import os
    index_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"msg": "英语学习 App API", "docs": "/docs"}

# ----- 课文数据 -----
@app.get("/api/textbook")
def get_textbook():
    """获取课文数据"""
    try:
        # 读取 JSON 文件
        with open("textbook3_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="课文数据文件未找到")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"读取课文数据失败: {str(e)}")


# 单词模块到课文模块 + 学期的映射
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
        raise HTTPException(status_code=500, detail=f"获取课文内容失败: {str(e)}")
# ----- 单词 -----

@app.get("/api/modules", response_model=List[ModuleInfo])
def list_modules():
    """列出所有模块"""
    all_modules = get_all_modules()
    return [
        {"module": m, "count": len(get_words_by_module(m))}
        for m in all_modules
    ]


@app.get("/api/words")
def list_words(module: Optional[str] = None):
    """获取单词列表（可按模块筛选）"""
    if module:
        words = get_words_by_module(module)
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


# ----- 学习进度 -----

@app.post("/api/progress/{user_id}/{word_id}")
def update_progress(user_id: str, word_id: int, status: str):
    """
    标记单词学习状态
    status: 'learned' | 'mastered'
    """
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
def get_word_statuses(user_id: str, module: str):
    """获取用户在指定模块下每个单词的学习状态，module 通过 query 参数传入"""
    all_statuses = progress_store.get_all_word_statuses(user_id, module)
    module_words = get_words_by_module(module)
    word_ids = [w["id"] for w in module_words]
    return {wid: all_statuses.get(wid, "new") for wid in word_ids}


# ----- 测试评分 -----

class ScoreRequest(BaseModel):
    user_answer: str
    correct_answer: str


def simple_score(user_answer: str, correct_answer: str) -> dict:
    """
    简单评分算法：
    - 完全一致：100分
    - 首字母/整体相似度高：80分
    - 部分匹配：60分
    - 无关：0分
    """
    u = user_answer.strip().lower()
    c = correct_answer.strip().lower()

    if u == c:
        return {"score": 100, "feedback": "太棒了！完全正确！🎉"}

    if not u:
        return {"score": 0, "feedback": "没有输入答案哦，再试一次！"}

    # 完全包含
    if c in u or u in c:
        return {"score": 80, "feedback": "很接近了！注意大小写和空格哦 💪"}

    # 首字母对比
    if u[0] == c[0] and len(u) >= 2:
        return {"score": 70, "feedback": "开头对了！再仔细看看 ✨"}

    # 长度相近
    if abs(len(u) - len(c)) <= 2:
        return {"score": 50, "feedback": "差不多对了，再想想 🤔"}

    return {"score": 0, "feedback": "不对哦，再看看答案示例 🔍"}


@app.post("/api/score")
def score(req: ScoreRequest):
    """评测用户答案"""
    result = simple_score(req.user_answer, req.correct_answer)
    result["correct_answer"] = req.correct_answer
    return result


# ========== KET 学习 API ==========

@app.get("/api/ket/categories")
def get_ket_categories():
    """获取 KET 学习分类列表"""
    categories = []
    for cat_type, cat_data in KET_DATA.items():
        if cat_type == "词汇":
            for sub_cat in cat_data["分类"].keys():
                categories.append({
                    "type": "词汇",
                    "category": sub_cat,
                    "count": len(cat_data["分类"][sub_cat])
                })
        elif cat_type in ["句型", "语法"]:
            for sub_cat in cat_data.keys():
                count = len(cat_data[sub_cat]) if isinstance(cat_data[sub_cat], list) else 1
                categories.append({
                    "type": cat_type,
                    "category": sub_cat,
                    "count": count
                })
    return {"categories": categories}


@app.get("/api/ket/words")
def get_ket_words(category: str):
    """获取指定分类的 KET 词汇"""
    if "词汇" in KET_DATA and category in KET_DATA["词汇"]["分类"]:
        return {"words": KET_DATA["词汇"]["分类"][category]}
    return {"words": []}


@app.get("/api/ket/sentences")
def get_ket_sentences(category: str):
    """获取指定分类的 KET 句型"""
    if "句型" in KET_DATA and category in KET_DATA["句型"]:
        return {"sentences": KET_DATA["句型"][category]}
    return {"sentences": []}


@app.get("/api/ket/grammar")
def get_ket_grammar(category: str):
    """获取指定分类的 KET 语法"""
    if "语法" in KET_DATA and category in KET_DATA["语法"]:
        return {"grammar": KET_DATA["语法"][category]}
    return {"grammar": {}}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
