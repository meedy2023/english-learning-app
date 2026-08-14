# -*- coding: utf-8 -*-
"""自动更新前端 API 地址为当前电脑 IP"""
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

def update_api_ip():
    # 获取当前 IP
    ip = get_local_ip()
    port = "8080"
    new_api = f"http://{ip}:{port}"
    
    # 读取 index.html
    html_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 API 地址
    old_api = 'const API = "'
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if old_api in line and 'localhost' in line or (old_api in line and '10.255.' in line):
            # 提取现有值
            start = line.index(old_api) + len(old_api)
            end = line.index('"', start)
            old_value = line[start:end]
            lines[i] = f'const API = "{new_api}";'
            print(f"✅ 已更新 API: {old_value} → {new_api}")
            break
    
    # 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return ip

if __name__ == "__main__":
    ip = update_api_ip()
    print(f"\n当前电脑 IP: {ip}")
    print(f"Pad 访问地址: http://{ip}:8080")
