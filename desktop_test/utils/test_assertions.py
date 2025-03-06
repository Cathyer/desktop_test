import os
from utils.test_helper import TestHelper
from utils.config import *
from utils.custom_logger import CustomLogger

class TestAssertions:
    """测试断言类，提供通用的断言方法"""
    _logger = CustomLogger()
    
    @staticmethod
    def assert_element_exists(image_path, timeout=DEFAULT_TIMEOUT, message=None):
        """断言元素存在
        
        Args:
            image_path: 元素图片路径
            timeout: 超时时间（秒）
            message: 断言失败时的错误信息
        """
        if not TestHelper.wait_for_element(image_path, timeout):
            error_msg = message or f"元素不存在: {image_path}"
            TestAssertions._logger.log_assertion("元素存在", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_element_not_exists(image_path, timeout=DEFAULT_TIMEOUT, message=None):
        """断言元素不存在
        
        Args:
            image_path: 元素图片路径
            timeout: 超时时间（秒）
            message: 断言失败时的错误信息
        """
        if TestHelper.wait_for_element(image_path, timeout):
            error_msg = message or f"元素仍然存在: {image_path}"
            TestAssertions._logger.log_assertion("元素不存在", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_image_match(expected_image, actual_image, threshold=IMAGE_SIMILARITY_THRESHOLD, message=None):
        """断言图片匹配
        
        Args:
            expected_image: 期望的图片路径
            actual_image: 实际的图片路径
            threshold: 相似度阈值
            message: 断言失败时的错误信息
        """
        similarity = TestHelper.compare_images(expected_image, actual_image)
        if similarity < threshold:
            error_msg = message or f"图片相似度不足: {similarity:.4f} < {threshold}"
            TestAssertions._logger.log_assertion("图片匹配", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_file_exists(file_path, message=None):
        """断言文件存在
        
        Args:
            file_path: 文件路径
            message: 断言失败时的错误信息
        """
        if not os.path.exists(file_path):
            error_msg = message or f"文件不存在: {file_path}"
            TestAssertions._logger.log_assertion("文件存在", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_file_not_exists(file_path, message=None):
        """断言文件不存在
        
        Args:
            file_path: 文件路径
            message: 断言失败时的错误信息
        """
        if os.path.exists(file_path):
            error_msg = message or f"文件仍然存在: {file_path}"
            TestAssertions._logger.log_assertion("文件不存在", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_equal(actual, expected, message=None):
        """断言值相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 断言失败时的错误信息
        """
        if actual != expected:
            error_msg = message or f"值不相等: {actual} != {expected}"
            TestAssertions._logger.log_assertion("值相等", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_true(condition, message=None):
        """断言条件为真
        
        Args:
            condition: 要断言的条件
            message: 断言失败时的错误信息
        """
        if not condition:
            error_msg = message or "条件不为真"
            TestAssertions._logger.log_assertion("条件为真", error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_false(condition, message=None):
        """断言条件为假
        
        Args:
            condition: 要断言的条件
            message: 断言失败时的错误信息
        """
        if condition:
            error_msg = message or "条件不为假"
            TestAssertions._logger.log_assertion("条件为假", error_msg)
            raise AssertionError(error_msg) 