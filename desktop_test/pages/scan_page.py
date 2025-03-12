import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.image_paths import ImagePaths
from desktop_test.utils.exceptions import ScanError, ElementNotFoundError, ElementNotVisibleError, TimeoutError
from desktop_test.utils.test_data import TestData
from desktop_test.utils.config import DEFAULT_TIMEOUT

class ScanPage(BasePage):
    """扫描页面类"""
    
    SUPPORTED_RESOLUTIONS = [100, 200, 300]
    SUPPORTED_COLOR_MODES = ['color', 'gray', 'bw']
    SUPPORTED_PAPER_SIZES = ['A4', 'A3', 'Letter']
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.SCAN
        self.test_data = TestData()
        self._initialize_elements()
    
    def _initialize_elements(self):
        """初始化页面元素"""
        # 扫描功能按钮
        self._buttons = {
            'start': self.images['start_button'],
            'stop': self.images['stop_button'],
            'preview': self.images['preview_button'],
            'settings': self.images['settings_button']
        }
        
        # 扫描设置选项
        self._settings = {
            'resolution': self.images['resolution_dropdown'],
            'color_mode': self.images['color_mode_dropdown'],
            'paper_size': self.images['paper_size_dropdown']
        }
        
        # 分辨率选项
        self._resolution_options = {
            100: self.images['resolution_100'],
            200: self.images['resolution_200'],
            300: self.images['resolution_300']
        }
        
        # 颜色模式选项
        self._color_mode_options = {
            'color': self.images['color_mode_color'],
            'gray': self.images['color_mode_gray'],
            'bw': self.images['color_mode_bw']
        }
        
        # 纸张大小选项
        self._paper_size_options = {
            'A4': self.images['paper_size_a4'],
            'A3': self.images['paper_size_a3'],
            'Letter': self.images['paper_size_letter']
        }
        
        # 预览区域
        self._preview_elements = {
            'area': self.images['preview_area'],
            'progress': self.images['progress_bar']
        }
    
    def _validate_resolution(self, resolution):
        """验证分辨率"""
        if resolution not in self.SUPPORTED_RESOLUTIONS:
            raise ValueError(f"不支持的分辨率: {resolution}. 支持的分辨率: {self.SUPPORTED_RESOLUTIONS}")
    
    def _validate_color_mode(self, mode):
        """验证颜色模式"""
        if mode.lower() not in self.SUPPORTED_COLOR_MODES:
            raise ValueError(f"不支持的颜色模式: {mode}. 支持的模式: {self.SUPPORTED_COLOR_MODES}")
    
    def _validate_paper_size(self, size):
        """验证纸张大小"""
        if size.upper() not in self.SUPPORTED_PAPER_SIZES:
            raise ValueError(f"不支持的纸张大小: {size}. 支持的大小: {self.SUPPORTED_PAPER_SIZES}")
    
    def _handle_scan_operation(self, operation_name, action):
        """处理扫描操作"""
        self.logger.info(f"执行扫描操作: {operation_name}")
        try:
            result = self.retry_action(action)
            if not result:
                raise ScanError(operation_name, "操作失败")
            return result
        except Exception as e:
            self.logger.error(f"{operation_name}失败: {str(e)}")
            self.take_screenshot(f"{operation_name}_failed")
            raise ScanError(operation_name, str(e))
    
    def start_scan(self):
        """开始扫描"""
        return self._handle_scan_operation(
            "开始扫描",
            lambda: self.wait_and_click(self._buttons['start'])
        )
    
    def stop_scan(self):
        """停止扫描"""
        return self._handle_scan_operation(
            "停止扫描",
            lambda: self.wait_and_click(self._buttons['stop'])
        )
    
    def open_preview(self):
        """打开预览"""
        return self._handle_scan_operation(
            "打开预览",
            lambda: self.wait_and_click(self._buttons['preview'])
        )
    
    def open_settings(self):
        """打开设置"""
        return self._handle_scan_operation(
            "打开设置",
            lambda: self.wait_and_click(self._buttons['settings'])
        )
    
    def select_scanner(self, scanner_name):
        """选择扫描仪"""
        self.logger.info(f"选择扫描仪: {scanner_name}")
        try:
            # 点击扫描仪下拉框
            if not self.wait_and_click(self._settings['scanner']):
                raise ElementNotFoundError("扫描仪下拉框")
            
            # 选择扫描仪选项
            option_key = f"{scanner_name.lower()}_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的扫描仪: {scanner_name}")
            
            if not self.wait_and_click(self.images[option_key]):
                raise ElementNotFoundError(f"{scanner_name}选项")
            
            return True
        except Exception as e:
            self.logger.error(f"选择扫描仪{scanner_name}失败")
            self.take_screenshot(f"select_scanner_{scanner_name}_failed")
            raise ScanError(f"选择扫描仪 {scanner_name}", str(e))
    
    def set_resolution(self, dpi):
        """设置扫描分辨率"""
        self.logger.info(f"设置扫描分辨率: {dpi} DPI")
        try:
            self._validate_resolution(dpi)
            
            # 点击分辨率下拉框
            if not self.wait_and_click(self._settings['resolution']):
                raise ElementNotFoundError("分辨率下拉框")
            
            # 选择分辨率选项
            if not self.wait_and_click(self._resolution_options[dpi]):
                raise ElementNotFoundError(f"{dpi} DPI选项")
            
            return True
        except Exception as e:
            self.logger.error(f"设置分辨率{dpi}失败")
            self.take_screenshot(f"set_resolution_{dpi}_failed")
            raise ScanError(f"设置分辨率 {dpi}", str(e))
    
    def set_color_mode(self, mode):
        """设置颜色模式"""
        self.logger.info(f"设置颜色模式: {mode}")
        try:
            self._validate_color_mode(mode)
            
            # 点击颜色模式下拉框
            if not self.wait_and_click(self._settings['color_mode']):
                raise ElementNotFoundError("颜色模式下拉框")
            
            # 选择颜色模式选项
            if not self.wait_and_click(self._color_mode_options[mode.lower()]):
                raise ElementNotFoundError(f"{mode}模式选项")
            
            return True
        except Exception as e:
            self.logger.error(f"设置颜色模式{mode}失败")
            self.take_screenshot(f"set_color_mode_{mode}_failed")
            raise ScanError(f"设置颜色模式 {mode}", str(e))
    
    def set_paper_size(self, size):
        """设置纸张大小"""
        self.logger.info(f"设置纸张大小: {size}")
        try:
            self._validate_paper_size(size)
            
            # 点击纸张大小下拉框
            if not self.wait_and_click(self._settings['paper_size']):
                raise ElementNotFoundError("纸张大小下拉框")
            
            # 选择纸张大小选项
            if not self.wait_and_click(self._paper_size_options[size.upper()]):
                raise ElementNotFoundError(f"{size}大小选项")
            
            return True
        except Exception as e:
            self.logger.error(f"设置纸张大小{size}失败")
            self.take_screenshot(f"set_paper_size_{size}_failed")
            raise ScanError(f"设置纸张大小 {size}", str(e))
    
    def preview_scan(self):
        """预览扫描"""
        return self._handle_scan_operation(
            "预览扫描",
            lambda: self.wait_and_click(self._buttons['preview'])
        )
    
    def is_preview_visible(self, timeout=DEFAULT_TIMEOUT):
        """检查预览窗口是否可见"""
        try:
            return self.wait_for_element(self._preview_elements['area'], timeout)
        except Exception as e:
            self.logger.error(f"检查预览窗口可见性失败: {str(e)}")
            return False
    
    def is_scan_complete(self, timeout=DEFAULT_TIMEOUT):
        """检查扫描是否完成"""
        try:
            return self.wait_for_element_disappear(self._preview_elements['progress'], timeout)
        except TimeoutError:
            self.logger.error("等待扫描完成超时")
            self.take_screenshot("scan_complete_timeout")
            return False
        except Exception as e:
            self.logger.error(f"检查扫描完成状态失败: {str(e)}")
            return False
    
    def perform_scan(self, scanner_name, resolution=300, color_mode='color', paper_size='A4', timeout=DEFAULT_TIMEOUT):
        """执行完整的扫描流程"""
        self.logger.info(f"执行扫描: 扫描仪={scanner_name}, 分辨率={resolution}DPI, 颜色模式={color_mode}, 纸张大小={paper_size}")
        try:
            # 验证参数
            self._validate_resolution(resolution)
            self._validate_color_mode(color_mode)
            self._validate_paper_size(paper_size)
            
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
            if not self.is_preview_visible(timeout):
                raise ScanError("扫描预览", "预览窗口未显示")
            
            # 开始扫描
            self.start_scan()
            
            # 等待扫描完成
            if not self.is_scan_complete(timeout):
                raise ScanError("扫描", "扫描超时")
            
            return True
        except Exception as e:
            self.logger.error("扫描流程失败")
            self.take_screenshot("perform_scan_failed")
            raise ScanError("扫描流程", str(e)) 