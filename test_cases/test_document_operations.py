import os
import time
from desktop_test.test_cases.base_test import BaseTest
from desktop_test.test_cases.test_fixtures import TestFixtures
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import *

class TestDocumentOperations(BaseTest):
    """文档处理测试用例"""
    
    def setup_method(self, method):
        """每个测试方法开始前的设置"""
        super().setup_method(method)
        TestFixtures.setup_document_operation()

    def teardown_method(self, method):
        """每个测试方法结束后的清理"""
        try:
            TestFixtures.teardown_application()
        finally:
            super().teardown_method(method)

    def test_ocr_recognition(self):
        """测试OCR文字识别功能"""
        try:
            # 点击OCR识别按钮
            self._logger.log_step("点击OCR识别按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ocr_button.png'))
            
            # 选择识别语言
            self._logger.log_step("选择识别语言")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/language_chinese.png'))
            
            # 开始识别
            self._logger.log_step("开始识别")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_ocr.png'))
            
            # 等待识别完成
            time.sleep(5)  # 根据实际识别时间调整
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'document/ocr_result.png'),
                "OCR识别失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_ocr_recognition",
                str(e),
                "OCR识别测试失败"
            )
            raise

    def test_pdf_conversion(self):
        """测试PDF转换功能"""
        try:
            # 点击PDF转换按钮
            self._logger.log_step("点击PDF转换按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/pdf_button.png'))
            
            # 设置转换参数
            self._logger.log_step("设置转换参数")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/pdf_settings.png'))
            
            # 开始转换
            self._logger.log_step("开始转换")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_conversion.png'))
            
            # 等待转换完成
            time.sleep(3)  # 根据实际转换时间调整
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'document/pdf_converted.png'),
                "PDF转换失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_pdf_conversion",
                str(e),
                "PDF转换测试失败"
            )
            raise

    def test_ofd_handling(self):
        """测试OFD文件处理功能"""
        try:
            # 点击OFD处理按钮
            self._logger.log_step("点击OFD处理按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ofd_button.png'))
            
            # 设置处理参数
            self._logger.log_step("设置处理参数")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ofd_settings.png'))
            
            # 开始处理
            self._logger.log_step("开始处理")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_ofd_process.png'))
            
            # 等待处理完成
            time.sleep(3)  # 根据实际处理时间调整
            
            # 验证结果
            TestFixtures.verify_operation_result(
                os.path.join(TEST_DATA_DIR, 'document/ofd_processed.png'),
                "OFD处理失败"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_ofd_handling",
                str(e),
                "OFD处理测试失败"
            )
            raise 