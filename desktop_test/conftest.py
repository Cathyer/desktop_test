import pytest
import os
import pyautogui
from datetime import datetime
from desktop_test.utils.config import *
from desktop_test.utils.custom_logger import CustomLogger

logger = CustomLogger()

def pytest_configure(config):
    """配置pytest"""
    # 添加HTML报告
    config.option.htmlpath = os.path.join(REPORTS_DIR, REPORT_NAME)
    config.option.self_contained_html = True
    logger.log_step("pytest配置完成")

def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = REPORT_TITLE
    logger.log_step("HTML报告标题设置完成")

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
            logger.log_test_error(
                f"{item.name}",
                str(report.longrepr),
                "测试失败"
            )
        except Exception as e:
            logger.log_test_error(
                "pytest报告生成",
                str(e),
                "报告生成失败"
            ) 