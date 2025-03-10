import pytest
import os
import time
from desktop_test.pages.main_page import MainPage
from desktop_test.pages.file_page import FilePage
from desktop_test.pages.ocr_page import OCRPage
from desktop_test.pages.scan_page import ScanPage
from desktop_test.utils.test_helper import TestHelper

class TestExamples:
    """示例测试类"""
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_basic_file_operations(self, test_environment, performance_timer, take_screenshot):
        """测试基本文件操作（使用性能计时器和截图）"""
        # 初始化页面
        main_page = MainPage()
        file_page = FilePage()
        
        # 创建新文件
        file_page.create_new_file()
        take_screenshot(main_page, "创建新文件.png")
        
        # 输入文件名
        file_name = "test_file.txt"
        file_page.input_file_name(file_name)
        take_screenshot(main_page, "输入文件名.png")
        
        # 保存文件
        file_page.save_current_file()
        take_screenshot(main_page, "保存文件.png")
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_ocr_performance(self, performance_timer, test_config, wait_for_condition):
        """测试OCR性能（使用性能计时器和配置）"""
        # 加载OCR配置
        ocr_config = test_config("ocr")
        
        # 初始化页面
        main_page = MainPage()
        ocr_page = OCRPage()
        
        # 打开OCR功能
        main_page.open_ocr()
        
        # 等待OCR窗口显示
        assert wait_for_condition(ocr_page.is_ocr_window_visible), "OCR窗口未显示"
        
        # 设置OCR参数
        ocr_page.select_language(ocr_config.get("language", "chinese"))
        ocr_page.set_accuracy(ocr_config.get("accuracy", 0.7))
        ocr_page.select_output_format(ocr_config.get("output_format", "txt"))
        
        # 开始OCR识别
        ocr_page.start_ocr()
        
        # 等待识别完成
        assert wait_for_condition(ocr_page.is_progress_complete), "OCR识别未完成"
    
    @pytest.mark.ui
    @pytest.mark.regression
    def test_scan_ui(self, compare_images, test_data, cleanup_files):
        """测试扫描界面（使用图片比较和测试数据）"""
        # 初始化页面
        main_page = MainPage()
        scan_page = ScanPage()
        
        # 打开扫描功能
        main_page.open_scan()
        
        # 获取测试数据
        scan_data = test_data("scan")
        
        # 设置扫描参数
        scan_page.select_scanner(scan_data.get("scanner", "default"))
        scan_page.set_resolution(scan_data.get("resolution", 300))
        scan_page.set_color_mode(scan_data.get("color_mode", "color"))
        scan_page.set_paper_size(scan_data.get("paper_size", "A4"))
        
        # 预览扫描
        scan_page.preview_scan()
        
        # 比较预览结果
        expected_preview = os.path.join(TEST_DATA_DIR, "scan", "expected_preview.png")
        actual_preview = os.path.join(SCREENSHOTS_DIR, "scan_preview.png")
        scan_page.save_screenshot(actual_preview)
        
        assert compare_images(expected_preview, actual_preview), "预览结果不匹配"
        
        # 添加到清理列表
        cleanup_files.append(actual_preview)
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_file_security(self, retry_on_failure, test_environment):
        """测试文件安全操作（使用重试机制和环境配置）"""
        # 初始化页面
        file_page = FilePage()
        
        # 使用重试机制执行文件操作
        def create_secure_file():
            file_page.create_new_file()
            file_page.input_file_name("secure_file.txt")
            file_page.select_file_type("txt")
            return file_page.save_current_file()
        
        assert retry_on_failure(create_secure_file), "创建安全文件失败"
        
        # 验证环境配置
        assert test_environment["env"] == "dev", "测试环境不正确"
    
    @pytest.mark.bugfix
    def test_ocr_bugfix(self, wait_for_condition, test_config):
        """测试OCR问题修复（使用等待机制和配置）"""
        # 加载OCR配置
        ocr_config = test_config("ocr_bugfix")
        
        # 初始化页面
        ocr_page = OCRPage()
        
        # 设置OCR参数
        ocr_page.select_language(ocr_config.get("language", "chinese"))
        ocr_page.set_accuracy(ocr_config.get("accuracy", 0.7))
        
        # 开始OCR识别
        ocr_page.start_ocr()
        
        # 等待识别完成
        assert wait_for_condition(
            ocr_page.is_progress_complete,
            timeout=ocr_config.get("timeout", 30),
            interval=ocr_config.get("interval", 0.5)
        ), "OCR识别未完成"
        
        # 获取结果
        result = ocr_page.get_result_text()
        assert result, "未获取到OCR识别结果"
    
    @pytest.mark.api
    def test_scan_api(self, performance_timer, test_data):
        """测试扫描API（使用性能计时器和测试数据）"""
        # 获取测试数据
        scan_data = test_data("scan_api")
        
        # 初始化页面
        scan_page = ScanPage()
        
        # 执行扫描
        result = scan_page.perform_scan(
            scanner_name=scan_data.get("scanner"),
            resolution=scan_data.get("resolution"),
            color_mode=scan_data.get("color_mode"),
            paper_size=scan_data.get("paper_size")
        )
        
        assert result, "扫描API调用失败" 