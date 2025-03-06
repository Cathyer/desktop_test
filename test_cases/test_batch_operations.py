import os
from test_cases.base_test import BaseTest
from utils.test_fixtures import TestFixtures
from utils.test_helper import TestHelper
from utils.config import *

class TestBatchOperations(BaseTest):
    """批量操作测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        super().setup_method(method)
        TestFixtures.setup_batch_operation()

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        try:
            TestFixtures.teardown_application()
        finally:
            super().teardown_method(method)

    def test_batch_color_mode(self):
        """测试批量色彩模式转换"""
        try:
            # 点击批量操作按钮
            self._logger.log_step("点击批量操作按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/batch_operation_button.png'))
            
            # 选择色彩模式
            self._logger.log_step("选择色彩模式")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/color_mode_button.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/grayscale_option.png'))
            
            # 点击确定
            self._logger.log_step("确认操作")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'batch/grayscale_result.png'),
                "色彩模式转换失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_batch_color_mode",
                str(e),
                "批量色彩模式转换失败"
            )
            raise

    def test_batch_crop(self):
        """测试批量裁剪功能"""
        try:
            # 点击批量裁剪
            self._logger.log_step("点击批量裁剪")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/batch_crop_button.png'))
            
            # 设置裁剪参数
            self._logger.log_step("设置裁剪参数")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/crop_settings.png'))
            
            # 输入裁剪尺寸
            self._logger.log_step("输入裁剪尺寸")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/width_input.png'))
            TestHelper.write_text('800')
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/height_input.png'))
            TestHelper.write_text('600')
            
            # 确认裁剪
            self._logger.log_step("确认裁剪")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'batch/cropped_result.png'),
                "批量裁剪失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_batch_crop",
                str(e),
                "批量裁剪测试失败"
            )
            raise

    def test_batch_normalize(self):
        """测试批量规格化功能"""
        try:
            # 点击规格化按钮
            self._logger.log_step("点击规格化按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/normalize_button.png'))
            
            # 选择规格
            self._logger.log_step("选择规格")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'batch/size_option.png'))
            
            # 确认规格化
            self._logger.log_step("确认规格化")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'batch/normalized_result.png'),
                "批量规格化失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_batch_normalize",
                str(e),
                "批量规格化测试失败"
            )
            raise 