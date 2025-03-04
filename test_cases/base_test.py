import os
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.custom_logger import CustomLogger
from desktop_test.utils.config import *

class BaseTest:
    _logger = CustomLogger()
    
    @classmethod
    def setup_class(cls):
        """测试类开始前的设置"""
        # 设置日志
        TestHelper.setup_logging()
        cls._logger.log_test_start(cls.__name__)
        
        # 确保所需目录存在
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)

    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        self._logger.log_test_start(f"{self.__class__.__name__}.{method.__name__}")

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        self._logger.log_test_end(f"{self.__class__.__name__}.{method.__name__}")

    @classmethod
    def teardown_class(cls):
        """测试类结束后的清理"""
        cls._logger.log_test_end(cls.__name__)

    def assert_element_exists(self, image_path, timeout=DEFAULT_TIMEOUT, message=None):
        """
        断言元素存在
        :param image_path: 元素图片路径
        :param timeout: 超时时间
        :param message: 断言失败消息
        """
        if not message:
            message = f"元素未找到: {image_path}"
        
        try:
            assert TestHelper.wait_for_element(image_path, timeout), message
            self._logger.log_assertion("元素存在", image_path)
        except AssertionError as e:
            # 测试失败时截图
            screenshot_path = TestHelper.take_screenshot(f"assertion_failed_{os.path.basename(image_path)}")
            self._logger.log_test_error(
                f"{self.__class__.__name__}.assert_element_exists",
                str(e),
                "元素未找到"
            )
            raise

    def assert_images_match(self, expected_image_path, actual_image_path=None, threshold=IMAGE_SIMILARITY_THRESHOLD, message=None):
        """
        断言图片匹配
        :param expected_image_path: 期望的图片路径
        :param actual_image_path: 实际的图片路径（如果为None，则自动截图）
        :param threshold: 相似度阈值
        :param message: 断言失败消息
        """
        if actual_image_path is None:
            actual_image_path = TestHelper.take_screenshot(f"actual_{os.path.basename(expected_image_path)}")
        
        if not message:
            message = f"图片不匹配: 期望 {expected_image_path}, 实际 {actual_image_path}"
        
        try:
            similarity = TestHelper.compare_images(expected_image_path, actual_image_path)
            assert similarity >= threshold, f"{message} (相似度: {similarity:.4f}, 阈值: {threshold})"
            self._logger.log_assertion("图片匹配", f"相似度: {similarity:.4f}")
        except AssertionError as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.assert_images_match",
                str(e),
                "图片不匹配"
            )
            raise 