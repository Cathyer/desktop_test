import pytest
import os
import time
from desktop_test.pages.main_page import MainPage
from desktop_test.pages.ocr_page import OCRPage
from desktop_test.test_cases.base_test import BaseTest
from desktop_test.utils.config import TEST_DATA_DIR
from desktop_test.utils.file_validator import FileValidator
from desktop_test.utils.test_helper import TestHelper

class TestOCR(BaseTest):
    """OCR功能测试用例"""
    
    def setup_method(self, method):
        """测试方法前置处理"""
        super().setup_method(method)
        self.main_page = MainPage()
        self.ocr_page = OCRPage()
        self.file_validator = FileValidator()
        self.test_image = os.path.join(TEST_DATA_DIR, 'ocr', 'test_image.png')
        self.output_file = os.path.join(TEST_DATA_DIR, 'ocr', 'output.txt')
    
    def teardown_method(self, method):
        """测试方法后置处理"""
        # 清理测试文件
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        super().teardown_method(method)
    
    def test_ocr_basic_function(self):
        """测试OCR基本功能"""
        # 打开OCR功能
        self.main_page.open_ocr()
        assert self.ocr_page.is_ocr_window_visible(), "OCR窗口未打开"
        
        # 选择识别语言
        self.ocr_page.select_language('chinese')
        
        # 开始识别
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "OCR识别未完成"
        
        # 获取识别结果
        result = self.ocr_page.get_result_text()
        assert result is not None, "未获取到识别结果"
    
    def test_ocr_with_different_languages(self):
        """测试不同语言的OCR识别"""
        # 打开OCR功能
        self.main_page.open_ocr()
        assert self.ocr_page.is_ocr_window_visible(), "OCR窗口未打开"
        
        # 测试中文识别
        self.ocr_page.select_language('chinese')
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "中文OCR识别未完成"
        
        # 测试英文识别
        self.ocr_page.select_language('english')
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "英文OCR识别未完成"
    
    def test_ocr_with_different_output_formats(self):
        """测试不同输出格式的OCR识别"""
        # 打开OCR功能
        self.main_page.open_ocr()
        assert self.ocr_page.is_ocr_window_visible(), "OCR窗口未打开"
        
        # 测试TXT格式输出
        self.ocr_page.select_output_format('txt')
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "TXT格式OCR识别未完成"
        assert self.file_validator.wait_for_file_exists(self.output_file), "TXT输出文件未创建"
        
        # 测试DOC格式输出
        self.ocr_page.select_output_format('doc')
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "DOC格式OCR识别未完成"
        assert self.file_validator.wait_for_file_exists(self.output_file.replace('.txt', '.doc')), "DOC输出文件未创建"
        
        # 测试PDF格式输出
        self.ocr_page.select_output_format('pdf')
        self.ocr_page.start_ocr()
        assert self.ocr_page.is_progress_complete(), "PDF格式OCR识别未完成"
        assert self.file_validator.wait_for_file_exists(self.output_file.replace('.txt', '.pdf')), "PDF输出文件未创建"
    
    def test_ocr_accuracy_settings(self):
        """测试OCR识别精度设置"""
        # 打开OCR功能
        self.main_page.open_ocr()
        assert self.ocr_page.is_ocr_window_visible(), "OCR窗口未打开"
        
        # 测试不同精度设置
        for accuracy in [0.5, 0.7, 0.9]:
            self.ocr_page.set_accuracy(accuracy)
            self.ocr_page.start_ocr()
            assert self.ocr_page.is_progress_complete(), f"精度{accuracy}的OCR识别未完成" 