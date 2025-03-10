import os
from .config import *

def init_project_structure():
    """初始化项目目录结构"""
    # 创建必要的目录
    directories = [
        TEST_DATA_DIR,
        SCREENSHOTS_DIR,
        LOGS_DIR,
        REPORTS_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"已创建目录: {directory}")

    # 创建 .gitkeep 文件以保持目录结构
    for directory in directories:
        gitkeep_file = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                pass
            print(f"已创建 .gitkeep 文件: {gitkeep_file}")

if __name__ == '__main__':
    init_project_structure() 