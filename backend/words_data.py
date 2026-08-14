# -*- coding: utf-8 -*-
"""
外研社三年级英语上下册完整单词数据
每条包含：单词、音标、中文、英文例句、中文例句、所属模块、类型
"""

WORDS = [
    # ===================== 上册 =====================
    # Module 1 - Hello! / Hi!
    {
        "id": 1, "module": "上1", "word": "hello", "phonetic": "/həˈləʊ/",
        "chinese": "你好", "type": "greeting",
        "example_en": "Hello! I'm Amy.",
        "example_cn": "你好！我是 Amy。",
    },
    {
        "id": 2, "module": "上1", "word": "hi", "phonetic": "/haɪ/",
        "chinese": "你好（口语）", "type": "greeting",
        "example_en": "Hi! I'm Sam.",
        "example_cn": "你好！我是 Sam。",
    },
    {
        "id": 3, "module": "上1", "word": "goodbye", "phonetic": "/ɡʊdˈbaɪ/",
        "chinese": "再见", "type": "greeting",
        "example_en": "Goodbye, Ms Smart!",
        "example_cn": "再见，Smart 老师！",
    },
    {
        "id": 4, "module": "上1", "word": "bye", "phonetic": "/baɪ/",
        "chinese": "再见（口语）", "type": "greeting",
        "example_en": "Bye, Dad!",
        "example_cn": "再见，爸爸！",
    },

    # Module 2 - I'm Ms Smart.
    {
        "id": 5, "module": "上2", "word": "I", "phonetic": "/aɪ/",
        "chinese": "我", "type": "pronoun",
        "example_en": "I'm Amy. (I am)",
        "example_cn": "我是 Amy。",
    },
    {
        "id": 6, "module": "上2", "word": "am", "phonetic": "/æm/",
        "chinese": "是（我）", "type": "verb",
        "example_en": "I'm a teacher.",
        "example_cn": "我是一名老师。",
    },
    {
        "id": 7, "module": "上2", "word": "you", "phonetic": "/juː/",
        "chinese": "你", "type": "pronoun",
        "example_en": "You are (You're) my friend.",
        "example_cn": "你是我的朋友。",
    },
    {
        "id": 8, "module": "上2", "word": "Mr", "phonetic": "/ˈmɪstə(r)/",
        "chinese": "先生", "type": "title",
        "example_en": "Mr Li is a teacher.",
        "example_cn": "李老师是一位老师。",
    },
    {
        "id": 9, "module": "上2", "word": "Ms", "phonetic": "/mɪz/",
        "chinese": "女士（不知婚否）", "type": "title",
        "example_en": "Ms Smart is a teacher.",
        "example_cn": "Smart 女士是一位老师。",
    },

    # Module 3 - Point to the door.
    {
        "id": 10, "module": "上3", "word": "point", "phonetic": "/pɔɪnt/",
        "chinese": "指向", "type": "verb",
        "example_en": "Point to the door.",
        "example_cn": "指向门。",
    },
    {
        "id": 11, "module": "上3", "word": "to", "phonetic": "/tuː/",
        "chinese": "向（介词）", "type": "prep",
        "example_en": "Point to the window.",
        "example_cn": "指向窗户。",
    },
    {
        "id": 12, "module": "上3", "word": "the", "phonetic": "/ðə/",
        "chinese": "这/那（定冠词）", "type": "article",
        "example_en": "The door is red.",
        "example_cn": "门是红色的。",
    },
    {
        "id": 13, "module": "上3", "word": "door", "phonetic": "/dɔː(r)/",
        "chinese": "门", "type": "noun",
        "example_en": "Point to the door.",
        "example_cn": "指向门。",
    },
    {
        "id": 14, "module": "上3", "word": "window", "phonetic": "/ˈwɪndəʊ/",
        "chinese": "窗户", "type": "noun",
        "example_en": "Point to the window.",
        "example_cn": "指向窗户。",
    },
    {
        "id": 15, "module": "上3", "word": "blackboard", "phonetic": "/ˈblækbɔːd/",
        "chinese": "黑板", "type": "noun",
        "example_en": "The blackboard is black.",
        "example_cn": "黑板是黑色的。",
    },
    {
        "id": 16, "module": "上3", "word": "sit", "phonetic": "/sɪt/",
        "chinese": "坐", "type": "verb",
        "example_en": "Sit down, please.",
        "example_cn": "请坐下。",
    },
    {
        "id": 17, "module": "上3", "word": "down", "phonetic": "/daʊn/",
        "chinese": "向下", "type": "adv",
        "example_en": "Sit down.",
        "example_cn": "坐下。",
    },
    {
        "id": 18, "module": "上3", "word": "stand", "phonetic": "/stænd/",
        "chinese": "站", "type": "verb",
        "example_en": "Stand up, please.",
        "example_cn": "请站起来。",
    },
    {
        "id": 19, "module": "上3", "word": "up", "phonetic": "/ʌp/",
        "chinese": "向上", "type": "adv",
        "example_en": "Stand up.",
        "example_cn": "站起来。",
    },
    {
        "id": 20, "module": "上3", "word": "open", "phonetic": "/ˈəʊpən/",
        "chinese": "打开", "type": "verb",
        "example_en": "Open your book.",
        "example_cn": "打开你的书。",
    },
    {
        "id": 21, "module": "上3", "word": "close", "phonetic": "/kləʊz/",
        "chinese": "关上", "type": "verb",
        "example_en": "Close the window.",
        "example_cn": "关上窗户。",
    },
    {
        "id": 22, "module": "上3", "word": "see", "phonetic": "/siː/",
        "chinese": "看见", "type": "verb",
        "example_en": "See you!",
        "example_cn": "再见！",
    },

    # Module 4 - It's red!
    {
        "id": 23, "module": "上4", "word": "it", "phonetic": "/ɪt/",
        "chinese": "它", "type": "pronoun",
        "example_en": "It's a cat.",
        "example_cn": "它是一只猫。",
    },
    {
        "id": 24, "module": "上4", "word": "it's", "phonetic": "/ɪts/",
        "chinese": "它是 / 它有", "type": "abbr",
        "example_en": "It's red!",
        "example_cn": "它是红色的！",
    },
    {
        "id": 25, "module": "上4", "word": "red", "phonetic": "/red/",
        "chinese": "红色", "type": "color",
        "example_en": "The apple is red.",
        "example_cn": "苹果是红色的。",
    },
    {
        "id": 26, "module": "上4", "word": "blue", "phonetic": "/bluː/",
        "chinese": "蓝色", "type": "color",
        "example_en": "The sky is blue.",
        "example_cn": "天空是蓝色的。",
    },
    {
        "id": 27, "module": "上4", "word": "yellow", "phonetic": "/ˈjeləʊ/",
        "chinese": "黄色", "type": "color",
        "example_en": "The banana is yellow.",
        "example_cn": "香蕉是黄色的。",
    },
    {
        "id": 28, "module": "上4", "word": "green", "phonetic": "/ɡriːn/",
        "chinese": "绿色", "type": "color",
        "example_en": "The tree is green.",
        "example_cn": "树是绿色的。",
    },
    {
        "id": 29, "module": "上4", "word": "colour", "phonetic": "/ˈkʌlə(r)/",
        "chinese": "颜色（英）", "type": "noun",
        "example_en": "What colour is it?",
        "example_cn": "它是什么颜色？",
    },
    {
        "id": 30, "module": "上4", "word": "color", "phonetic": "/ˈkʌlər/",
        "chinese": "颜色（美）", "type": "noun",
        "example_en": "What color is it?",
        "example_cn": "它是什么颜色？",
    },

    # Module 5 - How many?
    {
        "id": 31, "module": "上5", "word": "one", "phonetic": "/wʌn/",
        "chinese": "一", "type": "number",
        "example_en": "One apple.",
        "example_cn": "一个苹果。",
    },
    {
        "id": 32, "module": "上5", "word": "two", "phonetic": "/tuː/",
        "chinese": "二", "type": "number",
        "example_en": "Two birds.",
        "example_cn": "两只鸟。",
    },
    {
        "id": 33, "module": "上5", "word": "three", "phonetic": "/θriː/",
        "chinese": "三", "type": "number",
        "example_en": "Three cats.",
        "example_cn": "三只猫。",
    },
    {
        "id": 34, "module": "上5", "word": "four", "phonetic": "/fɔː(r)/",
        "chinese": "四", "type": "number",
        "example_en": "Four dogs.",
        "example_cn": "四只狗。",
    },
    {
        "id": 35, "module": "上5", "word": "five", "phonetic": "/faɪv/",
        "chinese": "五", "type": "number",
        "example_en": "Five books.",
        "example_cn": "五本书。",
    },
    {
        "id": 36, "module": "上5", "word": "six", "phonetic": "/sɪks/",
        "chinese": "六", "type": "number",
        "example_en": "Six pens.",
        "example_cn": "六支笔。",
    },
    {
        "id": 37, "module": "上5", "word": "seven", "phonetic": "/ˈsevn/",
        "chinese": "七", "type": "number",
        "example_en": "Seven oranges.",
        "example_cn": "七个橙子。",
    },
    {
        "id": 38, "module": "上5", "word": "eight", "phonetic": "/eɪt/",
        "chinese": "八", "type": "number",
        "example_en": "Eight birds.",
        "example_cn": "八只鸟。",
    },
    {
        "id": 39, "module": "上5", "word": "nine", "phonetic": "/naɪn/",
        "chinese": "九", "type": "number",
        "example_en": "Nine books.",
        "example_cn": "九本书。",
    },
    {
        "id": 40, "module": "上5", "word": "ten", "phonetic": "/ten/",
        "chinese": "十", "type": "number",
        "example_en": "Ten students.",
        "example_cn": "十个学生。",
    },
    {
        "id": 41, "module": "上5", "word": "how many", "phonetic": "/haʊ ˈmeni/",
        "chinese": "多少", "type": "phrase",
        "example_en": "How many books?",
        "example_cn": "有多少本书？",
    },
    {
        "id": 42, "module": "上5", "word": "pencil", "phonetic": "/ˈpensl/",
        "chinese": "铅笔", "type": "noun",
        "example_en": "This is a pencil.",
        "example_cn": "这是一支铅笔。",
    },
    {
        "id": 43, "module": "上5", "word": "pen", "phonetic": "/pen/",
        "chinese": "钢笔", "type": "noun",
        "example_en": "This is a pen.",
        "example_cn": "这是一支钢笔。",
    },
    {
        "id": 44, "module": "上5", "word": "book", "phonetic": "/bʊk/",
        "chinese": "书", "type": "noun",
        "example_en": "Open your book.",
        "example_cn": "打开你的书。",
    },
    {
        "id": 45, "module": "上5", "word": "bag", "phonetic": "/bæɡ/",
        "chinese": "包", "type": "noun",
        "example_en": "My bag is blue.",
        "example_cn": "我的包是蓝色的。",
    },

    # Module 6 - Happy birthday!
    {
        "id": 46, "module": "上6", "word": "happy", "phonetic": "/ˈhæpi/",
        "chinese": "快乐的", "type": "adj",
        "example_en": "Happy birthday!",
        "example_cn": "生日快乐！",
    },
    {
        "id": 47, "module": "上6", "word": "birthday", "phonetic": "/ˈbɜːθdeɪ/",
        "chinese": "生日", "type": "noun",
        "example_en": "Happy birthday to you!",
        "example_cn": "祝你生日快乐！",
    },
    {
        "id": 48, "module": "上6", "word": "eleven", "phonetic": "/ɪˈlevn/",
        "chinese": "十一", "type": "number",
        "example_en": "I'm eleven.",
        "example_cn": "我十一岁。",
    },
    {
        "id": 49, "module": "上6", "word": "twelve", "phonetic": "/twelv/",
        "chinese": "十二", "type": "number",
        "example_en": "I'm twelve.",
        "example_cn": "我十二岁。",
    },
    {
        "id": 50, "module": "上6", "word": "thirteen", "phonetic": "/ˌθɜːˈtiːn/",
        "chinese": "十三", "type": "number",
        "example_en": "I'm thirteen years old.",
        "example_cn": "我十三岁。",
    },
    {
        "id": 51, "module": "上6", "word": "fourteen", "phonetic": "/ˌfɔːˈtiːn/",
        "chinese": "十四", "type": "number",
        "example_en": "I'm fourteen.",
        "example_cn": "我十四岁。",
    },
    {
        "id": 52, "module": "上6", "word": "fifteen", "phonetic": "/ˌfɪfˈtiːn/",
        "chinese": "十五", "type": "number",
        "example_en": "I'm fifteen.",
        "example_cn": "我十五岁。",
    },
    {
        "id": 53, "module": "上6", "word": "sixteen", "phonetic": "/ˌsɪksˈtiːn/",
        "chinese": "十六", "type": "number",
        "example_en": "I'm sixteen.",
        "example_cn": "我十六岁。",
    },
    {
        "id": 54, "module": "上6", "word": "seventeen", "phonetic": "/ˌsevnˈtiːn/",
        "chinese": "十七", "type": "number",
        "example_en": "I'm seventeen.",
        "example_cn": "我十七岁。",
    },
    {
        "id": 55, "module": "上6", "word": "eighteen", "phonetic": "/ˌeɪˈtiːn/",
        "chinese": "十八", "type": "number",
        "example_en": "I'm eighteen.",
        "example_cn": "我十八岁。",
    },
    {
        "id": 56, "module": "上6", "word": "nineteen", "phonetic": "/ˌnaɪnˈtiːn/",
        "chinese": "十九", "type": "number",
        "example_en": "I'm nineteen.",
        "example_cn": "我十九岁。",
    },
    {
        "id": 57, "module": "上6", "word": "twenty", "phonetic": "/ˈtwenti/",
        "chinese": "二十", "type": "number",
        "example_en": "I'm twenty.",
        "example_cn": "我二十岁。",
    },
    {
        "id": 58, "module": "上6", "word": "brother", "phonetic": "/ˈbrʌðə(r)/",
        "chinese": "兄弟", "type": "family",
        "example_en": "This is my brother.",
        "example_cn": "这是我的兄弟。",
    },

    # Module 7 - What's this?
    {
        "id": 59, "module": "上7", "word": "what's", "phonetic": "/wɒts/",
        "chinese": "什么（what is）", "type": "abbr",
        "example_en": "What's this?",
        "example_cn": "这是什么？",
    },
    {
        "id": 60, "module": "上7", "word": "what", "phonetic": "/wɒt/",
        "chinese": "什么", "type": "pronoun",
        "example_en": "What is your name?",
        "example_cn": "你叫什么名字？",
    },
    {
        "id": 61, "module": "上7", "word": "is", "phonetic": "/ɪz/",
        "chinese": "是", "type": "verb",
        "example_en": "It is a bird.",
        "example_cn": "它是一只鸟。",
    },
    {
        "id": 62, "module": "上7", "word": "this", "phonetic": "/ðɪs/",
        "chinese": "这", "type": "pronoun",
        "example_en": "This is a book.",
        "example_cn": "这是一本书。",
    },
    {
        "id": 63, "module": "上7", "word": "in", "phonetic": "/ɪn/",
        "chinese": "在...里面", "type": "prep",
        "example_en": "What's in the box?",
        "example_cn": "盒子里是什么？",
    },
    {
        "id": 64, "module": "上7", "word": "bird", "phonetic": "/bɜːd/",
        "chinese": "鸟", "type": "animal",
        "example_en": "It's a bird.",
        "example_cn": "它是一只鸟。",
    },
    {
        "id": 65, "module": "上7", "word": "tiger", "phonetic": "/ˈtaɪɡə(r)/",
        "chinese": "老虎", "type": "animal",
        "example_en": "The tiger is big.",
        "example_cn": "老虎很大。",
    },
    {
        "id": 66, "module": "上7", "word": "monkey", "phonetic": "/ˈmʌŋki/",
        "chinese": "猴子", "type": "animal",
        "example_en": "The monkey is clever.",
        "example_cn": "猴子很聪明。",
    },
    {
        "id": 67, "module": "上7", "word": "lion", "phonetic": "/ˈlaɪən/",
        "chinese": "狮子", "type": "animal",
        "example_en": "The lion is strong.",
        "example_cn": "狮子很强壮。",
    },
    {
        "id": 68, "module": "上7", "word": "cat", "phonetic": "/kæt/",
        "chinese": "猫", "type": "animal",
        "example_en": "The cat is cute.",
        "example_cn": "猫很可爱。",
    },
    {
        "id": 69, "module": "上7", "word": "dog", "phonetic": "/dɒɡ/",
        "chinese": "狗", "type": "animal",
        "example_en": "The dog is lovely.",
        "example_cn": "狗很可爱。",
    },
    {
        "id": 70, "module": "上7", "word": "zoo", "phonetic": "/zuː/",
        "chinese": "动物园", "type": "place",
        "example_en": "Let's go to the zoo!",
        "example_cn": "我们去动物园吧！",
    },

    # Module 8 - It's a boy.
    {
        "id": 71, "module": "上8", "word": "that", "phonetic": "/ðæt/",
        "chinese": "那", "type": "pronoun",
        "example_en": "That is my father.",
        "example_cn": "那是我的爸爸。",
    },
    {
        "id": 72, "module": "上8", "word": "boy", "phonetic": "/bɔɪ/",
        "chinese": "男孩", "type": "noun",
        "example_en": "This is a boy.",
        "example_cn": "这是一个男孩。",
    },
    {
        "id": 73, "module": "上8", "word": "girl", "phonetic": "/ɡɜːl/",
        "chinese": "女孩", "type": "noun",
        "example_en": "She is a girl.",
        "example_cn": "她是一个女孩。",
    },
    {
        "id": 74, "module": "上8", "word": "father", "phonetic": "/ˈfɑːðə(r)/",
        "chinese": "父亲/爸爸", "type": "family",
        "example_en": "This is my father.",
        "example_cn": "这是我的父亲。",
    },
    {
        "id": 75, "module": "上8", "word": "mother", "phonetic": "/ˈmʌðə(r)/",
        "chinese": "母亲/妈妈", "type": "family",
        "example_en": "This is my mother.",
        "example_cn": "这是我的母亲。",
    },
    {
        "id": 76, "module": "上8", "word": "sister", "phonetic": "/ˈsɪstə(r)/",
        "chinese": "姐妹", "type": "family",
        "example_en": "She is my sister.",
        "example_cn": "她是我的姐妹。",
    },
    {
        "id": 77, "module": "上8", "word": "teacher", "phonetic": "/ˈtiːtʃə(r)/",
        "chinese": "老师", "type": "job",
        "example_en": "Ms Smart is a teacher.",
        "example_cn": "Smart 女士是一位老师。",
    },
    {
        "id": 78, "module": "上8", "word": "school", "phonetic": "/skuːl/",
        "chinese": "学校", "type": "place",
        "example_en": "I go to school.",
        "example_cn": "我去学校。",
    },
    {
        "id": 79, "module": "上8", "word": "pupil", "phonetic": "/ˈpjuːpl/",
        "chinese": "小学生", "type": "noun",
        "example_en": "I'm a pupil.",
        "example_cn": "我是一名小学生。",
    },
    {
        "id": 80, "module": "上8", "word": "class", "phonetic": "/klɑːs/",
        "chinese": "班级", "type": "noun",
        "example_en": "We're in Class 1.",
        "example_cn": "我们在一班。",
    },

    # Module 9 - This is my mother.
    {
        "id": 81, "module": "上9", "word": "my", "phonetic": "/maɪ/",
        "chinese": "我的", "type": "pronoun",
        "example_en": "This is my mother.",
        "example_cn": "这是我的妈妈。",
    },
    {
        "id": 82, "module": "上9", "word": "your", "phonetic": "/jɔː(r)/",
        "chinese": "你的", "type": "pronoun",
        "example_en": "What's your name?",
        "example_cn": "你叫什么名字？",
    },
    {
        "id": 83, "module": "上9", "word": "grandpa", "phonetic": "/ˈɡrænpɑː/",
        "chinese": "爷爷/外公", "type": "family",
        "example_en": "This is my grandpa.",
        "example_cn": "这是我的爷爷。",
    },
    {
        "id": 84, "module": "上9", "word": "grandma", "phonetic": "/ˈɡrænmɑː/",
        "chinese": "奶奶/外婆", "type": "family",
        "example_en": "This is my grandma.",
        "example_cn": "这是我的奶奶。",
    },
    {
        "id": 85, "module": "上9", "word": "family", "phonetic": "/ˈfæməli/",
        "chinese": "家庭", "type": "noun",
        "example_en": "This is my family.",
        "example_cn": "这是我的家庭。",
    },
    {
        "id": 86, "module": "上9", "word": "photo", "phonetic": "/ˈfəʊtəʊ/",
        "chinese": "照片", "type": "noun",
        "example_en": "This is a photo of my family.",
        "example_cn": "这是一张我的全家福。",
    },
    {
        "id": 87, "module": "上9", "word": "there", "phonetic": "/ðeə(r)/",
        "chinese": "那里", "type": "adv",
        "example_en": "There is a photo.",
        "example_cn": "那里有一张照片。",
    },
    {
        "id": 88, "module": "上9", "word": "there is", "phonetic": "/ðeər ɪz/",
        "chinese": "有（单数）", "type": "phrase",
        "example_en": "There is a book on the desk.",
        "example_cn": "桌上有一本书。",
    },

    # Module 10 - That is my father.
    {
        "id": 89, "module": "上10", "word": "his", "phonetic": "/hɪz/",
        "chinese": "他的", "type": "pronoun",
        "example_en": "This is his book.",
        "example_cn": "这是他的书。",
    },
    {
        "id": 90, "module": "上10", "word": "her", "phonetic": "/hɜː(r)/",
        "chinese": "她的", "type": "pronoun",
        "example_en": "This is her bag.",
        "example_cn": "这是她的包。",
    },
    {
        "id": 91, "module": "上10", "word": "doctor", "phonetic": "/ˈdɒktə(r)/",
        "chinese": "医生", "type": "job",
        "example_en": "My mother is a doctor.",
        "example_cn": "我的妈妈是一名医生。",
    },
    {
        "id": 92, "module": "上10", "word": "nurse", "phonetic": "/nɜːs/",
        "chinese": "护士", "type": "job",
        "example_en": "She is a nurse.",
        "example_cn": "她是一名护士。",
    },
    {
        "id": 93, "module": "上10", "word": "driver", "phonetic": "/ˈdraɪvə(r)/",
        "chinese": "司机", "type": "job",
        "example_en": "My father is a driver.",
        "example_cn": "我的爸爸是一名司机。",
    },
    {
        "id": 94, "module": "上10", "word": "farmer", "phonetic": "/ˈfɑːmə(r)/",
        "chinese": "农民", "type": "job",
        "example_en": "He is a farmer.",
        "example_cn": "他是一名农民。",
    },
    {
        "id": 95, "module": "上10", "word": "he", "phonetic": "/hiː/",
        "chinese": "他", "type": "pronoun",
        "example_en": "He is my father.",
        "example_cn": "他是我的爸爸。",
    },
    {
        "id": 96, "module": "上10", "word": "she", "phonetic": "/ʃiː/",
        "chinese": "她", "type": "pronoun",
        "example_en": "She is my mother.",
        "example_cn": "她是我的妈妈。",
    },

    # ===================== 下册 =====================
    # Module 1 - She's a doctor.
    {
        "id": 97, "module": "下1", "word": "she's", "phonetic": "/ʃiːz/",
        "chinese": "她是 / 她有", "type": "abbr",
        "example_en": "She's a doctor.",
        "example_cn": "她是一名医生。",
    },
    {
        "id": 98, "module": "下1", "word": "he", "phonetic": "/hiː/",
        "chinese": "他", "type": "pronoun",
        "example_en": "He's a farmer.",
        "example_cn": "他是一名农民。",
    },
    {
        "id": 99, "module": "下1", "word": "he's", "phonetic": "/hiːz/",
        "chinese": "他是 / 他有", "type": "abbr",
        "example_en": "He's a driver.",
        "example_cn": "他是一名司机。",
    },
    {
        "id": 100, "module": "下1", "word": "police", "phonetic": "/pəˈliːs/",
        "chinese": "警察", "type": "job",
        "example_en": "He's a police officer.",
        "example_cn": "他是一名警察。",
    },

    # Module 2 - That man is tall.
    {
        "id": 101, "module": "下2", "word": "tall", "phonetic": "/tɔːl/",
        "chinese": "高的", "type": "adj",
        "example_en": "He is tall.",
        "example_cn": "他很高。",
    },
    {
        "id": 102, "module": "下2", "word": "short", "phonetic": "/ʃɔːt/",
        "chinese": "矮的 / 短的", "type": "adj",
        "example_en": "He is short.",
        "example_cn": "他很矮。",
    },
    {
        "id": 103, "module": "下2", "word": "big", "phonetic": "/bɪɡ/",
        "chinese": "大的", "type": "adj",
        "example_en": "The elephant is big.",
        "example_cn": "大象很大。",
    },
    {
        "id": 104, "module": "下2", "word": "small", "phonetic": "/smɔːl/",
        "chinese": "小的", "type": "adj",
        "example_en": "The mouse is small.",
        "example_cn": "老鼠很小。",
    },
    {
        "id": 105, "module": "下2", "word": "thin", "phonetic": "/θɪn/",
        "chinese": "瘦的", "type": "adj",
        "example_en": "He is thin.",
        "example_cn": "他很瘦。",
    },
    {
        "id": 106, "module": "下2", "word": "fat", "phonetic": "/fæt/",
        "chinese": "胖的", "type": "adj",
        "example_en": "The pig is fat.",
        "example_cn": "猪很胖。",
    },
    {
        "id": 107, "module": "下2", "word": "strong", "phonetic": "/strɒŋ/",
        "chinese": "强壮的", "type": "adj",
        "example_en": "He is strong.",
        "example_cn": "他很强壮。",
    },
    {
        "id": 108, "module": "下2", "word": "man", "phonetic": "/mæn/",
        "chinese": "男人", "type": "noun",
        "example_en": "That man is tall.",
        "example_cn": "那个男人很高。",
    },
    {
        "id": 109, "module": "下2", "word": "woman", "phonetic": "/ˈwʊmən/",
        "chinese": "女人", "type": "noun",
        "example_en": "That woman is short.",
        "example_cn": "那个女人很矮。",
    },
    {
        "id": 110, "module": "下2", "word": "giant", "phonetic": "/ˈdʒaɪənt/",
        "chinese": "巨人", "type": "noun",
        "example_en": "The giant is very tall.",
        "example_cn": "巨人非常高。",
    },
    {
        "id": 111, "module": "下2", "word": "clever", "phonetic": "/ˈklevə(r)/",
        "chinese": "聪明的", "type": "adj",
        "example_en": "The monkey is clever.",
        "example_cn": "猴子很聪明。",
    },
    {
        "id": 112, "module": "下2", "word": "naughty", "phonetic": "/ˈnɔːti/",
        "chinese": "调皮的", "type": "adj",
        "example_en": "The boy is naughty.",
        "example_cn": "男孩很调皮。",
    },
    {
        "id": 113, "module": "下2", "word": "kind", "phonetic": "/kaɪnd/",
        "chinese": "善良的", "type": "adj",
        "example_en": "She is kind.",
        "example_cn": "她很善良。",
    },

    # Module 3 - I like football.
    {
        "id": 114, "module": "下3", "word": "like", "phonetic": "/laɪk/",
        "chinese": "喜欢", "type": "verb",
        "example_en": "I like football.",
        "example_cn": "我喜欢足球。",
    },
    {
        "id": 115, "module": "下3", "word": "football", "phonetic": "/ˈfʊtbɔːl/",
        "chinese": "足球", "type": "sport",
        "example_en": "I like football.",
        "example_cn": "我喜欢足球。",
    },
    {
        "id": 116, "module": "下3", "word": "piano", "phonetic": "/piˈænəʊ/",
        "chinese": "钢琴", "type": "hobby",
        "example_en": "I like the piano.",
        "example_cn": "我喜欢钢琴。",
    },
    {
        "id": 117, "module": "下3", "word": "swimming", "phonetic": "/ˈswɪmɪŋ/",
        "chinese": "游泳", "type": "sport",
        "example_en": "I like swimming.",
        "example_cn": "我喜欢游泳。",
    },
    {
        "id": 118, "module": "下3", "word": "riding", "phonetic": "/ˈraɪdɪŋ/",
        "chinese": "骑自行车", "type": "sport",
        "example_en": "I like bike riding.",
        "example_cn": "我喜欢骑自行车。",
    },
    {
        "id": 119, "module": "下3", "word": "skipping", "phonetic": "/ˈskɪpɪŋ/",
        "chinese": "跳绳", "type": "sport",
        "example_en": "I like skipping.",
        "example_cn": "我喜欢跳绳。",
    },

    # Module 4 - He likes football.
    {
        "id": 120, "module": "下4", "word": "he", "phonetic": "/hiː/",
        "chinese": "他", "type": "pronoun",
        "example_en": "He likes football.",
        "example_cn": "他喜欢足球。",
    },
    {
        "id": 121, "module": "下4", "word": "she", "phonetic": "/ʃiː/",
        "chinese": "她", "type": "pronoun",
        "example_en": "She likes swimming.",
        "example_cn": "她喜欢游泳。",
    },
    {
        "id": 122, "module": "下4", "word": "likes", "phonetic": "/laɪks/",
        "chinese": "喜欢（第三人称单数）", "type": "verb",
        "example_en": "He likes football.",
        "example_cn": "他喜欢足球。",
    },
    {
        "id": 123, "module": "下4", "word": "him", "phonetic": "/hɪm/",
        "chinese": "他（宾格）", "type": "pronoun",
        "example_en": "I like him.",
        "example_cn": "我喜欢他。",
    },
    {
        "id": 124, "module": "下4", "word": "her", "phonetic": "/hɜː(r)/",
        "chinese": "她（宾格）", "type": "pronoun",
        "example_en": "I like her.",
        "example_cn": "我喜欢她。",
    },
    {
        "id": 125, "module": "下4", "word": "does", "phonetic": "/dʌz/",
        "chinese": "做（第三人称单数）", "type": "verb",
        "example_en": "He does not (doesn't) like it.",
        "example_cn": "他不喜欢它。",
    },

    # Module 5 - Amy has short hair.
    {
        "id": 126, "module": "下5", "word": "has", "phonetic": "/hæz/",
        "chinese": "有（第三人称单数）", "type": "verb",
        "example_en": "Amy has short hair.",
        "example_cn": "Amy 留着短发。",
    },
    {
        "id": 127, "module": "下5", "word": "long", "phonetic": "/lɒŋ/",
        "chinese": "长的", "type": "adj",
        "example_en": "She has long hair.",
        "example_cn": "她有长发。",
    },
    {
        "id": 128, "module": "下5", "word": "hair", "phonetic": "/heə(r)/",
        "chinese": "头发", "type": "body",
        "example_en": "She has long hair.",
        "example_cn": "她有长发。",
    },
    {
        "id": 129, "module": "下5", "word": "head", "phonetic": "/hed/",
        "chinese": "头", "type": "body",
        "example_en": "The head is round.",
        "example_cn": "头是圆的。",
    },
    {
        "id": 130, "module": "下5", "word": "eye", "phonetic": "/aɪ/",
        "chinese": "眼睛", "type": "body",
        "example_en": "I have two eyes.",
        "example_cn": "我有两只眼睛。",
    },
    {
        "id": 131, "module": "下5", "word": "nose", "phonetic": "/nəʊz/",
        "chinese": "鼻子", "type": "body",
        "example_en": "I have a small nose.",
        "example_cn": "我有一个小鼻子。",
    },
    {
        "id": 132, "module": "下5", "word": "mouth", "phonetic": "/maʊθ/",
        "chinese": "嘴巴", "type": "body",
        "example_en": "Open your mouth.",
        "example_cn": "张开你的嘴巴。",
    },
    {
        "id": 133, "module": "下5", "word": "ear", "phonetic": "/ɪə(r)/",
        "chinese": "耳朵", "type": "body",
        "example_en": "I have two ears.",
        "example_cn": "我有两只耳朵。",
    },
    {
        "id": 134, "module": "下5", "word": "face", "phonetic": "/feɪs/",
        "chinese": "脸", "type": "body",
        "example_en": "I have a round face.",
        "example_cn": "我有一张圆脸。",
    },

    # Module 6 - Then we can go.
    {
        "id": 135, "module": "下6", "word": "can", "phonetic": "/kæn/",
        "chinese": "会 / 能", "type": "modal",
        "example_en": "I can swim.",
        "example_cn": "我会游泳。",
    },
    {
        "id": 136, "module": "下6", "word": "can't", "phonetic": "/kɑːnt/",
        "chinese": "不会 / 不能", "type": "modal",
        "example_en": "I can't fly.",
        "example_cn": "我不会飞。",
    },
    {
        "id": 137, "module": "下6", "word": "we", "phonetic": "/wiː/",
        "chinese": "我们", "type": "pronoun",
        "example_en": "We can go.",
        "example_cn": "我们能走了。",
    },
    {
        "id": 138, "module": "下6", "word": "run", "phonetic": "/rʌn/",
        "chinese": "跑", "type": "verb",
        "example_en": "I can run fast.",
        "example_cn": "我会跑步。",
    },
    {
        "id": 139, "module": "下6", "word": "jump", "phonetic": "/dʒʌmp/",
        "chinese": "跳", "type": "verb",
        "example_en": "I can jump high.",
        "example_cn": "我能跳得很高。",
    },
    {
        "id": 140, "module": "下6", "word": "fast", "phonetic": "/fɑːst/",
        "chinese": "快地", "type": "adv",
        "example_en": "He runs fast.",
        "example_cn": "他跑得很快。",
    },
    {
        "id": 141, "module": "下6", "word": "high", "phonetic": "/haɪ/",
        "chinese": "高地", "type": "adv",
        "example_en": "He can jump high.",
        "example_cn": "他能跳得很高。",
    },
    {
        "id": 142, "module": "下6", "word": "slow", "phonetic": "/sləʊ/",
        "chinese": "慢的", "type": "adj",
        "example_en": "The tortoise is slow.",
        "example_cn": "乌龟很慢。",
    },
    {
        "id": 143, "module": "下6", "word": "slowly", "phonetic": "/ˈsləʊli/",
        "chinese": "慢地", "type": "adv",
        "example_en": "He walks slowly.",
        "example_cn": "他走得很慢。",
    },

    # Module 7 - Robots can talk.
    {
        "id": 144, "module": "下7", "word": "robot", "phonetic": "/ˈrəʊbɒt/",
        "chinese": "机器人", "type": "noun",
        "example_en": "Robots can talk.",
        "example_cn": "机器人会说话。",
    },
    {
        "id": 145, "module": "下7", "word": "talk", "phonetic": "/tɔːk/",
        "chinese": "说话", "type": "verb",
        "example_en": "We can talk.",
        "example_cn": "我们会说话。",
    },
    {
        "id": 146, "module": "下7", "word": "sing", "phonetic": "/sɪŋ/",
        "chinese": "唱歌", "type": "verb",
        "example_en": "She can sing.",
        "example_cn": "她会唱歌。",
    },
    {
        "id": 147, "module": "下7", "word": "dance", "phonetic": "/dɑːns/",
        "chinese": "跳舞", "type": "verb",
        "example_en": "He can dance.",
        "example_cn": "他会跳舞。",
    },
    {
        "id": 148, "module": "下7", "word": "play", "phonetic": "/pleɪ/",
        "chinese": "玩 / 播放", "type": "verb",
        "example_en": "We can play games.",
        "example_cn": "我们会玩游戏。",
    },
    {
        "id": 149, "module": "下7", "word": "game", "phonetic": "/ɡeɪm/",
        "chinese": "游戏", "type": "noun",
        "example_en": "Let's play a game!",
        "example_cn": "我们玩游戏吧！",
    },
    {
        "id": 150, "module": "下7", "word": "these", "phonetic": "/ðiːz/",
        "chinese": "这些", "type": "pronoun",
        "example_en": "These are robots.",
        "example_cn": "这些是机器人。",
    },
    {
        "id": 151, "module": "下7", "word": "those", "phonetic": "/ðəʊz/",
        "chinese": "那些", "type": "pronoun",
        "example_en": "Those are birds.",
        "example_cn": "那些是鸟。",
    },
    {
        "id": 152, "module": "下7", "word": "write", "phonetic": "/raɪt/",
        "chinese": "写", "type": "verb",
        "example_en": "I can write.",
        "example_cn": "我会写字。",
    },
    {
        "id": 153, "module": "下7", "word": "read", "phonetic": "/riːd/",
        "chinese": "读", "type": "verb",
        "example_en": "I can read.",
        "example_cn": "我会读书。",
    },
    {
        "id": 154, "module": "下7", "word": "draw", "phonetic": "/drɔː/",
        "chinese": "画", "type": "verb",
        "example_en": "I can draw.",
        "example_cn": "我会画画。",
    },

    # Module 8 - There are two butterflies.
    {
        "id": 155, "module": "下8", "word": "there are", "phonetic": "/ðeər ɑː(r)/",
        "chinese": "有（复数）", "type": "phrase",
        "example_en": "There are two butterflies.",
        "example_cn": "有两只蝴蝶。",
    },
    {
        "id": 156, "module": "下8", "word": "butterfly", "phonetic": "/ˈbʌtəflaɪ/",
        "chinese": "蝴蝶", "type": "animal",
        "example_en": "The butterfly is beautiful.",
        "example_cn": "蝴蝶很美丽。",
    },
    {
        "id": 157, "module": "下8", "word": "insect", "phonetic": "/ˈɪnsekt/",
        "chinese": "昆虫", "type": "animal",
        "example_en": "A butterfly is an insect.",
        "example_cn": "蝴蝶是一种昆虫。",
    },
    {
        "id": 158, "module": "下8", "word": "dragonfly", "phonetic": "/ˈdræɡənflaɪ/",
        "chinese": "蜻蜓", "type": "animal",
        "example_en": "A dragonfly has big eyes.",
        "example_cn": "蜻蜓有大眼睛。",
    },
    {
        "id": 159, "module": "下8", "word": "bee", "phonetic": "/biː/",
        "chinese": "蜜蜂", "type": "animal",
        "example_en": "The bee can fly.",
        "example_cn": "蜜蜂会飞。",
    },
    {
        "id": 160, "module": "下8", "word": "ant", "phonetic": "/ænt/",
        "chinese": "蚂蚁", "type": "animal",
        "example_en": "The ant is small.",
        "example_cn": "蚂蚁很小。",
    },
    {
        "id": 161, "module": "下8", "word": "some", "phonetic": "/sʌm/",
        "chinese": "一些", "type": "adj",
        "example_en": "There are some apples.",
        "example_cn": "有一些苹果。",
    },
    {
        "id": 162, "module": "下8", "word": "animal", "phonetic": "/ˈænɪml/",
        "chinese": "动物", "type": "noun",
        "example_en": "What animal is this?",
        "example_cn": "这是什么动物？",
    },

    # Module 9 - I've got a headache.
    {
        "id": 163, "module": "下9", "word": "headache", "phonetic": "/ˈhedeɪk/",
        "chinese": "头疼", "type": "health",
        "example_en": "I've got a headache.",
        "example_cn": "我头疼。",
    },
    {
        "id": 164, "module": "下9", "word": "stomachache", "phonetic": "/ˈstʌməkeɪk/",
        "chinese": "胃疼", "type": "health",
        "example_en": "I've got a stomachache.",
        "example_cn": "我胃疼。",
    },
    {
        "id": 165, "module": "下9", "word": "toothache", "phonetic": "/ˈtuːθeɪk/",
        "chinese": "牙疼", "type": "health",
        "example_en": "I've got a toothache.",
        "example_cn": "我牙疼。",
    },
    {
        "id": 166, "module": "下9", "word": "fever", "phonetic": "/ˈfiːvə(r)/",
        "chinese": "发烧", "type": "health",
        "example_en": "I've got a fever.",
        "example_cn": "我发烧了。",
    },
    {
        "id": 167, "module": "下9", "word": "cold", "phonetic": "/kəʊld/",
        "chinese": "感冒", "type": "health",
        "example_en": "I've got a cold.",
        "example_cn": "我感冒了。",
    },
    {
        "id": 168, "module": "下9", "word": "have got", "phonetic": "/hæv ɡɒt/",
        "chinese": "有（口语）", "type": "phrase",
        "example_en": "I've got a headache.",
        "example_cn": "我头疼。",
    },
    {
        "id": 169, "module": "下9", "word": "arm", "phonetic": "/ɑːm/",
        "chinese": "胳膊", "type": "body",
        "example_en": "I hurt my arm.",
        "example_cn": "我伤了胳膊。",
    },
    {
        "id": 170, "module": "下9", "word": "hand", "phonetic": "/hænd/",
        "chinese": "手", "type": "body",
        "example_en": "Wash your hands.",
        "example_cn": "洗你的手。",
    },
    {
        "id": 171, "module": "下9", "word": "leg", "phonetic": "/leɡ/",
        "chinese": "腿", "type": "body",
        "example_en": "I hurt my leg.",
        "example_cn": "我伤了腿。",
    },
    {
        "id": 172, "module": "下9", "word": "foot", "phonetic": "/fʊt/",
        "chinese": "脚（单数）", "type": "body",
        "example_en": "I hurt my foot.",
        "example_cn": "我伤了脚。",
    },
    {
        "id": 173, "module": "下9", "word": "feet", "phonetic": "/fiːt/",
        "chinese": "脚（复数）", "type": "body",
        "example_en": "I hurt my feet.",
        "example_cn": "我伤了脚。",
    },

    # Module 10 - Then I'll carry it.
    {
        "id": 174, "module": "下10", "word": "I'll", "phonetic": "/aɪl/",
        "chinese": "我将（I will）", "type": "abbr",
        "example_en": "I'll carry it.",
        "example_cn": "我来拿它。",
    },
    {
        "id": 175, "module": "下10", "word": "will", "phonetic": "/wɪl/",
        "chinese": "将要", "type": "modal",
        "example_en": "It will rain tomorrow.",
        "example_cn": "明天会下雨。",
    },
    {
        "id": 176, "module": "下10", "word": "carry", "phonetic": "/ˈkæri/",
        "chinese": "拿", "type": "verb",
        "example_en": "I'll carry the bag.",
        "example_cn": "我来拿这个包。",
    },
    {
        "id": 177, "module": "下10", "word": "back", "phonetic": "/bæk/",
        "chinese": "背 / 后面", "type": "noun",
        "example_en": "I'll carry your bag back home.",
        "example_cn": "我帮你把包拿回家。",
    },
    {
        "id": 178, "module": "下10", "word": "home", "phonetic": "/həʊm/",
        "chinese": "家", "type": "noun",
        "example_en": "Let's go home.",
        "example_cn": "我们回家吧。",
    },
    {
        "id": 179, "module": "下10", "word": "tomorrow", "phonetic": "/təˈmɒrəʊ/",
        "chinese": "明天", "type": "time",
        "example_en": "Tomorrow is Monday.",
        "example_cn": "明天是星期一。",
    },
    {
        "id": 180, "module": "下10", "word": "Monday", "phonetic": "/ˈmʌndeɪ/",
        "chinese": "星期一", "type": "day",
        "example_en": "Tomorrow is Monday.",
        "example_cn": "明天是星期一。",
    },
    {
        "id": 181, "module": "下10", "word": "Tuesday", "phonetic": "/ˈtjuːzdeɪ/",
        "chinese": "星期二", "type": "day",
        "example_en": "Today is Tuesday.",
        "example_cn": "今天是星期二。",
    },
    {
        "id": 182, "module": "下10", "word": "Wednesday", "phonetic": "/ˈwenzdeɪ/",
        "chinese": "星期三", "type": "day",
        "example_en": "Today is Wednesday.",
        "example_cn": "今天是星期三。",
    },
    {
        "id": 183, "module": "下10", "word": "Thursday", "phonetic": "/ˈθɜːzdeɪ/",
        "chinese": "星期四", "type": "day",
        "example_en": "Today is Thursday.",
        "example_cn": "今天是星期四。",
    },
    {
        "id": 184, "module": "下10", "word": "Friday", "phonetic": "/ˈfraɪdeɪ/",
        "chinese": "星期五", "type": "day",
        "example_en": "Today is Friday.",
        "example_cn": "今天是星期五。",
    },
    {
        "id": 185, "module": "下10", "word": "Saturday", "phonetic": "/ˈsætədeɪ/",
        "chinese": "星期六", "type": "day",
        "example_en": "Today is Saturday.",
        "example_cn": "今天是星期六。",
    },
    {
        "id": 186, "module": "下10", "word": "Sunday", "phonetic": "/ˈsʌndeɪ/",
        "chinese": "星期日", "type": "day",
        "example_en": "Today is Sunday.",
        "example_cn": "今天是星期日。",
    },
    {
        "id": 187, "module": "下10", "word": "today", "phonetic": "/təˈdeɪ/",
        "chinese": "今天", "type": "time",
        "example_en": "Today is Monday.",
        "example_cn": "今天是星期一。",
    },
    {
        "id": 188, "module": "下10", "word": "weekend", "phonetic": "/ˌwiːkˈend/",
        "chinese": "周末", "type": "time",
        "example_en": "What do you do at the weekend?",
        "example_cn": "你周末做什么？",
    },
    {
        "id": 189, "module": "下10", "word": "next", "phonetic": "/nekst/",
        "chinese": "下一个", "type": "adj",
        "example_en": "Next week.",
        "example_cn": "下周。",
    },
    {
        "id": 190, "module": "下10", "word": "learn", "phonetic": "/lɜːn/",
        "chinese": "学习", "type": "verb",
        "example_en": "I learn English.",
        "example_cn": "我学英语。",
    },
    {
        "id": 191, "module": "下10", "word": "study", "phonetic": "/ˈstʌdi/",
        "chinese": "学习", "type": "verb",
        "example_en": "I study English every day.",
        "example_cn": "我每天学英语。",
    },
    {
        "id": 192, "module": "下10", "word": "again", "phonetic": "/əˈɡen/",
        "chinese": "再", "type": "adv",
        "example_en": "See you again!",
        "example_cn": "再见！",
    },
]


def get_words_by_module(module_name):
    """按模块筛选"""
    return [w for w in WORDS if w["module"] == module_name]


def search_words(keyword):
    """搜索单词"""
    kw = keyword.lower()
    return [w for w in WORDS
            if kw in w["word"].lower()
            or kw in w["chinese"]
            or kw in w["example_en"].lower()]


def get_all_modules():
    """获取所有模块列表"""
    modules = []
    for w in WORDS:
        if w["module"] not in modules:
            modules.append(w["module"])
    return modules
