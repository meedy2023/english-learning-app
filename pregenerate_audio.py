# -*- coding: utf-8 -*-
"""预生成课文逐句音频（Edge Neural，无需 API Key），供前端优先播放。

脚本使用当前可用的 edge-tts 协议，生成的是完整音频文件，浏览器端只做普通播放，
因此不受运行时 WebSocket / 讯飞接口波动影响，音质与自然度上限更高。

生成规则与 frontend/index.html 中的角色音色、缩写展开、语速换算保持一致；
每条音频文件名由 (engine, roleVoiceId, speechRate, human, text) 的 FNV-1a 决定，
前端可用同样算法直接定位文件，无需 manifest。缺失文件自动回退现有 TTS 链路。

用法：
    python pregenerate_audio.py --dry-run                        # 课文：只看将生成多少条
    python pregenerate_audio.py --kind words --all-rates         # 单词发音：5 档全量
    python pregenerate_audio.py --kind ket-reading --all-rates   # KET短文单句：5 档全量
    python pregenerate_audio.py --kind examples --all-rates      # 四模块词汇例句：5 档全量
    python pregenerate_audio.py --kind plan-reading --all-rates  # 40天计划短文：5 档全量
    python pregenerate_audio.py --kind vocab-extra --all-rates   # 补充词汇短句(KET/小托福/拼读)：5 档全量
    python pregenerate_audio.py --kind ket-reading-full --all-rates  # KET短文整篇(human=1)：5 档全量
    python pregenerate_audio.py --limit 20                       # 试生成前 20 条
    python pregenerate_audio.py --all-rates --workers 8          # 课文：5 档全量

依赖：
    pip install --upgrade edge-tts
"""
import argparse
import asyncio
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE = ROOT / "docs" / "data" / "textbook.json"
DEFAULT_OUT = ROOT / "docs" / "audio" / "lesson"

# 与 frontend/index.html 的 ROLE_VOICE_POOL / ROLE_VOICE_ASSIGN 保持同步。
ROLE_VOICE_POOL = [
    {"id": "role_f1", "gender": "female", "edge": "en-GB-SoniaNeural"},
    {"id": "role_f2", "gender": "female", "edge": "en-US-JennyNeural"},
    {"id": "role_f3", "gender": "female", "edge": "en-GB-LibbyNeural"},
    {"id": "role_f4", "gender": "female", "edge": "en-US-EmmaNeural"},
    {"id": "role_f5", "gender": "female", "edge": "en-GB-MaisieNeural"},
    {"id": "role_m1", "gender": "male",   "edge": "en-GB-RyanNeural"},
    {"id": "role_m2", "gender": "male",   "edge": "en-GB-ThomasNeural"},
    {"id": "role_m3", "gender": "male",   "edge": "en-US-GuyNeural"},
    {"id": "role_m4", "gender": "male",   "edge": "en-US-ChristopherNeural"},
    {"id": "role_m5", "gender": "male",   "edge": "en-US-EricNeural"},
    # 仅固定分配使用（老师 / 学生），不参与名字哈希兜底，避免影响其它角色。
    # Edge 无真童声：女童声用 Ana（Cute），男童声用 Roger（Lively 年轻男声）。
    {"id": "role_teacher", "gender": "female", "edge": "en-US-AriaNeural", "fixedOnly": True},
    {"id": "role_child_f", "gender": "female", "edge": "en-US-AnaNeural",  "fixedOnly": True},
    {"id": "role_child_m", "gender": "male",   "edge": "en-US-RogerNeural", "fixedOnly": True},
]
ROLE_VOICE_ASSIGN = {
    "teacher": "role_teacher", "narrator": "role_m4",
    "barbapapa": "role_m2",  # 巴巴爸爸是孩子们的 Dad，固定低沉男声（避免与 Tom 撞青年男声）
    "lingling": "role_f1", "amy": "role_f2", "wenwen": "role_f3", "jingjing": "role_f4", "yanyan": "role_f5",
    "huahua": "role_f1", "weiwei": "role_f2", "lanlan": "role_f3", "nana": "role_f4", "jiajia": "role_f5",
    "tippi": "role_f3", "little chicken": "role_f3", "baby": "role_f3",
    # 学生标签统一用儿童音：女童声 / 男童声
    "girl": "role_child_f", "student": "role_child_f", "students": "role_child_f",
    "boy": "role_child_m", "kids": "role_child_m", "children": "role_child_m",
    "mum": "role_f4", "mother": "role_f4", "amy's mum": "role_f4", "ms smart": "role_f4", "ms li": "role_f4", "ms olivia": "role_f4",
    "grandma": "role_f5", "mother hen": "role_f5", "woman": "role_f5",
    "tom": "role_m1", "bob": "role_m1", "bobo": "role_m1", "bobby": "role_m1", "li han": "role_m1", "jay": "role_m1",
    "dad": "role_m2", "father": "role_m2", "man": "role_m2", "liu fei": "role_m2", "jim": "role_m2", "doctor": "role_m2", "detective sharp": "role_m2",
    "sam": "role_m3", "taotao": "role_m3", "ray": "role_m3",
    "daming": "role_m5", "ben": "role_m5", "david": "role_m5", "yangyang": "role_m5",
    "grandpa": "role_m4", "terry": "role_m4", "old man": "role_m4", "lu xun": "role_m4", "fabre": "role_m4", "samuel pepys": "role_m4",
}
ROLE_FEMALE_NAMES = [
    "amy", "lingling", "wenwen", "yanyan", "jingjing", "lanlan", "huahua", "weiwei",
    "nana", "jiajia", "yoyo", "lulu", "coco", "susu", "mia", "tippi",
    "mum", "mother", "grandma", "sister", "girl", "woman", "baby",
    "ms smart", "ms li", "ms olivia", "mother hen", "mum bird",
    "duoduo", "zuzu",
]
ROLE_MALE_NAMES = [
    "sam", "daming", "tom", "ben", "bob", "bobo", "david", "terry", "jay", "ray",
    "jim", "bobby", "taotao", "yangyang", "li han", "liu fei", "lu xun", "fabre",
    "yang shanzhou", "samuel pepys", "detective sharp", "dad", "father", "grandpa",
    "boy", "man", "old man", "dad dog",
]
ROLE_HUMAN_NEUTRAL = re.compile(
    r"^(teacher|narrator|student|students|kids|children|everyone|all|both|family|friend|"
    r"my new friend|host|old friends|zookeeper|police officer|forest keeper|barbapapa|tutu|lin jia)\b",
    re.I,
)
# 以下角色一律沿用设置页发音人（不分配独立音色），与前端 roleShouldDefault 保持一致：
# 1) 多人合读：含 & / , / and；2) 群体齐读；3) 动物（真实动物 + 拟人会说话的动物）
ROLE_GROUP_CHORUS = re.compile(r"^(both|everyone|everybody|all|family|children|kids|students|people)$", re.I)
ROLE_ANIMAL = re.compile(
    r"^(susu|baby|mother hen|mum bird|dad dog|little chicken|little dog|bird|dog|duck|frog|"
    r"rabbit|bear|mouse 1|mouse 2|night owl|silkworm|giraffe)$", re.I)


def role_should_default(raw, role):
    if re.search(r"[&,]|\band\b", raw, re.I):
        return True
    if ROLE_GROUP_CHORUS.match(raw):
        return True
    if ROLE_ANIMAL.match(raw):
        return True
    return False
ROLE_BY_ID = {p["id"]: p for p in ROLE_VOICE_POOL}
ROLE_IDS_BY_GENDER = {
    g: [p["id"] for p in ROLE_VOICE_POOL if p["gender"] == g and not p.get("fixedOnly")]
    for g in ("female", "male")
}
ALL_ROLE_IDS = [p["id"] for p in ROLE_VOICE_POOL if not p.get("fixedOnly")]

RATE_TABLE = [
    (0.5, 0.775),
    (0.8, 0.830),
    (1.0, 1.000),
    (1.2, 1.180),
    (1.5, 1.390),
]
ALL_RATES = [r for r, _ in RATE_TABLE]


def fnv1a32(text):
    h = 0x811C9DC5
    for ch in text:
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def single_role_gender(role):
    p = role.strip().lower().replace("’", "'")
    if p in ROLE_FEMALE_NAMES:
        return "female"
    if p in ROLE_MALE_NAMES:
        return "male"
    if re.search(r"^(ms|mrs|miss)\b|mum|mother|grandma|sister|girl|woman", p):
        return "female"
    if re.search(r"^(mr|sir)\b|dad|father|grandpa|boy|man", p):
        return "male"
    return None


def role_gender(role):
    raw = str(role or "").strip().lower().replace("’", "'")
    if not raw:
        return None
    parts = [s.strip() for s in re.split(r"\s*(?:&|,|\band\b)\s*", raw, flags=re.I) if s.strip()]
    gs = [single_role_gender(p) for p in parts]
    if len(gs) > 1:
        if all(g == "female" for g in gs):
            return "female"
        if all(g == "male" for g in gs):
            return "male"
        return None
    return gs[0] if gs else None


def role_voice_id(role):
    raw = str(role or "").strip().lower().replace("’", "'")
    if not raw:
        return None
    if role_should_default(raw, role):
        return None
    if raw in ROLE_VOICE_ASSIGN:
        return ROLE_VOICE_ASSIGN[raw]
    gender = role_gender(role)
    if not gender and not ROLE_HUMAN_NEUTRAL.match(raw):
        return None
    ids = ROLE_IDS_BY_GENDER[gender] if gender else ALL_ROLE_IDS
    return ids[fnv1a32(raw) % len(ids)]


def edge_voice_for(voice_id):
    profile = ROLE_BY_ID.get(voice_id)
    return profile["edge"] if profile else "en-GB-SoniaNeural"


def synth_rate(rate):
    r = max(0.5, min(1.5, float(rate)))
    for (ua, sa), (ub, sb) in zip(RATE_TABLE, RATE_TABLE[1:]):
        if r <= ub:
            t = (r - ua) / (ub - ua)
            return sa + t * (sb - sa)
    return RATE_TABLE[-1][1]


def edge_rate_pct(rate):
    return int(round((synth_rate(rate) - 1) * 100))


# 英文朗读文本里偶尔嵌入单个汉字（如课文 'The word is "早".'）。
# en-US 英文音色会静默跳过汉字导致不发音，发音前把汉字替换成无声调拼音。
# 此表必须与前端 index.html 的 ZH_TO_PINYIN 逐字一致，否则本地音频哈希 key 对不上。
# 扩展：若课文新增汉字，用 pypinyin 的 lazy_pinyin(ch)[0] 得到无声调拼音，
#       在此表和前端同步添加。
ZH_TO_PINYIN = {"早": "zao"}


def han_to_pinyin(text):
    if not text or not re.search(r"[\u3400-\u9fff]", text):
        return text
    return re.sub(r"[\u3400-\u9fff]", lambda m: ZH_TO_PINYIN.get(m.group(0), m.group(0)), text)


def expand_abbrev(text):
    text = han_to_pinyin(text)
    text = re.sub(r"\bMs\.?\s+(?=[A-Z])", "Miz ", text)
    text = re.sub(r"\bMr\.?\s+(?=[A-Z])", "Mister ", text)
    text = re.sub(r"\bMrs\.?\s+(?=[A-Z])", "Missus ", text)
    text = re.sub(r"\bDr\.?\s+(?=[A-Z])", "Doctor ", text)
    text = re.sub(r"\bSt\.?\s+(?=[A-Z])", "Saint ", text)
    return text


# 含汉字拼音占位的文本，音频内容曾从「英文读拼音」改为「中文音色读汉字」，二者共用同一哈希 key。
# 设备一旦缓存旧音频（HTTP/SW cache-first），同名文件会一直命中旧内容。给这类文本的 canon
# 追加内容版本 tag 换一个新 key，强制所有缓存层重新拉取。必须与前端 audioContentTag() 逐字一致。
AUDIO_ZH_CONTENT_TAG = "|zhmix2"


def audio_content_tag(text):
    for pinyin in ZH_TO_PINYIN.values():
        if re.search(r"\b" + re.escape(pinyin) + r"\b", text, re.I):
            return AUDIO_ZH_CONTENT_TAG
    return ""


def audio_key(text, voice_id, rate, human=True):
    # human=1：课文逐句/短文（speakSentence，分角色 human prosody）
    # human=0：单词/例句/KET短文单句（speak，普通发音）
    # 与前端 preAudioUrl 的 canon：'edge|' + (voiceId||'default') + '|' + speechRate + '|' + (human?'1':'0') + '|' + text + audioContentTag(text)
    h = "1" if human else "0"
    canon = "edge|" + (voice_id or "default") + "|" + format(float(rate), "g") + "|" + h + "|" + text + audio_content_tag(text)
    return format(fnv1a32(canon), "08x")


def audio_path(out_dir, text, voice_id, rate, human=True):
    key = audio_key(text, voice_id, rate, human)
    return Path(out_dir) / key[:2] / (key + ".mp3")


async def _synth_edge(text, voice, rate_pct, timeout):
    """调用 Edge TTS 合成单段文本，返回 mp3 字节。"""
    try:
        import edge_tts
    except ImportError:
        raise RuntimeError("缺少依赖 edge-tts，请先执行：pip install --upgrade edge-tts")

    rate = format(rate_pct, "+d") + "%"
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        boundary="SentenceBoundary",
        connect_timeout=max(5, timeout),
        receive_timeout=max(10, timeout),
    )
    chunks = []
    async for chunk in communicate.stream():
        if chunk.get("type") == "audio" and chunk.get("data"):
            chunks.append(chunk["data"])
    if not chunks:
        raise RuntimeError("Edge 未返回音频数据")
    return b"".join(chunks)


# 英文句子里嵌入的单个汉字，展开成拼音后由英文音色读会变成按字母拼读（zao → /zɔː/），
# 不是汉字本身的音。合成时把这些拼音占位还原成汉字，改用中文音色朗读，再按原顺序拼接 mp3。
# 哈希 key 仍基于展开后的拼音文本（前端 preAudioUrl 口径），只是音频内容换成了正确的中文发音。
PINYIN_TO_HAN = {pinyin: han for han, pinyin in ZH_TO_PINYIN.items()}
ZH_SOLO_VOICE = "zh-CN-YunxiaNeural"   # 单字朗读用清晰女声；音色池见 ROLE_VOICE_POOL 注释


async def synth_async(text, voice, rate_pct, timeout):
    """合成文本；若含有由汉字展开来的拼音占位，则分段用对应中文音色朗读后拼接。"""
    # 仅当文本里出现已知的拼音占位时才走混合路径；普通文本保持原样，零开销。
    hits = [p for p in PINYIN_TO_HAN if re.search(r"\b" + re.escape(p) + r"\b", text, re.I)]
    if not hits:
        return await _synth_edge(text, voice, rate_pct, timeout)

    # 按拼音占位切段：英文段沿用角色音色，拼音段还原成汉字用中文音色。
    pattern = re.compile(r"\b(" + "|".join(re.escape(p) for p in hits) + r")\b", re.I)
    pieces = []
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            seg = text[pos:m.start()]
            if seg.strip():
                pieces.append((seg, voice))
        han = PINYIN_TO_HAN[m.group(1).lower()]
        pieces.append((han, ZH_SOLO_VOICE))
        pos = m.end()
    if pos < len(text) and text[pos:].strip():
        # 尾部若只剩标点（如 "zao". 的 "）. 英文音色读不出，丢弃不影响语义。
        pieces.append((text[pos:], voice))

    parts = []
    for seg, seg_voice in pieces:
        # Edge 对纯标点（如 "."、""）不返回音频，跳过即可。
        if not re.search(r"[A-Za-z\u3400-\u9fff0-9]", seg):
            continue
        parts.append(await _synth_edge(seg, seg_voice, rate_pct, timeout))
    if not parts:
        raise RuntimeError("混合文本未返回任何音频数据")
    return b"".join(parts)


def generate_one(job, out_dir, timeout, retries):
    text, voice_id, rate, voice, human = job
    target = audio_path(out_dir, text, voice_id, rate, human)
    if target.exists() and target.stat().st_size > 0:
        return "skip", target, None
    target.parent.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            data = asyncio.run(synth_async(text, voice, edge_rate_pct(rate), timeout))
            tmp = target.with_name(target.name + ".tmp." + str(os.getpid()) + "." + str(attempt))
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, target)
            return "ok", target, None
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.6 * attempt)
    return "fail", target, last_error


def _add_jobs(jobs, seen, texts, rates, human=True, role=""):
    """把一批文本按 (spoken, voice_id, rate, edge_voice, human) 加入 job 列表。"""
    voice_id = role_voice_id(role) if role else None
    edge = edge_voice_for(voice_id)
    for raw in texts:
        spoken = expand_abbrev(str(raw or "").strip())
        if not spoken:
            continue
        for rate in rates:
            key = audio_key(spoken, voice_id, rate, human)
            if key in seen:
                continue
            seen.add(key)
            jobs.append((spoken, voice_id, rate, edge, human))


KIND_LABELS = {
    "lesson": "课文逐句",
    "words": "单词发音",
    "ket-reading": "KET短文单句",
    "examples": "词汇例句（四模块）",
    "plan-reading": "40天计划短文",
    "vocab-extra": "补充词汇短句（KET/小托福/拼读，human=0）",
    "ket-reading-full": "KET短文整篇（human=1）",
    "phonics-reading": "自然拼读分类短文整段（human=1）",
}
# 各 kind 的默认数据源；--source 可显式覆盖（多源聚合 kind 忽略 --source）
DEFAULT_SOURCE_BY_KIND = {
    "lesson": ROOT / "docs" / "data" / "textbook.json",
    "words": ROOT / "docs" / "data" / "words.json",
    "ket-reading": ROOT / "docs" / "data" / "ket.json",
    "examples": ROOT / "docs" / "data",          # 目录：words/ket/toefl/toefl-plan 四份
    "plan-reading": ROOT / "docs" / "data" / "toefl-plan.json",
    "vocab-extra": ROOT / "docs" / "data",       # 目录：ket/toefl/phonics 三份 + 固定预览文本
    "ket-reading-full": ROOT / "docs" / "data" / "ket.json",
    "phonics-reading": ROOT / "docs" / "data" / "phonics.json",
}
DATA_DIR = ROOT / "docs" / "data"


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_jobs(source, rates, limit, kind="lesson"):
    """按 kind 收集音频任务，每条 job 为 (spoken, voice_id, rate, edge_voice, human)：
    - lesson：课文逐句（human=1，分角色音色），5 层嵌套的 content[].text/role
    - words：单词发音（human=0，默认音），words.json 的 word 字段
    - ket-reading：KET 短文单句（human=0，默认音），ket.json 的 短文[].sentences[].en
    - examples：词汇例句（human=0，默认音）——前端 speakWord(example_en/example) → TTS.speak → human=0
        来源：words.json 的 example_en、ket.json 词汇.example、toefl.json 词汇.example、
              toefl-plan.json 的 words[].word（40天计划单词也走 speakWord）
    - plan-reading：40天计划短文（human=1，默认音）——LessonReader.bind([{en:passage.en}])
        → speakSentence(human=true, voiceId=null)；静态文本，可预生成
    - vocab-extra：补充词汇短句（human=0，默认音）——凡经 speakWord() 朗读、
        但不在 words.json / 例句覆盖内的静态文本：KET 词汇 word、KET 句型 english、
        KET 语法例句、小托福词汇 word、拼读 words[].w 与 sound_word，以及设置页固定预览句。
        前端入口：KET/小托福词表朗读、测验 speakKetQuizWord、PK/Spell/Doodle/Match、
        词卡、音标缺素材回退、发音人预览。
    - ket-reading-full：KET 短文整篇（human=1，默认音）——LessonReader.bind(sentences)
        → speakSentence(human=true, voiceId=null)。单句朗读是 human=0（ket-reading kind），
        哈希 key 不同，必须单独生成，不能复用 ket-reading 的文件。
    - phonics-reading：自然拼读分类短文整段（human=1，默认音）——renderPhonicsReading()
        按固定模板+分组词表抽样拼装成一段，LessonReader.bind([{text:para}]) → speakSentence
        (human=true, voiceId=null)。词表/模板/步长全固定，短文文本可精确复现，故可做预生成；
        必须与前端 renderPhonicsReading() 的抽样算法逐字一致，否则 key 对不上。
    注：小托福分类短文仍依赖运行时抽样，文本不固定，走
        「预生成 miss → 网络合成+内存缓存 → 本机」回退，不做预生成。
    """
    jobs, seen = [], set()

    if kind == "lesson":
        data = _load(source)
        for grades in data.values():
            for terms in grades.values():
                for units in terms.values():
                    for lessons in units.values():
                        for lesson in lessons:
                            for line in lesson.get("content", []):
                                _add_jobs(jobs, seen, [line.get("text")], rates, True, line.get("role") or "")
    elif kind == "words":
        data = _load(source)
        texts = [w.get("word") for w in data if isinstance(w, dict)] if isinstance(data, list) else []
        _add_jobs(jobs, seen, texts, rates, False, "")
    elif kind == "ket-reading":
        data = _load(source)
        texts = []
        for item in (data.get("短文") or {}).values():
            for sent in (item.get("sentences") or []):
                texts.append(sent.get("en"))
        _add_jobs(jobs, seen, texts, rates, False, "")
    elif kind == "examples":
        texts = []
        # words.json：example_en
        for w in _load(DATA_DIR / "words.json"):
            if isinstance(w, dict):
                texts.append(w.get("example_en"))
        # ket.json：词汇/分类/*[].example
        ket = _load(DATA_DIR / "ket.json")
        for cat in (ket.get("词汇", {}).get("分类") or {}).values():
            for item in cat:
                texts.append(item.get("example"))
        # toefl.json：词汇/分类/*[].example
        toefl = _load(DATA_DIR / "toefl.json")
        for cat in (toefl.get("词汇", {}).get("分类") or {}).values():
            for item in cat:
                texts.append(item.get("example"))
        # toefl-plan.json：每单词的 word（同样走 speakWord）
        plan = _load(DATA_DIR / "toefl-plan.json")
        for st in plan.get("stages", []):
            for day in st.get("days", []):
                for w in day.get("words", []):
                    texts.append(w.get("word"))
        _add_jobs(jobs, seen, texts, rates, False, "")
    elif kind == "plan-reading":
        plan = _load(source)
        texts = [day.get("passage", {}).get("en")
                 for st in plan.get("stages", []) for day in st.get("days", [])]
        _add_jobs(jobs, seen, texts, rates, True, "")
    elif kind == "vocab-extra":
        texts = []
        ket = _load(DATA_DIR / "ket.json")
        # 词汇/分类/*[].word（KET 词表朗读、测验 speak=item.en、PK/Spell 等）
        for cat in (ket.get("词汇", {}).get("分类") or {}).values():
            for item in cat:
                texts.append(item.get("word"))
        # 句型/*[].english
        for cat in (ket.get("句型") or {}).values():
            for item in cat:
                texts.append(item.get("english"))
        # 语法/*.例句[]（语法挖空题朗读完整例句）
        for item in (ket.get("语法") or {}).values():
            if isinstance(item, dict):
                for sent in (item.get("例句") or []):
                    texts.append(sent)
        # 小托福 词汇/分类/*[].word
        toefl = _load(DATA_DIR / "toefl.json")
        for cat in (toefl.get("词汇", {}).get("分类") or {}).values():
            for item in cat:
                texts.append(item.get("word"))
        # 拼读：[].lessons[].words[].w 与 lessons[].sound_word
        phonics = _load(DATA_DIR / "phonics.json")
        for group in phonics:
            for lesson in group.get("lessons", []):
                texts.append(lesson.get("sound_word"))
                for word in lesson.get("words", []):
                    texts.append(word.get("w"))
        # 设置页语速预览固定句（前端 previewSpeechRate 硬编码）
        texts.append("Hello! How are you today?")
        _add_jobs(jobs, seen, texts, rates, False, "")
    elif kind == "ket-reading-full":
        ket = _load(source)
        texts = []
        for item in (ket.get("短文") or {}).values():
            for sent in (item.get("sentences") or []):
                texts.append(sent.get("en"))
        # 整篇播放器 bind(sentences) 取 text||en，无 role → voiceId=null，human=1
        _add_jobs(jobs, seen, texts, rates, True, "")
    elif kind == "phonics-reading":
        # 复现前端 renderPhonicsReading() + phonicsGroupWords()：
        #   词表 = 各组 lessons[].words[].w 按出现顺序去重(lower)；
        #   取样 = step=max(1,floor(len/12))，从 0 起每 step 取一个，最多 12 个；
        #   模板 = PHONICS_READING_TPL[idx % 8] 套 {w}；整段 = 各句空格拼接。
        tpl = [
            "Look at the {w}.", "I can see a {w}.", "This is a {w}.", "I like the {w}.",
            "Can you find the {w}?", "The {w} is here.", "I have a {w}.", "Where is the {w}?",
        ]
        texts = []
        for group in _load(source):
            items, seen_w = [], set()
            for lesson in (group.get("lessons") or []):
                for w in (lesson.get("words") or []):
                    word = str(w.get("w") or "").strip()
                    key = word.lower()
                    if not key or key in seen_w:
                        continue
                    seen_w.add(key)
                    items.append(word)
            n = len(items)
            if not n:
                continue
            step = max(1, n // 12)
            picked, i = [], 0
            while i < n and len(picked) < 12:
                picked.append(items[i])
                i += step
            para = " ".join(tpl[idx % len(tpl)].replace("{w}", w) for idx, w in enumerate(picked))
            texts.append(para)
        # 播放器 bind([{text:para}]) 无 role → voiceId=null，human=1
        _add_jobs(jobs, seen, texts, rates, True, "")
    else:
        raise ValueError("未知 kind: " + kind)

    if limit:
        jobs = jobs[:limit]
    return jobs


def main():
    ap = argparse.ArgumentParser(description="预生成固定文本音频（Edge Neural）")
    ap.add_argument("--kind", default="lesson", choices=list(KIND_LABELS),
                    help="数据源类型：lesson=课文逐句 / words=单词发音 / ket-reading=KET短文单句 / "
                         "examples=四模块词汇例句 / plan-reading=40天计划短文 / "
                         "vocab-extra=补充词汇短句(KET/小托福/拼读,human=0) / "
                         "ket-reading-full=KET短文整篇(human=1) / "
                         "phonics-reading=自然拼读分类短文整段(human=1)")
    ap.add_argument("--source", default=None, help="JSON 路径（默认按 --kind 自动选择）")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT), help="音频输出目录")
    ap.add_argument("--rate", type=float, action="append", help="生成语速档，可重复；默认 0.8")
    ap.add_argument("--all-rates", action="store_true", help="生成全部 5 个语速档")
    ap.add_argument("--limit", type=int, default=0, help="最多生成条数（0=全部）")
    ap.add_argument("--workers", type=int, default=6, help="并发数")
    ap.add_argument("--timeout", type=int, default=30, help="单次连接超时秒数")
    ap.add_argument("--retries", type=int, default=3, help="失败重试次数")
    ap.add_argument("--dry-run", action="store_true", help="只统计不合成")
    args = ap.parse_args()

    source = Path(args.source) if args.source else DEFAULT_SOURCE_BY_KIND[args.kind]
    rates = ALL_RATES if args.all_rates else (args.rate or [0.8])
    for r in rates:
        if r not in ALL_RATES:
            ap.error("不支持的语速 " + str(r) + "，可选：" + ", ".join(map(str, ALL_RATES)))

    jobs = collect_jobs(source, rates, args.limit, args.kind)
    print("类型：" + KIND_LABELS[args.kind] + "  数据源：" + source.name +
          "  待处理：" + str(len(jobs)) + " 条，语速=" + ", ".join(format(r, "g") for r in rates))
    if args.dry_run:
        for job in jobs[:5]:
            print("  " + audio_path(args.out_dir, job[0], job[1], job[2], job[4]).name +
                  "  " + job[3] + "  " + job[0][:50])
        return 0

    counts = {"ok": 0, "skip": 0, "fail": 0}
    failures = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(generate_one, j, args.out_dir, args.timeout, args.retries): j for j in jobs}
        for done, future in enumerate(as_completed(futures), 1):
            status, target, error = future.result()
            counts[status] += 1
            if status == "fail":
                failures.append((futures[future][0], str(error)))
            if done % 50 == 0 or done == len(jobs):
                print("进度 " + str(done) + "/" + str(len(jobs)) +
                      "  新增 " + str(counts["ok"]) + "  跳过 " + str(counts["skip"]) +
                      "  失败 " + str(counts["fail"]))

    print("完成：新增 " + str(counts["ok"]) + "，跳过 " + str(counts["skip"]) +
          "，失败 " + str(counts["fail"]))
    for text, error in failures[:10]:
        print("  失败：" + text[:50] + " -> " + error)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
