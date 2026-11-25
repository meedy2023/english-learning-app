# 课文朗读 · 角色音色分配表

> 代码位置：`frontend/index.html` 与 `docs/index.html` 中 `// ========== 课文分角色朗读` 段落，**两份必须完全一致**。
> 当前 SW 缓存版本：`english-app-v261`；改完两份 HTML 后，把两份 `sw.js` 的版本号 +1。

## 1. 音色池（10 组）

| 音色 id | 性别 | 显示名 | 讯飞 vcn | 讯飞 pitch | 讯飞 speed | Edge 音色 | 系统语音 pitch |
|---|---|---|---|---:|---:|---|---:|
| `role_f1` | 女 | 清亮女声 | catherine | 50 | 50 | en-GB-SoniaNeural | 1.24 |
| `role_f2` | 女 | 柔美女声 | catherine | 58 | 52 | en-US-JennyNeural | 1.18 |
| `role_f3` | 女 | 少女音 | catherine | 60 | 55 | en-GB-LibbyNeural | 1.30 |
| `role_f4` | 女 | 成熟女声 | catherine | 44 | 46 | en-US-EmmaNeural | 1.10 |
| `role_f5` | 女 | 沉稳女声 | catherine | 40 | 44 | en-GB-MaisieNeural | 1.02 |
| `role_m1` | 男 | 青年男声 | henry | 50 | 50 | en-GB-RyanNeural | 0.88 |
| `role_m2` | 男 | 低沉男声 | henry | 42 | 46 | en-GB-ThomasNeural | 0.76 |
| `role_m3` | 男 | 活泼男声 | henry | 57 | 55 | en-US-GuyNeural | 0.98 |
| `role_m4` | 男 | 沉稳男声 | henry | 40 | 42 | en-US-ChristopherNeural | 0.70 |
| `role_m5` | 男 | 温和男声 | henry | 47 | 48 | en-US-EricNeural | 0.82 |
| `role_teacher` | 女 | 成年女声·老师 | catherine | 44 | 46 | en-US-AriaNeural | 1.08 |
| `role_child_f` | 女 | 女童声 | catherine | 60 | 55 | en-US-AnaNeural | 1.32 |
| `role_child_m` | 男 | 男童声 | henry | 58 | 55 | en-US-RogerNeural | 1.12 |

- **年龄匹配**：`Teacher` 固定用成年女声（`role_teacher`，原 `role_f5`/MaisieNeural 是偏童声的年轻女声，听感像儿童）；`Girl/Student/Students` 用女童声、`Boy/Kids/Children` 用男童声。
- **Edge 无真童声**：官方英文音色均为成人录制，女童声用 `en-US-AnaNeural`（Cute 标签，最接近童声），男童声用 `en-US-RogerNeural`（Lively 年轻男声）；讯飞端靠高 pitch（58~60）模拟。
- 上表后 3 个（`role_teacher`/`role_child_f`/`role_child_m`）标了 `fixedOnly: true`，**只按固定分配使用，不进入第 3 节的名字哈希池**，避免未列出的角色随机落到老师/儿童音。
- 为避免与老师撞音，`role_f4`（成熟女声，Mum 等）的 Edge 音色从 `en-US-AriaNeural` 改为 `en-US-EmmaNeural`，Aria 让给老师专用。
- 讯飞只有 `catherine`（女）和 `henry`（男）两个真实 vcn，靠 pitch / speed 变体拉开同性别差异。
- **pitch 已收敛**：讯飞 pitch 在合成时钳制到 40~60（`XFYunTTS.synth`），系统 `sysPitch` 收敛到 0.70~1.30。原因是 pitch 偏离 50 越远，合成音越容易带金属电音；角色区分主要靠 vcn + Edge 不同音色实现。
- 表格里的讯飞 speed 字段是角色**语速微调**，不是全局语速；全局语速现在由 `xfSynthSpeed()` 按用户设定统一生成（见第 4 节），会覆盖此字段。
- Edge 每组用不同真实音色，是网络链路上听感差异的主要来源。
- 系统语音（无网络 / 本机 TTS）靠 `sysPitch` 区分。
- `role_f*` / `role_m*` 是**虚拟 id**，必须在 `VOICE_PROFILES` 里注册真实 vcn/pitch/speed。代码已通过 `Object.assign({...}, ROLE_VOICE_TTS_PROFILES)` 自动注册，不要改回普通对象字面量。
- **Edge 音色名必须是 Edge TTS 真实存在的 ShortName**（如 Christopher 只有 `en-US-ChristopherNeural`，没有 `en-GB-` 版；George/David 不是有效音色）。写错会导致 Edge 链路连接即失败，只能落系统语音——移动端 WebView 系统语音常无声，表现为"某句没声音"。改音色名后对照 Edge 官方音色表核验。

## 2. 固定分配（按音色查角色）

| 音色 id | 音色名 | 固定角色（代码匹配键为小写） |
|---|---|---|
| `role_f1` | 清亮女声 | Lingling、Huahua |
| `role_f2` | 柔美女声 | Amy、Weiwei |
| `role_f3` | 少女音 | Wenwen、Lanlan、Tippi、Little Chicken、Baby |
| `role_f4` | 成熟女声 | Jingjing、Nana、Mum、Mother、Amy's mum、Ms Smart、Ms Li、Ms Olivia |
| `role_f5` | 沉稳女声 | Yanyan、Jiajia、Grandma、Mother Hen、Woman |
| `role_m1` | 青年男声 | **Tom**、Bob、Bobo、Bobby、Li Han、Jay |
| `role_m2` | 低沉男声 | **Dad / Father**、Man、Liu Fei、Jim、Doctor、Detective Sharp |
| `role_m3` | 活泼男声 | Sam、Taotao、Ray |
| `role_m4` | 沉稳男声 | Narrator、Grandpa、Terry、Old man、Lu Xun、Fabre、Samuel Pepys |
| `role_m5` | 温和男声 | Daming、Ben、David、Yangyang |
| `role_teacher` | 成年女声·老师 | **Teacher** |
| `role_child_f` | 女童声 | **Girl、Student、Students** |
| `role_child_m` | 男童声 | **Boy、Kids、Children** |
| `role_m2` | 低沉男声 | Dad、Father 等 + **Barbapapa（孩子们的 Dad，避免与 Tom 撞音）** |

> 用户举例的三个角色：**Tom = 青年男声、Mum = 成熟女声、Dad = 低沉男声**，三者音色互不相同。
> 年龄匹配：**Teacher = 成年女声（不再用偏童声的 Maisie）**；学生标签（Girl/Boy/Student/Students/Kids/Children）统一用儿童音。

## 3. 未列出的角色怎么分配

| 情况 | 规则 |
|---|---|
| 命中默认音规则（见下） | 返回 `null`，沿用设置页发音人 |
| 能识别性别 | 在同性别 5 组里按角色名做 FNV-1a 哈希，同一角色每次声音一致 |
| 无性别但属于人物 | 在全部 10 组里按名字哈希（白名单见下） |
| 其它（物体 / 自然景物） | 返回 `null`，沿用设置页发音人 |

**默认音规则 `roleShouldDefault()`（前端）/ `role_should_default()`（脚本）——优先于固定分配与性别判定，命中任一即返回 `null`：**
- **多人合读**：角色名含 `&` / `,` / ` and ` 分隔符（如 `Sam & Amy`、`Daming and Sam`），整句不该只像一个人发声。
- **群体齐读**：`ROLE_GROUP_CHORUS` = both / everyone / everybody / all / family / children / kids / students / people。
- **动物**：`ROLE_ANIMAL` = susu、baby、mother hen、mum bird、dad dog、little chicken、little dog、bird、dog、duck、frog、rabbit、bear、mouse 1、mouse 2、night owl、silkworm、giraffe（含真实动物与会说话的拟人动物）。

- 女性名字表 `ROLE_FEMALE_NAMES`：amy, lingling, wenwen, yanyan, jingjing, lanlan, huahua, weiwei, nana, jiajia, yoyo, lulu, coco, susu, mia, tippi, mum, mother, grandma, sister, girl, woman, baby, ms smart, ms li, ms olivia, mother hen, mum bird, duoduo, zuzu
- 男性名字表 `ROLE_MALE_NAMES`：sam, daming, tom, ben, bob, bobo, david, terry, jay, ray, jim, bobby, taotao, yangyang, li han, liu fei, lu xun, fabre, yang shanzhou, samuel pepys, detective sharp, dad, father, grandpa, boy, man, old man, dad dog
- 无性别人物白名单 `ROLE_HUMAN_NEUTRAL`（正则）：teacher, narrator, student, students, kids, children, everyone, all, both, family, friend, my new friend, host, old friends, zookeeper, police officer, forest keeper, barbapapa, tutu, lin jia
- 注：`susu`/`baby`/`mother hen`/`mum bird`/`dad dog`/`little chicken` 虽仍在性别表里，但会被默认音规则先拦截，不会发人声；保留在表中仅为兼容其它调用。

## 4. 语速与音质策略（消除电子杂音）

**核心原则：变速尽量在合成端完成，播放端只补极小残余。**

`audio.playbackRate` 远离 1 时浏览器做的是实时重采样（无音高补偿），会产生金属音/电子杂音，0.8 倍尤其 0.5 倍最明显。合成端（讯飞 speed / Edge prosody rate）是引擎按目标语速重新生成，音质无损。

| 用户设定 | 合成端倍速（`rateSynthPoint().synth`） | 讯飞 speed | 播放端残余（`audioPlaybackRate()`） |
|---:|---:|---:|---:|
| 0.5 | 0.775 | 0 | 0.645 |
| 0.8（默认） | 0.830 | 12 | **0.964**（几乎无重采样） |
| 1.0 | 1.000 | 50 | 1.000 |
| 1.2 | 1.180 | 78 | 1.017 |
| 1.5 | 1.390 | 100 | 1.079 |

- 映射表在 `RATE_SYNTH_TABLE`（`speechRate` 定义之后），由实测得出：讯飞 speed 0~100 实际覆盖约 0.775x~1.39x 语速。
- 换档函数：`xfSynthSpeed()` 给讯飞、`edgeSynthRatePct()` 给 Edge、`audioPlaybackRate()` 给播放端。三处必须一致，改映射表即可全链路生效。
- 0.5 档残余仍偏大（讯飞 speed 下限只能到 0.775x），是引擎物理限制；默认 0.8 档已基本消除重采样。
- **homo 分支缓存键已包含 `speechRate`**：切换语速后不会命中旧语速音频。
- `humanProsody` 的 pitchAdj 已收敛（疑问 +7 / 感叹 +5 / 陈述 +2），避免与角色 pitch 叠加后冲到极端值产生电音。
- Edge SSML 去掉了 `mstts:express-as style='friendly'`（部分音色不支持会导致合成失败），自然度靠标点停顿 + 句末 contour。

## 5. 提示音（庆祝/答对/答错）

`Celebrate` 里三处合成音效（`chime` / `_tone` / `_melody`）统一做了：
- 起音 attack 从 15~20ms 延长到 30ms，消除咔哒爆音；
- 每个增益节点后串一个 `lowpass` 滤波（2600Hz），柔化三角波高次谐波的"电子感"；
- 高八度泛音峰值略降（0.28 → 0.24）。

## 6. P0 预生成音频（固定课文）

固定课文不再完全依赖浏览器端 WebSocket / 讯飞接口，而是由脚本离线生成逐句 MP3，前端优先播放本地文件；文件缺失或加载失败时静默回退原 TTS 链路。

- 生成脚本：`pregenerate_audio.py`（根目录），依赖 `pip install --upgrade edge-tts`，不需要 API Key。
- 输出目录：`docs/audio/lesson/<哈希前2位>/<哈希>.mp3`。
- 哈希规则：`FNV-1a("edge|" + roleVoiceId + "|" + speechRate + "|1|" + expandAbbrev(text))`，与前端 `preAudioUrl()` 完全一致，无需 manifest。
- 默认只生成 0.8 档；`--all-rates` 生成 5 档。当前五档合计 6180 条（合读/群体/动物走默认音，无需预生成独立音色）。
- 前端接入点：`TTS.speakSentence()` 与 `speakLine()` 先试本地音频；`LessonReader` 播放当前句时预热下一句。
- 预生成音频按目标语速合成，播放端 `playbackRate = 1`，不再叠加残余系数。
- SW 策略：`sw.js` 中音频走**缓存优先**（命中即返回，弱网/离线秒开），未命中才走网络并写缓存；文件名带内容哈希，内容变了名字就变，不存在缓存陈旧问题。`index.html` 仍走网络优先，避免缓存旧页面。
- 切换角色音色或改名后，必须重新运行脚本覆盖旧文件（文件名随 voiceId 变化，不会互相覆盖）。

常用命令：

```bash
python pregenerate_audio.py --dry-run
python pregenerate_audio.py --limit 20
python pregenerate_audio.py --workers 6
python pregenerate_audio.py --all-rates
```

## 7. 以后怎么改

1. **调音色听感**：改第 1 节对应的 `ROLE_VOICE_POOL` 那一行（vcn / pitch / speed / edge / sysPitch / label），**不要改 id**，否则第 2 节的固定分配会失配。
2. **给角色换声音 / 修撞音**：改 `ROLE_VOICE_ASSIGN` 对应条目，并同步更新本文件第 2 节。
3. **新增人物名字**：加进 `ROLE_FEMALE_NAMES` / `ROLE_MALE_NAMES`；无性别标记的人物名（老师、主持人等）加进 `ROLE_HUMAN_NEUTRAL` 正则。
   - 如果是老师/学生这类要锁定年龄身份的角色，直接用 `ROLE_VOICE_ASSIGN` 固定到 `role_teacher` / `role_child_f` / `role_child_m`，不要只靠性别哈希。
4. **调语速/音质**：改 `RATE_SYNTH_TABLE` 或第 4 节提到的三个函数；改 `humanProsody` 的 pitchAdj 幅度；改 `Celebrate` 三处音效的滤波/包络。
5. **重新生成音频**：改过角色音色、语速映射或课文文本后，重跑 `pregenerate_audio.py`；只改 HTML 不重跑会继续播放旧音色/旧语速的预生成文件。
6. **同步与发布**：两份 HTML 改完后两份 `sw.js` 版本号 +1，提交并 push（`origin main`），GitHub Pages 约 1 分钟后生效。

> TTS 音频缓存是页面内存 `Map`，刷新即清空，改音色参数后刷新页面就能听到新声音；但 HTML 被 SW 缓存，不升版本号用户拿不到新表。
> 当前真实数据覆盖：126 个角色 / 1253 行课文，1149 行（92%）分配了独立音色。
