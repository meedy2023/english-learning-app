# -*- coding: utf-8 -*-
"""修复分页按钮：第一页隐藏上一页，最后一页隐藏下一页"""

import re

# 读取文件
with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 找到 renderKetPagination 函数
old_pattern = r'''function renderKetPagination\(totalItems\) \{[\s\S]*?paginationContainer\.innerHTML = html;[\s\S]*?\}'''

new_function = '''function renderKetPagination(totalItems) {
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
    
    // 上一页按钮 - 仅在非第一页时显示
    if (ketCurrentPage > 1) {
      html += `<button class="btn btn-secondary" onclick="changeKetPage(${ketCurrentPage - 1})" style="padding:8px 16px;font-size:14px">← 上一页</button>`;
    }
    
    // 页码信息
    html += `<span style="font-size:14px;color:#666;padding:0 12px">第 ${ketCurrentPage} / ${totalPages} 页 (共 ${totalItems} 项)</span>`;
    
    // 每页数量选择
    html += `<select onchange="changeKetItemsPerPage(this.value)" style="padding:8px 12px;border:1px solid #ddd;border-radius:8px;font-size:14px;margin-left:8px">`;
    html += `<option value="5" ${ketItemsPerPage === 5 ? 'selected' : ''}>每页5项</option>`;
    html += `<option value="10" ${ketItemsPerPage === 10 ? 'selected' : ''}>每页10项</option>`;
    html += `<option value="20" ${ketItemsPerPage === 20 ? 'selected' : ''}>每页20项</option>`;
    html += `</select>`;
    
    // 下一页按钮 - 仅在非最后一页时显示
    if (ketCurrentPage < totalPages) {
      html += `<button class="btn btn-secondary" onclick="changeKetPage(${ketCurrentPage + 1})" style="padding:8px 16px;font-size:14px;margin-left:8px">下一页 →</button>`;
    }
    
    paginationContainer.innerHTML = html;
  }'''

# 替换函数
content_new = re.sub(old_pattern, new_function, content, flags=re.DOTALL)

if content_new != content:
    with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content_new)
    print("✓ 分页按钮已修复")
else:
    print("✗ 未找到匹配的函数")

print("完成")