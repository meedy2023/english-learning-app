// api-shim.js
// 纯静态版：支持多年级（三年级/四年级/五年级），用本地 JSON 模拟 FastAPI 后端接口。
(function () {
  "use strict";

  const _origFetch = window.fetch ? window.fetch.bind(window) : null;

  // ---------- 数据容器 ----------
  const DATA = { words: [], textbook: {}, ket: {} };
  let _ready = null;

  function loadData() {
    if (_ready) return _ready;
    _ready = Promise.all([
      fetch("./data/words.json").then((r) => r.json()),
      fetch("./data/textbook.json").then((r) => r.json()),
      fetch("./data/ket.json").then((r) => r.json()),
    ])
      .then(([w, t, k]) => {
        DATA.words = Array.isArray(w) ? w : w.words || [];
        DATA.textbook = t || {};
        DATA.ket = k || {};
      })
      .catch((e) => {
        console.error("[静态版] 数据加载失败：", e);
        alert("数据加载失败，请确认 data/ 目录下的 JSON 文件存在。");
      });
    return _ready;
  }
  loadData();

  // ---------- 进度存储（localStorage 替代后端内存） ----------
  function progKey(uid) { return "progress_" + uid; }
  function getProg(uid) {
    try { return JSON.parse(localStorage.getItem(progKey(uid)) || "{}"); }
    catch (e) { return {}; }
  }
  function setProg(uid, p) { localStorage.setItem(progKey(uid), JSON.stringify(p)); }
  const RANK = { new: 0, learned: 1, mastered: 2 };

  function json(obj, status) {
    return new Response(JSON.stringify(obj), {
      status: status || 200,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }

  // ---------- 年级 ----------
  function getGrades() {
    const root = DATA.textbook["外研社"] || DATA.textbook;
    return Object.keys(root).filter((k) => typeof root[k] === "object");
  }

  // ---------- 单词模块（支持年级过滤） ----------
  function getModules(grade) {
    const seen = {};
    DATA.words.forEach((w) => {
      if (!w.module) return;
      if (grade && w.grade !== grade) return;
      seen[w.module] = true;
    });
    return Object.keys(seen).sort();
  }

  function wordsByModuleAndGrade(m, grade) {
    return DATA.words.filter((w) => {
      if (w.module !== m) return false;
      if (grade && w.grade !== grade) return false;
      return true;
    });
  }

  function searchWords(q) {
    q = (q || "").toLowerCase();
    return DATA.words.filter((w) =>
      (w.word || "").toLowerCase().includes(q) ||
      (w.chinese || "").includes(q) ||
      (w.phonetic || "").toLowerCase().includes(q) ||
      (w.example_en || "").toLowerCase().includes(q)
    );
  }

  // ---------- 单词模块→课文映射（三个年级） ----------
  const WORD_TO_LESSON = {
    // 三年级上册（2024新版：Welcome + Unit 1~6）
    "三上0": ["Welcome to school", "三年级上册"],
    "三上1": ["Unit 1 Let's be friends!", "三年级上册"],
    "三上2": ["Unit 2 My school things", "三年级上册"],
    "三上3": ["Unit 3 It's a colourful world!", "三年级上册"],
    "三上4": ["Unit 4 Fun with numbers", "三年级上册"],
    "三上5": ["Unit 5 We're family", "三年级上册"],
    "三上6": ["Unit 6 My sweet home", "三年级上册"],
    // 三年级下册（2024新版：Unit 1~6）
    "三下1": ["Unit 1 Animal friends", "三年级下册"], "三下2": ["Unit 2 Know your body", "三年级下册"],
    "三下3": ["Unit 3 Yummy food", "三年级下册"], "三下4": ["Unit 4 What's your hobby?", "三年级下册"],
    "三下5": ["Unit 5 What time is it?", "三年级下册"], "三下6": ["Unit 6 A great week", "三年级下册"],
    // 四年级
    "四三上1": ["Unit 1 I love sports", "四年级上册"], "四三上2": ["Unit 2 Helping at home", "四年级上册"],
    "四三上3": ["Unit 3 What's the weather like?", "四年级上册"], "四三上4": ["Unit 4 Wonderful seasons", "四年级上册"],
    "四三上5": ["Unit 5 Let's go!", "四年级上册"], "四三上6": ["Unit 6 Find your way", "四年级上册"],
    "四三下1": ["Unit 1 People at work", "四年级下册"], "四三下2": ["Unit 2 How do you feel today", "四年级下册"],
    "四三下3": ["Unit 3 Everyone's got talent", "四年级下册"], "四三下4": ["Unit 4 Plant life", "四年级下册"],
    "四三下5": ["Unit 5 School activities", "四年级下册"], "四三下6": ["Unit 6 Cool clothes", "四年级下册"],
            // 五年级
    "五三上1": ["Unit 1 What's on your plate?", "五年级上册"], "五三上2": ["Unit 2 A green life", "五年级上册"],
    "五三上3": ["Unit 3 Happy together", "五年级上册"], "五三上4": ["Unit 4 A better me", "五年级上册"],
    "五三上5": ["Unit 5 Look into the future", "五年级上册"], "五三上6": ["Unit 6 Enjoy the festivals", "五年级上册"],
    "五三下1": ["Unit 1 Growing up", "五年级下册"], "五三下2": ["Unit 2 You can make a difference", "五年级下册"],
    "五三下3": ["Unit 3 We love reading", "五年级下册"], "五三下4": ["Unit 4 Back in time", "五年级下册"],
    "五三下5": ["Unit 5 Work it out", "五年级下册"], "五三下6": ["Unit 6 Then and now", "五年级下册"],
  };

  // ---------- 课文模块列表 ----------
  // 数据结构：{外研社: {年级: {学期: {Module N: [units]}}}}}
  function textbookModules(grade) {
    const res = [];
    const root = DATA.textbook["外研社"] || {};
    const grades = grade ? [grade] : Object.keys(root);
    grades.forEach((g) => {
      const semesters = root[g] || {};  // {上册: {...}, 下册: {...}}
      Object.keys(semesters).forEach((sem) => {
        const modDict = semesters[sem];  // {Module 1: [...], Module 2: [...]}
        if (typeof modDict !== "object") return;
        Object.keys(modDict).forEach((modName) => {
          const units = modDict[modName];
          if (Array.isArray(units) && units.length > 0) {
            res.push({ module: modName, grade: g, semester: sem, grade_label: g + sem, unit_count: units.length });
          }
        });
      });
    });
    // 去重：同年级同 Module 只保留一个
    const seen = {};
    return res.filter((item) => {
      const key = item.grade + "/" + item.module;
      if (seen[key]) return false;
      seen[key] = true;
      return true;
    });
  }

  // ---------- 课文模块详情 ----------
  function textbookModuleDetail(moduleName, grade) {
    const root = DATA.textbook["外研社"] || {};
    const grades = grade ? [grade] : Object.keys(root);
    const target = String(moduleName).trim().toLowerCase();
    for (const g of grades) {
      const semesters = root[g] || {};
      for (const sem of Object.keys(semesters)) {
        const modDict = semesters[sem];
        if (typeof modDict !== "object") continue;
        for (const key of Object.keys(modDict)) {
          const k = key.trim().toLowerCase();
          if (k === target || k.startsWith(target)) {
            return { module: key, grade: g, semester: sem, units: modDict[key] };
          }
        }
      }
    }
    return null;
  }

  // ---------- 进度统计（支持年级前缀 key） ----------
  function moduleProgress(uid, m, grade) {
    const ws = wordsByModuleAndGrade(m, grade || null);
    const total = ws.length;
    const prog = getProg(uid);
    let learned = 0, mastered = 0;
    ws.forEach((w) => {
      const s = prog[w.id] || "new";
      if (s === "learned" || s === "mastered") learned++;
      if (s === "mastered") mastered++;
    });
    const pct = total ? Math.round((learned / total) * 100) : 0;
    return { module: m, grade: grade || "", total, learned, mastered, percent: pct };
  }

  function allStats(uid) {
    const grades = getGrades();
    const result = {};
    let tw = 0, tl = 0, tm = 0;
    grades.forEach((g) => {
      getModules(g).forEach((m) => {
        const p = moduleProgress(uid, m, g);
        const key = g + "/" + m;
        result[key] = p;
        tw += p.total; tl += p.learned; tm += p.mastered;
      });
    });
    result._total = {
      total: tw, learned: tl, mastered: tm,
      percent: tw ? Math.round((tl / tw) * 100) : 0,
    };
    return result;
  }

  // ---------- KET 分类 ----------
  function ketCategories() {
    const cats = [];
    const kd = DATA.ket;
    if (kd["词汇"] && kd["词汇"]["分类"]) {
      Object.keys(kd["词汇"]["分类"]).forEach((sub) =>
        cats.push({ type: "词汇", category: sub, count: (kd["词汇"]["分类"][sub] || []).length })
      );
    }
    ["句型", "语法"].forEach((t) => {
      if (kd[t]) {
        Object.keys(kd[t]).forEach((sub) => {
          const arr = kd[t][sub];
          cats.push({ type: t, category: sub, count: Array.isArray(arr) ? arr.length : 1 });
        });
      }
    });
    return { categories: cats };
  }

  // ---------- 评分 ----------
  function simpleScore(user_answer, correct_answer) {
    const u = (user_answer || "").trim().toLowerCase();
    const c = (correct_answer || "").trim().toLowerCase();
    if (u === c) return { score: 100, feedback: "太棒了！完全正确！🎉" };
    if (!u) return { score: 0, feedback: "没有输入答案哦，再试一次！" };
    if (c.includes(u) || u.includes(c)) return { score: 80, feedback: "很接近了！注意大小写和空格哦 💪" };
    if (u[0] === c[0] && u.length >= 2) return { score: 70, feedback: "开头对了！再仔细看看 ✨" };
    if (Math.abs(u.length - c.length) <= 2) return { score: 50, feedback: "差不多对了，再想想 🤔" };
    return { score: 0, feedback: "不对哦，再看看答案示例 🔍" };
  }

  // ---------- API 路由 ----------
  async function handleApi(url, init) {
    await loadData();
    const u = new URL(url, location.href);
    const path = u.pathname;
    const idx = path.indexOf("/api/");
    const api = idx >= 0 ? path.slice(idx + 5) : path.replace(/^\/+/, "");
    const params = u.searchParams;
    const method = (init && init.method) || "GET";

    try {
      // ===== 多年级新增接口 =====
      if (api === "grades") return json(getGrades());
      // /api/modules?grade_label=三年级
      if (api === "modules") {
        const grade = params.get("grade") || null;
        const mods = getModules(grade);
        return json(mods.map((m) => ({
          module: m,
          grade: grade || DATA.words.find((w) => w.module === m)?.grade || "",
          count: wordsByModuleAndGrade(m, grade || null).length,
        })));
      }

      // ===== 课文系列 =====
      if (api === "textbook") return json(DATA.textbook);
      if (api === "textbook/modules") {
        const grade = params.get("grade") || null;
        return json(textbookModules(grade));
      }
      if (api.startsWith("textbook/grade/")) {
        const wm = decodeURIComponent(api.slice("textbook/grade/".length));
        const r = WORD_TO_LESSON[wm];
        if (!r) return json({ detail: "无对应课文: " + wm }, 404);
        return json({ word_module: wm, module: r[0], grade: r[1] });
      }
      if (api.startsWith("textbook/")) {
        const rest = decodeURIComponent(api.slice("textbook/".length));
        const parts = rest.split("/");
        const moduleName = parts[0];
        const gradeLabel = params.get("grade_label") || null;
        const root = DATA.textbook["外研社"] || {};
        // 正确拆分年级和学期："五年级下册" → grade="五年级", semKey="下册"
        const _gk = gradeLabel || "";
        const _grade = _gk.replace(/(上册|下册)$/, "");
        const _semKey = _gk ? _gk.slice(_grade.length) : "";
        const _targetGrades = _grade ? [_grade] : Object.keys(root);
        for (const g of _targetGrades) {
          const semesters = root[g] || {};
          for (const sem of Object.keys(semesters)) {
            // 若指定了学期，匹配"下册"=="下册"，不匹配则跳过
            if (_semKey && sem !== _semKey) continue;
            const modDict = semesters[sem];
            if (typeof modDict !== "object") continue;
            const target = String(moduleName).trim().toLowerCase();
            for (const key of Object.keys(modDict)) {
              const k = key.trim().toLowerCase();
              if (k === target || k.startsWith(target)) {
                return json({ module: key, grade: g, semester: sem, units: modDict[key] });
              }
            }
          }
        }
        return json({ detail: "模块不存在: " + moduleName + (gradeLabel ? " (年级: " + gradeLabel + ")" : "") }, 404);
      }

      // ===== 单词系列 =====
      if (api === "words") {
        const m = params.get("module");
        const grade = params.get("grade");
        let ws = DATA.words;
        if (m) ws = ws.filter((w) => w.module === m);
        if (grade) ws = ws.filter((w) => w.grade === grade);
        return json({ total: ws.length, words: ws });
      }
      if (api.startsWith("word/")) {
        const id = parseInt(api.slice(5), 10);
        const w = DATA.words.find((x) => x.id === id);
        if (!w) return json({ detail: "单词不存在" }, 404);
        return json(w);
      }
      if (api === "search") {
        const r = searchWords(params.get("q") || "");
        return json({ total: r.length, words: r });
      }

      // ===== 进度系列 =====
      if (api.startsWith("progress/")) {
        const rest = api.slice("progress/".length);
        const parts = rest.split("/");
        const uid = parts[0];
        if (parts.length === 1) return json(allStats(uid));
        // parts[1] 可能是 "grade/module" 或纯 module
        const gradeSlashModule = decodeURIComponent(parts.slice(1).join("/"));
        const slashIdx = gradeSlashModule.indexOf("/");
        let m, g;
        if (slashIdx >= 0) {
          g = gradeSlashModule.slice(0, slashIdx);
          m = gradeSlashModule.slice(slashIdx + 1);
        } else {
          m = gradeSlashModule;
          g = null;
        }
        return json(moduleProgress(uid, m, g));
      }
      if (api.startsWith("word-status/")) {
        const rest = api.slice("word-status/".length);
        const uid = rest.split("/")[0];
        const m = params.get("module");
        const g = params.get("grade");
        const prog = getProg(uid);
        const out = {};
        wordsByModuleAndGrade(m, g || null).forEach((w) => {
          out[w.id] = prog[w.id] || "new";
        });
        return json(out);
      }
      if (api === "score") {
        let body = {};
        try { body = JSON.parse((init && init.body) || "{}"); } catch (e) {}
        const r = simpleScore(body.user_answer, body.correct_answer);
        return json(Object.assign({ correct_answer: body.correct_answer }, r));
      }

      // ===== KET 系列 =====
      if (api === "ket/categories") return json(ketCategories());
      if (api === "ket/words") {
        const c = params.get("category");
        const list = (DATA.ket["词汇"] && DATA.ket["词汇"]["分类"] && DATA.ket["词汇"]["分类"][c]) || [];
        return json({ words: list });
      }
      if (api === "ket/sentences") {
        const c = params.get("category");
        const list = (DATA.ket["句型"] && DATA.ket["句型"][c]) || [];
        return json({ sentences: list });
      }
      if (api === "ket/grammar") {
        const c = params.get("category");
        const g = (DATA.ket["语法"] && DATA.ket["语法"][c]) || {};
        return json({ grammar: g });
      }
      if (api === "ket/reading") {
        const c = params.get("category");
        const r = (DATA.ket["短文"] && DATA.ket["短文"][c]) || null;
        return json({ reading: r });
      }

      return json({ detail: "未知接口: " + api }, 404);
    } catch (e) {
      return json({ detail: "静态接口错误: " + e.message }, 500);
    }
  }

  // ---------- 拦截 fetch ----------
  window.fetch = function (input, init) {
    let url = typeof input === "string" ? input : (input && input.url) || "";
    if (url.indexOf("api/") !== -1) {
      const method = (init && init.method) || "GET";
      if (method === "POST" && url.indexOf("progress/") !== -1) {
        return (async () => {
          await loadData();
          const u = new URL(url, location.href);
          const path = u.pathname;
          const idx = path.indexOf("/api/");
          const api = idx >= 0 ? path.slice(idx + 5) : path;
          const m = api.match(/^progress\/([^/]+)\/(\d+)$/);
          if (m) {
            const uid = m[1];
            const wid = parseInt(m[2], 10);
            const status = u.searchParams.get("status");
            const prog = getProg(uid);
            const cur = prog[wid] || "new";
            if ((RANK[status] || 0) >= (RANK[cur] || 0)) { prog[wid] = status; setProg(uid, prog); }
            return json({ ok: true, word_id: wid, status: status });
          }
          return json({ ok: false }, 400);
        })();
      }
      return handleApi(url, init);
    }
    return _origFetch ? _origFetch(input, init) : fetch(input, init);
  };

  console.log("[静态版] API 模拟层已加载（多年级支持）");
})();
