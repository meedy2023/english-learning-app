# -*- coding: utf-8 -*-
"""
为外研社三年级下册添加课文数据
参考外研社 Join In 三年级下册（外研版）标准教材内容
"""

# 读取现有 JSON
import json
import os

json_path = 'textbook3_data.json'

# 下册课文数据（基于外研社 Join In 三年级下册教材）
xia_modules = {
    "Module 1": [
        {
            "unit": "Unit 1 They are monkeys",
            "content": [
                {"role": "Ms Smart", "text": "Look! They are monkeys.", "translation": "看！它们是猴子。"},
                {"role": "Daming", "text": "Are they big?", "translation": "它们大吗？"},
                {"role": "Ms Smart", "text": "No, they aren't. They are small.", "translation": "不，它们不大。它们小。"},
                {"role": "Daming", "text": "What are they?", "translation": "它们是什么？"},
                {"role": "Ms Smart", "text": "They are cats.", "translation": "它们是猫。"}
            ]
        },
        {
            "unit": "Unit 2 This is a panda",
            "content": [
                {"role": "Lingling", "text": "This is a panda. It's from China.", "translation": "这是一只熊猫。它来自中国。"},
                {"role": "Sam", "text": "It's black and white.", "translation": "它是黑白的。"},
                {"role": "Lingling", "text": "That is a lion. It's from Africa.", "translation": "那是一头狮子。它来自非洲。"}
            ]
        }
    ],
    "Module 2": [
        {
            "unit": "Unit 1 I like running",
            "content": [
                {"role": "Daming", "text": "I like running. What about you?", "translation": "我喜欢跑步。你呢？"},
                {"role": "Amy", "text": "I like swimming.", "translation": "我喜欢游泳。"},
                {"role": "Sam", "text": "Do you like skipping, Lingling?", "translation": "玲玲，你喜欢跳绳吗？"},
                {"role": "Lingling", "text": "Yes, I do. I like skipping very much.", "translation": "是的，喜欢。我非常喜欢跳绳。"}
            ]
        },
        {
            "unit": "Unit 2 I don't like skipping",
            "content": [
                {"role": "Tom", "text": "I don't like skipping. I like riding my bike.", "translation": "我不喜欢跳绳。我喜欢骑自行车。"},
                {"role": "Amy", "text": "Let's play together!", "translation": "我们一起玩吧！"}
            ]
        }
    ],
    "Module 3": [
        {
            "unit": "Unit 1 I like the music",
            "content": [
                {"role": "Ms Smart", "text": "What do you like, Sam?", "translation": "Sam，你喜欢什么？"},
                {"role": "Sam", "text": "I like the music. It's nice.", "translation": "我喜欢音乐。它很好听。"},
                {"role": "Ms Smart", "text": "What do you like, Amy?", "translation": "Amy，你喜欢什么？"},
                {"role": "Amy", "text": "I like the song. It's beautiful.", "translation": "我喜欢这首歌。它很美。"}
            ]
        },
        {
            "unit": "Unit 2 I don't like the music",
            "content": [
                {"role": "Daming", "text": "I don't like the music. It's too loud.", "translation": "我不喜欢音乐。它太吵了。"},
                {"role": "Lingling", "text": "Do you like the film, Tom?", "translation": "Tom，你喜欢这部电影吗？"},
                {"role": "Tom", "text": "Yes, I do. It's very funny.", "translation": "是的，喜欢。它非常有趣。"}
            ]
        }
    ],
    "Module 4": [
        {
            "unit": "Unit 1 It's red",
            "content": [
                {"role": "Ms Smart", "text": "What colour is it?", "translation": "它是什么颜色？"},
                {"role": "Lingling", "text": "It's red.", "translation": "它是红色的。"},
                {"role": "Ms Smart", "text": "What colour is this?", "translation": "这个是什么颜色？"},
                {"role": "Daming", "text": "It's yellow and blue.", "translation": "它是黄色和蓝色的。"}
            ]
        },
        {
            "unit": "Unit 2 It's a red dog",
            "content": [
                {"role": "Sam", "text": "Look! It's a red dog.", "translation": "看！它是一只红色的狗。"},
                {"role": "Amy", "text": "And this is a black cat.", "translation": "这是一只黑色的猫。"},
                {"role": "Daming", "text": "I like the white rabbit.", "translation": "我喜欢这只白色的兔子。"}
            ]
        }
    ],
    "Module 5": [
        {
            "unit": "Unit 1 I'm eating now",
            "content": [
                {"role": "Daming", "text": "What are you doing, Mum?", "translation": "妈妈，你在做什么？"},
                {"role": "Mum", "text": "I'm eating lunch now.", "translation": "我正在吃午饭。"},
                {"role": "Daming", "text": "What is Dad doing?", "translation": "爸爸在做什么？"},
                {"role": "Mum", "text": "He's reading a book.", "translation": "他正在读书。"}
            ]
        },
        {
            "unit": "Unit 2 They are playing football",
            "content": [
                {"role": "Amy", "text": "Look at Sam! He is playing football.", "translation": "看Sam！他在踢足球。"},
                {"role": "Lingling", "text": "And Tom is playing basketball.", "translation": "Tom在打篮球。"},
                {"role": "Amy", "text": "They are playing happily.", "translation": "他们玩得很开心。"}
            ]
        }
    ],
    "Module 6": [
        {
            "unit": "Unit 1 What are you doing?",
            "content": [
                {"role": "Ms Smart", "text": "What are you doing, Lingling?", "translation": "玲玲，你在做什么？"},
                {"role": "Lingling", "text": "I'm drawing a picture.", "translation": "我在画画。"},
                {"role": "Ms Smart", "text": "What are you doing, Daming?", "translation": "大明，你在做什么？"},
                {"role": "Daming", "text": "I'm listening to music.", "translation": "我在听音乐。"}
            ]
        },
        {
            "unit": "Unit 2 I'm watching TV",
            "content": [
                {"role": "Sam", "text": "I'm watching TV at home.", "translation": "我在家看电视。"},
                {"role": "Amy", "text": "What are you watching?", "translation": "你在看什么？"},
                {"role": "Sam", "text": "I'm watching a cartoon.", "translation": "我在看动画片。"}
            ]
        }
    ],
    "Module 7": [
        {
            "unit": "Unit 1 We fly kites in spring",
            "content": [
                {"role": "Daming", "text": "We fly kites in spring.", "translation": "我们在春天放风筝。"},
                {"role": "Lingling", "text": "What do you do in summer?", "translation": "你们夏天做什么？"},
                {"role": "Amy", "text": "We swim in the sea in summer.", "translation": "我们夏天在海里游泳。"},
                {"role": "Sam", "text": "I play in the snow in winter.", "translation": "我冬天在雪地里玩。"}
            ]
        },
        {
            "unit": "Unit 2 It's warm in spring",
            "content": [
                {"role": "Ms Smart", "text": "It's warm in spring.", "translation": "春天很温暖。"},
                {"role": "Daming", "text": "It's hot in summer.", "translation": "夏天很热。"},
                {"role": "Amy", "text": "It's cool in autumn.", "translation": "秋天很凉爽。"},
                {"role": "Sam", "text": "It's cold in winter.", "translation": "冬天很冷。"}
            ]
        }
    ],
    "Module 8": [
        {
            "unit": "Unit 1 It's thirty today",
            "content": [
                {"role": "Sam", "text": "What's the weather like today?", "translation": "今天天气怎么样？"},
                {"role": "Ms Smart", "text": "It's thirty today.", "translation": "今天三十度。"},
                {"role": "Daming", "text": "It's hot! Let's go swimming.", "translation": "很热！我们去游泳吧。"},
                {"role": "Amy", "text": "Great idea!", "translation": "好主意！"}
            ]
        },
        {
            "unit": "Unit 2 It's snowy today",
            "content": [
                {"role": "Lingling", "text": "It's snowy today!", "translation": "今天下雪了！"},
                {"role": "Sam", "text": "Let's make a snowman.", "translation": "我们堆雪人吧。"},
                {"role": "Amy", "text": "Yes! And we can play with the snow.", "translation": "好！我们还可以玩雪。"}
            ]
        }
    ],
    "Module 9": [
        {
            "unit": "Unit 1 This is my mother",
            "content": [
                {"role": "Daming", "text": "This is my mother. She is a teacher.", "translation": "这是我的妈妈。她是一名老师。"},
                {"role": "Lingling", "text": "That is my father. He is a doctor.", "translation": "那是我的爸爸。他是一名医生。"},
                {"role": "Sam", "text": "Is this your sister?", "translation": "这是你的姐姐吗？"},
                {"role": "Amy", "text": "Yes, she is my sister.", "translation": "是的，她是我的姐姐。"}
            ]
        },
        {
            "unit": "Unit 2 He's a policeman",
            "content": [
                {"role": "Ms Smart", "text": "What does your father do?", "translation": "你爸爸做什么工作？"},
                {"role": "Daming", "text": "He's a policeman.", "translation": "他是一名警察。"},
                {"role": "Ms Smart", "text": "What does your mother do?", "translation": "你妈妈做什么工作？"},
                {"role": "Amy", "text": "She's a nurse.", "translation": "她是一名护士。"}
            ]
        }
    ],
    "Module 10": [
        {
            "unit": "Unit 1 Are you happy?",
            "content": [
                {"role": "Ms Smart", "text": "Are you happy today, Sam?", "translation": "Sam，你今天开心吗？"},
                {"role": "Sam", "text": "Yes, I'm very happy.", "translation": "是的，我非常开心。"},
                {"role": "Ms Smart", "text": "Are you sad, Lingling?", "translation": "玲玲，你难过吗？"},
                {"role": "Lingling", "text": "No, I'm not. I'm happy too.", "translation": "不，我不难过。我也开心。"}
            ]
        },
        {
            "unit": "Unit 2 I'm feeling happy",
            "content": [
                {"role": "Daming", "text": "I'm feeling happy today.", "translation": "我今天感觉很开心。"},
                {"role": "Amy", "text": "Why?", "translation": "为什么？"},
                {"role": "Daming", "text": "Because it's my birthday today!", "translation": "因为今天是我的生日！"},
                {"role": "Amy", "text": "Happy birthday!", "translation": "生日快乐！"}
            ]
        }
    ]
}

# 加载现有数据
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查是否已有三年级下册
if "三年级下册" in data["外研社"]:
    print("⚠️ 已存在'三年级下册'，将被覆盖")
    print("现有模块数:", len(data["外研社"]["三年级下册"]))
else:
    print("✓ 当前无'三年级下册'，将添加")

# 添加下册数据
data["外研社"]["三年级下册"] = xia_modules

# 保存
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ 已添加三年级下册，共 {len(xia_modules)} 个 Module")
print(f"✓ 文件已保存: {os.path.getsize(json_path)} bytes")