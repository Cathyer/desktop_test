import time
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
            # 通过双击图标启动计算器
            self._logger.log_step("查找计算器图标")
            if not TestHelper.wait_for_element(
                os.path.join(TEST_DATA_DIR, 'calculator_icon.png'),
                timeout=5
            ):
                raise Exception("未找到计算器图标")
            
            # 双击图标
            self._logger.log_step("双击启动计算器")
            TestHelper.double_click_element(os.path.join(TEST_DATA_DIR, 'calculator_icon.png'))
            
            # 等待计算器窗口出现
            if self._wait_for_calculator_start():
                self._logger.log_step("计算器应用启动成功")
            else:
                raise Exception("计算器启动超时")
            
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
            # 查找并点击关闭按钮
            self._logger.log_step("查找关闭按钮")
            if TestHelper.wait_for_element(
                os.path.join(TEST_DATA_DIR, 'close_button.png'),
                timeout=5
            ):
                self._logger.log_step("点击关闭按钮")
                TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'close_button.png'))
                
                # 等待窗口关闭
                start_time = time.time()
                while time.time() - start_time < 5:  # 5秒超时
                    if not TestHelper.element_exists(
                        os.path.join(TEST_DATA_DIR, 'calculator_title.png')
                    ):
                        self._logger.log_step("计算器应用关闭成功")
                        break
                    time.sleep(0.5)
                else:
                    raise Exception("计算器关闭超时")
            else:
                raise Exception("未找到关闭按钮")
                
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
            if TestHelper.wait_for_element(
                os.path.join(TEST_DATA_DIR, 'calculator_title.png'),
                timeout=1
            ):
                return True
            time.sleep(0.5)
        return False
        
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