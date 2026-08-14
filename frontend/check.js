// frontend/check.js - 完整修复版
// 全局变量
let textbookData = []; // 存储课文数据
let currentQuizWord = null; // 当前测验的单词

// 1. 切换视图函数 (对应 HTML 里的 onclick="switchView(...)")
function switchView(viewName) {
    // 隐藏所有 view
    document.querySelectorAll('.view').forEach(el => {
        el.style.display = 'none';
        el.classList.remove('active');
    });

    // 显示目标 view
    const target = document.getElementById('view-' + viewName);
    if (target) {
        target.style.display = 'block';
        target.classList.add('active');
    }

    // 如果切换到测验页，自动开始一轮测验
    if (viewName === 'quiz') {
        startQuiz();
    }
}

// 2. 显示单词列表 (对应 onclick="showWordList()")
async function showWordList() {
    const listContainer = document.getElementById('word-list');
    if (!listContainer) return;

    listContainer.innerHTML = '<div class="spinner"></div>'; // 显示加载中

    try {
        // 统一使用 8080 端口
        const res = await fetch('http://localhost:8080/api/words');
        const words = await res.json();

        listContainer.innerHTML = ''; // 清空加载动画

        words.forEach(w => {
            const item = document.createElement('div');
            item.className = 'word-item';
            // 简单的样式，你可以根据需要调整
            item.style.cssText = "padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;";
            item.innerHTML = `
                <div>
                    <strong>${w.word}</strong> 
                    <span style="color:#666; font-size:0.9em;">${w.phonetic || ''}</span>
                </div>
                <div style="color:#888;">${w.translation}</div>
            `;
            // 点击单词可以查看详情（可选功能）
            item.onclick = () => showWordDetail(w);
            listContainer.appendChild(item);
        });

    } catch (err) {
        console.error("获取单词列表失败:", err);
        listContainer.innerHTML = '<p style="color:red">加载失败，请检查后端服务是否启动。</p>';
    }
}

// 3. 显示单词详情 (辅助函数)
function showWordDetail(wordObj) {
    const detailArea = document.getElementById('word-detail-area');
    if (detailArea) {
        detailArea.style.display = 'block';
        detailArea.innerHTML = `
            <h3>${wordObj.word}</h3>
            <p>${wordObj.translation}</p>
            <p><em>${wordObj.example || '暂无例句'}</em></p>
            <button class="btn btn-secondary" onclick="document.getElementById('word-detail-area').style.display='none'">关闭</button>
        `;
    }
}

// 4. 加载课文内容 (对应 onclick="loadTextContent()")
async function loadTextContent() {
    const contentArea = document.getElementById('learn-module-title'); // 或者你指定的显示区域
    // 注意：这里假设你想把标题改一下，或者在某个区域显示课文
    // 如果你的 HTML 里有一个专门放课文内容的 div，请替换下面的选择器
    
    // 这里演示：获取课文数据并打印，或者渲染到页面
    try {
        // 统一使用 8080 端口
        const res = await fetch('http://localhost:8080/api/textbook');
        const data = await res.json();
        
        textbookData = data; // 存入全局变量
        
        // 简单的渲染逻辑：找到 id 为 'module-grid' 的地方显示课文标题
        const grid = document.getElementById('module-grid');
        if(grid) {
            grid.innerHTML = ''; // 清空之前的 spinner
            data.forEach((textbook, index) => {
                const card = document.createElement('div');
                card.className = 'card'; // 假设你有 card 样式
                card.style.cssText = "border:1px solid #ddd; padding:15px; margin:10px; border-radius:8px; cursor:pointer;";
                card.innerHTML = `<h4>${textbook.title}</h4><p>${textbook.content ? textbook.content.substring(0, 50) + '...' : '暂无内容'}</p>`;
                
                // 点击卡片可以展开详情（这里简单处理）
                card.onclick = () => alert(`你选择了: ${textbook.title}\n内容: ${textbook.content}`);
                
                grid.appendChild(card);
            });
        }

        // 切换视图到学习页（如果需要）
        // switchView('learn'); 

    } catch (err) {
        console.error("加载课文失败:", err);
        alert("无法连接到服务器获取课文数据");
    }
}

// 5. 开始测验 (对应 onclick="startQuiz()")
async function startQuiz() {
    const quizWordEl = document.getElementById('quiz-word');
    const quizPromptEl = document.getElementById('quiz-prompt');
    const quizOptionsEl = document.getElementById('quiz-options');

    if (!quizWordEl || !quizOptionsEl) return;

    // 显示加载状态
    quizWordEl.innerText = "...";
    quizOptionsEl.innerHTML = '<div class="spinner"></div>';

    try {
        // 获取所有单词用于出题
        const res = await fetch('http://localhost:8080/api/words');
        const allWords = await res.json();

        if (allWords.length === 0) {
            quizWordEl.innerText = "无数据";
            return;
        }

        // 随机选一个正确答案
        const correctIndex = Math.floor(Math.random() * allWords.length);
        currentQuizWord = allWords[correctIndex];

        // 随机选3个干扰项
        let distractors = [];
        while (distractors.length < 3 && distractors.length < allWords.length - 1) {
            const randIndex = Math.floor(Math.random() * allWords.length);
            if (randIndex !== correctIndex && !distractors.includes(allWords[randIndex])) {
                distractors.push(allWords[randIndex]);
            }
        }

        // 混合选项
        const options = shuffle([currentQuizWord, ...distractors]);

        // 渲染界面
        quizWordEl.innerText = currentQuizWord.word; // 显示英文单词
        if(quizPromptEl) quizPromptEl.innerText = "这个单词的中文意思是？";

        quizOptionsEl.innerHTML = ""; // 清空选项区

        options.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = "btn btn-secondary quiz-option-btn"; // 添加特定类名方便后续处理
            btn.style.cssText = "width:100%; margin-bottom:10px; padding:12px; text-align:left;";
            btn.innerText = opt.translation; // 选项显示中文
            
            // 点击事件
            btn.onclick = () => checkAnswer(opt, currentQuizWord, btn, options);
            
            quizOptionsEl.appendChild(btn);
        });

    } catch (err) {
        console.error("测验加载失败:", err);
        quizWordEl.innerText = "Error";
    }
}

// 6. 检查答案逻辑
function checkAnswer(selected, correct, btnElement, allOptionsBtns) {
    // 禁用所有按钮防止重复点击
    const buttons = document.querySelectorAll('.quiz-option-btn');
    buttons.forEach(b => b.disabled = true);

    if (selected.word === correct.word) {
        // 答对了
        btnElement.style.backgroundColor = "#d4edda"; // 绿色背景
        btnElement.style.borderColor = "#c3e6cb";
        btnElement.innerHTML += " ✅";
        
        // 1秒后下一题
        setTimeout(() => {
            startQuiz();
        }, 1000);
    } else {
        // 答错了
        btnElement.style.backgroundColor = "#f8d7da"; // 红色背景
        btnElement.style.borderColor = "#f5c6cb";
        btnElement.innerHTML += " ❌";
        
        // 找出正确的按钮并标绿
        buttons.forEach(b => {
            if (b.innerText === correct.translation) {
                b.style.backgroundColor = "#d4edda";
            }
        });
    }
}

// 7. 播放发音 (对应 onclick="speakQuizWord()")
function speakQuizWord() {
    if (!currentQuizWord || !currentQuizWord.word) return;
    
    const utterance = new SpeechSynthesisUtterance(currentQuizWord.word);
    utterance.lang = 'en-US'; // 设置为美式英语
    window.speechSynthesis.speak(utterance);
}

// 工具函数：数组乱序 (Fisher-Yates Shuffle)
function shuffle(array) {
    let currentIndex = array.length, randomIndex;
    while (currentIndex != 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
    }
    return array;
}

// 页面加载完成后初始化（可选）
window.onload = function() {
    console.log("JS Loaded Successfully");
    // 默认显示首页
    switchView('home');
};