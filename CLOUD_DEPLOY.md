# 🚀 部署到云端（免费）

## 方案：Render.com 免费部署

### 部署步骤

**1. 创建 GitHub 仓库**
- 把 `english_app` 文件夹上传到 GitHub
- 需要包含 `backend/` 和 `frontend/` 两个文件夹

**2. 注册 Render**
- 访问 https://render.com
- 用 GitHub 账号登录

**3. 创建 Web Service**
- 点击 "New +" → "Web Service"
- 连接你的 GitHub 仓库
- 设置：
  - Name: `english-learning-app`
  - Region: Singapore（离中国近）
  - Branch: `main`
  - Root Directory: `backend`
  - Runtime: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Plan: `Free`

**4. 点击 "Create Web Service"**

等待 2-3 分钟部署完成！

**5. 修改前端 API 地址**

部署后获取你的服务地址，如：`https://english-learning-app.onrender.com`

然后修改 `frontend/index.html` 中的 API 地址：
```javascript
// 把所有 http://localhost:8080 改成你的云地址
const API_BASE = 'https://english-learning-app.onrender.com';
```

**6. 部署前端到免费托管**

方案A - Vercel（推荐）:
1. 把 `frontend` 文件夹单独上传 GitHub
2. 在 Vercel 创建项目
3. 修改 `index.html` 中的 API 地址
4. 部署

方案B - GitHub Pages:
1. 修改 `index.html` 中的 API 地址为云地址
2. 把 `frontend` 文件夹部署到 GitHub Pages

---

## 📱 部署后访问

```
https://你的服务名.onrender.com
```

## 💰 费用

- Render 免费额度：750小时/月
- 每月足够用（一个月31天，每天24小时 = 744小时）

## ⚠️ 注意

免费版服务不使用时会休眠，首次访问可能需要等待几秒启动。
