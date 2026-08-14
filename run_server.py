import os
import sys
import subprocess

def main():
    # 获取脚本所在目录的绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    
    # 检查 backend 目录是否存在
    if not os.path.exists(backend_dir):
        print(f"[错误] 找不到 backend 目录: {backend_dir}")
        return

    # 切换到 backend 目录
    os.chdir(backend_dir)
    
    # 检查 main.py 是否存在
    if not os.path.exists("main.py"):
        print("[错误] backend 目录下缺少 main.py")
        return

    print("=" * 40)
    print("  正在启动后端服务 (Port: 8080)")
    print("=" * 40)
    
    try:
        # 执行 uvicorn 命令
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8080"
        ])
    except KeyboardInterrupt:
        print("\n服务已停止。")
    except FileNotFoundError:
        print("[错误] 未找到 uvicorn，请运行: pip install uvicorn fastapi")

if __name__ == "__main__":
    main()