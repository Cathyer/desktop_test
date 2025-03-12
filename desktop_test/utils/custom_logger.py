import os
import sys
import json
import logging
import traceback
import pyautogui
import time
from datetime import datetime
from typing import Optional, Dict, Any, Union
from desktop_test.utils.config import *
from desktop_test.utils.exceptions import ValidationError

class LogLevel:
    """日志级别常量"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class CustomLogger:
    """自定义日志类，提供测试过程中的日志记录功能"""
    
    _instance = None
    _test_context: Dict[str, Any] = {}
    
    def __new__(cls, name: str = None):
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
            cls._instance._initialize_logger(name or __name__)
        return cls._instance
    
    def _initialize_logger(self, name: str):
        """初始化日志配置"""
        try:
            # 确保日志目录存在
            os.makedirs(LOGS_DIR, exist_ok=True)
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            
            # 创建logger实例
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)
            
            # 如果已经有处理器，不重复添加
            if self.logger.handlers:
                return
            
            # 设置日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # 添加控制台输出
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # 添加普通日志文件
            log_file = os.path.join(LOGS_DIR, f"test_{datetime.now():%Y-%m-%d}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # 添加错误日志文件
            error_file = os.path.join(LOGS_DIR, f"error_{datetime.now():%Y-%m-%d}.log")
            error_handler = logging.FileHandler(error_file, encoding='utf-8')
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            self.logger.addHandler(error_handler)
            
            # 添加JSON格式日志文件
            json_file = os.path.join(LOGS_DIR, f"test_{datetime.now():%Y-%m-%d}.json")
            json_handler = logging.FileHandler(json_file, encoding='utf-8')
            json_handler.setLevel(logging.DEBUG)
            json_handler.setFormatter(
                logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            )
            self.logger.addHandler(json_handler)
            
        except Exception as e:
            print(f"初始化日志系统失败: {e}")
            raise
    
    def set_test_context(self, **kwargs):
        """设置测试上下文信息
        
        Args:
            **kwargs: 上下文信息键值对
        """
        self._test_context.update(kwargs)
    
    def clear_test_context(self):
        """清除测试上下文信息"""
        self._test_context.clear()
    
    def _format_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化日志数据
        
        Args:
            data: 原始日志数据
            
        Returns:
            Dict[str, Any]: 格式化后的日志数据
        """
        formatted_data = {
            "timestamp": datetime.now().isoformat(),
            "context": self._test_context.copy()
        }
        formatted_data.update(data)
        return formatted_data
    
    def _save_screenshot(self, name: str) -> Optional[str]:
        """保存屏幕截图
        
        Args:
            name: 截图名称
            
        Returns:
            Optional[str]: 截图文件路径
        """
        try:
            time.sleep(SCREENSHOT_DELAY)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return filepath
        except Exception as e:
            self.logger.error(f"保存截图失败: {e}")
            return None
    
    def debug(self, msg, *args, **kwargs):
        """记录调试级别日志"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """记录信息级别日志"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """记录警告级别日志"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        """记录错误级别日志"""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        """记录严重错误级别日志"""
        self.logger.critical(msg, *args, **kwargs)
    
    def log_test_start(self, test_name: str, **kwargs):
        """记录测试开始
        
        Args:
            test_name: 测试用例名称
            **kwargs: 附加信息
        """
        self.set_test_context(test_name=test_name, **kwargs)
        log_data = self._format_log_data({
            "event": "test_start",
            "test_name": test_name,
            "extra": kwargs
        })
        self.info(f"开始执行测试用例: {test_name}")
        
        # 保存测试开始时的截图
        if screenshot_path := self._save_screenshot(f"test_start_{test_name}"):
            self.debug(f"测试开始截图: {screenshot_path}")
    
    def log_test_end(self, test_name: str, status: str = "通过", **kwargs):
        """记录测试结束
        
        Args:
            test_name: 测试用例名称
            status: 测试状态
            **kwargs: 附加信息
        """
        log_data = self._format_log_data({
            "event": "test_end",
            "test_name": test_name,
            "status": status,
            "extra": kwargs
        })
        self.info(f"测试用例执行完成: {test_name} - {status}")
        
        # 保存测试结束时的截图
        if screenshot_path := self._save_screenshot(f"test_end_{test_name}"):
            self.debug(f"测试结束截图: {screenshot_path}")
        
        self.clear_test_context()
    
    def log_test_error(
        self,
        test_name: str,
        error_msg: str,
        error_type: Optional[str] = None,
        save_screenshot: bool = True
    ):
        """记录测试错误
        
        Args:
            test_name: 测试用例名称
            error_msg: 错误信息
            error_type: 错误类型
            save_screenshot: 是否保存错误截图
        """
        error_info = {
            "event": "test_error",
            "test_name": test_name,
            "error_time": datetime.now().isoformat(),
            "error_type": error_type or "未知错误",
            "error_message": error_msg,
            "stack_trace": traceback.format_exc()
        }
        
        log_data = self._format_log_data(error_info)
        
        # 格式化错误信息
        formatted_error = "\n".join([
            f"{k}: {v}" for k, v in error_info.items()
            if k not in ("event", "stack_trace")
        ])
        self.error(formatted_error)
        self.error(f"堆栈跟踪:\n{error_info['stack_trace']}")
        
        # 保存错误截图
        if save_screenshot:
            if screenshot_path := self._save_screenshot(f"error_{test_name}"):
                self.error(f"错误截图已保存: {screenshot_path}")
                error_info["screenshot"] = screenshot_path
    
    def log_element_not_found(
        self,
        element_name: str,
        timeout: Union[int, float],
        save_screenshot: bool = True
    ):
        """记录元素未找到
        
        Args:
            element_name: 元素名称
            timeout: 超时时间
            save_screenshot: 是否保存截图
        """
        log_data = self._format_log_data({
            "event": "element_not_found",
            "element_name": element_name,
            "timeout": timeout
        })
        self.error(f"元素未找到: {element_name} (超时时间: {timeout}秒)")
        
        # 保存错误截图
        if save_screenshot:
            if screenshot_path := self._save_screenshot(f"element_not_found_{element_name}"):
                self.error(f"元素未找到截图已保存: {screenshot_path}")
                log_data["screenshot"] = screenshot_path
    
    def log_image_mismatch(
        self,
        expected: str,
        actual: str,
        similarity: float,
        threshold: float,
        save_diff: bool = True
    ):
        """记录图片不匹配
        
        Args:
            expected: 期望图片路径
            actual: 实际图片路径
            similarity: 相似度
            threshold: 匹配阈值
            save_diff: 是否保存差异图
        """
        log_data = self._format_log_data({
            "event": "image_mismatch",
            "expected_image": expected,
            "actual_image": actual,
            "similarity": similarity,
            "threshold": threshold
        })
        self.error(
            "图片不匹配:\n"
            f"期望图片: {expected}\n"
            f"实际图片: {actual}\n"
            f"相似度: {similarity:.4f}\n"
            f"阈值: {threshold:.4f}"
        )
    
    def log_step(
        self,
        step_name: str,
        status: str = "成功",
        details: Optional[Dict[str, Any]] = None,
        save_screenshot: bool = False
    ):
        """记录测试步骤
        
        Args:
            step_name: 步骤名称
            status: 步骤状态
            details: 步骤详情
            save_screenshot: 是否保存截图
        """
        log_data = self._format_log_data({
            "event": "test_step",
            "step_name": step_name,
            "status": status,
            "details": details or {}
        })
        self.info(f"执行步骤: {step_name} - {status}")
        
        if details:
            self.debug("步骤详情:\n{}", json.dumps(details, ensure_ascii=False, indent=2))
        
        if save_screenshot:
            if screenshot_path := self._save_screenshot(f"step_{step_name}"):
                self.debug(f"步骤截图: {screenshot_path}")
    
    def log_assertion(
        self,
        assertion_type: str,
        expected: Any,
        actual: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """记录断言信息
        
        Args:
            assertion_type: 断言类型
            expected: 期望值
            actual: 实际值
            details: 附加详情
        """
        log_data = self._format_log_data({
            "event": "assertion",
            "type": assertion_type,
            "expected": expected,
            "actual": actual,
            "details": details or {}
        })
        
        if actual is None:
            self.info(f"断言: {assertion_type} - 期望值: {expected}")
        else:
            self.info(f"断言: {assertion_type} - 期望值: {expected}, 实际值: {actual}")
            
        if details:
            self.debug("断言详情:\n{}", json.dumps(details, ensure_ascii=False, indent=2))
    
    def log_performance(
        self,
        operation: str,
        duration: float,
        threshold: Optional[float] = None
    ):
        """记录性能指标
        
        Args:
            operation: 操作名称
            duration: 执行时间（秒）
            threshold: 阈值（秒）
        """
        log_data = self._format_log_data({
            "event": "performance",
            "operation": operation,
            "duration": duration,
            "threshold": threshold
        })
        
        if threshold and duration > threshold:
            self.warning(
                f"性能警告: {operation} - 执行时间: {duration:.3f}秒 "
                f"(超过阈值: {threshold:.3f}秒)"
            )
        else:
            self.info(f"性能指标: {operation} - 执行时间: {duration:.3f}秒")

def setup_logger(log_file):
    """设置日志记录器
    
    Args:
        log_file: 日志文件路径
    """
    # 确保日志目录存在
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    
    # 如果已经有处理器，不重复添加
    if logger.handlers:
        return logger
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 添加文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger