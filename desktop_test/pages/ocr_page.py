import os
from .base_page import BasePage
from utils.image_paths import ImagePaths
from utils.exceptions import OCRError, ElementNotFoundError, ElementNotVisibleError
from utils.test_data import TestData

class OCRPage(BasePage):
    """OCR页面类"""
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.OCR
        self.test_data = TestData()
        # OCR功能按钮
        self.start_button = os.path.join(TEST_DATA_DIR, 'ocr', 'start_button.png')
        self.stop_button = os.path.join(TEST_DATA_DIR, 'ocr', 'stop_button.png')
        self.settings_button = os.path.join(TEST_DATA_DIR, 'ocr', 'settings_button.png')
        
        # OCR设置选项
        self.language_dropdown = os.path.join(TEST_DATA_DIR, 'ocr', 'language_dropdown.png')
        self.accuracy_slider = os.path.join(TEST_DATA_DIR, 'ocr', 'accuracy_slider.png')
        self.output_format_dropdown = os.path.join(TEST_DATA_DIR, 'ocr', 'output_format_dropdown.png')
        
        # 语言选项
        self.chinese_option = os.path.join(TEST_DATA_DIR, 'ocr', 'chinese_option.png')
        self.english_option = os.path.join(TEST_DATA_DIR, 'ocr', 'english_option.png')
        
        # 输出格式选项
        self.txt_option = os.path.join(TEST_DATA_DIR, 'ocr', 'txt_option.png')
        self.doc_option = os.path.join(TEST_DATA_DIR, 'ocr', 'doc_option.png')
        self.pdf_option = os.path.join(TEST_DATA_DIR, 'ocr', 'pdf_option.png')
        
        # 结果区域
        self.result_area = os.path.join(TEST_DATA_DIR, 'ocr', 'result_area.png')
        self.progress_bar = os.path.join(TEST_DATA_DIR, 'ocr', 'progress_bar.png')
    
    def start_ocr(self):
        """开始OCR识别"""
        self.logger.info("开始OCR识别")
        try:
            if not self.click_element(self.images['start_button']):
                raise ElementNotFoundError("开始按钮", self.timeout)
            return True
        except Exception as e:
            raise OCRError("开始OCR识别", str(e))
    
    def stop_ocr(self):
        """停止OCR识别"""
        self.logger.info("停止OCR识别")
        try:
            if not self.click_element(self.images['stop_button']):
                raise ElementNotFoundError("停止按钮", self.timeout)
            return True
        except Exception as e:
            raise OCRError("停止OCR识别", str(e))
    
    def open_settings(self):
        """打开设置"""
        self.logger.info("打开设置")
        try:
            if not self.click_element(self.images['settings_button']):
                raise ElementNotFoundError("设置按钮", self.timeout)
            return True
        except Exception as e:
            raise OCRError("打开设置", str(e))
    
    def select_language(self, language):
        """选择识别语言"""
        self.logger.info(f"选择识别语言: {language}")
        try:
            if not self.click_element(self.images['language_dropdown']):
                raise ElementNotFoundError("语言下拉框", self.timeout)
            
            option_key = f"{language.lower()}_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的语言: {language}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{language}选项", self.timeout)
            return True
        except Exception as e:
            raise OCRError(f"选择语言 {language}", str(e))
    
    def set_accuracy(self, value):
        """设置识别精度"""
        self.logger.info(f"设置识别精度: {value}")
        try:
            if not self.is_element_visible(self.images['accuracy_slider']):
                raise ElementNotVisibleError("精度滑块")
            
            # 获取滑块位置
            slider_pos = self.get_element_position(self.images['accuracy_slider'])
            if not slider_pos:
                raise ElementNotFoundError("精度滑块", self.timeout)
            
            # 计算目标位置
            target_x = slider_pos[0] + int(value * slider_pos[2])
            
            # 滑动到目标位置
            if not self.mouse_slide(slider_pos[0], slider_pos[1], target_x, slider_pos[1]):
                raise OCRError("设置精度", "滑块移动失败")
            return True
        except Exception as e:
            raise OCRError(f"设置精度 {value}", str(e))
    
    def select_output_format(self, format_type):
        """选择输出格式"""
        self.logger.info(f"选择输出格式: {format_type}")
        try:
            if not self.click_element(self.images['output_format_dropdown']):
                raise ElementNotFoundError("输出格式下拉框", self.timeout)
            
            option_key = f"{format_type.lower()}_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的输出格式: {format_type}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{format_type}选项", self.timeout)
            return True
        except Exception as e:
            raise OCRError(f"选择输出格式 {format_type}", str(e))
    
    def get_result_text(self):
        """获取识别结果"""
        self.logger.info("获取识别结果")
        try:
            if not self.is_element_visible(self.images['result_area']):
                raise ElementNotVisibleError("结果区域")
            return self.get_element_text(self.images['result_area'])
        except Exception as e:
            raise OCRError("获取识别结果", str(e))
    
    def is_progress_complete(self):
        """检查进度是否完成"""
        try:
            return self.wait_for_element_disappear(self.images['progress_bar'])
        except Exception as e:
            self.logger.error(f"检查进度完成状态失败: {str(e)}")
            return False
    
    def is_ocr_window_visible(self):
        """检查OCR窗口是否可见"""
        try:
            return self.is_element_visible(self.images['start_button'])
        except Exception as e:
            self.logger.error(f"检查OCR窗口可见性失败: {str(e)}")
            return False
    
    def perform_ocr(self, language='chinese', accuracy=0.7, output_format='txt'):
        """执行完整的OCR识别流程"""
        self.logger.info(f"执行OCR识别: 语言={language}, 精度={accuracy}, 输出格式={output_format}")
        try:
            # 选择语言
            self.select_language(language)
            
            # 设置精度
            self.set_accuracy(accuracy)
            
            # 选择输出格式
            self.select_output_format(output_format)
            
            # 开始识别
            self.start_ocr()
            
            # 等待识别完成
            if not self.is_progress_complete():
                raise OCRError("OCR识别", "识别未完成")
            
            # 获取结果
            result = self.get_result_text()
            if not result:
                raise OCRError("OCR识别", "未获取到识别结果")
            
            return result
        except Exception as e:
            raise OCRError("OCR识别流程", str(e)) 