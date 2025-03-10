import os
import time
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import *
from desktop_test.utils.custom_logger import CustomLogger

class TestFixtures:
    """测试夹具类，提供通用的前置和后置操作"""
    
    _logger = CustomLogger()
    _test_helper = TestHelper()
    
    @classmethod
    def setup_application(cls):
        """启动应用的通用前置操作"""
        try:
            # 通过双击图标启动采编王
            cls._logger.log_step("查找采编王图标")
            if not cls._test_helper.double_click_element(os.path.join(TEST_DATA_DIR, "common/caibian_icon.png")):
                cls._logger.log_test_error("TestFixtures.setup_application", "采编王启动失败", "未找到应用图标")
                raise Exception("应用程序启动失败")
            
            # 等待采编王窗口出现
            if cls._wait_for_window_appear():
                cls._logger.log_step("采编王应用启动成功")
                return True
            else:
                raise Exception("采编王启动超时")
                
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.setup_application",
                str(e),
                "采编王启动失败"
            )
            return False

    @classmethod
    def teardown_application(cls):
        """关闭应用的通用后置操作"""
        try:
            # 点击关闭按钮
            cls._logger.log_step("关闭采编王应用")
            if not cls._test_helper.click_element(os.path.join(TEST_DATA_DIR, "common/close_button.png")):
                cls._logger.log_test_error("TestFixtures.teardown_application", "采编王关闭失败", "未找到关闭按钮")
                raise Exception("应用程序关闭失败")
            
            # 确认关闭
            if TestHelper.wait_for_element(os.path.join(TEST_DATA_DIR, 'common/confirm_close.png')):
                TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_close.png'))
            
            # 等待窗口关闭
            time.sleep(2)
            
            return True
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.teardown_application",
                str(e),
                "采编王关闭失败"
            )
            return False

    @classmethod
    def import_test_files(cls, file_paths, text):
        """导入测试文件夹的通用操作

        Args:
            file_paths: 要导入的测试文件路径列表
            text: 要输入的文本
        """
        try:
            # 点击导入按钮
            cls._logger.log_step("点击导入按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/import_button.png'))

            # 点击导入文件夹按钮
            cls._logger.log_step("点击导入文件夹按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/import_file_button.png'))

            # 点击目录输入框
            cls._logger.log_step("点击目录输入框")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/file_input.png'))
            # 点击写入内容
            TestHelper.write_text(text)

            # 确认选择导入
            cls._logger.log_step("确认选择导入")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/select_button.png'))

            time.sleep(2)

            return True
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.import_test_files",
                str(e),
                "测试文件导入失败"
            )
            return False

    @classmethod
    def setup_batch_operation(cls):
        """批量操作的通用前置设置"""
        try:
            if not cls.setup_application():
                raise Exception("应用程序启动失败")
            cls.import_test_files([
                os.path.join(TEST_DATA_DIR, 'batch/test_image1.png'),
                os.path.join(TEST_DATA_DIR, 'batch/test_image2.png'),
                os.path.join(TEST_DATA_DIR, 'batch/test_image3.png')
            ])
            return True
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.setup_batch_operation",
                str(e),
                "批量操作前置设置失败"
            )
            return False

    @classmethod
    def setup_document_operation(cls):
        """文档处理的通用前置设置"""
        try:
            if not cls.setup_application():
                raise Exception("应用程序启动失败")
            # 根据测试类型导入不同的测试文件
            cls.import_test_files([os.path.join(TEST_DATA_DIR, 'document/test_doc.pdf')])
            return True
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.setup_document_operation",
                str(e),
                "文档处理前置设置失败"
            )
            return False

    @classmethod
    def setup_toolbar_operation(cls):
        """工具栏操作的通用前置设置"""
        try:
            cls.setup_application()
            cls.import_test_files([os.path.join(TEST_DATA_DIR, 'toolbar/test_image.png')])
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.setup_toolbar_operation",
                str(e),
                "工具栏操作前置设置失败"
            )
            raise

    @classmethod
    def setup_scan_operation(cls):
        """扫描操作的通用前置设置"""
        try:
            cls.setup_application()
            # 切换到扫描页面
            cls._logger.log_step("切换到扫描页面")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'scan/scan_tab.png'))
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.setup_scan_operation",
                str(e),
                "扫描操作前置设置失败"
            )
            raise

    @classmethod
    def _wait_for_window_appear(cls, timeout=10):
        """等待采编王窗口出现"""
        return TestHelper.wait_for_element(
            os.path.join(TEST_DATA_DIR, 'common/main_window.png'),
            timeout=timeout
        )

    @classmethod
    def verify_operation_result(cls, result_image_path, error_message):
        """验证操作结果的通用方法
        
        Args:
            result_image_path: 用于验证的结果图片路径
            error_message: 验证失败时的错误信息
        """
        try:
            cls._logger.log_step("验证操作结果")
            if not TestHelper.wait_for_element(result_image_path, timeout=5):
                raise Exception(error_message)
        except Exception as e:
            cls._logger.log_test_error(
                "TestFixtures.verify_operation_result",
                str(e),
                error_message
            )
            raise 