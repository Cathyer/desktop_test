import os
import pytest
from utils.test_helper import TestHelper
from utils.custom_logger import CustomLogger
from utils.config import *
from test_utils.assertions import TestAssertions

class BaseTest(TestAssertions):
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