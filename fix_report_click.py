# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 找到 loadReport 函数里的模块卡片生成逻辑
old_html = """        div.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">' +
          '<div style="font-weight:600;font-size:15px">' + mod + '</div>' +
          '<div style="display:flex;align-items:center;gap:8px">' +
            statusLabel +
            '<span style="font-size:14px">' + pctBig + '</span></div></div>' +
          '<div style="height:8px;background:#f0f4ff;border-radius:4px;overflow:hidden;margin-bottom:8px">' +
            '<div style="height:100%;background:' + barColor + ';width:' + pctM + '%;border-radius:4px;transition:width .4s"></div></div>' +
          '<div style="display:flex;gap:16px;font-size:12px;color:#999">' +
            '<span>&#128214; 已学 <b style="color:#333">' + learned + '</b></span>' +
            '<span>&#11088; 已掌握 <b style="color:#333">' + mastered + '</b></span>' +
            '<span>&#128218; 共 <b style="color:#333">' + total + '</b></span></div>';"""

new_html = """        // 状态标签点击事件
        const statusOnclick = learned === total && total > 0 && mastered < total
          ? 'onclick="goToModuleLearn(\\'' + mod + '\\')" style="cursor:pointer"'
          : '';
        const masteredOnclick = mastered > 0
          ? 'onclick="goToModuleMastered(\\'' + mod + '\\')" style="cursor:pointer"'
          : '';

        div.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">' +
          '<div style="font-weight:600;font-size:15px">' + mod + '</div>' +
          '<div style="display:flex;align-items:center;gap:8px">' +
            '<span ' + statusOnclick + '>' + statusLabel + '</span>' +
            '<span style="font-size:14px">' + pctBig + '</span></div></div>' +
          '<div style="height:8px;background:#f0f4ff;border-radius:4px;overflow:hidden;margin-bottom:8px">' +
            '<div style="height:100%;background:' + barColor + ';width:' + pctM + '%;border-radius:4px;transition:width .4s"></div></div>' +
          '<div style="display:flex;gap:16px;font-size:12px;color:#999">' +
            '<span>&#128214; 已学 <b style="color:#333">' + learned + '</b></span>' +
            '<span ' + masteredOnclick + '>&#11088; 已掌握 <b style="color:#333">' + mastered + '</b></span>' +
            '<span>&#128218; 共 <b style="color:#333">' + total + '</b></span></div>';"""

if old_html in content:
    content = content.replace(old_html, new_html)
    print('HTML replaced OK')
else:
    print('HTML pattern not found')

# 在 loadReport 函数后面添加跳转函数
marker = '// ========== 底部导航 =========='
new_funcs = '''// ========== 报告页跳转函数 ==========
  function goToModuleLearn(mod) {
    currentModule = mod;
    switchView("learn");
    loadWords(mod);
    // 自动开始选择学习
    setTimeout(startChoiceLearn, 100);
  }

  function goToModuleMastered(mod) {
    currentModule = mod;
    switchView("learn");
    loadWords(mod);
    // 只显示已掌握的单词
    setTimeout(function() {
      filterWordsByStatus("mastered");
    }, 100);
  }

  function filterWordsByStatus(status) {
    // 获取当前单词的状态
    const list = document.getElementById("word-list");
    const items = list.querySelectorAll(".word-item");
    let visibleCount = 0;
    items.forEach(function(item) {
      const dot = item.querySelector(".word-status-dot");
      if (dot) {
        const hasStatus = dot.classList.contains(status);
        item.style.display = hasStatus ? "flex" : "none";
        if (hasStatus) visibleCount++;
      }
    });
    if (visibleCount === 0) {
      toast("该模块没有" + (status === "mastered" ? "已掌握" : "已学") + "的单词");
      // 显示全部
      items.forEach(function(item) { item.style.display = "flex"; });
    } else {
      document.getElementById("learn-module-title").textContent = "📖 " + currentModule + " (已掌握)";
    }
  }

'''

if marker in content:
    content = content.replace(marker, new_funcs + marker)
    print('Functions added OK')
else:
    print('Marker not found')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('File written OK')
