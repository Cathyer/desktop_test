import pytest
import os
import pyautogui
import json
import time
from datetime import datetime
from desktop_test.utils.config import *
from desktop_test.utils.custom_logger import CustomLogger
import logging
from desktop_test.utils.config import (
    TEST_DATA_DIR,
    SCREENSHOTS_DIR,
    LOGS_DIR,
    REPORTS_DIR
)
from desktop_test.utils.custom_logger import setup_logger

custom_logger = CustomLogger()

def pytest_configure(config):
    """配置pytest"""
    # 添加HTML报告
    config.option.htmlpath = os.path.join(REPORTS_DIR, REPORT_NAME)
    config.option.self_contained_html = True
    custom_logger.log_step("pytest配置完成")

    # 创建必要的目录
    for directory in [TEST_DATA_DIR, SCREENSHOTS_DIR, LOGS_DIR, REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # 设置日志
    log_file = os.path.join(LOGS_DIR, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    setup_logger(log_file)

def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = REPORT_TITLE
    custom_logger.log_step("HTML报告标题设置完成")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用于在测试失败时添加截图到HTML报告"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            # 在报告中添加失败截图
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"failure_{timestamp}.png")
            pyautogui.screenshot(screenshot_path)
            
            # 将截图添加到HTML报告
            extra = getattr(report, 'extra', [])
            extra.append({
                'name': '失败截图',
                'format': 'image',
                'content': screenshot_path,
                'mime_type': 'image/png',
                'extension': 'png'
            })
            report.extra = extra
            
            # 记录失败信息
            custom_logger.log_test_error(
                f"{item.name}",
                str(report.longrepr),
                "测试失败"
            )
        except Exception as e:
            custom_logger.log_test_error(
                "pytest报告生成",
                str(e),
                "报告生成失败"
            )

@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录"""
    return TEST_DATA_DIR

@pytest.fixture(scope="session")
def screenshots_dir():
    """截图目录"""
    return SCREENSHOTS_DIR

@pytest.fixture(scope="session")
def logs_dir():
    """日志目录"""
    return LOGS_DIR

@pytest.fixture(scope="session")
def reports_dir():
    """报告目录"""
    return REPORTS_DIR

@pytest.fixture(scope="function")
def test_logger():
    """测试用例日志记录器"""
    return logging.getLogger("test")

@pytest.fixture(scope="function")
def screenshot_name(request):
    """生成截图文件名"""
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{test_name}_{timestamp}.png"

@pytest.fixture(scope="function")
def take_screenshot(request, screenshot_name, screenshots_dir):
    """截图功能"""
    def _take_screenshot(page, name=None):
        if name is None:
            name = screenshot_name
        screenshot_path = os.path.join(screenshots_dir, name)
        page.save_screenshot(screenshot_path)
        return screenshot_path
    return _take_screenshot

@pytest.fixture(scope="function")
def test_data(request, test_data_dir):
    """测试数据"""
    def _get_test_data(category):
        data_file = os.path.join(test_data_dir, f"{category}.json")
        if os.path.exists(data_file):
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    return _get_test_data

@pytest.fixture(scope="function")
def cleanup_files():
    """清理测试文件"""
    files_to_cleanup = []
    yield files_to_cleanup
    for file_path in files_to_cleanup:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logging.error(f"清理文件失败: {file_path}, 错误: {str(e)}")

@pytest.fixture(scope="function")
def retry_on_failure():
    """失败重试装饰器"""
    def _retry_on_failure(func, max_retries=3, delay=1):
        import time
        for i in range(max_retries):
            try:
                return func()
            except Exception as e:
                if i == max_retries - 1:
                    raise
                time.sleep(delay)
        return None
    return _retry_on_failure

@pytest.fixture(scope="session")
def test_environment():
    """测试环境配置"""
    return {
        "env": os.getenv("TEST_ENV", "dev"),
        "browser": os.getenv("TEST_BROWSER", "chrome"),
        "platform": os.getenv("TEST_PLATFORM", "desktop"),
        "resolution": os.getenv("TEST_RESOLUTION", "1920x1080")
    }

@pytest.fixture(scope="function")
def performance_timer():
    """性能计时器"""
    start_time = time.time()
    yield
    end_time = time.time()
    duration = end_time - start_time
    custom_logger.info(f"测试执行时间: {duration:.2f}秒")

@pytest.fixture(scope="function")
def test_config():
    """测试配置"""
    def _load_config(config_name):
        config_file = os.path.join(TEST_DATA_DIR, "config", f"{config_name}.json")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    return _load_config

@pytest.fixture(scope="function")
def compare_images():
    """图片比较功能"""
    def _compare_images(image1_path, image2_path, threshold=0.95):
        try:
            import cv2
            import numpy as np
            
            # 读取图片
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None or img2 is None:
                return False
            
            # 调整图片大小
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            
            # 计算相似度
            similarity = np.mean(cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED))
            return similarity >= threshold
        except Exception as e:
            custom_logger.error(f"图片比较失败: {str(e)}")
            return False
    return _compare_images

@pytest.fixture(scope="function")
def wait_for_condition():
    """等待条件满足"""
    def _wait_for_condition(condition_func, timeout=10, interval=0.5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    return _wait_for_condition 