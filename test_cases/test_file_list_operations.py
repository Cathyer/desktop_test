import os
from test_cases.base_test import BaseTest
from utils.test_fixtures import TestFixtures
from utils.test_helper import TestHelper
from utils.config import *

class TestFileListOperations(BaseTest):
    """文件列表操作测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        super().setup_method(method)
        TestFixtures.setup_application()

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        try:
            TestFixtures.teardown_application()
        finally:
            super().teardown_method(method)

    def test_import_files(self):
        """测试文件导入功能"""
        try:
            # 点击导入按钮
            self._logger.log_step("点击导入按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/import_button.png'))
            
            # 选择多个文件
            self._logger.log_step("选择多个文件")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/test_image1.png'))
            TestHelper.key_press('ctrl')  # 按住Ctrl键进行多选
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/test_image2.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/test_image3.png'))
            TestHelper.key_release('ctrl')
            
            # 确认导入
            self._logger.log_step("确认导入")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/open_button.png'))
            
            # 验证文件列表
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'file_list/imported_files.png'),
                "文件导入失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_import_files",
                str(e),
                "文件导入测试失败"
            )
            raise

    def test_insert_files(self):
        """测试文件插入功能"""
        try:
            # 导入初始文件
            TestFixtures.import_test_files([
                os.path.join(TEST_DATA_DIR, 'file_list/test_image1.png')
            ])
            
            # 选择插入位置
            self._logger.log_step("选择插入位置")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/file_list_item.png'))
            
            # 点击插入按钮
            self._logger.log_step("点击插入按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/insert_button.png'))
            
            # 选择要插入的文件
            self._logger.log_step("选择要插入的文件")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'file_list/test_image2.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/open_button.png'))
            
            # 验证插入结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'file_list/inserted_files.png'),
                "文件插入失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_insert_files",
                str(e),
                "文件插入测试失败"
            )
            raise

    def test_file_reorder(self):
        """测试文件重排序功能"""
        try:
            # 导入多个文件
            TestFixtures.import_test_files([
                os.path.join(TEST_DATA_DIR, 'file_list/test_image1.png'),
                os.path.join(TEST_DATA_DIR, 'file_list/test_image2.png'),
                os.path.join(TEST_DATA_DIR, 'file_list/test_image3.png')
            ])
            
            # 拖动文件进行重排序
            self._logger.log_step("拖动文件重排序")
            TestHelper.click_and_drag(
                os.path.join(TEST_DATA_DIR, 'file_list/file_item_1.png'),
                start_x=100,
                start_y=100,
                end_x=100,
                end_y=300
            )
            
            # 验证重排序结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'file_list/reordered_files.png'),
                "文件重排序失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_file_reorder",
                str(e),
                "文件重排序测试失败"
            )
            raise 