# Cloudflare Worker 部署说明（讯飞 ASR 代理）

## 目标
把讯飞的 APIKey/APISecret 藏到 Cloudflare Worker 服务端环境变量里，前端源码不再暴露任何凭据，杜绝盗刷。

## 架构
```
华为平板前端 → Cloudflare Worker（藏着 Key，转发）→ 讯飞语音听写 → 返回文字
```

## 部署步骤（约 5 分钟，全免费，无需信用卡）

### 1. 注册 Cloudflare（如已有账号跳过）
打开 https://dash.cloudflare.com/sign-up ，用邮箱注册，验证邮箱即可，**不需要信用卡**。

### 2. 创建 Worker
1. 登录后左侧点 **「Workers & Pages」**
2. 点 **「创建」/「Create Worker」**
3. 给 Worker 起个名字（例如 `english-asr`，会得到 `english-asr.xxx.workers.dev` 地址）
4. 点 **「部署」/「Deploy」**（会先生成一个默认示例）

### 3. 粘贴代码
1. 进入刚创建的 Worker，点 **「编辑代码」/「Edit Code」**
2. 把编辑器里默认代码全部删掉
3. 粘贴 `cloudflare-worker.js` 的**全部内容**（已放在项目根目录 `C:\Users\omap\english_app\cloudflare-worker.js`）
4. 点右上角 **「部署」/「Deploy」**

### 4. 配置环境变量（关键！Key 就藏在这里）
1. 进入 Worker 的 **「设置 → 变量」/「Settings → Variables」**
2. 添加三个变量（类型选 Secret 或 Plain text 都行）：

| 变量名 | 值 |
|--------|-----|
| `XF_APPID` | `b6392404` |
| `XF_KEY` | `c757277ed0729711d3b7887a9450b416` |
| `XF_SECRET` | `ZjA3M2ZkZTBmNTVjOTk5Njk3OThkZTRk` |

3. 保存，重新部署（Deploy）一次让变量生效

### 5. 验证
浏览器访问 `https://<你的worker名>.<子域>.workers.dev/health`，应返回 `{"ok":true}`

### 6. 把地址发给我
把你 Worker 的完整地址（形如 `https://english-asr.你的子域.workers.dev`）发给我，我替换前端里的占位地址，然后重新构建并推送上线。

## 部署完成后的前端改动
前端 `XFYunASR.WORKER_URL` 占位符会替换成你的真实 Worker 地址，然后：
1. `python build_static.py` 重建
2. git 提交推送
3. GitHub Pages 上线

## 安全效果
- 前端源码、GitHub 仓库里**不再有 APIKey/APISecret**（已确认清除）
- Key 只存在于 Cloudflare 服务端环境变量，网页访问者无法获取
- 盗刷者拿不到 Key，无法绕过你的 Worker 直接刷讯飞额度
