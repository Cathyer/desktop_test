import pytest
from test_cases.base_test import BaseTest
from test_utils.helpers.ui import UIHelper
from utils.config import *

class TestCalculator(BaseTest):
    """计算器功能测试"""
    
    def test_calculator_basic_operations(self):
        """测试基本运算功能"""
        # 启动计算器
        self._logger.log_step("启动计算器")
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "calculator_icon.png"))
        
        # 测试加法
        self._logger.log_step("测试加法运算")
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "number_1.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "plus.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "number_2.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "equals.png"))
        
        # 验证结果
        self.assert_element_exists(os.path.join(TEST_DATA_DIR, "result_3.png"))
        
        # 测试减法
        self._logger.log_step("测试减法运算")
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "number_5.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "minus.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "number_3.png"))
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "equals.png"))
        
        # 验证结果
        self.assert_element_exists(os.path.join(TEST_DATA_DIR, "result_2.png"))
        
        # 关闭计算器
        self._logger.log_step("关闭计算器")
        UIHelper.click_element(os.path.join(TEST_DATA_DIR, "close.png")) 