# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 1. 修改选择学习的 handleChoiceAnswer：答对且是最后一题且全对时标记 mastered
old_choice_handle = '''  function handleChoiceAnswer(btnEl, opt, word, mode) {
    // 禁止重复点击
    document.querySelectorAll('#choice-options button').forEach(function(b) { b.style.pointerEvents = 'none'; });
    cl_total++;
    const feedback = document.getElementById('choice-feedback');
    const nextBtn = document.getElementById('cl-next-btn');
    const isCorrect = opt.correct;

    if (isCorrect) {
      cl_correct++;
      btnEl.style.background = '#f6ffed';
      btnEl.style.borderColor = '#52c41a';
      btnEl.style.color = '#52c41a';
      feedback.style.display = 'block';
      feedback.style.background = '#f6ffed';
      feedback.style.color = '#52c41a';
      feedback.innerHTML = '<strong>✅ 正确！</strong><br>' + (mode === 'en2cn' ? capitalize(word.word) + ' = ' + word.chinese : word.chinese + ' = ' + capitalize(word.word));
      speakChinese('正确');
      // 记录进度
      saveChoiceProgress(word.id);
    } else {'''

new_choice_handle = '''  function handleChoiceAnswer(btnEl, opt, word, mode) {
    // 禁止重复点击
    document.querySelectorAll('#choice-options button').forEach(function(b) { b.style.pointerEvents = 'none'; });
    cl_total++;
    const feedback = document.getElementById('choice-feedback');
    const nextBtn = document.getElementById('cl-next-btn');
    const isCorrect = opt.correct;

    if (isCorrect) {
      cl_correct++;
      btnEl.style.background = '#f6ffed';
      btnEl.style.borderColor = '#52c41a';
      btnEl.style.color = '#52c41a';
      feedback.style.display = 'block';
      feedback.style.background = '#f6ffed';
      feedback.style.color = '#52c41a';
      feedback.innerHTML = '<strong>✅ 正确！</strong><br>' + (mode === 'en2cn' ? capitalize(word.word) + ' = ' + word.chinese : word.chinese + ' = ' + capitalize(word.word));
      speakChinese('正确');
      // 记录进度：全对时标记 mastered，否则 learned
      const isLast = cl_idx + 1 >= cl_order.length;
      const isPerfect = isLast && (cl_correct === cl_total);
      saveChoiceProgress(word.id, isPerfect ? 'mastered' : 'learned');
    } else {'''

if old_choice_handle in content:
    content = content.replace(old_choice_handle, new_choice_handle)
    print('Choice handleChoiceAnswer updated OK')
else:
    print('Choice handleChoiceAnswer not found')

# 2. 修改 saveChoiceProgress 接受 status 参数
old_save = '''  async function saveChoiceProgress(wordId) {
    try {
      await apiPOST('/api/progress/' + USER_ID + '/' + wordId + '?status=learned', {});
    } catch(e) {}
  }'''

new_save = '''  async function saveChoiceProgress(wordId, status) {
    status = status || 'learned';
    try {
      await apiPOST('/api/progress/' + USER_ID + '/' + wordId + '?status=' + status, {});
    } catch(e) {}
  }'''

if old_save in content:
    content = content.replace(old_save, new_save)
    print('saveChoiceProgress updated OK')
else:
    print('saveChoiceProgress not found')

# 3. 修改闯关测验的 handleQuizChoice：答对且是最后一题且全对时标记 mastered
old_quiz_handle = '''  function handleQuizChoice(btnEl, opt, correctWord, mode) {
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
    } else {'''

new_quiz_handle = '''  function handleQuizChoice(btnEl, opt, correctWord, mode) {
    // 禁用所有选项
    document.querySelectorAll("#quiz-options button").forEach(function(b) {
      b.style.pointerEvents = "none";
    });

    const feedback = document.getElementById("quiz-feedback");
    const nextBtn = document.getElementById("quiz-next-btn");
    const isCorrect = opt.correct;

    // 记录本题结果用于判断是否全对
    if (!window.quizResults) window.quizResults = [];
    window.quizResults.push(isCorrect);

    if (isCorrect) {
      btnEl.style.background = "#f6ffed";
      btnEl.style.borderColor = "#52c41a";
      btnEl.style.color = "#52c41a";
      feedback.style.display = "block";
      feedback.style.background = "#f6ffed";
      feedback.style.color = "#52c41a";
      feedback.innerHTML = "<strong>✅ 正确！</strong><br>" + (mode === "en_to_cn" ? capitalize(correctWord.word) + " = " + correctWord.chinese : correctWord.chinese + " = " + capitalize(correctWord.word));
      speakChinese("正确");
      // 保存进度：最后一题且全对时标记 mastered
      const isLast = currentQuizIndex + 1 >= quizOrder.length;
      const allCorrect = isLast && window.quizResults.every(function(r) { return r; });
      apiPOST("/api/progress/" + USER_ID + "/" + correctWord.id + "?status=" + (allCorrect ? "mastered" : "learned"), {});
    } else {'''

if old_quiz_handle in content:
    content = content.replace(old_quiz_handle, new_quiz_handle)
    print('Quiz handleQuizChoice updated OK')
else:
    print('Quiz handleQuizChoice not found')

# 4. 修改 nextQuizQuestion：重置 quizResults
old_next = '''  function nextQuizQuestion() {
    currentQuizIndex++;
    loadQuizQuestion();
  }'''

new_next = '''  function nextQuizQuestion() {
    currentQuizIndex++;
    loadQuizQuestion();
  }

  function resetQuizResults() {
    window.quizResults = [];
  }'''

if old_next in content:
    content = content.replace(old_next, new_next)
    print('nextQuizQuestion updated OK')
else:
    print('nextQuizQuestion not found')

# 5. 在 startQuiz 中重置 quizResults
old_start = '''  function startQuiz() {
    if (currentWords.length === 0) { toast("请先选择一个模块"); return; }
    quizOrder = shuffle(currentWords.map(w => w.id));
    currentQuizIndex = 0;
    switchView("quiz");
    loadQuizQuestion();
  }'''

new_start = '''  function startQuiz() {
    if (currentWords.length === 0) { toast("请先选择一个模块"); return; }
    quizOrder = shuffle(currentWords.map(w => w.id));
    currentQuizIndex = 0;
    window.quizResults = [];
    switchView("quiz");
    loadQuizQuestion();
  }'''

if old_start in content:
    content = content.replace(old_start, new_start)
    print('startQuiz updated OK')
else:
    print('startQuiz not found')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('All done!')
