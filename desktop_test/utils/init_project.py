import os
from desktop_test.utils.config import *

def init_project_structure():
    """初始化项目目录结构"""
    # 创建主要目录
    directories = [
        TEST_DATA_DIR,
        SCREENSHOTS_DIR,
        LOGS_DIR,
        REPORTS_DIR
    ]
    
    # 创建测试数据子目录
    test_data_subdirs = [
        os.path.join(TEST_DATA_DIR, 'common'),
        os.path.join(TEST_DATA_DIR, 'toolbar'),
        os.path.join(TEST_DATA_DIR, 'file_list'),
        os.path.join(TEST_DATA_DIR, 'ocr'),
        os.path.join(TEST_DATA_DIR, 'scan')
    ]
    
    # 创建所有目录
    all_directories = directories + test_data_subdirs
    
    for directory in all_directories:
        os.makedirs(directory, exist_ok=True)
        print(f"已创建目录: {directory}")

    # 创建 .gitkeep 文件以保持目录结构
    for directory in all_directories:
        gitkeep_file = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                pass
            print(f"已创建 .gitkeep 文件: {gitkeep_file}")

if __name__ == '__main__':
    init_project_structure() 