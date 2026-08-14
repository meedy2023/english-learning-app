# -*- coding: utf-8 -*-
"""一键启动英语学习App - 支持手机/平板访问"""
import subprocess
import webbrowser
import time
import os
import socket

def get_local_ip():
    """获取本机局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

print("=" * 55)
print("   English Learning App - Starting...")
print("=" * 55)

# 获取本机IP
local_ip = get_local_ip()

# 1. 关闭占用 8080 端口的进程
print("\n[1/4] Checking port 8080...")
try:
    result = subprocess.run(
        'netstat -ano | findstr :8080 | findstr LISTENING',
        shell=True, capture_output=True, text=True
    )
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                try:
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                    print(f"   Stopped process {pid}")
                except:
                    pass
except:
    pass

# 2. 启动后端（绑定所有网卡，支持手机访问）
print("[2/4] Starting backend (supporting mobile access)...")
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

subprocess.Popen(
    'python -m uvicorn main:app --reload --port 8080 --host 0.0.0.0',
    shell=False,
    cwd=backend_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print("   Backend starting in new window...")

# 3. 等待后端启动
print("[3/4] Waiting for backend...")
time.sleep(5)

# 4. 打开浏览器
print("[4/4] Opening browser...")
webbrowser.open('http://localhost:8080')

print("\n" + "=" * 55)
print("   ✅ 启动完成！")
print("=" * 55)
print(f"""
📱 手机/平板访问:
   确保手机和电脑连同一个WiFi，然后浏览器访问:
   
   👉  http://{local_ip}:8080

💻 电脑访问:
   👉  http://localhost:8080

📋 操作说明:
   1. 手机连接和电脑相同的WiFi
   2. 打开手机浏览器
   3. 输入上面的手机访问地址
   4. 即可使用！

🔴 关闭: 关掉显示 "English App Backend" 的黑色窗口
""")
print("=" * 55)
