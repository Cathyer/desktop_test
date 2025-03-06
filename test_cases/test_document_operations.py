import os
import time
from test_cases.base_test import BaseTest
from test_utils.fixtures import TestFixtures
from utils.test_helper import TestHelper
from utils.config import *

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
            # 导入测试图片
            self._logger.log_step("导入测试图片")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/import_button.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/test_ocr_image.png'))
            
            # 点击OCR识别按钮
            self._logger.log_step("点击OCR识别按钮")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ocr_button.png'))
            
            # 选择识别语言
            self._logger.log_step("选择识别语言")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/language_chinese.png'))
            
            # 输入保存文件名
            self._logger.log_step("输入保存文件名")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/filename_input.png'))
            TestHelper.write_text("OCR识别结果")
            
            # 选择保存路径
            self._logger.log_step("选择保存路径")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/save_path_button.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/target_folder.png'))
            
            # 确认保存设置
            self._logger.log_step("确认保存设置")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 开始识别
            self._logger.log_step("开始识别")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_ocr.png'))
            
            # 等待识别完成
            time.sleep(5)  # 根据实际识别时间调整
            
            # 验证结果文件是否存在
            self.assert_file_exists(
                os.path.join(TEST_DATA_DIR, 'document/OCR识别结果.txt'),
                "OCR结果文件不存在"
            )
            
            # 验证文件类型
            self.assert_file_type(
                os.path.join(TEST_DATA_DIR, 'document/OCR识别结果.txt'),
                'TXT',
                "OCR结果文件类型不正确"
            )
            
            # 验证识别结果
            self.assert_text_content(
                os.path.join(TEST_DATA_DIR, 'document/OCR识别结果.txt'),
                "预期的OCR识别文本内容",
                "OCR识别结果不正确"
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
            
            # 输入输出文件名
            self._logger.log_step("输入输出文件名")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/output_filename.png'))
            TestHelper.write_text("转换后的文档")
            
            # 选择输出路径
            self._logger.log_step("选择输出路径")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/output_path_button.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/target_folder.png'))
            
            # 确认转换设置
            self._logger.log_step("确认转换设置")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 开始转换
            self._logger.log_step("开始转换")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_conversion.png'))
            
            # 等待转换完成
            time.sleep(3)  # 根据实际转换时间调整
            
            # 验证结果文件是否存在
            self.assert_file_exists(
                os.path.join(TEST_DATA_DIR, 'document/转换后的文档.pdf'),
                "PDF转换结果文件不存在"
            )
            
            # 验证文件类型
            self.assert_file_type(
                os.path.join(TEST_DATA_DIR, 'document/转换后的文档.pdf'),
                'PDF',
                "PDF转换结果文件类型不正确"
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
            
            # 输入输出文件名
            self._logger.log_step("输入输出文件名")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ofd_output_filename.png'))
            TestHelper.write_text("处理后的OFD文档")
            
            # 选择输出路径
            self._logger.log_step("选择输出路径")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/ofd_output_path_button.png'))
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/target_folder.png'))
            
            # 确认处理设置
            self._logger.log_step("确认处理设置")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'common/confirm_button.png'))
            
            # 开始处理
            self._logger.log_step("开始处理")
            TestHelper.click_element(os.path.join(TEST_DATA_DIR, 'document/start_ofd_process.png'))
            
            # 等待处理完成
            time.sleep(3)  # 根据实际处理时间调整
            
            # 验证结果文件是否存在
            self.assert_file_exists(
                os.path.join(TEST_DATA_DIR, 'document/处理后的OFD文档.ofd'),
                "OFD处理结果文件不存在"
            )
            
            # 验证文件类型
            self.assert_file_type(
                os.path.join(TEST_DATA_DIR, 'document/处理后的OFD文档.ofd'),
                'OFD',
                "OFD处理结果文件类型不正确"
            )
            
        except Exception as e:
            self._logger.log_test_error(
                f"{self.__class__.__name__}.test_ofd_handling",
                str(e),
                "OFD处理测试失败"
            )
            raise 