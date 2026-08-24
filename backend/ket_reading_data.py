# -*- coding: utf-8 -*-
"""
为 KET_DATA 增加"短文"阅读数据：12 个词汇分类各一篇短文
每篇短文含 title + sentences（逐句 en/zh 对照）
"""
import io, json

READING = {
    "个人信息": {
        "title": "My New Friend",
        "sentences": [
            {"en": "Hello! My name is Anna Smith.", "zh": "你好！我叫安娜·史密斯。"},
            {"en": "I am ten years old.", "zh": "我十岁了。"},
            {"en": "My birthday is on June 1st.", "zh": "我的生日是六月一日。"},
            {"en": "I am from China.", "zh": "我来自中国。"},
            {"en": "I am a girl.", "zh": "我是一个女孩。"},
            {"en": "I speak Chinese and English.", "zh": "我说中文和英语。"},
            {"en": "My address is 123 Main Street.", "zh": "我的地址是主街 123 号。"},
            {"en": "My phone number is 123-4567.", "zh": "我的电话号码是 123-4567。"},
            {"en": "My email is anna@mail.com.", "zh": "我的邮箱是 anna@mail.com。"},
        ],
    },
    "家庭与朋友": {
        "title": "My Family",
        "sentences": [
            {"en": "I have a big family.", "zh": "我有一个大家庭。"},
            {"en": "My father is a doctor.", "zh": "我的爸爸是一名医生。"},
            {"en": "My mother is a teacher.", "zh": "我的妈妈是一名老师。"},
            {"en": "I have one sister and one brother.", "zh": "我有一个妹妹和一个弟弟。"},
            {"en": "My grandparents live with us.", "zh": "我的祖父母和我们住在一起。"},
            {"en": "My aunt and uncle have a cute baby.", "zh": "我的姑姑和姑父有一个可爱的宝宝。"},
            {"en": "I have many friends at school.", "zh": "我在学校有很多朋友。"},
            {"en": "My best friend is Lily.", "zh": "我最好的朋友是莉莉。"},
            {"en": "We play together every day.", "zh": "我们每天一起玩。"},
        ],
    },
    "学校与学习": {
        "title": "My School Day",
        "sentences": [
            {"en": "I go to school every day.", "zh": "我每天去上学。"},
            {"en": "My classroom is big and bright.", "zh": "我的教室又大又明亮。"},
            {"en": "My teacher is very kind.", "zh": "我的老师非常和蔼。"},
            {"en": "My favorite subject is science.", "zh": "我最喜欢的科目是科学。"},
            {"en": "I like math and art too.", "zh": "我也喜欢数学和美术。"},
            {"en": "I have a lot of homework today.", "zh": "我今天有很多家庭作业。"},
            {"en": "I use my dictionary in English lessons.", "zh": "我在英语课上使用词典。"},
            {"en": "I sit at my desk and read books.", "zh": "我坐在书桌前读书。"},
            {"en": "I have a test tomorrow.", "zh": "我明天有一场考试。"},
        ],
    },
    "日常生活": {
        "title": "My Daily Life",
        "sentences": [
            {"en": "I get up early in the morning.", "zh": "我早上起得很早。"},
            {"en": "I have breakfast at seven o'clock.", "zh": "我七点吃早餐。"},
            {"en": "I go to school on weekdays.", "zh": "我在工作日去上学。"},
            {"en": "On Saturday I play with my friends.", "zh": "周六我和朋友们一起玩。"},
            {"en": "On Sunday I visit my grandma.", "zh": "周日我去看望奶奶。"},
            {"en": "I have lunch at school.", "zh": "我在学校吃午饭。"},
            {"en": "I have dinner with my family in the evening.", "zh": "晚上我和家人一起吃晚饭。"},
            {"en": "I go to bed at nine o'clock at night.", "zh": "我晚上九点睡觉。"},
        ],
    },
    "食物与饮料": {
        "title": "Yummy Food",
        "sentences": [
            {"en": "I like eating good food.", "zh": "我喜欢吃美食。"},
            {"en": "For breakfast I have bread and milk.", "zh": "早餐我吃面包和喝牛奶。"},
            {"en": "For lunch I eat rice, chicken and vegetables.", "zh": "午餐我吃米饭、鸡肉和蔬菜。"},
            {"en": "My favorite food is pizza.", "zh": "我最喜欢的食物是披萨。"},
            {"en": "I like hamburgers and sandwiches too.", "zh": "我也喜欢汉堡和三明治。"},
            {"en": "I drink water and juice.", "zh": "我喝水和果汁。"},
            {"en": "My mother makes delicious soup and dumplings.", "zh": "我妈妈做的汤和饺子很好吃。"},
            {"en": "I love cake and chocolate.", "zh": "我爱吃蛋糕和巧克力。"},
        ],
    },
    "爱好与运动": {
        "title": "My Hobbies",
        "sentences": [
            {"en": "My hobby is swimming.", "zh": "我的爱好是游泳。"},
            {"en": "I also like playing football and basketball.", "zh": "我也喜欢踢足球和打篮球。"},
            {"en": "I like reading books and drawing pictures.", "zh": "我喜欢读书和画画。"},
            {"en": "I listen to music and sing songs.", "zh": "我听音乐和唱歌。"},
            {"en": "On weekends I go hiking with my dad.", "zh": "周末我和爸爸去远足。"},
            {"en": "I love traveling to new places.", "zh": "我喜欢去新的地方旅行。"},
            {"en": "Sport is good for my health.", "zh": "运动对我的健康有好处。"},
            {"en": "I exercise every day.", "zh": "我每天锻炼。"},
        ],
    },
    "身体与健康": {
        "title": "My Body",
        "sentences": [
            {"en": "My body has many parts.", "zh": "我的身体有很多部位。"},
            {"en": "I have two eyes and two ears.", "zh": "我有两只眼睛和两只耳朵。"},
            {"en": "My nose and mouth are on my face.", "zh": "我的鼻子和嘴在脸上。"},
            {"en": "I use my hands to write.", "zh": "我用手写字。"},
            {"en": "I brush my teeth every day.", "zh": "我每天刷牙。"},
            {"en": "My hair is long and black.", "zh": "我的头发又长又黑。"},
            {"en": "I have two legs and two feet.", "zh": "我有两条腿和两只脚。"},
            {"en": "I eat healthy food to keep my body strong.", "zh": "我吃健康的食物让身体强壮。"},
        ],
    },
    "衣服与购物": {
        "title": "My Clothes",
        "sentences": [
            {"en": "I like buying clothes.", "zh": "我喜欢买衣服。"},
            {"en": "Today I wear a T-shirt and jeans.", "zh": "今天我穿 T 恤和牛仔裤。"},
            {"en": "In winter I wear a coat and a scarf.", "zh": "冬天我穿外套和戴围巾。"},
            {"en": "I have a nice dress for parties.", "zh": "我有一条聚会穿的漂亮连衣裙。"},
            {"en": "My shoes are new.", "zh": "我的鞋子是新的。"},
            {"en": "I wear socks every day.", "zh": "我每天穿袜子。"},
            {"en": "On cold days I wear gloves and a hat.", "zh": "在寒冷的天气我戴手套和帽子。"},
            {"en": "I like shopping with my mother.", "zh": "我喜欢和妈妈一起购物。"},
        ],
    },
    "交通与旅行": {
        "title": "Travel and Transport",
        "sentences": [
            {"en": "I like traveling.", "zh": "我喜欢旅行。"},
            {"en": "I go to school by bus.", "zh": "我坐公交车去上学。"},
            {"en": "My father drives a car to work.", "zh": "我爸爸开车去上班。"},
            {"en": "We take a train to visit my grandparents.", "zh": "我们坐火车去看望祖父母。"},
            {"en": "I ride my bike in the park.", "zh": "我在公园里骑自行车。"},
            {"en": "When I go far away, I take a plane.", "zh": "我去远方时坐飞机。"},
            {"en": "The airport is very big.", "zh": "机场非常大。"},
            {"en": "Traveling by ship is fun too.", "zh": "坐船旅行也很有趣。"},
        ],
    },
    "房屋与家居": {
        "title": "My House",
        "sentences": [
            {"en": "I live in a big house.", "zh": "我住在一栋大房子里。"},
            {"en": "My house has three bedrooms.", "zh": "我的房子有三间卧室。"},
            {"en": "I sleep in my bedroom.", "zh": "我在我的卧室睡觉。"},
            {"en": "We watch TV in the living room.", "zh": "我们在客厅看电视。"},
            {"en": "My mother cooks in the kitchen.", "zh": "我妈妈在厨房做饭。"},
            {"en": "I take a shower in the bathroom.", "zh": "我在浴室洗澡。"},
            {"en": "We have a small garden with flowers.", "zh": "我们有一个种满花的小花园。"},
            {"en": "I open the window to see the garden.", "zh": "我打开窗户看花园。"},
        ],
    },
    "工作与职业": {
        "title": "Jobs in My Family",
        "sentences": [
            {"en": "My father is a doctor.", "zh": "我的爸爸是一名医生。"},
            {"en": "He works in a hospital.", "zh": "他在医院工作。"},
            {"en": "My mother is a teacher.", "zh": "我的妈妈是一名老师。"},
            {"en": "She works in a school.", "zh": "她在学校工作。"},
            {"en": "My uncle is a driver.", "zh": "我的叔叔是一名司机。"},
            {"en": "He drives a bus.", "zh": "他开公交车。"},
            {"en": "My aunt works in an office.", "zh": "我的姑姑在办公室工作。"},
            {"en": "She is a manager.", "zh": "她是一名经理。"},
            {"en": "I want to be a teacher when I grow up.", "zh": "我长大后想当一名老师。"},
        ],
    },
    "自然与环境": {
        "title": "Beautiful Nature",
        "sentences": [
            {"en": "I love nature.", "zh": "我热爱大自然。"},
            {"en": "The world is beautiful.", "zh": "世界很美丽。"},
            {"en": "I like the sea and the ocean.", "zh": "我喜欢大海和海洋。"},
            {"en": "There is a river near my home.", "zh": "我家附近有一条河。"},
            {"en": "We climb the mountain in summer.", "zh": "我们夏天爬山。"},
            {"en": "The forest has many trees and animals.", "zh": "森林里有很多树和动物。"},
            {"en": "I pick flowers in the garden.", "zh": "我在花园里摘花。"},
            {"en": "We must protect our environment.", "zh": "我们必须保护环境。"},
        ],
    },
}

if __name__ == "__main__":
    print("短文数量:", len(READING))
    total_sent = sum(len(v["sentences"]) for v in READING.values())
    print("总句数:", total_sent)
    for k, v in READING.items():
        print(f'  {k}: {len(v["sentences"])} 句 - {v["title"]}')
