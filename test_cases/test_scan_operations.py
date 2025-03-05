import os
import time
from desktop_test.test_cases.base_test import BaseTest
from desktop_test.test_cases.test_fixtures import TestFixtures
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import *

class TestScanOperations(BaseTest):
    """扫描页面操作测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        super().setup_method(method)
        TestFixtures.setup_scan_operation()

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        try:
            TestFixtures.teardown_application()
        finally:
            super().teardown_method(method)

    def test_color_mode_settings(self):
        """测试扫描色彩模式设置"""
        try:
            # 点击色彩模式下拉框
            self._logger.log_step("点击色彩模式下拉框")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/color_mode_dropdown.png'))
            
            # 选择彩色模式
            self._logger.log_step("选择彩色模式")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/color_mode_rgb.png'))
            
            # 验证选择结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'scan/color_mode_selected.png'),
                "色彩模式设置失败"
            )
            
            # 选择灰度模式
            self._logger.log_step("选择灰度模式")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/color_mode_dropdown.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/color_mode_gray.png'))
            
            # 验证选择结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'scan/gray_mode_selected.png'),
                "灰度模式设置失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_color_mode_settings",
                str(e),
                "扫描色彩模式测试失败"
            )
            raise

    def test_scan_type_settings(self):
        """测试扫描类型设置"""
        try:
            # 点击扫描类型下拉框
            self._logger.log_step("点击扫描类型下拉框")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_type_dropdown.png'))
            
            # 选择单面扫描
            self._logger.log_step("选择单面扫描")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_type_single.png'))
            
            # 验证选择结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'scan/single_scan_selected.png'),
                "单面扫描设置失败"
            )
            
            # 选择双面扫描
            self._logger.log_step("选择双面扫描")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_type_dropdown.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_type_double.png'))
            
            # 验证选择结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'scan/double_scan_selected.png'),
                "双面扫描设置失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_scan_type_settings",
                str(e),
                "扫描类型测试失败"
            )
            raise

    def test_start_scan(self):
        """测试开始扫描功能"""
        try:
            # 设置扫描参数
            self._logger.log_step("设置扫描参数")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_settings.png'))
            
            # 选择扫描仪
            self._logger.log_step("选择扫描仪")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scanner_dropdown.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scanner_device.png'))
            
            # 点击开始扫描
            self._logger.log_step("点击开始扫描")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/start_scan_button.png'))
            
            # 等待扫描完成
            time.sleep(5)  # 根据实际扫描时间调整
            
            # 验证扫描结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'scan/scan_result.png'),
                "扫描操作失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_start_scan",
                str(e),
                "扫描功能测试失败"
            )
            raise 