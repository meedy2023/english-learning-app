# -*- coding: utf-8 -*-
"""
鑻辫瀛︿範 App 鍚庣
杩愯鏂瑰紡: uvicorn main:app --reload --port 8080
璁块棶鏂囨。: http://localhost:8080/docs
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
    title="鑻辫瀛︿範 App API",
    description="澶栫爺绀句笁骞寸骇鑻辫瀛︿範骞冲彴",
    version="1.0.0"
)

# 鍏佽鍓嶇璺ㄥ煙璁块棶锛堝紑鍙戞椂鏀惧紑锛?
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 鐢熶骇鐜鏀规垚鍏蜂綋鍩熷悕
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====================== 鏁版嵁妯″瀷 ======================

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


# ====================== 瀛︿範杩涘害锛堝唴瀛樼増锛?======================
# 鍚庣画鍙互鎹㈡垚 MySQL / SQLite 鎸佷箙鍖?
class ProgressStore:
    """绠€鍗曞唴瀛樺瓨鍌細user_id -> {word_id -> 'learned'/'mastered'}"""

    def __init__(self):
        self._store: dict[str, dict[int, str]] = {}

    def mark(self, user_id: str, word_id: int, status: str):
        if user_id not in self._store:
            self._store[user_id] = {}
        # mastered 瑕嗙洊 learned锛宭earned 瑕嗙洊 new
        current = self._store[user_id].get(word_id, "new")
        rank = {"new": 0, "learned": 1, "mastered": 2}
        if rank.get(status, 0) >= rank.get(current, 0):
            self._store[user_id][word_id] = status

    def get_word_status(self, user_id: str, word_id: int) -> str:
        return self._store.get(user_id, {}).get(word_id, "new")

    def get_all_word_statuses(self, user_id: str, module: str) -> dict[int, str]:
        """杩斿洖璇ョ敤鎴峰湪璇ユā鍧椾笅鎵€鏈夊崟璇嶇殑鐘舵€?dict{word_id: status}"""
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


# ====================== API 鎺ュ彛 ======================

REPLACED
