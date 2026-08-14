# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 1. 修改测验区 HTML：输入框改成选项区
old_quiz_html = '''  <!-- ======= 测验 ======= -->
  <div id="view-quiz" class="view">
    <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>
    <div class="quiz-card">
      <div class="quiz-prompt" id="quiz-prompt">这个单词的中文是什么意思？</div>
      <div class="quiz-word" id="quiz-word">hello</div>
      <div style="margin-bottom:16px">
        <button class="speak-btn" id="quiz-speak-btn" onclick="speakQuizWord()">🔊 听发音</button>
      </div>
      <input class="quiz-input" id="quiz-input" placeholder="输入答案后按回车" autocomplete="off">
      <button class="btn btn-primary" id="quiz-submit-btn" onclick="submitQuiz()" style="margin-top:12px">提交答案</button>
    </div>
    <div style="display:flex;gap:8px;margin-top:12px">
      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="skipQuiz()">跳过 →</button>
      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="showAnswer()">显示答案</button>
    </div>
    <div id="quiz-hint" style="text-align:center;margin-top:12px;color:#bbb;font-size:13px">第 <span id="quiz-num">1</span> / <span id="quiz-total">0</span> 题</div>
  </div>'''

new_quiz_html = '''  <!-- ======= 测验 ======= -->
  <div id="view-quiz" class="view">
    <button class="btn btn-secondary btn-sm" onclick="showWordList()" style="margin-bottom:12px">← 返回单词表</button>
    <div class="quiz-card">
      <div class="quiz-prompt" id="quiz-prompt">这个单词的中文是什么意思？</div>
      <div class="quiz-word" id="quiz-word">hello</div>
      <div style="margin-bottom:16px">
        <button class="speak-btn" id="quiz-speak-btn" onclick="speakQuizWord()">🔊 听发音</button>
      </div>
      <!-- 选择题选项区 -->
      <div id="quiz-options" style="display:flex;flex-direction:column;gap:10px;margin-top:12px"></div>
      <!-- 反馈区 -->
      <div id="quiz-feedback" style="display:none;margin-top:16px;text-align:center;padding:14px;border-radius:12px;font-size:15px"></div>
      <button class="btn btn-primary" id="quiz-next-btn" onclick="nextQuizQuestion()" style="display:none;margin-top:12px;width:100%">下一题 →</button>
    </div>
    <div style="display:flex;gap:8px;margin-top:12px">
      <button class="btn btn-secondary btn-sm" style="flex:1" onclick="skipQuiz()">跳过 →</button>
    </div>
    <div id="quiz-hint" style="text-align:center;margin-top:12px;color:#bbb;font-size:13px">第 <span id="quiz-num">1</span> / <span id="quiz-total">0</span> 题</div>
  </div>'''

if old_quiz_html in content:
    content = content.replace(old_quiz_html, new_quiz_html)
    print('Quiz HTML replaced OK')
else:
    print('Quiz HTML not found')

# 2. 替换 startQuiz 和 loadQuizQuestion 函数
old_start = '''  function startQuiz() {
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
  }'''

new_start = '''  function startQuiz() {
    if (currentWords.length === 0) { toast("请先选择一个模块"); return; }
    quizOrder = shuffle(currentWords.map(w => w.id));
    currentQuizIndex = 0;
    switchView("quiz");
    loadQuizQuestion();
  }

  function loadQuizQuestion() {
    if (currentQuizIndex >= quizOrder.length) {
      showQuizSummary();
      return;
    }
    // 重置反馈区
    document.getElementById("quiz-feedback").style.display = "none";
    document.getElementById("quiz-next-btn").style.display = "none";

    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    if (!w) { currentQuizIndex++; loadQuizQuestion(); return; }

    // 随机决定题型
    const mode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    currentQuizMode = mode;

    if (mode === "en_to_cn") {
      document.getElementById("quiz-prompt").textContent = "这个单词的中文是？";
      document.getElementById("quiz-word").textContent = capitalize(w.word);
    } else {
      document.getElementById("quiz-prompt").textContent = "这个中文的英文是？";
      document.getElementById("quiz-word").textContent = w.chinese;
    }
    document.getElementById("quiz-num").textContent = currentQuizIndex + 1;
    document.getElementById("quiz-total").textContent = quizOrder.length;

    // 生成4个选项
    const others = currentWords.filter(x => x.id !== wordId);
    const distractors = shuffle(others).slice(0, 3);
    let options;
    if (mode === "en_to_cn") {
      options = shuffle([
        { text: w.chinese, correct: true, word: w },
        ...distractors.map(d => ({ text: d.chinese, correct: false, word: d }))
      ]);
    } else {
      options = shuffle([
        { text: w.word, correct: true, word: w },
        ...distractors.map(d => ({ text: d.word, correct: false, word: d }))
      ]);
    }

    // 渲染选项
    const optsContainer = document.getElementById("quiz-options");
    optsContainer.innerHTML = "";
    const labels = ["A", "B", "C", "D"];
    options.forEach(function(opt, i) {
      const btn = document.createElement("button");
      btn.className = "btn btn-secondary";
      btn.style.cssText = "width:100%;text-align:left;padding:14px 18px;font-size:16px;border-radius:12px;background:white;border:2px solid #e8eeff;color:#333;cursor:pointer;transition:all .15s";
      btn.innerHTML = '<span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#f0f4ff;color:#6c63ff;font-size:13px;text-align:center;line-height:28px;font-weight:700;margin-right:10px">' + labels[i] + '</span><span>' + opt.text + '</span>';
      btn.onclick = function() { handleQuizChoice(btn, opt, w, mode); };
      optsContainer.appendChild(btn);
    });

    // 自动发音
    if (mode === "en_to_cn") setTimeout(function() { speakWord(w.word); }, 100);
  }

  function handleQuizChoice(btnEl, opt, correctWord, mode) {
    // 禁用所有选项
    document.querySelectorAll("#quiz-options button").forEach(function(b) {
      b.style.pointerEvents = "none";
    });

    const feedback = document.getElementById("quiz-feedback");
    const nextBtn = document.getElementById("quiz-next-btn");
    const isCorrect = opt.correct;

    if (isCorrect) {
      btnEl.style.background = "#f6ffed";
      btnEl.style.borderColor = "#52c41a";
      btnEl.style.color = "#52c41a";
      feedback.style.display = "block";
      feedback.style.background = "#f6ffed";
      feedback.style.color = "#52c41a";
      feedback.innerHTML = "<strong>✅ 正确！</strong><br>" + (mode === "en_to_cn" ? capitalize(correctWord.word) + " = " + correctWord.chinese : correctWord.chinese + " = " + capitalize(correctWord.word));
      speakChinese("正确");
      // 保存进度
      apiPOST("/api/progress/" + USER_ID + "/" + correctWord.id + "?status=learned", {});
    } else {
      btnEl.style.background = "#fff2f0";
      btnEl.style.borderColor = "#ff4d4f";
      btnEl.style.color = "#ff4d4f";
      // 高亮正确答案
      const correctText = mode === "en_to_cn" ? correctWord.chinese : correctWord.word;
      document.querySelectorAll("#quiz-options button").forEach(function(b) {
        const span = b.querySelector("span:last-child");
        if (span && span.textContent.trim() === correctText) {
          b.style.background = "#f6ffed";
          b.style.borderColor = "#52c41a";
          b.style.color = "#52c41a";
        }
      });
      feedback.style.display = "block";
      feedback.style.background = "#fff2f0";
      feedback.style.color = "#ff4d4f";
      feedback.innerHTML = "<strong>❌ 不对哦~</strong><br>正确答案：<strong>" + correctText + "</strong>";
      speakChinese("不对");
    }

    nextBtn.style.display = "block";
    nextBtn.textContent = currentQuizIndex + 1 >= quizOrder.length ? "查看成绩 🎉" : "下一题 →";
  }

  function nextQuizQuestion() {
    currentQuizIndex++;
    loadQuizQuestion();
  }

  function showQuizSummary() {
    const container = document.getElementById("quiz-options");
    container.innerHTML = '<div style="text-align:center;padding:40px 20px"><div style="font-size:64px;margin-bottom:16px">🎉</div><div style="font-size:24px;font-weight:700;color:#6c63ff;margin-bottom:8px">测验完成！</div><div style="font-size:14px;color:#999">已完成本模块所有单词</div><button class="btn btn-primary" style="margin-top:24px;width:100%" onclick="switchView(\\'learn\\')">返回学习</button></div>';
    document.getElementById("quiz-feedback").style.display = "none";
    document.getElementById("quiz-next-btn").style.display = "none";
    speakChinese("测验完成，真棒");
  }'''

if old_start in content:
    content = content.replace(old_start, new_start)
    print('Start/Load functions replaced OK')
else:
    print('Start function not found')

# 3. 删除旧的 submitQuiz, showResult, nextQuestion 等函数（因为已经不需要了）
# 但保留 speakQuizWord 和 skipQuiz

# 删除 submitQuiz
old_submit = '''  async function submitQuiz() {
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
  }'''

if old_submit in content:
    content = content.replace(old_submit, '')
    print('submitQuiz removed OK')

# 删除 showResult
old_showresult = '''  function showResult(result, correct) {
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
  }'''

if old_showresult in content:
    content = content.replace(old_showresult, '')
    print('showResult removed OK')

# 删除 nextQuestion（旧版）
old_next = '''  function nextQuestion() {
    document.getElementById("result-overlay").style.display = "none";
    // 随机切换方向
    currentQuizMode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    currentQuizIndex++;
    loadQuizQuestion();
  }'''

if old_next in content:
    content = content.replace(old_next, '')
    print('nextQuestion removed OK')

# 删除 showAnswer
old_showanswer = '''  function showAnswer() {
    const wordId = quizOrder[currentQuizIndex];
    const w = currentWords.find(x => x.id === wordId);
    if (!w) return;
    const answer = currentQuizMode === "en_to_cn" ? w.chinese : w.word;
    toast("答案是：" + answer);
  }'''

if old_showanswer in content:
    content = content.replace(old_showanswer, '')
    print('showAnswer removed OK')

# 4. 修改 skipQuiz
old_skip = '''  function skipQuiz() {
    currentQuizIndex++;
    currentQuizMode = Math.random() > 0.5 ? "en_to_cn" : "cn_to_en";
    loadQuizQuestion();
  }'''

new_skip = '''  function skipQuiz() {
    currentQuizIndex++;
    loadQuizQuestion();
  }'''

if old_skip in content:
    content = content.replace(old_skip, new_skip)
    print('skipQuiz updated OK')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('All done!')
