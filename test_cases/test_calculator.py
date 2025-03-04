import time
import subprocess
import signal
import os
from desktop_test.test_cases.base_test import BaseTest
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import *

class TestCalculator(BaseTest):
    """计算器应用测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前启动计算器"""
        super().setup_method(method)
        try:
            # 启动计算器应用
            self.calculator_process = subprocess.Popen(
                ['deepin-calculator'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待应用启动
            self._wait_for_calculator_start()
            self._logger.log_step("计算器应用启动成功")
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.setup_method",
                str(e),
                "计算器启动失败"
            )
            raise
        
    def teardown_method(self, method):
        """每个测试方法结束后关闭计算器"""
        try:
            # 关闭计算器
            if hasattr(self, 'calculator_process'):
                self.calculator_process.send_signal(signal.SIGTERM)
                try:
                    self.calculator_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.calculator_process.kill()
                self._logger.log_step("计算器应用关闭成功")
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.teardown_method",
                str(e),
                "计算器关闭失败"
            )
        finally:
            super().teardown_method(method)
    
    def _wait_for_calculator_start(self, timeout=10):
        """等待计算器应用启动"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 检查进程是否在运行
                if self.calculator_process.poll() is None:
                    # 等待窗口出现
                    if TestHelper.wait_for_element(
                        os.path.join(TEST_DATA_DIR, 'calculator_title.png'),
                        timeout=1
                    ):
                        return True
            except Exception:
                pass
            time.sleep(0.5)
        
        raise TimeoutError("计算器应用启动超时")
        
    def test_basic_calculation(self):
        """测试基本的加法运算"""
        try:
            # 点击数字1
            self._logger.log_step("点击数字1")
            self.assert_element_exists(os.path.join(TEST_DATA_DIR, 'button_1.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'button_1.png'))
            
            # 点击加号
            self._logger.log_step("点击加号")
            self.assert_element_exists(os.path.join(TEST_DATA_DIR, 'button_plus.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'button_plus.png'))
            
            # 点击数字2
            self._logger.log_step("点击数字2")
            self.assert_element_exists(os.path.join(TEST_DATA_DIR, 'button_2.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'button_2.png'))
            
            # 点击等号
            self._logger.log_step("点击等号")
            self.assert_element_exists(os.path.join(TEST_DATA_DIR, 'button_equals.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'button_equals.png'))
            
            # 验证结果是否为3
            self._logger.log_step("验证计算结果")
            self.assert_images_match(
                os.path.join(TEST_DATA_DIR, 'result_3.png'),
                message="计算结果不正确，期望显示3"
            )
            
            self._logger.log_step("基本运算测试完成", "成功")
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_basic_calculation",
                str(e),
                "基本运算测试失败"
            )
            raise
            
    def test_calculator_ui(self):
        """测试计算器UI元素是否正确显示"""
        try:
            # 验证计算器窗口标题
            self._logger.log_step("验证计算器窗口标题")
            self.assert_element_exists(
                os.path.join(TEST_DATA_DIR, 'calculator_title.png'),
                message="计算器窗口标题未找到"
            )
            
            # 验证数字按钮是否都存在
            self._logger.log_step("验证数字按钮")
            for i in range(10):
                self.assert_element_exists(
                    os.path.join(TEST_DATA_DIR, f'button_{i}.png'),
                    message=f"数字按钮 {i} 未找到"
                )
            
            self._logger.log_step("UI元素验证完成", "成功")
                
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_calculator_ui",
                str(e),
                "UI元素验证失败"
            )
            raise