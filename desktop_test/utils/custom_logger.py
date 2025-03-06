import os
import sys
import traceback
from datetime import datetime
from loguru import logger
from .config import *

class CustomLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """初始化日志配置"""
        # 确保日志目录存在
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # 设置日志格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        # 移除所有现有的处理器
        logger.remove()
        
        # 添加控制台输出
        logger.add(
            sys.stdout,
            format=log_format,
            level="INFO",
            colorize=True,
            enqueue=True
        )
        
        # 添加普通日志文件
        logger.add(
            os.path.join(LOGS_DIR, "test_{time:YYYY-MM-DD}.log"),
            format=log_format,
            level="DEBUG",
            rotation="00:00",  # 每天午夜轮转
            retention="7 days",
            encoding="utf-8",
            enqueue=True
        )
        
        # 添加错误日志文件
        logger.add(
            os.path.join(LOGS_DIR, "error_{time:YYYY-MM-DD}.log"),
            format=log_format,
            level="ERROR",
            rotation="00:00",  # 每天午夜轮转
            retention="7 days",
            encoding="utf-8",
            enqueue=True
        )
    
    def log_test_start(self, test_name):
        """记录测试开始"""
        logger.info(f"开始执行测试用例: {test_name}")
    
    def log_test_end(self, test_name, status="通过"):
        """记录测试结束"""
        logger.info(f"测试用例执行完成: {test_name} - {status}")
    
    def log_test_error(self, test_name, error_msg, error_type=None):
        """记录测试错误"""
        error_info = {
            "测试用例": test_name,
            "错误时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "错误类型": error_type or "未知错误",
            "错误信息": error_msg,
            "堆栈跟踪": traceback.format_exc()
        }
        
        # 格式化错误信息
        formatted_error = "\n".join([f"{k}: {v}" for k, v in error_info.items()])
        logger.error(formatted_error)
        
        # 保存错误截图
        try:
            from .test_helper import TestHelper
            screenshot_path = TestHelper.take_screenshot(f"error_{test_name}")
            logger.error(f"错误截图已保存: {screenshot_path}")
        except Exception as e:
            logger.error(f"保存错误截图失败: {str(e)}")
    
    def log_element_not_found(self, element_name, timeout):
        """记录元素未找到"""
        logger.error(f"元素未找到: {element_name} (超时时间: {timeout}秒)")
    
    def log_image_mismatch(self, expected, actual, similarity):
        """记录图片不匹配"""
        logger.error(
            f"图片不匹配:\n"
            f"期望图片: {expected}\n"
            f"实际图片: {actual}\n"
            f"相似度: {similarity:.4f}"
        )
    
    def log_step(self, step_name, status="成功"):
        """记录测试步骤"""
        logger.info(f"执行步骤: {step_name} - {status}")
    
    def log_assertion(self, assertion_type, expected, actual=None):
        """记录断言信息"""
        if actual is None:
            logger.info(f"断言: {assertion_type} - 期望值: {expected}")
        else:
            logger.info(f"断言: {assertion_type} - 期望值: {expected}, 实际值: {actual}")