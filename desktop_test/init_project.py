import os

def create_directories():
    """创建项目所需的目录结构"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义目录结构
    directories = [
        os.path.join(current_dir, 'test_data'),
        os.path.join(current_dir, 'screenshots'),
        os.path.join(current_dir, 'logs'),
        os.path.join(current_dir, 'reports'),
        # 创建测试数据子目录
        os.path.join(current_dir, 'test_data', 'batch'),
        os.path.join(current_dir, 'test_data', 'document'),
        os.path.join(current_dir, 'test_data', 'toolbar'),
        os.path.join(current_dir, 'test_data', 'file_list'),
        os.path.join(current_dir, 'test_data', 'scan'),
        os.path.join(current_dir, 'test_data', 'common')
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")
        else:
            print(f"目录已存在: {directory}")

if __name__ == "__main__":
    create_directories() 