import pytest
import os
import time
from desktop_test.pages.main_page import MainPage
from desktop_test.pages.scan_page import ScanPage
from desktop_test.test_cases.base_test import BaseTest
from desktop_test.utils.config import TEST_DATA_DIR
from desktop_test.utils.file_validator import FileValidator
from desktop_test.utils.test_helper import TestHelper

class TestScan(BaseTest):
    """扫描功能测试用例"""
    
    def setup_method(self, method):
        """测试方法前置处理"""
        super().setup_method(method)
        self.main_page = MainPage()
        self.scan_page = ScanPage()
        self.file_validator = FileValidator()
        self.output_file = os.path.join(TEST_DATA_DIR, 'scan', 'output.pdf')
    
    def teardown_method(self, method):
        """测试方法后置处理"""
        # 清理测试文件
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        super().teardown_method(method)
    
    def test_scan_basic_function(self):
        """测试扫描基本功能"""
        # 打开扫描功能
        self.main_page.open_scan()
        assert self.scan_page.is_scan_window_visible(), "扫描窗口未打开"
        
        # 开始扫描
        self.scan_page.start_scan()
        assert self.scan_page.is_scan_complete(), "扫描未完成"
        
        # 检查预览
        self.scan_page.open_preview()
        assert self.scan_page.is_preview_visible(), "预览未显示"
    
    def test_scan_with_different_resolutions(self):
        """测试不同分辨率的扫描"""
        # 打开扫描功能
        self.main_page.open_scan()
        assert self.scan_page.is_scan_window_visible(), "扫描窗口未打开"
        
        # 测试不同分辨率
        for resolution in [100, 200, 300]:
            self.scan_page.select_resolution(resolution)
            self.scan_page.start_scan()
            assert self.scan_page.is_scan_complete(), f"分辨率{resolution}的扫描未完成"
    
    def test_scan_with_different_color_modes(self):
        """测试不同颜色模式的扫描"""
        # 打开扫描功能
        self.main_page.open_scan()
        assert self.scan_page.is_scan_window_visible(), "扫描窗口未打开"
        
        # 测试不同颜色模式
        for mode in ['color', 'gray', 'bw']:
            self.scan_page.select_color_mode(mode)
            self.scan_page.start_scan()
            assert self.scan_page.is_scan_complete(), f"颜色模式{mode}的扫描未完成"
    
    def test_scan_with_different_paper_sizes(self):
        """测试不同纸张大小的扫描"""
        # 打开扫描功能
        self.main_page.open_scan()
        assert self.scan_page.is_scan_window_visible(), "扫描窗口未打开"
        
        # 测试不同纸张大小
        for size in ['a4', 'a3', 'letter']:
            self.scan_page.select_paper_size(size)
            self.scan_page.start_scan()
            assert self.scan_page.is_scan_complete(), f"纸张大小{size}的扫描未完成"
    
    def test_scan_preview_function(self):
        """测试扫描预览功能"""
        # 打开扫描功能
        self.main_page.open_scan()
        assert self.scan_page.is_scan_window_visible(), "扫描窗口未打开"
        
        # 开始扫描
        self.scan_page.start_scan()
        assert self.scan_page.is_scan_complete(), "扫描未完成"
        
        # 打开预览
        self.scan_page.open_preview()
        assert self.scan_page.is_preview_visible(), "预览未显示"
        
        # 检查预览区域
        preview_pos = self.scan_page.get_element_position('preview_area')
        assert preview_pos is not None, "预览区域未找到" 