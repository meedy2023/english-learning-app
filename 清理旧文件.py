# 清理旧的 bat 文件脚本
# 运行后会删除有问题的旧 bat 文件

import os

old_files = [
    'start_backend.bat',
    '启动学习App.bat',
    '启动应用.bat',
    '停止服务.bat'  # 旧版本
]

for f in old_files:
    path = f'C:\\Users\\omap\\english_app\\{f}'
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f'✓ 已删除: {f}')
        except Exception as e:
            print(f'✗ 删除失败 {f}: {e}')
    else:
        print(f'- 不存在: {f}')

print('\n保留的文件:')
for f in ['启动App.bat', '停止服务.bat', '仅启动后端.bat']:
    path = f'C:\\Users\\omap\\english_app\\{f}'
    if os.path.exists(path):
        print(f'  ✓ {f}')