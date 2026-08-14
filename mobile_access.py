# -*- coding: utf-8 -*-
"""生成手机/平板访问脚本"""
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
        return None

# 获取IP
ip = get_local_ip()
port = 8080
url = f"http://{ip}:{port}" if ip else f"http://localhost:{port}"

print("=" * 55)
print("   📱 手机/平板访问设置")
print("=" * 55)
print(f"""
🎯 访问地址: {url}

📋 操作步骤:
   1. 确保手机/平板和电脑连的是同一个WiFi
   2. 打开手机浏览器（Safari/Chrome等）
   3. 在地址栏输入上面的地址访问

💡 小提示:
   - 如果访问不了，检查电脑防火墙设置
   - 关闭防火墙命令（管理员运行）:
     netsh advfirewall set allprofiles state off
   - 开启防火墙命令:
     netsh advfirewall set allprofiles state on

📊 当前状态:
   - 电脑IP: {ip}
   - 端口: {port}
""")
print("=" * 55)
