# -*- coding: utf-8 -*-
"""添加 KET 学习 JavaScript 函数"""

ket_js = '''
  // ========== KET 学习功能 ==========
  let ketCategories = [];

  async function loadKetCategories() {
    try {
      const data = await apiGET('/api/ket/categories');
      ketCategories = data.categories || [];

      const container = document.getElementById('ket-category-list');
      container.innerHTML = '';

      // 按类型分组
      const grouped = {};
      ketCategories.forEach(cat => {
        if (!grouped[cat.type]) grouped[cat.type] = [];
        grouped[cat.type].push(cat);
      });

      // 渲染分类卡片
      for (const [type, cats] of Object.entries(grouped)) {
        const typeDiv = document.createElement('div');
        typeDiv.style.gridColumn = '1 / -1';
        typeDiv.style.marginTop = '12px';
        typeDiv.style.marginBottom = '8px';
        typeDiv.style.fontSize = '16px';
        typeDiv.style.fontWeight = '600';
        typeDiv.style.color = '#333';
        typeDiv.textContent = type === '词汇' ? '📖 词汇学习' : type === '句型' ? '💬 句型练习' : '📝 语法知识';
        container.appendChild(typeDiv);

        cats.forEach(cat => {
          const card = document.createElement('div');
          card.className = 'module-card';
          card.innerHTML = `
            <div class="module-name">${cat.category}</div>
            <div class="module-count">${cat.count} 项</div>
          `;
          card.onclick = () => openKetCategory(cat.type, cat.category);
          container.appendChild(card);
        });
      }

      // 显示分类列表，隐藏内容区
      container.style.display = 'grid';
      document.getElementById('ket-content-area').style.display = 'none';

    } catch (e) {
      console.error('加载 KET 分类失败:', e);
      toast('加载失败，请检查后端服务');
    }
  }

  async function openKetCategory(type, category) {
    try {
      const container = document.getElementById('ket-content-list');
      const titleEl = document.getElementById('ket-content-title');

      // 隐藏分类列表，显示内容区
      document.getElementById('ket-category-list').style.display = 'none';
      document.getElementById('ket-content-area').style.display = 'block';

      if (type === '词汇') {
        titleEl.textContent = '📖 ' + category;
        const data = await apiGET('/api/ket/words?category=' + encodeURIComponent(category));
        const words = data.words || [];

        container.innerHTML = words.map((w, i) => `
          <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
            <div style="font-size:20px;font-weight:600;color:#4f9fff;margin-bottom:8px">
              ${w.word}
              <button class="speak-btn" onclick="speakWord('${w.word}')" style="margin-left:8px;padding:4px 12px;font-size:12px">🔊</button>
            </div>
            <div style="font-size:14px;color:#666;margin-bottom:4px">${w.chinese}</div>
            <div style="font-size:13px;color:#999;font-style:italic">例：${w.example}</div>
          </div>
        `).join('');

      } else if (type === '句型') {
        titleEl.textContent = '💬 ' + category;
        const data = await apiGET('/api/ket/sentences?category=' + encodeURIComponent(category));
        const sentences = data.sentences || [];

        container.innerHTML = sentences.map((s, i) => `
          <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
            <div style="font-size:18px;font-weight:600;color:#4f9fff;margin-bottom:8px">
              ${s.english}
              <button class="speak-btn" onclick="speakWord('${s.english}')" style="margin-left:8px;padding:4px 12px;font-size:12px">🔊</button>
            </div>
            <div style="font-size:14px;color:#666;margin-bottom:4px">${s.chinese}</div>
            <div style="font-size:12px;color:#999;background:#f0f4ff;padding:4px 8px;border-radius:4px;display:inline-block">用途：${s.usage}</div>
          </div>
        `).join('');

      } else if (type === '语法') {
        titleEl.textContent = '📝 ' + category;
        const data = await apiGET('/api/ket/grammar?category=' + encodeURIComponent(category));
        const grammar = data.grammar || {};

        let html = `
          <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
            <div style="font-size:16px;font-weight:600;color:#d48806;margin-bottom:8px">📖 规则</div>
            <div style="font-size:14px;color:#666;line-height:1.6">${grammar.规则 || ''}</div>
          </div>
        `;

        if (grammar.例句 && grammar.例句.length > 0) {
          html += `
            <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:#fffbf0;border-radius:12px;border:2px solid #ffe7ba">
              <div style="font-size:16px;font-weight:600;color:#d48806;margin-bottom:12px">📝 例句</div>
              ${grammar.例句.map(ex => `
                <div style="padding:8px 0;border-bottom:1px dashed #ffe7ba">
                  <div style="font-size:15px;color:#333">${ex}
                    <button class="speak-btn" onclick="speakWord('${ex}')" style="margin-left:8px;padding:2px 8px;font-size:11px">🔊</button>
                  </div>
                </div>
              `).join('')}
            </div>
          `;
        }

        container.innerHTML = html;
      }

    } catch (e) {
      console.error('加载 KET 内容失败:', e);
      toast('加载失败');
    }
  }

  function backToKetCategories() {
    document.getElementById('ket-category-list').style.display = 'grid';
    document.getElementById('ket-content-area').style.display = 'none';
  }
'''

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 在 loadModules() 之前插入
if 'loadKetCategories' not in content:
    # 找到 // ========== 启动 ==========
    insert_pos = content.find('  // ========== 启动 ==========')
    if insert_pos > 0:
        content = content[:insert_pos] + ket_js + '\n' + content[insert_pos:]
        print("✓ 添加 KET JavaScript 函数")
    else:
        print("✗ 未找到插入位置")
else:
    print("⚠ KET 函数已存在")

# 保存
with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("✓ 完成")