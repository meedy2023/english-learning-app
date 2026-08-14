# English Learning App - 启动说明

## 快速启动

双击 `start_app.bat` 即可启动应用。

启动后会自动：
1. 关闭占用 8080 端口的旧进程
2. 启动后端服务器
3. 打开浏览器访问 `http://localhost:8080`

## 停止服务

关闭显示 "English App Backend" 的黑色命令行窗口即可。

## 文件说明

| 文件 | 说明 |
|------|------|
| `start_app.bat` | 一键启动脚本（推荐） |
| `backend/` | 后端代码（FastAPI） |
| `frontend/` | 前端代码（HTML/JS/CSS） |

## 功能说明

- **首页**：单词学习（按模块）
- **学习**：课文学习（上下册共 20 个模块）
- **KET**：KET 词汇、句型、语法学习（带分页）
- **报告**：学习进度统计

## 端口说明

- 后端端口：`8080`
- 访问地址：`http://localhost:8080`

## 注意事项

- 确保已安装 Python 3.8+
- 确保已安装依赖：`pip install fastapi uvicorn`
