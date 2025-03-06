import os
from datetime import datetime

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 各个目录路径
TEST_DATA_DIR = os.path.join(ROOT_DIR, 'test_data')
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, 'screenshots')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')

# 测试报告配置
REPORT_TITLE = "桌面应用自动化测试报告"
REPORT_NAME = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

# 图像比较配置
IMAGE_SIMILARITY_THRESHOLD = 0.95  # 图像相似度阈值

# 等待时间配置
DEFAULT_TIMEOUT = 10  # 默认超时时间（秒）
SCREENSHOT_DELAY = 0.5  # 截图前等待时间

# 日志配置
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOG_FILENAME = os.path.join(LOGS_DIR, f"test_log_{datetime.now().strftime('%Y%m%d')}.log") 