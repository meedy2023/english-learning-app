# -*- coding: utf-8 -*-
"""把 english_app 构建为纯静态版（无后端），输出到 docs/ 供 GitHub Pages 使用。

用法：
    cd english_app
    python build_static.py
"""
import os
import sys
import json
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, "backend")
FRONTEND = os.path.join(ROOT, "frontend")
DOCS = os.path.join(ROOT, "docs")
DATA_DIR = os.path.join(DOCS, "data")

os.makedirs(DATA_DIR, exist_ok=True)
sys.path.insert(0, BACKEND)


def export_words():
    import words_data
    words = getattr(words_data, "WORDS", None)
    if words is None:
        # 兼容不同命名
        words = [w for w in dir(words_data) if isinstance(w, list) and w and isinstance(w[0], dict)]
        words = words[0] if words else []
    with open(os.path.join(DATA_DIR, "words.json"), "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=1)
    print(f"[OK] words.json  ({len(words)} 个单词)")


def export_ket():
    import ket_data
    ket = getattr(ket_data, "KET_DATA", None)
    with open(os.path.join(DATA_DIR, "ket.json"), "w", encoding="utf-8") as f:
        json.dump(ket, f, ensure_ascii=False, indent=1)
    print("[OK] ket.json")


def export_phonics():
    import phonics_data
    phonics = getattr(phonics_data, "PHONICS", [])
    with open(os.path.join(DATA_DIR, "phonics.json"), "w", encoding="utf-8") as f:
        json.dump(phonics, f, ensure_ascii=False, indent=1)
    print(f"[OK] phonics.json  ({len(phonics)} \u7ec4)")


def export_textbook():
    # 优先读新版多年级结构，回退到旧版
    for src_name in ["textbook_data.json", "textbook3_data.json"]:
        src = os.path.join(BACKEND, src_name)
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(os.path.join(DATA_DIR, "textbook.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            print(f"[OK] textbook.json  ({src_name})")
            return
    print("[WARN] textbook.json 未找到")


def copy_pwa():
    """复制 PWA 资源（manifest/sw/icons）到 docs/"""
    for name in ["manifest.json", "sw.js"]:
        src = os.path.join(FRONTEND, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DOCS, name))
            print(f"[OK] docs/{name}")
    icons_src = os.path.join(FRONTEND, "icons")
    icons_dst = os.path.join(DOCS, "icons")
    if os.path.isdir(icons_src):
        os.makedirs(icons_dst, exist_ok=True)
        for f in os.listdir(icons_src):
            shutil.copy2(os.path.join(icons_src, f), os.path.join(icons_dst, f))
        print(f"[OK] docs/icons/ ({len(os.listdir(icons_src))} 个图标)")


def build_index():
    src = os.path.join(FRONTEND, "index.html")
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    # 1) 修改 API 基地址为相对路径（GitHub Pages 子路径友好）
    #    先尝试当前已改过的 IP，再尝试 localhost 兜底
    for old in ['const API = "http://10.255.100.133:8080";',
                'const API = "http://localhost:8080";',
                'const API = "http://10.255.100.251:8080";']:
        if old in html:
            html = html.replace(old, 'const API = ".";')
            break
    if 'const API = "."' not in html:
        # 用正则兜底
        import re
        html = re.sub(r'const API\s*=\s*"[^"]*";', 'const API = ".";', html, count=1)

    # 2) 在主脚本前注入 api-shim.js
    marker = '<script>\n  // ========== 全局状态 =========='
    inject = '<script src="api-shim.js"></script>\n<script>\n  // ========== 全局状态 =========='
    if marker in html and "<script src=\"api-shim.js\"></script>" not in html:
        html = html.replace(marker, inject, 1)
    elif "api-shim.js" not in html:
        # 兜底：在 </head> 前注入
        html = html.replace("</head>", '<script src="api-shim.js"></script></head>')

    out = os.path.join(DOCS, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] docs/index.html  (API 基地址已改为相对路径，已注入 api-shim.js)")


if __name__ == "__main__":
    print("=== 构建静态版 english_app ===")
    export_textbook()
    export_words()
    export_ket()
    export_phonics()
    build_index()
    copy_pwa()
    print("\n完成！静态版已生成在 docs/ 目录。")
    print("把 docs/ 提交并推送到 GitHub，然后在仓库 Settings -> Pages 选择 main 分支 /docs 目录即可。")
