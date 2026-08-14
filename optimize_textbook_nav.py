# -*- coding: utf-8 -*-
"""
优化课文学习导航：
1. showTextbookList() 改为智能跳转：
   - 如果当前在单词模块中（currentModule 有值），直接打开对应的课文模块
   - 否则显示所有课文模块列表

2. 添加 showLessonUnits() 函数：从单元详情跳转到该模块的单元列表

3. 添加 goToNextUnit() 函数：从单元详情跳转到下一个单元

4. 在 showLessonDetail 中添加"下一个单元"按钮
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

original = content

# ============================================================
# 优化 1: 修改 showTextbookList 函数，支持智能跳转
# ============================================================
# 找到 showTextbookList 的定义
old_showTextbookList = """  async function showTextbookList() {
    // 切换到学习视图
    switchView('learn');
    document.getElementById('word-list').style.display = 'none';
    document.getElementById('word-detail-area').style.display = 'none';
    document.getElementById('choice-learn-area').style.display = 'none';
    document.getElementById('quiz-toggle-bar').style.display = 'none';
    
    const area = document.getElementById('word-list');
    area.style.display = 'block';
    area.innerHTML = '<div class="spinner"></div>';
    
    try {
      const modules = await apiGET('/api/textbook/modules');
      area.innerHTML = '<div class="section-title">选择课文模块</div>';
      
      const grid = document.createElement('div');
      grid.className = 'module-grid';
      
      for (const m of modules) {
        const card = document.createElement('div');
        card.className = 'module-card';
        card.innerHTML = `
          <div class="module-name">${m.module}</div>
          <div class="module-count">${m.unit_count} 个单元</div>
        `;
        card.onclick = () => openLessonModule(m.module);
        grid.appendChild(card);
      }
      
      area.appendChild(grid);
    } catch (e) {
      area.innerHTML = '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div>加载失败：' + e.message + '</div></div>';
    }
  }"""

new_showTextbookList = """  // 单词模块到课文模块的映射
  const WORD_TO_LESSON = {
    '上1': 'Module 1', '上2': 'Module 2', '上3': 'Module 3', '上4': 'Module 4', '上5': 'Module 5',
    '上6': 'Module 6', '上7': 'Module 7', '上8': 'Module 8', '上9': 'Module 9', '上10': 'Module 10'
  };

  async function showTextbookList() {
    // 智能跳转：如果当前在某个单词模块中，直接打开对应的课文模块
    if (currentModule && WORD_TO_LESSON[currentModule]) {
      const lessonModule = WORD_TO_LESSON[currentModule];
      // 直接进入对应模块的单元列表
      await openLessonModule(lessonModule);
      return;
    }

    // 否则显示所有课文模块列表
    switchView('learn');
    document.getElementById('word-list').style.display = 'none';
    document.getElementById('word-detail-area').style.display = 'none';
    document.getElementById('choice-learn-area').style.display = 'none';
    document.getElementById('quiz-toggle-bar').style.display = 'none';

    const area = document.getElementById('word-list');
    area.style.display = 'block';
    area.innerHTML = '<div class="spinner"></div>';

    try {
      const modules = await apiGET('/api/textbook/modules');
      area.innerHTML = '<div class="section-title">选择课文模块</div>';

      const grid = document.createElement('div');
      grid.className = 'module-grid';

      for (const m of modules) {
        const card = document.createElement('div');
        card.className = 'module-card';
        card.innerHTML = `
          <div class="module-name">${m.module}</div>
          <div class="module-count">${m.unit_count} 个单元</div>
        `;
        card.onclick = () => openLessonModule(m.module);
        grid.appendChild(card);
      }

      area.appendChild(grid);
    } catch (e) {
      area.innerHTML = '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div>加载失败：' + e.message + '</div></div>';
    }
  }"""

if old_showTextbookList in content:
    content = content.replace(old_showTextbookList, new_showTextbookList)
    print("✓ 优化 1: 智能跳转 showTextbookList")
else:
    print("✗ 未找到 showTextbookList")

# ============================================================
# 优化 2: 修改 openLessonModule 中的返回按钮文案
# ============================================================
old_back_btn = """      backBtn.innerHTML = '<span style="font-size:16px">←</span> 返回模块列表';"""
new_back_btn = """      backBtn.innerHTML = '<span style="font-size:16px">←</span> 返回课文模块';"""

if old_back_btn in content:
    content = content.replace(old_back_btn, new_back_btn)
    print("✓ 优化 2: 更新返回按钮文案")

# ============================================================
# 优化 3: 在 showLessonDetail 中添加"下一个单元"按钮
# ============================================================
# 找到 showLessonDetail 函数中的整篇朗读按钮位置
old_full_speak_section = """        <button class="speak-btn" id="lesson-full-speak-btn" style="margin-top:20px;width:100%;background:linear-gradient(135deg,#4f9fff,#6c63ff);color:white;border:none;font-weight:600">
          🔊 朗读整篇课文
        </button>
      </div>"""

new_full_speak_section = """        <button class="speak-btn" id="lesson-full-speak-btn" style="margin-top:20px;width:100%;background:linear-gradient(135deg,#4f9fff,#6c63ff);color:white;border:none;font-weight:600">
          🔊 朗读整篇课文
        </button>
        <div style="display:flex;gap:8px;margin-top:12px">
          <button class="btn btn-secondary" id="lesson-prev-unit-btn" style="flex:1;padding:10px;font-size:14px;background:#f5f7ff;border:1px solid #e0e6ff;color:#6c63ff;font-weight:500;display:none">
            ← 上一单元
          </button>
          <button class="btn btn-primary" id="lesson-next-unit-btn" style="flex:1;padding:10px;font-size:14px;background:linear-gradient(135deg,#52c41a,#73d13d);color:white;border:none;font-weight:500;display:none">
            下一单元 →
          </button>
        </div>
        <button class="btn btn-secondary" id="lesson-back-to-units-btn" style="margin-top:8px;width:100%;padding:10px;font-size:14px;background:#fff;border:1px solid #e0e6ff;color:#6c63ff;font-weight:500">
          📋 返回单元列表
        </button>
      </div>"""

if old_full_speak_section in content:
    content = content.replace(old_full_speak_section, new_full_speak_section)
    print("✓ 优化 3: 添加上下单元导航按钮")
else:
    print("✗ 未找到 full speak section")

# ============================================================
# 优化 4: 在 showLessonDetail 末尾添加按钮事件绑定
# ============================================================
# 找到现有 fullSpeakBtn 的事件绑定
old_btn_binding = """    // 绑定整篇朗读按钮
    var fullSpeakBtn = document.getElementById("lesson-full-speak-btn");
    if (fullSpeakBtn) {
      fullSpeakBtn.onclick = function() {
        speakAllLessonLines(unit.content);
      };
    }
  }"""

new_btn_binding = """    // 绑定整篇朗读按钮
    var fullSpeakBtn = document.getElementById("lesson-full-speak-btn");
    if (fullSpeakBtn) {
      fullSpeakBtn.onclick = function() {
        speakAllLessonLines(unit.content);
      };
    }

    // 计算当前单元在模块中的位置
    var unitIndex = -1;
    if (currentLessonData) {
      for (var i = 0; i < currentLessonData.length; i++) {
        if (currentLessonData[i].unit === unit.unit) {
          unitIndex = i;
          break;
        }
      }
    }

    // 绑定"上一单元"按钮
    var prevBtn = document.getElementById("lesson-prev-unit-btn");
    if (prevBtn) {
      if (unitIndex > 0) {
        prevBtn.style.display = 'block';
        prevBtn.onclick = function() {
          showLessonDetail(currentLessonData[unitIndex - 1]);
        };
      } else {
        prevBtn.style.display = 'none';
      }
    }

    // 绑定"下一单元"按钮
    var nextBtn = document.getElementById("lesson-next-unit-btn");
    if (nextBtn) {
      if (currentLessonData && unitIndex >= 0 && unitIndex < currentLessonData.length - 1) {
        nextBtn.style.display = 'block';
        nextBtn.onclick = function() {
          showLessonDetail(currentLessonData[unitIndex + 1]);
        };
      } else {
        nextBtn.style.display = 'none';
      }
    }

    // 绑定"返回单元列表"按钮
    var backToUnitsBtn = document.getElementById("lesson-back-to-units-btn");
    if (backToUnitsBtn) {
      backToUnitsBtn.onclick = function() {
        backToLessonUnits();
      };
    }
  }"""

if old_btn_binding in content:
    content = content.replace(old_btn_binding, new_btn_binding)
    print("✓ 优化 4: 绑定上下单元导航按钮")
else:
    print("✗ 未找到现有绑定")

# 保存
if content != original:
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("\n✓ 文件已保存")
else:
    print("\n无修改")