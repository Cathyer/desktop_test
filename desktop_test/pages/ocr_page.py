import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.image_paths import ImagePaths
from desktop_test.utils.exceptions import OCRError, ElementNotFoundError, ElementNotVisibleError, TimeoutError
from desktop_test.utils.test_data import TestData
from desktop_test.utils.config import DEFAULT_TIMEOUT, TEST_DATA_DIR

class OCRPage(BasePage):
    """OCR页面类"""
    
    SUPPORTED_LANGUAGES = ['chinese', 'english']
    SUPPORTED_OUTPUT_FORMATS = ['txt', 'doc', 'pdf']
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.OCR
        self.test_data = TestData()
        self._initialize_elements()
    
    def _initialize_elements(self):
        """初始化页面元素"""
        # OCR功能按钮
        self._buttons = {
            'start': self.images['start_button'],
            'stop': self.images['stop_button'],
            'settings': self.images['settings_button']
        }
        
        # OCR设置选项
        self._settings = {
            'language': self.images['language_dropdown'],
            'accuracy': self.images['accuracy_slider'],
            'output_format': self.images['output_format_dropdown']
        }
        
        # 语言选项
        self._language_options = {
            'chinese': self.images['chinese_option'],
            'english': self.images['english_option']
        }
        
        # 输出格式选项
        self._format_options = {
            'txt': self.images['txt_option'],
            'doc': self.images['doc_option'],
            'pdf': self.images['pdf_option']
        }
        
        # 结果区域
        self._result_elements = {
            'area': self.images['result_area'],
            'progress': self.images['progress_bar']
        }
    
    def _validate_language(self, language):
        """验证语言选项"""
        if language.lower() not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"不支持的语言: {language}. 支持的语言: {self.SUPPORTED_LANGUAGES}")
    
    def _validate_output_format(self, format_type):
        """验证输出格式"""
        if format_type.lower() not in self.SUPPORTED_OUTPUT_FORMATS:
            raise ValueError(f"不支持的输出格式: {format_type}. 支持的格式: {self.SUPPORTED_OUTPUT_FORMATS}")
    
    def start_ocr(self):
        """开始OCR识别"""
        self.logger.info("开始OCR识别")
        try:
            return self.retry_action(
                lambda: self.wait_and_click(self._buttons['start'])
            )
        except Exception as e:
            self.logger.error("开始OCR识别失败")
            self.take_screenshot("start_ocr_failed")
            raise OCRError("开始OCR识别", str(e))
    
    def stop_ocr(self):
        """停止OCR识别"""
        self.logger.info("停止OCR识别")
        try:
            return self.retry_action(
                lambda: self.wait_and_click(self._buttons['stop'])
            )
        except Exception as e:
            self.logger.error("停止OCR识别失败")
            self.take_screenshot("stop_ocr_failed")
            raise OCRError("停止OCR识别", str(e))
    
    def open_settings(self):
        """打开设置"""
        self.logger.info("打开设置")
        try:
            return self.retry_action(
                lambda: self.wait_and_click(self._buttons['settings'])
            )
        except Exception as e:
            self.logger.error("打开设置失败")
            self.take_screenshot("open_settings_failed")
            raise OCRError("打开设置", str(e))
    
    def select_language(self, language):
        """选择识别语言"""
        self.logger.info(f"选择识别语言: {language}")
        try:
            self._validate_language(language)
            
            # 点击语言下拉框
            if not self.wait_and_click(self._settings['language']):
                raise ElementNotFoundError("语言下拉框")
            
            # 选择语言选项
            if not self.wait_and_click(self._language_options[language.lower()]):
                raise ElementNotFoundError(f"{language}选项")
            
            return True
        except Exception as e:
            self.logger.error(f"选择语言{language}失败")
            self.take_screenshot(f"select_language_{language}_failed")
            raise OCRError(f"选择语言 {language}", str(e))
    
    def set_accuracy(self, value):
        """设置识别精度"""
        self.logger.info(f"设置识别精度: {value}")
        try:
            if not 0 <= value <= 1:
                raise ValueError("精度值必须在0到1之间")
            
            # 获取滑块位置
            slider_pos = self.get_element_position(self._settings['accuracy'])
            if not slider_pos:
                raise ElementNotFoundError("精度滑块")
            
            # 计算目标位置
            target_x = slider_pos[0] + int(value * slider_pos[2])
            
            # 滑动到目标位置
            return self.retry_action(
                lambda: self.mouse_slide(slider_pos[0], slider_pos[1], target_x, slider_pos[1])
            )
        except Exception as e:
            self.logger.error(f"设置精度{value}失败")
            self.take_screenshot(f"set_accuracy_{value}_failed")
            raise OCRError(f"设置精度 {value}", str(e))
    
    def select_output_format(self, format_type):
        """选择输出格式"""
        self.logger.info(f"选择输出格式: {format_type}")
        try:
            self._validate_output_format(format_type)
            
            # 点击输出格式下拉框
            if not self.wait_and_click(self._settings['output_format']):
                raise ElementNotFoundError("输出格式下拉框")
            
            # 选择输出格式选项
            if not self.wait_and_click(self._format_options[format_type.lower()]):
                raise ElementNotFoundError(f"{format_type}选项")
            
            return True
        except Exception as e:
            self.logger.error(f"选择输出格式{format_type}失败")
            self.take_screenshot(f"select_output_format_{format_type}_failed")
            raise OCRError(f"选择输出格式 {format_type}", str(e))
    
    def get_result_text(self):
        """获取识别结果"""
        self.logger.info("获取识别结果")
        try:
            if not self.wait_for_element(self._result_elements['area']):
                raise ElementNotVisibleError("结果区域")
            return self.get_element_text(self._result_elements['area'])
        except Exception as e:
            self.logger.error("获取识别结果失败")
            self.take_screenshot("get_result_text_failed")
            raise OCRError("获取识别结果", str(e))
    
    def is_progress_complete(self, timeout=DEFAULT_TIMEOUT):
        """检查进度是否完成"""
        try:
            return self.wait_for_element_disappear(self._result_elements['progress'], timeout)
        except TimeoutError:
            self.logger.error("等待进度完成超时")
            self.take_screenshot("progress_complete_timeout")
            return False
        except Exception as e:
            self.logger.error(f"检查进度完成状态失败: {str(e)}")
            return False
    
    def is_ocr_window_visible(self):
        """检查OCR窗口是否可见"""
        try:
            return self.wait_for_element(self._buttons['start'])
        except Exception as e:
            self.logger.error(f"检查OCR窗口可见性失败: {str(e)}")
            return False
    
    def perform_ocr(self, language='chinese', accuracy=0.7, output_format='txt', timeout=DEFAULT_TIMEOUT):
        """执行完整的OCR识别流程"""
        self.logger.info(f"执行OCR识别: 语言={language}, 精度={accuracy}, 输出格式={output_format}")
        try:
            # 验证参数
            self._validate_language(language)
            self._validate_output_format(output_format)
            if not 0 <= accuracy <= 1:
                raise ValueError("精度值必须在0到1之间")
            
            # 选择语言
            self.select_language(language)
            
            # 设置精度
            self.set_accuracy(accuracy)
            
            # 选择输出格式
            self.select_output_format(output_format)
            
            # 开始识别
            self.start_ocr()
            
            # 等待识别完成
            if not self.is_progress_complete(timeout):
                raise OCRError("OCR识别", "识别超时")
            
            # 获取结果
            result = self.get_result_text()
            if not result:
                raise OCRError("OCR识别", "未获取到识别结果")
            
            return result
        except Exception as e:
            self.logger.error("OCR识别流程失败")
            self.take_screenshot("perform_ocr_failed")
            raise OCRError("OCR识别流程", str(e)) 