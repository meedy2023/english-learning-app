// api-shim.js
// 纯静态版：在浏览器内用本地 JSON 数据模拟原 FastAPI 后端的所有接口，
// 这样前端代码（apiGET / apiPOST）无需改动即可在 GitHub Pages 上运行。
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
        console.error("数据加载失败：", e);
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

  // ---------- 数据查询辅助（对应 words_data.py） ----------
  function getModules() {
    const s = new Set();
    DATA.words.forEach((w) => { if (w.module) s.add(w.module); });
    return Array.from(s);
  }
  function wordsByModule(m) { return DATA.words.filter((w) => w.module === m); }
  function searchWords(q) {
    q = (q || "").toLowerCase();
    return DATA.words.filter((w) =>
      (w.word || "").toLowerCase().includes(q) ||
      (w.chinese || "").includes(q) ||
      (w.phonetic || "").toLowerCase().includes(q) ||
      (w.example_en || "").toLowerCase().includes(q)
    );
  }

  // ---------- 课文模块（对应 main.py） ----------
  const WORD_TO_LESSON = {
    "上1": ["Module 1", "三年级上册"], "上2": ["Module 2", "三年级上册"],
    "上3": ["Module 3", "三年级上册"], "上4": ["Module 4", "三年级上册"],
    "上5": ["Module 5", "三年级上册"], "上6": ["Module 6", "三年级上册"],
    "上7": ["Module 7", "三年级上册"], "上8": ["Module 8", "三年级上册"],
    "上9": ["Module 9", "三年级上册"], "上10": ["Module 10", "三年级上册"],
    "下1": ["Module 1", "三年级下册"], "下2": ["Module 2", "三年级下册"],
    "下3": ["Module 3", "三年级下册"], "下4": ["Module 4", "三年级下册"],
    "下5": ["Module 5", "三年级下册"], "下6": ["Module 6", "三年级下册"],
    "下7": ["Module 7", "三年级下册"], "下8": ["Module 8", "三年级下册"],
    "下9": ["Module 9", "三年级下册"], "下10": ["Module 10", "三年级下册"],
  };

  function textbookModules(grade) {
    const res = [];
    const root = DATA.textbook["外研社"] || {};
    const grades = grade ? [grade] : Object.keys(root);
    grades.forEach((g) => {
      const gd = root[g] || {};
      Object.keys(gd).forEach((mod) => {
        const units = gd[mod];
        if (Array.isArray(units)) {
          res.push({
            module: mod, grade: g, unit_count: units.length,
            units: units.map((u) => u.unit),
          });
        }
      });
    });
    return res;
  }

  // ---------- 进度统计 ----------
  function moduleProgress(uid, m) {
    const ws = wordsByModule(m);
    const total = ws.length;
    const prog = getProg(uid);
    let learned = 0, mastered = 0;
    ws.forEach((w) => {
      const s = prog[w.id] || "new";
      if (s === "learned" || s === "mastered") learned++;
      if (s === "mastered") mastered++;
    });
    return { module: m, total, learned, mastered, percent: total ? Math.round((learned / total) * 100) : 0 };
  }
  function allStats(uid) {
    const modules = getModules();
    const result = {};
    let tw = 0, tl = 0, tm = 0;
    modules.forEach((m) => {
      const p = moduleProgress(uid, m);
      result[m] = p;
      tw += p.total; tl += p.learned; tm += p.mastered;
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

  // ---------- 评分（对应 simple_score） ----------
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
      if (api === "textbook" && method === "GET") return json(DATA.textbook);
      if (api === "textbook/modules") return json(textbookModules(params.get("grade")));
      if (api.startsWith("textbook/grade/")) {
        const wm = decodeURIComponent(api.slice("textbook/grade/".length));
        const r = WORD_TO_LESSON[wm];
        if (!r) return json({ detail: "无对应课文: " + wm }, 404);
        return json({ word_module: wm, module: r[0], grade: r[1] });
      }
      if (api.startsWith("textbook/")) {
        const mod = decodeURIComponent(api.slice("textbook/".length));
        const grade = params.get("grade");
        const root = DATA.textbook["外研社"] || {};
        const grades = grade ? [grade] : Object.keys(root);
        for (const g of grades) {
          const gd = root[g] || {};
          if (mod in gd) return json({ module: mod, grade: g, units: gd[mod] });
        }
        return json({ detail: "模块不存在: " + mod }, 404);
      }

      if (api === "modules") return json(getModules().map((m) => ({ module: m, count: wordsByModule(m).length })));
      if (api === "words") {
        const m = params.get("module");
        const ws = m ? wordsByModule(m) : DATA.words;
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

      if (api.startsWith("progress/")) {
        const rest = api.slice("progress/".length);
        const parts = rest.split("/");
        const uid = parts[0];
        if (parts.length === 1) return json(allStats(uid));
        return json(moduleProgress(uid, decodeURIComponent(parts[1])));
      }
      if (api.startsWith("word-status/")) {
        const rest = api.slice("word-status/".length);
        const uid = rest.split("/")[0];
        const m = params.get("module");
        const prog = getProg(uid);
        const out = {};
        wordsByModule(m).forEach((w) => { out[w.id] = prog[w.id] || "new"; });
        return json(out);
      }
      if (api === "score") {
        let body = {};
        try { body = JSON.parse((init && init.body) || "{}"); } catch (e) {}
        const r = simpleScore(body.user_answer, body.correct_answer);
        return json(Object.assign({ correct_answer: body.correct_answer }, r));
      }

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

  console.log("[静态版] API 模拟层已加载");
})();
