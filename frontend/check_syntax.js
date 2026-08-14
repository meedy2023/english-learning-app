
  // ========== 全局状态 ==========
  const API = "http://localhost:8000";
  let USER_ID = localStorage.getItem("user_id") || ("user_" + Math.random().toString(36).substr(2, 8));
  localStorage.setItem("user_id", USER_ID);

  let currentModule = null;
  let currentWords = [];
  let currentQuizIndex = 0;
  let currentQuizMode = "en_to_cn"; // "en_to_cn" | "cn_to_en"
  let quizOrder = []; // 打乱顺序的单词ID列表

  // ========== 工具函数 ==========
  function toast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 2000);
  }

  function switchView(name) {
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    document.getElementById("view-" + name).classList.add("active");
    const titles = { home: "📚 英语学习", learn: "📖 单词学习", quiz: "✏️ 测验", report: "📊 学习报告" };
    document.getElementById("topbar-title").textContent = titles[name] || "";
    document.getElementById("topbar-right").style.display = (name === "report") ? "none" : "";
    if (name === "report") loadReport();
  }

  function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

// ========== TTS 发音（AI 增强版）==========

// 提前加载 voices
if (window.speechSynthesis) {
    speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
    speechSynthesis.getVoices();
}

function speakWord(word) {
    if (!word) {
        toast("没有可发音的内容");
        return;
    }
    if (!window.speechSynthesis) {
        toast("当前浏览器不支持发音功能");
        return;
    }
    try {
        speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(word);
        utter.lang = "en-US";
        utter.rate = 0.85;
        utter.pitch = 1.1;

        const voices = speechSynthesis.getVoices();
        const aiVoice = voices.find(v =>
            v.name.includes('Aria') ||
            v.name.includes('Guy') ||
            v.name.includes('Ana') ||
            v.name.includes('Jenny')
        );
        if (aiVoice) {
            utter.voice = aiVoice;
        } else {
            const enVoice = voices.find(v => v.lang.startsWith("en"));
            if (enVoice) utter.voice = enVoice;
        }

        speechSynthesis.speak(utter);
    } catch (e) {
        toast("发音失败: " + e.message);
    }
}

function speakChinese(text) {
    if (!text) return;
    if (!window.speechSynthesis) {
        toast("当前浏览器不支持发音功能");
        return;
    }
    try {
        speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "zh-CN";
        utter.rate = 0.9;
        const voices = speechSynthesis.getVoices();
        const zhVoice = voices.find(v => v.lang.startsWith("zh"));
        if (zhVoice) utter.voice = zhVoice;
        speechSynthesis.speak(utter);
    } catch (e) {
        toast("发音失败");
    }
}

function speakAll(word, chinese, exampleEn, exampleCn) {
    const parts = [
        { text: word, lang: 'en-US', delay: 600 },
        { text: chinese, lang: 'zh-CN', delay: 500 },
        { text: exampleEn, lang: 'en-US', delay: 600 },
        { text: exampleCn, lang: 'zh-CN', delay: 0 },
    ];
    let delay = 300;
    for (const p of parts) {
        setTimeout(() => {
            if (!p.text) return;
            speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(p.text);
            u.lang = p.lang;
            u.rate = p.lang === 'en-US' ? 0.85 : 0.9;

            const vlist = speechSynthesis.getVoices();
            if (p.lang === 'en-US') {
                const aiVoice = vlist.find(v =>
                    v.name.includes('Aria') ||
                    v.name.includes('Guy') ||
                    v.name.includes('Ana') ||
                    v.name.includes('Jenny')
                );
                if (aiVoice) u.voice = aiVoice;
            } else {
                const v = vlist.find(x => x.lang.startsWith(p.lang.slice(0, 2)));
                if (v) u.voice = v;
            }

            speechSynthesis.speak(u);
        }, delay);
        delay += p.delay + 200;
    }
}

  // ========== API 请求 ==========
  async function apiGET(path) {
    const res = await fetch(API + path);
    if (!res.ok) throw new Error(`API 错误: ${res.status}`);
    return res.json();
  }
  async function apiPOST(path, body) {
    const res = await fetch(API + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(`API 错误: ${res.status}`);
    return res.json();
  }

  // ========== 首页：加载模块 ==========
  async function loadModules() {
    try {
      const data = await apiGET("/api/modules");
      const progressData = await apiGET(`/api/progress/${USER_ID}`);
      const grid = document.getElementById("module-grid");
      grid.innerHTML = "";
      for (const m of data) {
        const prog = progressData[m.module] || { total: m.count, learned: 0, mastered: 0, percent: 0 };
        const pct = prog.learned > 0 ? Math.round(prog.learned / prog.total * 100) : 0;
        const card = document.createElement("div");
        card.className = "module-card";
        card.innerHTML = `
          <div class="module-name">${m.module}</div>
          <div class="module-count">${m.count} 个单词</div>
          <div class="progress-bar">
            <div class="progress-fill" style="width:${pct}%"></div>
          </div>
          <div class="progress-text">${prog.learned}/${prog.total} 已学</div>
        `;
        card.onclick = () => openModule(m.module);
        grid.appendChild(card);
      }
    } catch (e) {
      document.getElementById("module-grid").innerHTML =
        `<div class="empty-state">
          <div class="empty-state-icon">⚠️</div>
          <div>无法连接服务器</div>
          <div style="font-size:12px;margin-top:8px">请确保后端已启动：<br><code style="background:#eee;padding:2px 6px;border-radius:4px">uvicorn main:app --reload</code></div>
        </div>`;
    }
  }

  // ========== 模块：加载单词列表 ==========
  async function openModule(module) {
    currentModule = module;
    try {
      const data = await apiGET(`/api/words?module=${encodeURIComponent(module)}`);
      currentWords = data.words;
      document.getElementById("learn-module-title").textContent = "📖 " + module;
      switchView("learn");
      showWordList();
    } catch (e) { toast("加载失败: " + e.message); }
  }

  async function showWordList() {
    document.getElementById("word-detail-area").style.display = "none";
    document.getElementById("word-list").style.display = "block";
    document.getElementById("quiz-toggle-bar").style.display = "flex";
    const list = document.getElementById("word-list");
    list.innerHTML = "<div class='spinner'></div>";
    // 批量获取当前模块所有单词状态
    let wordStatuses = {};
    try {
      wordStatuses = await apiGET(`/api/word-status/${USER_ID}?module=${encodeURIComponent(currentModule)}`);
    } catch(e) { wordStatuses = {}; }
    list.innerHTML = "";
    for (const w of currentWords) {
      const status = wordStatuses[w.id] || "new";
      const item = document.createElement("div");
      item.className = "word-item";
      item.innerHTML = `
        <div class="word-item-left">
          <div class="word-item-word">${capitalize(w.word)}</div>
          <div class="word-item-phonetic">${w.phonetic}</div>
        </div>
        <div style="display:flex;align-items:center;gap:12px">
          <div class="word-item-chinese">${w.chinese}</div>
          <div class="word-status-dot ${status}" title="${status === "new" ? "未学" : status === "learned" ? "已学" : "已掌握"}"></div>
        </div>
      `;
      item.onclick = () => showWordDetail(w);
      list.appendChild(item);
    }
  }

  async function getWordStatus(wordId) {
    try {
      const all = await apiGET(`/api/word-status/${USER_ID}?module=${encodeURIComponent(currentModule)}`);
      return all[wordId] || "new";
    } catch { return "new"; }
  }

  // ========== 单词详情 ==========
  function showWordDetail(w) {
    document.getElementById("word-list").style.display = "none";
    document.getElementById("quiz-toggle-bar").style.display = "none";
    const area = document.getElementById("word-detail-area");
    area.style.display = "block";
    // 转义单引号，防止破坏 HTML onclick 属性的 JS 字符串
    const esc = s => (s || "").replace(/'/g, "\\'");
    area.innerHTML = `
      <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>
      <div class="word-detail-card">
        <div class="word-type-badge">${w.type}</div>
        <div class="word-text">${capitalize(w.word)}</div>
        <div class="word-phonetic">${w.phonetic}</div>
        <button class="speak-btn" onclick="speakWord('${esc(w.word)}')">🔊 听发音</button>
        <div class="word-chinese">${w.chinese}</div>
        <div class="word-example">
          <div>${capitalize(w.example_en)}</div>
          <div class="word-example-cn">${w.example_cn}</div>
        </div>
      </div>
      <button class="btn btn-primary" onclick="markWord('${w.id}', 'learned')">✓ 我学会了</button>
      <button class="btn btn-secondary" onclick="markWord('${w.id}', 'mastered')" style="margin-top:8px;width:100%">⭐ 我已掌握</button>
      <button class="btn btn-secondary" onclick="speakAll('${esc(w.word)}','${esc(w.chinese)}','${esc(w.example_en)}','${esc(w.example_cn)}')" style="margin-top:8px;width:100%">🔊 朗读全部</button>
    `;
  }

  // ========== 测验 ==========
  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function startQuiz() {
    if (currentWords.length === 0) { toast("请先选择一个模块"); return; }
    quizOrder = shuffle(currentWords.map(w => w.id));
    currentQuizIndex = 0;
    // 随机决定测验方向
    currentQuizMode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    switchView("quiz");
    loadQuizQuestion();
  }

  function loadQuizQuestion() {
    if (currentQuizIndex >= quizOrder.length) {
      toast("🎉 模块测验完成！");
      switchView("learn");
      return;
    }
    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    if (!w) return;
    if (currentQuizMode === "en_to_cn") {
      document.getElementById("quiz-prompt").textContent = "这个单词的中文是什么意思？";
      document.getElementById("quiz-word").textContent = capitalize(w.word);
      document.getElementById("quiz-submit-btn").onclick = submitQuiz;
    } else {
      document.getElementById("quiz-prompt").textContent = "这个中文的英文怎么写？";
      document.getElementById("quiz-word").textContent = w.chinese;
      document.getElementById("quiz-submit-btn").onclick = submitQuiz;
    }
    document.getElementById("quiz-input").value = "";
    document.getElementById("quiz-input").focus();
    document.getElementById("quiz-num").textContent = currentQuizIndex + 1;
    document.getElementById("quiz-total").textContent = quizOrder.length;
    // 自动发音（英文单词题才自动发音）
    if (currentQuizMode === "en_to_cn") speakWord(w.word);
  }

  function speakQuizWord() {
    // 获取当前测验题目对应的单词并朗读
    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    if (!w) return;
    if (currentQuizMode === "en_to_cn") {
      speakWord(w.word);
    } else {
      // 中文题：朗读中文
      speakChinese(w.chinese);
    }
  }

  async function submitQuiz() {
    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    const input = document.getElementById("quiz-input").value;
    let correct;
    if (currentQuizMode === "en_to_cn") {
      correct = w.chinese;
    } else {
      correct = w.word;
    }
    try {
      const result = await apiPOST("/api/score", {
        user_answer: input,
        correct_answer: correct
      });
      showResult(result, correct);
      // 答对60分以上自动记录学习进度
      if (result.score >= 60) {
        const status = result.score >= 90 ? "mastered" : "learned";
        apiPOST(`/api/progress/${USER_ID}/${wordId}?status=${status}`, {});
      }
    } catch (e) {
      // 离线模式：用本地评分
      let score = 0, feedback = "";
      const u = input.trim().toLowerCase();
      const c = correct.toLowerCase();
      if (u === c) { score = 100; feedback = "太棒了！完全正确！🎉"; }
      else if (!u) { score = 0; feedback = "没有输入答案哦，再试一次！"; }
      else if (c.includes(u) || u.includes(c)) { score = 80; feedback = "很接近了！💪"; }
      else { score = 0; feedback = "不对哦，看看正确答案吧 🔍"; }
      showResult({ score, feedback }, correct);
      // 离线模式也保存进度
      if (score >= 60) {
        const status2 = score >= 90 ? "mastered" : "learned";
        try { apiPOST(`/api/progress/${USER_ID}/${wordId}?status=${status2}`, {}); } catch(_){}
      }
    }
  }

  function showResult(result, correct) {
    const emoji = result.score >= 80 ? "🎉" : result.score >= 50 ? "🤔" : "❌";
    document.getElementById("result-emoji").textContent = emoji;
    document.getElementById("result-score").textContent = result.score;
    document.getElementById("result-feedback").textContent = result.feedback;
    document.getElementById("result-correct-text").textContent = correct;
    document.getElementById("result-correct").style.display =
      result.score < 100 ? "flex" : "none";
    document.getElementById("result-overlay").style.display = "flex";
    // 发音反馈
    if (result.score >= 80) speakChinese("正确，太棒了");
    else speakChinese("不对，再试一次");
  }

  function nextQuestion() {
    document.getElementById("result-overlay").style.display = "none";
    // 随机切换方向
    currentQuizMode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    currentQuizIndex++;
    loadQuizQuestion();
  }

  function skipQuiz() {
    currentQuizIndex++;
    currentQuizMode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    loadQuizQuestion();
  }

  function showAnswer() {
    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    let correct;
    if (currentQuizMode === "en_to_cn") correct = w.chinese;
    else correct = w.word;
    showResult({ score: 0, feedback: "参考正确答案：" }, correct);
    document.getElementById("result-emoji").textContent = "📖";
  }

  // 回车提交
  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("quiz-input").addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitQuiz();
    });
  });

  
  // ========== 选择题学习 ==========
  let cl_words = [];
  let cl_idx = 0;
  let cl_order = [];
  let cl_correct = 0;
  let cl_total = 0;

  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function startChoiceLearn() {
    if (!currentModule || currentWords.length === 0) {
      toast('请先选择一个模块');
      switchView('home');
      return;
    }
    cl_words = [...currentWords];
    cl_idx = 0;
    cl_correct = 0;
    cl_total = 0;
    const ids = cl_words.map(w => w.id);
    cl_order = shuffle(ids);
    document.getElementById('word-list').style.display = 'none';
    document.getElementById('word-detail-area').style.display = 'none';
    document.getElementById('quiz-toggle-bar').style.display = 'none';
    const area = document.getElementById('choice-learn-area');
    area.style.display = 'block';
    switchView('learn');
    document.getElementById('topbar-title').textContent = '🎯 英语学习';
    loadChoiceQuestion();
  }

  function loadChoiceQuestion() {
    if (cl_idx >= cl_order.length) {
      showChoiceSummary();
      return;
    }
    const wordId = cl_order[cl_idx];
    const word = cl_words.find(w => w.id === wordId);
    if (!word) { cl_idx++; loadChoiceQuestion(); return; }
    const mode = Math.random() > 0.5 ? 'en2cn' : 'cn2en';
    const others = cl_words.filter(w => w.id !== wordId);
    const distractors = shuffle(others).slice(0, 3);
    let options;
    if (mode === 'en2cn') {
      options = shuffle([
        { text: word.chinese, correct: true },
        ...distractors.map(d => ({ text: d.chinese, correct: false }))
      ]);
    } else {
      options = shuffle([
        { text: word.word, correct: true },
        ...distractors.map(d => ({ text: d.word, correct: false }))
      ]);
    }
    const prompt = mode === 'en2cn' ? '这个单词的中文是？' : '这个中文的英文是？';
    const question = mode === 'en2cn' ? capitalize(word.word) : word.chinese;
    const pct = Math.round((cl_idx / cl_order.length) * 100);
    if (mode === 'en2cn') setTimeout(function() { speakWord(word.word); }, 100);

    const esc = function(s) { return (s || '').replace(/'/g, "\'"); };

    const area = document.getElementById('choice-learn-area');
    area.innerHTML = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">' +
      '<span style="font-size:13px;color:#999">' + currentModule + '</span>' +
      '<div style="flex:1;height:6px;background:#eee;border-radius:3px;overflow:hidden">' +
        '<div style="height:100%;background:linear-gradient(90deg,#4f9fff,#6c63ff);width:' + pct + '%;border-radius:3px;transition:width .3s"></div>' +
      '</div>' +
      '<span style="font-size:12px;color:#999">' + (cl_idx + 1) + '/' + cl_order.length + '</span>' +
    '</div>' +
    '<div style="text-align:center;margin-bottom:8px">' +
      '<div style="font-size:40px;font-weight:800;color:#333;margin-bottom:4px">' + question + '</div>' +
      '<button class="speak-btn" onclick="speakChoiceWord(\'' + esc(mode) + '\',' + wordId + ')" style="margin:0 auto">🔊 听发音</button>' +
      '<div style="font-size:14px;color:#999;margin-top:4px">' + prompt + '</div>' +
    '</div>' +
    '<div id="choice-options" style="display:flex;flex-direction:column;gap:10px;margin-top:16px"></div>' +
    '<div id="choice-feedback" style="display:none;margin-top:12px;text-align:center;padding:14px;border-radius:12px;font-size:15px;line-height:1.5"></div>' +
    '<button id="cl-next-btn" class="btn btn-primary" style="display:none;margin-top:12px;width:100%" onclick="clNextQuestion()">下一题 →</button>';

    const optsContainer = document.getElementById('choice-options');
    const labels = ['A', 'B', 'C', 'D'];
    options.forEach(function(opt, i) {
      const btn = document.createElement('button');
      btn.className = 'choice-opt-btn';
      btn.style.cssText = 'width:100%;text-align:left;padding:14px 18px;font-size:16px;border-radius:12px;background:white;border:2px solid #e8eeff;color:#333;cursor:pointer;transition:all .15s';
      btn.innerHTML = '<span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#f0f4ff;color:#6c63ff;font-size:13px;text-align:center;line-height:28px;font-weight:700;margin-right:10px;flex-shrink:0">' + labels[i] + '</span><span>' + opt.text + '</span>';
      btn.onclick = (function(o) {
        return function() { handleChoiceAnswer(o, word, mode); };
      })(opt);
      optsContainer.appendChild(btn);
    });
  }

  function speakChoiceWord(mode, wordId) {
    const w = cl_words.find(function(x) { return x.id === wordId; });
    if (!w) return;
    if (mode === 'en2cn') speakWord(w.word);
    else speakChinese(w.chinese);
  }

  function handleChoiceAnswer(opt, word, mode) {
    document.querySelectorAll('.choice-opt-btn').forEach(function(b) { b.style.pointerEvents = 'none'; });
    cl_total++;
    const feedback = document.getElementById('choice-feedback');
    const nextBtn = document.getElementById('cl-next-btn');
    const isCorrect = opt.correct;

    if (isCorrect) {
      cl_correct++;
      clStyle(feedback, '#f6ffed', '#52c41a', '<strong>✅ 正确！</strong><br>' + (mode === 'en2cn' ? capitalize(word.word) + ' = ' + word.chinese : word.chinese + ' = ' + capitalize(word.word)));
      clStyleBtn(event.target, '#f6ffed', '#52c41a');
      speakChinese('正确');
      saveChoiceProgress(word.id);
    } else {
      clStyle(feedback, '#fff2f0', '#ff4d4f', '<strong>❌ 不对哦~</strong><br>正确答案：<strong>' + (mode === 'en2cn' ? word.chinese : capitalize(word.word)) + '</strong>');
      // 高亮正确答案
      document.querySelectorAll('.choice-opt-btn span:last-child').forEach(function(span) {
        const txt = span.textContent.trim();
        const correctTxt = mode === 'en2cn' ? word.chinese : word.word;
        if (txt === correctTxt) {
          span.parentElement.style.background = '#f6ffed';
          span.parentElement.style.borderColor = '#52c41a';
          span.parentElement.style.color = '#52c41a';
        }
      });
      // 标红选错的
      event.target.style.background = '#fff2f0';
      event.target.style.borderColor = '#ff4d4f';
      event.target.style.color = '#ff4d4f';
      speakChinese('不对');
    }

    nextBtn.style.display = 'block';
    nextBtn.textContent = (cl_idx + 1) >= cl_order.length ? '查看成绩 🎉' : '下一题 →';
  }

  function clStyle(el, bg, color, html) {
    el.style.display = 'block';
    el.style.background = bg;
    el.style.color = color;
    el.innerHTML = html;
  }

  function clStyleBtn(btn, bg, color) {
    btn.style.background = bg;
    btn.style.borderColor = color;
    btn.style.color = color;
  }

  async function saveChoiceProgress(wordId) {
    try {
      await apiPOST('/api/progress/' + USER_ID + '/' + wordId + '?status=learned', {});
    } catch(e) {}
  }

  function clNextQuestion() {
    cl_idx++;
    loadChoiceQuestion();
  }

  function showChoiceSummary() {
    const pct = cl_total > 0 ? Math.round(cl_correct / cl_total * 100) : 0;
    const emoji = pct >= 90 ? '🏆' : pct >= 70 ? '👏' : pct >= 50 ? '💪' : '📚';
    const msgs = pct >= 90 ? '太厉害了，全都会！' : pct >= 70 ? '很棒，继续加油！' : pct >= 50 ? '还不错，再接再厉！' : '多练练，一定会进步！';
    const area = document.getElementById('choice-learn-area');
    area.innerHTML = '<div style="text-align:center;padding:40px 20px">' +
      '<div style="font-size:72px;margin-bottom:16px">' + emoji + '</div>' +
      '<div style="font-size:40px;font-weight:800;color:#6c63ff;margin-bottom:8px">' + pct + '%</div>' +
      '<div style="font-size:15px;color:#999;margin-bottom:24px">' + cl_correct + '/' + cl_total + ' 题正确</div>' +
      '<div style="font-size:16px;color:#555;margin-bottom:32px">' + msgs + '</div>' +
      '<div style="background:white;border-radius:16px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.06);margin-bottom:24px">' +
        '<div style="display:flex;gap:16px">' +
          '<div style="flex:1;text-align:center"><div style="font-size:28px;font-weight:700;color:#52c41a">' + cl_correct + '</div><div style="font-size:12px;color:#999">正确</div></div>' +
          '<div style="width:1px;background:#eee"></div>' +
          '<div style="flex:1;text-align:center"><div style="font-size:28px;font-weight:700;color:#ff4d4f">' + (cl_total - cl_correct) + '</div><div style="font-size:12px;color:#999">错误</div></div>' +
          '<div style="width:1px;background:#eee"></div>' +
          '<div style="flex:1;text-align:center"><div style="font-size:28px;font-weight:700;color:#6c63ff">' + cl_total + '</div><div style="font-size:12px;color:#999">总题数</div></div>' +
        '</div>' +
      '</div>' +
      '<button class="btn btn-primary" style="width:100%;margin-bottom:10px" onclick="startChoiceLearn()">🔄 再来一轮</button>' +
      '<button class="btn btn-secondary" style="width:100%" onclick="switchView(\'home\'); loadModules()">🏠 返回首页</button>' +
    '</div>';
    speakChinese(msgs);
  }


// ========== 学习报告 ==========
  async function loadReport() {
    try {
      const data = await apiGET(`/api/progress/${USER_ID}`);
      const total = data._total;
      const pct = total.percent || 0;
      document.getElementById("total-percent").textContent = pct + "%";
      document.getElementById("total-percent").parentElement.style.setProperty("--pct", pct + "%");
      document.getElementById("stat-total").textContent = total.total;
      document.getElementById("stat-learned").textContent = total.learned;
      document.getElementById("stat-mastered").textContent = total.mastered;
      // 各模块
      const container = document.getElementById("report-modules");
      container.innerHTML = "";
      const keys = Object.keys(data).filter(k => k !== "_total");
      for (const mod of keys) {
        const p = data[mod];
        const pctM = p.total > 0 ? Math.round(p.learned / p.total * 100) : 0;
        const div = document.createElement("div");
        div.className = "report-card";
        div.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <div style="font-weight:600">${mod}</div>
            <div style="color:#999;font-size:13px">${p.learned}/${p.total}</div>
          </div>
          <div class="progress-bar" style="height:8px">
            <div class="progress-fill" style="width:${pctM}%"></div>
          </div>
        `;
        container.appendChild(div);
      }
    } catch (e) {
      toast("加载报告失败");
    }
  }

  // ========== 底部导航 ==========
  document.write(`
  <div class="bottom-nav">
    <div class="nav-item active" onclick="switchView('home'); loadModules()">
      <span class="nav-item-icon">🏠</span>首页
    </div>
    <div class="nav-item" onclick="switchView('learn')">
      <span class="nav-item-icon">📖</span>学习
    </div>
    <div class="nav-item" onclick="switchView('report')">
      <span class="nav-item-icon">📊</span>报告
    </div>
  </div>
  `);

  // ========== 启动 ==========
  loadModules();
