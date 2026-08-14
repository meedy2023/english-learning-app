# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

marker = '// ========== 学习报告 =========='
idx = content.find(marker)
if idx == -1:
    print('Marker not found')
    exit(1)

choice_code = """
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
    document.getElementById('topbar-title').textContent = '🎯 选择学习';
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

    const esc = function(s) { return (s || '').replace(/'/g, "\\'"); };

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
      '<button class="speak-btn" onclick="speakChoiceWord(\\'' + esc(mode) + '\\',' + wordId + ')" style="margin:0 auto">🔊 听发音</button>' +
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
      '<button class="btn btn-secondary" style="width:100%" onclick="switchView(\\'home\\'); loadModules()">🏠 返回首页</button>' +
    '</div>';
    speakChinese(msgs);
  }

"""

content = content[:idx] + choice_code + '\n' + content[idx:]
print('Choice code inserted at', idx)

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('File written OK')
