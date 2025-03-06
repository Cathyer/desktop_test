import os
import pytest
import hashlib
import magic  # 用于文件类型检测
from utils.test_helper import TestHelper
from utils.custom_logger import CustomLogger
from utils.config import *

class TestAssertions:
    """测试断言类，提供通用的断言方法"""
    _logger = CustomLogger()
    
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

    def assert_image_match(self, image_path, threshold=0.8, message="图片不匹配"):
        """断言图片匹配
        
        Args:
            image_path: 期望的图片路径
            threshold: 匹配阈值
            message: 断言失败时的错误信息
        """
        if not TestHelper.match_image(image_path, threshold):
            self._logger.log_test_error(
                f"{self.__class__.__name__}.{self._testMethodName}",
                message,
                "图片不匹配"
            )
            raise AssertionError(message)

    def assert_file_exists(self, file_path, message="文件不存在"):
        """断言文件存在
        
        Args:
            file_path: 文件路径
            message: 断言失败时的错误信息
        """
        if not os.path.exists(file_path):
            self._logger.log_test_error(
                f"{self.__class__.__name__}.{self._testMethodName}",
                message,
                "文件不存在"
            )
            raise AssertionError(message)

    def assert_file_type(self, file_path, expected_type, message="文件类型不匹配"):
        """断言文件类型
        
        Args:
            file_path: 文件路径
            expected_type: 期望的文件类型（如 'PDF', 'DOC', 'OFD', 'TXT'）
            message: 断言失败时的错误信息
        """
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            
            # 文件类型映射
            type_mapping = {
                'PDF': 'application/pdf',
                'DOC': 'application/msword',
                'DOCX': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'OFD': 'application/ofd',
                'TXT': 'text/plain'
            }
            
            expected_mime = type_mapping.get(expected_type.upper())
            if not expected_mime or file_type != expected_mime:
                self._logger.log_test_error(
                    f"{self.__class__.__name__}.{self._testMethodName}",
                    f"文件类型不匹配: 期望 {expected_type}, 实际 {file_type}",
                    message
                )
                raise AssertionError(message)
                
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.{self._testMethodName}",
                str(e),
                "文件类型检查失败"
            )
            raise

    def assert_files_equal(self, file1_path, file2_path, message="文件内容不匹配"):
        """断言两个文件内容相同
        
        Args:
            file1_path: 第一个文件路径
            file2_path: 第二个文件路径
            message: 断言失败时的错误信息
        """
        try:
            # 计算文件的MD5哈希值
            def get_file_hash(file_path):
                hash_md5 = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
            
            # 比较文件哈希值
            if get_file_hash(file1_path) != get_file_hash(file2_path):
                self._logger.log_test_error(
                    f"{self.__class__.__name__}.{self._testMethodName}",
                    "文件内容不匹配",
                    message
                )
                raise AssertionError(message)
                
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.{self._testMethodName}",
                str(e),
                "文件比较失败"
            )
            raise

    def assert_text_content(self, file_path, expected_text, message="文本内容不匹配"):
        """断言文本文件内容
        
        Args:
            file_path: 文本文件路径
            expected_text: 期望的文本内容
            message: 断言失败时的错误信息
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                actual_text = f.read()
            
            if actual_text.strip() != expected_text.strip():
                self._logger.log_test_error(
                    f"{self.__class__.__name__}.{self._testMethodName}",
                    "文本内容不匹配",
                    message
                )
                raise AssertionError(message)
                
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.{self._testMethodName}",
                str(e),
                "文本内容检查失败"
            )
            raise 