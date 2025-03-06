from loguru import logger
from utils.test_helper import TestHelper
from utils.config import IMAGE_SIMILARITY_THRESHOLD, DEFAULT_TIMEOUT

class BasePage:
    """基础页面类，提供通用的页面操作方法"""
    
    def __init__(self):
        self.test_helper = TestHelper()
        self.logger = logger
    
    def find_element(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """查找元素"""
        return self.test_helper.find_element(image_path, timeout, similarity)
    
    def click_element(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """点击元素"""
        return self.test_helper.click_element(image_path, timeout, similarity)
    
    def input_text(self, text):
        """输入文本"""
        return self.test_helper.input_text(text)
    
    def press_key(self, key):
        """按下按键"""
        return self.test_helper.press_key(key)
    
    def mouse_slide(self, start_x, start_y, end_x, end_y, duration=0.5):
        """鼠标滑动"""
        return self.test_helper.mouse_slide(start_x, start_y, end_x, end_y, duration)
    
    def wait_for_element(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """等待元素出现"""
        return self.test_helper.wait_for_element(image_path, timeout, similarity)
    
    def wait_for_element_disappear(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """等待元素消失"""
        return self.test_helper.wait_for_element_disappear(image_path, timeout, similarity)
    
    def get_element_position(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """获取元素位置"""
        return self.test_helper.get_element_position(image_path, timeout, similarity)
    
    def get_element_text(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """获取元素文本"""
        return self.test_helper.get_element_text(image_path, timeout, similarity)
    
    def is_element_visible(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """检查元素是否可见"""
        return self.test_helper.is_element_visible(image_path, timeout, similarity)
    
    def is_element_enabled(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """检查元素是否可用"""
        return self.test_helper.is_element_enabled(image_path, timeout, similarity) 