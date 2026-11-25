# 课文朗读 · 角色音色分配表

> 代码位置：`frontend/index.html` 与 `docs/index.html` 中 `// ========== 课文分角色朗读` 段落，**两份必须完全一致**。
> 当前 SW 缓存版本：`english-app-v254`；改完两份 HTML 后，把两份 `sw.js` 的版本号 +1。

## 1. 音色池（10 组）

| 音色 id | 性别 | 显示名 | 讯飞 vcn | 讯飞 pitch | 讯飞 speed | Edge 音色 | 系统语音 pitch |
|---|---|---|---|---:|---:|---|---:|
| `role_f1` | 女 | 清亮女声 | catherine | 50 | 50 | en-GB-SoniaNeural | 1.35 |
| `role_f2` | 女 | 柔美女声 | catherine | 60 | 52 | en-US-JennyNeural | 1.26 |
| `role_f3` | 女 | 少女音 | catherine | 70 | 55 | en-GB-LibbyNeural | 1.46 |
| `role_f4` | 女 | 成熟女声 | catherine | 42 | 46 | en-US-AriaNeural | 1.14 |
| `role_f5` | 女 | 沉稳女声 | catherine | 34 | 44 | en-GB-MaisieNeural | 1.05 |
| `role_m1` | 男 | 青年男声 | henry | 50 | 50 | en-GB-RyanNeural | 0.80 |
| `role_m2` | 男 | 低沉男声 | henry | 40 | 46 | en-GB-GeorgeNeural | 0.64 |
| `role_m3` | 男 | 活泼男声 | henry | 58 | 55 | en-US-GuyNeural | 0.92 |
| `role_m4` | 男 | 沉稳男声 | henry | 32 | 42 | en-GB-ChristopherNeural | 0.55 |
| `role_m5` | 男 | 温和男声 | henry | 46 | 48 | en-US-DavidNeural | 0.73 |

- 讯飞只有 `catherine`（女）和 `henry`（男）两个真实 vcn，靠 pitch / speed 变体拉开同性别差异。
- Edge 每组用不同真实音色，是网络链路上听感差异的主要来源。
- 系统语音（无网络 / 本机 TTS）靠 `sysPitch` 区分。
- `role_f*` / `role_m*` 是**虚拟 id**，必须在 `VOICE_PROFILES` 里注册真实 vcn/pitch/speed。代码已通过 `Object.assign({...}, ROLE_VOICE_TTS_PROFILES)` 自动注册，不要改回普通对象字面量。

## 2. 固定分配（按音色查角色）

| 音色 id | 音色名 | 固定角色（代码匹配键为小写） |
|---|---|---|
| `role_f1` | 清亮女声 | Lingling、Huahua |
| `role_f2` | 柔美女声 | Amy、Weiwei |
| `role_f3` | 少女音 | Wenwen、Lanlan、Tippi、Girl、Little Chicken、Baby |
| `role_f4` | 成熟女声 | Jingjing、Nana、Mum、Mother、Amy's mum、Ms Smart、Ms Li、Ms Olivia |
| `role_f5` | 沉稳女声 | Teacher、Yanyan、Jiajia、Grandma、Mother Hen、Woman |
| `role_m1` | 青年男声 | **Tom**、Bob、Bobo、Bobby、Li Han、Jay |
| `role_m2` | 低沉男声 | **Dad / Father**、Man、Liu Fei、Jim、Doctor、Detective Sharp |
| `role_m3` | 活泼男声 | Sam、Boy、Taotao、Ray |
| `role_m4` | 沉稳男声 | Narrator、Grandpa、Terry、Old man、Lu Xun、Fabre、Samuel Pepys |
| `role_m5` | 温和男声 | Daming、Ben、David、Yangyang |

> 用户举例的三个角色：**Tom = 青年男声、Mum = 成熟女声、Dad = 低沉男声**，三者音色互不相同。

## 3. 未列出的角色怎么分配

| 情况 | 规则 |
|---|---|
| 能识别性别 | 在同性别 5 组里按角色名做 FNV-1a 哈希，同一角色每次声音一致 |
| 无性别但属于人物 | 在全部 10 组里按名字哈希（白名单见下） |
| 动物 / 物体 / 自然景物 / 男女合读（如 Sam & Amy） | 返回 `null`，沿用设置页发音人 |

- 女性名字表 `ROLE_FEMALE_NAMES`：amy, lingling, wenwen, yanyan, jingjing, lanlan, huahua, weiwei, nana, jiajia, yoyo, lulu, coco, susu, mia, tippi, mum, mother, grandma, sister, girl, woman, baby, ms smart, ms li, ms olivia, mother hen, mum bird, duoduo, zuzu
- 男性名字表 `ROLE_MALE_NAMES`：sam, daming, tom, ben, bob, bobo, david, terry, jay, ray, jim, bobby, taotao, yangyang, li han, liu fei, lu xun, fabre, yang shanzhou, samuel pepys, detective sharp, dad, father, grandpa, boy, man, old man, dad dog
- 无性别人物白名单 `ROLE_HUMAN_NEUTRAL`（正则）：teacher, narrator, student, students, kids, children, everyone, all, both, family, friend, my new friend, host, old friends, zookeeper, police officer, forest keeper, barbapapa, tutu, lin jia

## 4. 以后怎么改

1. **调音色听感**：改第 1 节对应的 `ROLE_VOICE_POOL` 那一行（vcn / pitch / speed / edge / sysPitch / label），**不要改 id**，否则第 2 节的固定分配会失配。
2. **给角色换声音 / 修撞音**：改 `ROLE_VOICE_ASSIGN` 对应条目，并同步更新本文件第 2 节。
3. **新增人物名字**：加进 `ROLE_FEMALE_NAMES` / `ROLE_MALE_NAMES`；无性别标记的人物名（老师、主持人等）加进 `ROLE_HUMAN_NEUTRAL` 正则。
4. **同步与发布**：两份 HTML 改完后两份 `sw.js` 版本号 +1，提交并 push（`origin main`），GitHub Pages 约 1 分钟后生效。

> TTS 音频缓存是页面内存 `Map`，刷新即清空，改音色参数后刷新页面就能听到新声音；但 HTML 被 SW 缓存，不升版本号用户拿不到新表。
> 当前真实数据覆盖：126 个角色 / 1253 行课文，1149 行（92%）分配了独立音色。
