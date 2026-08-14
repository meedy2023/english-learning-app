# -*- coding: utf-8 -*-
"""优化TTS发音速度，放慢语速"""

with open('frontend/index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

changes = 0

# 1. 课文朗读速度：0.85 -> 0.7
content = content.replace("utter.rate = 0.85;", "utter.rate = 0.7;")
changes += content.count("utter.rate = 0.7;")
print(f"✓ 课文朗读速率: 0.85 → 0.7")

# 2. speakAll 中英文例句速率调整
content = content.replace("u.rate = p.lang === 'en-US' ? 0.85 : 1.0;", "u.rate = p.lang === 'en-US' ? 0.7 : 0.85;")
print("✓ speakAll 例句速率调整")

# 3. 课文朗读间隔：2.5秒 -> 3秒（给更多消化时间）
content = content.replace("delay += 2500; // 每句间隔2.5秒", "delay += 3500; // 每句间隔3.5秒")
print("✓ 课文朗读间隔: 2.5秒 → 3.5秒")

# 4. speakAll 单词到中文的间隔：500ms -> 800ms
content = content.replace("{ text: chinese,    lang: 'zh-CN', delay: 500 }", "{ text: chinese,    lang: 'zh-CN', delay: 800 }")
print("✓ 单词到中文间隔: 500ms → 800ms")

# 5. speakAll 英文例句的延迟：600ms -> 1000ms
content = content.replace("{ text: exampleEn,  lang: 'en-US', delay: 600 }", "{ text: exampleEn,  lang: 'en-US', delay: 1000 }")
print("✓ 英文例句间隔: 600ms → 1000ms")

with open('frontend/index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print(f"\n✓ 完成，共 {changes} 处修改")
