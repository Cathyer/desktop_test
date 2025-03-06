import os
import time
from test_cases.base_test import BaseTest
from utils.test_fixtures import TestFixtures
from utils.test_helper import TestHelper
from utils.config import *

class TestToolbarOperations(BaseTest):
    """工具栏操作测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        super().setup_method(method)
        TestFixtures.setup_toolbar_operation()

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        try:
            TestFixtures.teardown_application()
        finally:
            super().teardown_method(method)

    def test_crop_tool(self):
        """测试裁剪工具功能"""
        try:
            # 点击裁剪工具按钮
            self._logger.log_step("点击裁剪工具按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/crop_tool.png'))
            
            # 在图片上进行裁剪框选
            self._logger.log_step("进行裁剪框选")
            TestHelper.click_and_drag(
                os.path.join(TEST_DATA_DIR, 'toolbar/image_area.png'),
                start_x=100,
                start_y=100,
                end_x=300,
                end_y=300
            )
            
            # 确认裁剪
            self._logger.log_step("确认裁剪")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'toolbar/cropped_image.png'),
                "裁剪操作失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_crop_tool",
                str(e),
                "裁剪工具测试失败"
            )
            raise

    def test_selection_tool(self):
        """测试框选工具功能"""
        try:
            # 点击框选工具按钮
            self._logger.log_step("点击框选工具按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/selection_tool.png'))
            
            # 在图片上进行区域框选
            self._logger.log_step("进行区域框选")
            TestHelper.click_and_drag(
                os.path.join(TEST_DATA_DIR, 'toolbar/image_area.png'),
                start_x=50,
                start_y=50,
                end_x=200,
                end_y=200
            )
            
            # 验证选区
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'toolbar/selection_area.png'),
                "框选操作失败"
            )
            
            # 复制选区
            self._logger.log_step("复制选区")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/copy_button.png'))
            
            # 验证复制结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'toolbar/copied_area.png'),
                "选区复制失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_selection_tool",
                str(e),
                "框选工具测试失败"
            )
            raise

    def test_zoom_tool(self):
        """测试缩放工具功能"""
        try:
            # 点击缩放工具按钮
            self._logger.log_step("点击缩放工具按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/zoom_tool.png'))
            
            # 放大图片
            self._logger.log_step("放大图片")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/zoom_in.png'))
            time.sleep(1)
            
            # 验证放大效果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'toolbar/zoomed_in.png'),
                "放大操作失败"
            )
            
            # 缩小图片
            self._logger.log_step("缩小图片")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'toolbar/zoom_out.png'))
            time.sleep(1)
            
            # 验证缩小效果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'toolbar/zoomed_out.png'),
                "缩小操作失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_zoom_tool",
                str(e),
                "缩放工具测试失败"
            )
            raise 