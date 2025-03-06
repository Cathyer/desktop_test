import os
import hashlib
import magic  # 用于文件类型检测
from .test_helper import TestHelper
from .custom_logger import CustomLogger
from .config import *

class TestAssertions:
    """测试断言类，提供通用的断言方法"""
    _logger = CustomLogger()

    # ... existing code ... 