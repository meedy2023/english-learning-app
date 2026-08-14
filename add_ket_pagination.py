# -*- coding: utf-8 -*-
"""为 KET 学习添加分页功能"""

pagination_js = '''
  // ========== KET 分页功能 ==========
  let ketCurrentPage = 1;
  let ketItemsPerPage = 10; // 默认每页10项
  let ketCurrentItems = []; // 当前显示的数据
  let ketCurrentType = ''; // 当前类型
  let ketCurrentCategory = ''; // 当前分类

  function renderKetPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / ketItemsPerPage);
    const container = document.getElementById('ket-pagination');
    
    if (!container) {
      // 创建分页容器
      const contentArea = document.getElementById('ket-content-area');
      const paginationDiv = document.createElement('div');
      paginationDiv.id = 'ket-pagination';
      paginationDiv.style.cssText = 'display:flex;justify-content:center;align-items:center;gap:8px;margin-top:20px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)';
      contentArea.appendChild(paginationDiv);
    }
    
    if (totalPages <= 1) {
      if (container) container.style.display = 'none';
      return;
    }
    
    const paginationContainer = document.getElementById('ket-pagination');
    paginationContainer.style.display = 'flex';
    
    let html = '';
    
    // 上一页按钮
    html += `<button class="btn btn-secondary" onclick="changeKetPage(${ketCurrentPage - 1})" ${ketCurrentPage === 1 ? 'disabled' : ''} style="padding:8px 16px;font-size:14px">← 上一页</button>`;
    
    // 页码信息
    html += `<span style="font-size:14px;color:#666;padding:0 12px">第 ${ketCurrentPage} / ${totalPages} 页 (共 ${totalItems} 项)</span>`;
    
    // 每页数量选择
    html += `<select onchange="changeKetItemsPerPage(this.value)" style="padding:8px 12px;border:1px solid #ddd;border-radius:8px;font-size:14px;margin-left:8px">`;
    html += `<option value="5" ${ketItemsPerPage === 5 ? 'selected' : ''}>每页5项</option>`;
    html += `<option value="10" ${ketItemsPerPage === 10 ? 'selected' : ''}>每页10项</option>`;
    html += `<option value="20" ${ketItemsPerPage === 20 ? 'selected' : ''}>每页20项</option>`;
    html += `</select>`;
    
    // 下一页按钮
    html += `<button class="btn btn-secondary" onclick="changeKetPage(${ketCurrentPage + 1})" ${ketCurrentPage === totalPages ? 'disabled' : ''} style="padding:8px 16px;font-size:14px;margin-left:8px">下一页 →</button>`;
    
    paginationContainer.innerHTML = html;
  }

  function changeKetPage(page) {
    const totalPages = Math.ceil(ketCurrentItems.length / ketItemsPerPage);
    if (page < 1 || page > totalPages) return;
    
    ketCurrentPage = page;
    renderKetCurrentPage();
    renderKetPagination(ketCurrentItems.length);
    
    // 滚动到内容顶部
    document.getElementById('ket-content-title').scrollIntoView({ behavior: 'smooth' });
  }

  function changeKetItemsPerPage(count) {
    ketItemsPerPage = parseInt(count);
    ketCurrentPage = 1;
    renderKetCurrentPage();
    renderKetPagination(ketCurrentItems.length);
  }

  function renderKetCurrentPage() {
    const container = document.getElementById('ket-content-list');
    const start = (ketCurrentPage - 1) * ketItemsPerPage;
    const end = start + ketItemsPerPage;
    const pageItems = ketCurrentItems.slice(start, end);
    
    if (ketCurrentType === '词汇') {
      container.innerHTML = pageItems.map((w, i) => `
        <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
          <div style="font-size:20px;font-weight:600;color:#4f9fff;margin-bottom:8px;display:flex;align-items:center;gap:12px">
            <span style="background:#f0f4ff;color:#4f9fff;padding:4px 12px;border-radius:20px;font-size:14px">${start + i + 1}</span>
            ${w.word}
            <button class="speak-btn" onclick="speakWord('${w.word}')" style="margin-left:8px;padding:4px 12px;font-size:12px">🔊</button>
          </div>
          <div style="font-size:14px;color:#666;margin-bottom:4px">${w.chinese}</div>
          <div style="font-size:13px;color:#999;font-style:italic">例：${w.example}</div>
        </div>
      `).join('');
    } else if (ketCurrentType === '句型') {
      container.innerHTML = pageItems.map((s, i) => `
        <div class="word-detail-card" style="margin-bottom:12px;padding:16px;background:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
          <div style="font-size:18px;font-weight:600;color:#4f9fff;margin-bottom:8px;display:flex;align-items:center;gap:12px">
            <span style="background:#f0f4ff;color:#4f9fff;padding:4px 12px;border-radius:20px;font-size:14px">${start + i + 1}</span>
            ${s.english}
            <button class="speak-btn" onclick="speakWord('${s.english}')" style="margin-left:8px;padding:4px 12px;font-size:12px">🔊</button>
          </div>
          <div style="font-size:14px;color:#666;margin-bottom:4px">${s.chinese}</div>
          <div style="font-size:12px;color:#999;background:#f0f4ff;padding:4px 8px;border-radius:4px;display:inline-block">用途：${s.usage}</div>
        </div>
      `).join('');
    }
  }

  async function openKetCategory(type, category) {
    try {
      const container = document.getElementById('ket-content-list');
      const titleEl = document.getElementById('ket-content-title');
      
      // 重置分页状态
      ketCurrentPage = 1;
      ketCurrentType = type;
      ketCurrentCategory = category;
      
      // 隐藏分类列表，显示内容区
      document.getElementById('ket-category-list').style.display = 'none';
      document.getElementById('ket-content-area').style.display = 'block';
      
      // 移除旧的分页容器（如果存在）
      const oldPagination = document.getElementById('ket-pagination');
      if (oldPagination) oldPagination.remove();

      if (type === '词汇') {
        titleEl.textContent = '📖 ' + category;
        const data = await apiGET('/api/ket/words?category=' + encodeURIComponent(category));
        ketCurrentItems = data.words || [];
        
        renderKetCurrentPage();
        renderKetPagination(ketCurrentItems.length);

      } else if (type === '句型') {
        titleEl.textContent = '💬 ' + category;
        const data = await apiGET('/api/ket/sentences?category=' + encodeURIComponent(category));
        ketCurrentItems = data.sentences || [];
        
        renderKetCurrentPage();
        renderKetPagination(ketCurrentItems.length);

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
              <div style="font-size:16px;font-weight:600;color:#d48806;margin-bottom:12px">📝 例句 (${grammar.例句.length}个)</div>
              ${grammar.例句.map((ex, idx) => `
                <div style="padding:8px 0;border-bottom:1px dashed #ffe7ba;display:flex;align-items:center;gap:8px">
                  <span style="background:#ffe7ba;color:#d48806;padding:2px 8px;border-radius:10px;font-size:12px">${idx + 1}</span>
                  <span style="font-size:15px;color:#333">${ex}</span>
                  <button class="speak-btn" onclick="speakWord('${ex}')" style="margin-left:auto;padding:2px 8px;font-size:11px">🔊</button>
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
'''

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 检查是否已存在分页函数
if 'ketCurrentPage' in content:
    print("⚠ 分页函数已存在")
else:
    # 替换 openKetCategory 函数
    old_func_start = content.find('async function openKetCategory(type, category)')
    if old_func_start > 0:
        # 找到函数结束位置（下一个函数开始或文件结束）
        next_func = content.find('\n  async function', old_func_start + 1)
        if next_func == -1:
            next_func = content.find('\n  function', old_func_start + 1)
        
        # 替换整个函数
        content = content[:old_func_start] + pagination_js + content[next_func:]
        print("✓ 已添加分页功能")
    else:
        print("✗ 未找到 openKetCategory 函数")

# 保存
with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("✓ 完成")