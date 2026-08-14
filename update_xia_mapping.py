# -*- coding: utf-8 -*-
"""
更新前端 WORD_TO_LESSON 映射，添加下册支持
下册的映射需要带上学期信息（"三年级上册"/"三年级下册"）
"""

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

original_content = content

# ============================================================
# 改造 1: 扩展 WORD_TO_LESSON 为对象格式（包含学期信息）
# ============================================================
old_mapping = """  // 单词模块到课文模块的映射
  const WORD_TO_LESSON = {
    '上1': 'Module 1', '上2': 'Module 2', '上3': 'Module 3', '上4': 'Module 4', '上5': 'Module 5',
    '上6': 'Module 6', '上7': 'Module 7', '上8': 'Module 8', '上9': 'Module 9', '上10': 'Module 10'
  };"""

new_mapping = """  // 单词模块到课文模块的映射（包含学期信息）
  // 上N → Module N (三年级上册)
  // 下N → Module N (三年级下册)
  const WORD_TO_LESSON = {
    '上1': { module: 'Module 1', grade: '三年级上册' },
    '上2': { module: 'Module 2', grade: '三年级上册' },
    '上3': { module: 'Module 3', grade: '三年级上册' },
    '上4': { module: 'Module 4', grade: '三年级上册' },
    '上5': { module: 'Module 5', grade: '三年级上册' },
    '上6': { module: 'Module 6', grade: '三年级上册' },
    '上7': { module: 'Module 7', grade: '三年级上册' },
    '上8': { module: 'Module 8', grade: '三年级上册' },
    '上9': { module: 'Module 9', grade: '三年级上册' },
    '上10': { module: 'Module 10', grade: '三年级上册' },
    '下1': { module: 'Module 1', grade: '三年级下册' },
    '下2': { module: 'Module 2', grade: '三年级下册' },
    '下3': { module: 'Module 3', grade: '三年级下册' },
    '下4': { module: 'Module 4', grade: '三年级下册' },
    '下5': { module: 'Module 5', grade: '三年级下册' },
    '下6': { module: 'Module 6', grade: '三年级下册' },
    '下7': { module: 'Module 7', grade: '三年级下册' },
    '下8': { module: 'Module 8', grade: '三年级下册' },
    '下9': { module: 'Module 9', grade: '三年级下册' },
    '下10': { module: 'Module 10', grade: '三年级下册' }
  };"""

if old_mapping in content:
    content = content.replace(old_mapping, new_mapping)
    print("✓ WORD_TO_LESSON 扩展为对象格式（包含学期）")
else:
    print("✗ 未找到旧映射")

# ============================================================
# 改造 2: 更新 showTextbookList 智能跳转逻辑
# ============================================================
old_smart = """  async function showTextbookList() {
    // 智能跳转：如果当前在某个单词模块中，直接打开对应的课文模块
    if (currentModule && WORD_TO_LESSON[currentModule]) {
      const lessonModule = WORD_TO_LESSON[currentModule];
      // 直接进入对应模块的单元列表
      await openLessonModule(lessonModule);
      return;
    }"""

new_smart = """  async function showTextbookList() {
    // 智能跳转：如果当前在某个单词模块中，直接打开对应的课文模块
    if (currentModule && WORD_TO_LESSON[currentModule]) {
      const mapping = WORD_TO_LESSON[currentModule];
      // 直接进入对应模块的单元列表（带上学期参数）
      await openLessonModule(mapping.module, mapping.grade);
      return;
    }"""

if old_smart in content:
    content = content.replace(old_smart, new_smart)
    print("✓ showTextbookList 智能跳转更新（带学期）")
else:
    print("✗ 未找到 showTextbookList")

# ============================================================
# 改造 3: 更新 openLessonModule 支持学期参数
# ============================================================
old_open = """  async function openLessonModule(moduleName) {
    currentLessonModule = moduleName;
    document.getElementById('topbar-title').textContent = '📖 ' + moduleName;
    
    try {
      const data = await apiGET('/api/textbook/' + encodeURIComponent(moduleName));
      currentLessonData = data.units;"""

new_open = """  async function openLessonModule(moduleName, grade) {
    currentLessonModule = moduleName;
    currentLessonGrade = grade || currentLessonGrade || '三年级上册';
    document.getElementById('topbar-title').textContent = '📖 ' + currentLessonGrade + ' - ' + moduleName;

    try {
      // 根据是否有指定学期决定 URL
      let url = '/api/textbook/' + encodeURIComponent(moduleName);
      if (grade) {
        url += '?grade=' + encodeURIComponent(grade);
      }
      const data = await apiGET(url);
      currentLessonData = data.units;
      currentLessonGrade = data.grade || currentLessonGrade;"""

if old_open in content:
    content = content.replace(old_open, new_open)
    print("✓ openLessonModule 支持学期参数")
else:
    print("✗ 未找到 openLessonModule")

# ============================================================
# 改造 4: 添加 currentLessonGrade 状态变量
# ============================================================
old_state = """  // 课文学习相关状态
    let currentLessonModule = null;
    let currentLessonData = null;"""

new_state = """  // 课文学习相关状态
    let currentLessonModule = null;
    let currentLessonData = null;
    let currentLessonGrade = '三年级上册';"""

if old_state in content:
    content = content.replace(old_state, new_state)
    print("✓ 添加 currentLessonGrade 状态变量")
else:
    print("✗ 未找到状态变量")

# ============================================================
# 改造 5: 更新模块列表渲染，显示学期
# ============================================================
old_module_render = """      for (const m of modules) {
        const card = document.createElement('div');
        card.className = 'module-card';
        card.innerHTML = `
          <div class="module-name">${m.module}</div>
          <div class="module-count">${m.unit_count} 个单元</div>
        `;
        card.onclick = () => openLessonModule(m.module);
        grid.appendChild(card);
      }"""

new_module_render = """      for (const m of modules) {
        const card = document.createElement('div');
        card.className = 'module-card';
        const gradeLabel = m.grade ? ` <span style="font-size:11px;color:#888;font-weight:normal">(${m.grade})</span>` : '';
        card.innerHTML = `
          <div class="module-name">${m.module}${gradeLabel}</div>
          <div class="module-count">${m.unit_count} 个单元</div>
        `;
        // 模块点击时带上学期参数
        card.onclick = () => openLessonModule(m.module, m.grade);
        grid.appendChild(card);
      }"""

if old_module_render in content:
    content = content.replace(old_module_render, new_module_render)
    print("✓ 模块列表渲染显示学期")
else:
    print("✗ 未找到模块列表渲染")

# 保存
if content != original_content:
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("\n✓ index.html 已保存")
else:
    print("\n无修改")