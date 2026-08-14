# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

# 找到精确位置
idx = content.find('container.innerHTML = "";')
if idx == -1:
    print('NOT FOUND')
    exit(1)

# 找到 for 循环结束的大括号（container.appendChild(div); 后面那个 }）
append_idx = content.find('container.appendChild(div);', idx)
if append_idx == -1:
    print('appendChild NOT FOUND')
    exit(1)
for_end = content.find('}', append_idx + 30)
print('Replacing from', idx, 'to', for_end)

old = content[idx:for_end + 1]
print('OLD length:', len(old))
print('OLD snippet:', repr(old[:200]))

new = '''container.innerHTML = "";
      const keys = Object.keys(data).filter(k => k !== "_total");
      for (const mod of keys) {
        const p = data[mod];
        const total = p.total || 0;
        const learned = p.learned || 0;
        const mastered = p.mastered || 0;
        const pctM = total > 0 ? Math.round(learned / total * 100) : 0;

        // 状态标签
        let statusLabel = '<span style="font-size:11px;padding:2px 8px;border-radius:10px;background:#f5f5f5;color:#999">未开始</span>';
        if (learned > 0 && mastered === 0) statusLabel = '<span style="font-size:11px;padding:2px 8px;border-radius:10px;background:#e6f7ff;color:#1890ff">学习中</span>';
        if (mastered > 0) statusLabel = '<span style="font-size:11px;padding:2px 8px;border-radius:10px;background:#f6ffed;color:#52c41a">已掌握</span>';
        if (learned === total && total > 0 && mastered < total) statusLabel = '<span style="font-size:11px;padding:2px 8px;border-radius:10px;background:#fff7e6;color:#fa8c16">待巩固</span>';

        // 进度条颜色
        let barColor = '#e8eeff';
        if (pctM >= 100) barColor = '#52c41a';
        else if (pctM >= 60) barColor = '#4f9fff';

        const pctBig = pctM >= 100
          ? '<span style="color:#52c41a;font-weight:700">&#10004; ' + pctM + '%</span>'
          : '<span style="color:#6c63ff;font-weight:700">' + pctM + '%</span>';

        const div = document.createElement("div");
        div.className = "report-card";
        div.style.cssText = "cursor:pointer";
        div.onclick = (function(m) { return function() {
          currentModule = m;
          switchView("learn");
          loadWords(m);
        }; })(mod);
        div.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">' +
          '<div style="font-weight:600;font-size:15px">' + mod + '</div>' +
          '<div style="display:flex;align-items:center;gap:8px">' +
            statusLabel +
            '<span style="font-size:14px">' + pctBig + '</span></div></div>' +
          '<div style="height:8px;background:#f0f4ff;border-radius:4px;overflow:hidden;margin-bottom:8px">' +
            '<div style="height:100%;background:' + barColor + ';width:' + pctM + '%;border-radius:4px;transition:width .4s"></div></div>' +
          '<div style="display:flex;gap:16px;font-size:12px;color:#999">' +
            '<span>&#128214; 已学 <b style="color:#333">' + learned + '</b></span>' +
            '<span>&#11088; 已掌握 <b style="color:#333">' + mastered + '</b></span>' +
            '<span>&#128218; 共 <b style="color:#333">' + total + '</b></span></div>';
        container.appendChild(div);
      }'''

if old in content:
    content = content.replace(old, new)
    print('Replaced OK')
else:
    print('String mismatch')

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print('Written OK')
