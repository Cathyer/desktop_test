import os
from .base_page import BasePage
from utils.image_paths import ImagePaths
from utils.exceptions import ScanError, ElementNotFoundError, ElementNotVisibleError
from utils.test_data import TestData

class ScanPage(BasePage):
    """扫描页面类"""
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.SCAN
        self.test_data = TestData()
        # 扫描功能按钮
        self.start_button = os.path.join(TEST_DATA_DIR, 'scan', 'start_button.png')
        self.stop_button = os.path.join(TEST_DATA_DIR, 'scan', 'stop_button.png')
        self.preview_button = os.path.join(TEST_DATA_DIR, 'scan', 'preview_button.png')
        self.settings_button = os.path.join(TEST_DATA_DIR, 'scan', 'settings_button.png')
        
        # 扫描设置选项
        self.resolution_dropdown = os.path.join(TEST_DATA_DIR, 'scan', 'resolution_dropdown.png')
        self.color_mode_dropdown = os.path.join(TEST_DATA_DIR, 'scan', 'color_mode_dropdown.png')
        self.paper_size_dropdown = os.path.join(TEST_DATA_DIR, 'scan', 'paper_size_dropdown.png')
        
        # 分辨率选项
        self.resolution_100 = os.path.join(TEST_DATA_DIR, 'scan', 'resolution_100.png')
        self.resolution_200 = os.path.join(TEST_DATA_DIR, 'scan', 'resolution_200.png')
        self.resolution_300 = os.path.join(TEST_DATA_DIR, 'scan', 'resolution_300.png')
        
        # 颜色模式选项
        self.color_mode_color = os.path.join(TEST_DATA_DIR, 'scan', 'color_mode_color.png')
        self.color_mode_gray = os.path.join(TEST_DATA_DIR, 'scan', 'color_mode_gray.png')
        self.color_mode_bw = os.path.join(TEST_DATA_DIR, 'scan', 'color_mode_bw.png')
        
        # 纸张大小选项
        self.paper_size_a4 = os.path.join(TEST_DATA_DIR, 'scan', 'paper_size_a4.png')
        self.paper_size_a3 = os.path.join(TEST_DATA_DIR, 'scan', 'paper_size_a3.png')
        self.paper_size_letter = os.path.join(TEST_DATA_DIR, 'scan', 'paper_size_letter.png')
        
        # 预览区域
        self.preview_area = os.path.join(TEST_DATA_DIR, 'scan', 'preview_area.png')
        self.progress_bar = os.path.join(TEST_DATA_DIR, 'scan', 'progress_bar.png')
    
    def start_scan(self):
        """开始扫描"""
        self.logger.info("开始扫描")
        try:
            if not self.click_element(self.images['start_button']):
                raise ElementNotFoundError("开始按钮", self.timeout)
            return True
        except Exception as e:
            raise ScanError("开始扫描", str(e))
    
    def stop_scan(self):
        """停止扫描"""
        self.logger.info("停止扫描")
        try:
            if not self.click_element(self.images['stop_button']):
                raise ElementNotFoundError("停止按钮", self.timeout)
            return True
        except Exception as e:
            raise ScanError("停止扫描", str(e))
    
    def open_preview(self):
        """打开预览"""
        self.logger.info("打开预览")
        return self.click_element(self.images['preview_button'])
    
    def open_settings(self):
        """打开设置"""
        self.logger.info("打开设置")
        try:
            if not self.click_element(self.images['settings_button']):
                raise ElementNotFoundError("设置按钮", self.timeout)
            return True
        except Exception as e:
            raise ScanError("打开设置", str(e))
    
    def select_scanner(self, scanner_name):
        """选择扫描仪"""
        self.logger.info(f"选择扫描仪: {scanner_name}")
        try:
            if not self.click_element(self.images['scanner_dropdown']):
                raise ElementNotFoundError("扫描仪下拉框", self.timeout)
            
            option_key = f"{scanner_name.lower()}_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的扫描仪: {scanner_name}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{scanner_name}选项", self.timeout)
            return True
        except Exception as e:
            raise ScanError(f"选择扫描仪 {scanner_name}", str(e))
    
    def set_resolution(self, dpi):
        """设置扫描分辨率"""
        self.logger.info(f"设置扫描分辨率: {dpi} DPI")
        try:
            if not self.is_element_visible(self.images['resolution_dropdown']):
                raise ElementNotVisibleError("分辨率下拉框")
            
            if not self.click_element(self.images['resolution_dropdown']):
                raise ElementNotFoundError("分辨率下拉框", self.timeout)
            
            option_key = f"{dpi}_dpi_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的分辨率: {dpi} DPI")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{dpi} DPI选项", self.timeout)
            return True
        except Exception as e:
            raise ScanError(f"设置分辨率 {dpi} DPI", str(e))
    
    def set_color_mode(self, mode):
        """设置颜色模式"""
        self.logger.info(f"设置颜色模式: {mode}")
        try:
            if not self.click_element(self.images['color_mode_dropdown']):
                raise ElementNotFoundError("颜色模式下拉框", self.timeout)
            
            option_key = f"{mode.lower()}_mode_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的颜色模式: {mode}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{mode}模式选项", self.timeout)
            return True
        except Exception as e:
            raise ScanError(f"设置颜色模式 {mode}", str(e))
    
    def set_paper_size(self, size):
        """设置纸张大小"""
        self.logger.info(f"设置纸张大小: {size}")
        try:
            if not self.click_element(self.images['paper_size_dropdown']):
                raise ElementNotFoundError("纸张大小下拉框", self.timeout)
            
            option_key = f"{size.lower()}_size_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的纸张大小: {size}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{size}大小选项", self.timeout)
            return True
        except Exception as e:
            raise ScanError(f"设置纸张大小 {size}", str(e))
    
    def preview_scan(self):
        """预览扫描"""
        self.logger.info("预览扫描")
        try:
            if not self.click_element(self.images['preview_button']):
                raise ElementNotFoundError("预览按钮", self.timeout)
            return True
        except Exception as e:
            raise ScanError("预览扫描", str(e))
    
    def is_preview_visible(self):
        """检查预览窗口是否可见"""
        try:
            return self.is_element_visible(self.images['preview_area'])
        except Exception as e:
            self.logger.error(f"检查预览窗口可见性失败: {str(e)}")
            return False
    
    def is_scan_complete(self):
        """检查扫描是否完成"""
        try:
            return self.wait_for_element_disappear(self.images['progress_bar'])
        except Exception as e:
            self.logger.error(f"检查扫描完成状态失败: {str(e)}")
            return False
    
    def perform_scan(self, scanner_name, resolution=300, color_mode='color', paper_size='A4'):
        """执行完整的扫描流程"""
        self.logger.info(f"执行扫描: 扫描仪={scanner_name}, 分辨率={resolution}DPI, 颜色模式={color_mode}, 纸张大小={paper_size}")
        try:
            # 选择扫描仪
            self.select_scanner(scanner_name)
            
            # 设置分辨率
            self.set_resolution(resolution)
            
            # 设置颜色模式
            self.set_color_mode(color_mode)
            
            # 设置纸张大小
            self.set_paper_size(paper_size)
            
            # 预览扫描
            self.preview_scan()
            
            # 等待预览完成
            if not self.is_preview_visible():
                raise ScanError("扫描预览", "预览窗口未显示")
            
            # 开始扫描
            self.start_scan()
            
            # 等待扫描完成
            if not self.is_scan_complete():
                raise ScanError("扫描", "扫描未完成")
            
            return True
        except Exception as e:
            raise ScanError("扫描流程", str(e)) 