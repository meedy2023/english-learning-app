# -*- coding: utf-8 -*-
content = open(r'C:\Users\omap\english_app\frontend\index.html', 'r', encoding='utf-8-sig').read()

speak_all_fn = """
  function speakAll(word, chinese, exampleEn, exampleCn) {
    // 朗读顺序：单词 -> 中文 -> 英文例句 -> 例句中文
    const parts = [
      { text: word,       lang: 'en-US', delay: 600 },
      { text: chinese,    lang: 'zh-CN', delay: 500 },
      { text: exampleEn,  lang: 'en-US', delay: 600 },
      { text: exampleCn,  lang: 'zh-CN', delay: 0   },
    ];
    let delay = 300;
    for (const p of parts) {
      setTimeout(() => {
        if (!p.text) return;
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(p.text);
        u.lang = p.lang;
        u.rate = p.lang === 'en-US' ? 0.85 : 1.0;
        const vlist = speechSynthesis.getVoices();
        const v = vlist.find(x => x.lang.startsWith(p.lang.slice(0, 2)));
        if (v) u.voice = v;
        speechSynthesis.speak(u);
      }, delay);
      delay += p.delay + 200;
    }
  }

"""

# 插在 "// 提前加载 voices" 注释之前
marker = "  // 提前加载 voices"
idx = content.find(marker)
if idx == -1:
    print("Marker not found!")
    exit(1)
content = content[:idx] + speak_all_fn + content[idx:]
print("speakAll inserted at position", idx)

open(r'C:\Users\omap\english_app\frontend\index.html', 'w', encoding='utf-8-sig').write(content)
print("File written OK")
