from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import IMAGE_SIMILARITY_THRESHOLD, DEFAULT_TIMEOUT
from desktop_test.utils.exceptions import ElementNotFoundError, ElementNotVisibleError, TimeoutError
from desktop_test.utils.custom_logger import CustomLogger
import time
import os
import pyautogui

class BasePage:
    """基础页面类，提供通用的页面操作方法"""
    
    def __init__(self):
        self.test_helper = TestHelper()
        self.logger = CustomLogger(self.__class__.__name__)
        self.screenshot_dir = os.path.join(os.getcwd(), "test_results", "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
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

    def take_screenshot(self, name):
        """截取当前屏幕"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            self.logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
            return None

    def retry_action(self, action, max_retries=3, retry_interval=1):
        """重试执行操作"""
        for i in range(max_retries):
            try:
                result = action()
                if result:
                    return result
            except Exception as e:
                self.logger.warning(f"第{i+1}次尝试失败: {str(e)}")
                if i < max_retries - 1:
                    time.sleep(retry_interval)
                else:
                    raise
        return False

    def wait_and_click(self, image_path, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """等待元素出现并点击"""
        if self.wait_for_element(image_path, timeout, similarity):
            return self.click_element(image_path, timeout, similarity)
        raise ElementNotFoundError(f"等待点击元素失败: {image_path}")

    def wait_for_any_element(self, image_paths, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """等待多个元素中的任意一个出现"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            for image_path in image_paths:
                if self.is_element_visible(image_path, 1, similarity):
                    return image_path
            time.sleep(0.5)
        raise TimeoutError(f"等待元素超时: {image_paths}")

    def wait_for_all_elements(self, image_paths, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """等待所有元素出现"""
        start_time = time.time()
        found_elements = set()
        while time.time() - start_time < timeout:
            for image_path in image_paths:
                if image_path not in found_elements and self.is_element_visible(image_path, 1, similarity):
                    found_elements.add(image_path)
            if len(found_elements) == len(image_paths):
                return True
            time.sleep(0.5)
        raise TimeoutError(f"等待元素超时: {set(image_paths) - found_elements}")

    def verify_element_state(self, image_path, expected_state, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """验证元素状态"""
        if expected_state == "visible":
            return self.wait_for_element(image_path, timeout, similarity)
        elif expected_state == "invisible":
            return self.wait_for_element_disappear(image_path, timeout, similarity)
        elif expected_state == "enabled":
            return self.is_element_enabled(image_path, timeout, similarity)
        else:
            raise ValueError(f"不支持的元素状态: {expected_state}")

    def scroll_to_element(self, image_path, direction="down", max_scrolls=10, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """滚动到元素位置"""
        for _ in range(max_scrolls):
            if self.is_element_visible(image_path, 1, similarity):
                return True
            if direction == "down":
                pyautogui.scroll(-100)
            else:
                pyautogui.scroll(100)
            time.sleep(0.5)
        raise ElementNotFoundError(f"滚动查找元素失败: {image_path}")

    def drag_and_drop(self, source_image, target_image, timeout=DEFAULT_TIMEOUT, similarity=IMAGE_SIMILARITY_THRESHOLD):
        """拖拽元素"""
        source_pos = self.get_element_position(source_image, timeout, similarity)
        target_pos = self.get_element_position(target_image, timeout, similarity)
        
        if not source_pos or not target_pos:
            raise ElementNotFoundError("未找到源元素或目标元素")
            
        pyautogui.moveTo(source_pos[0], source_pos[1])
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.moveTo(target_pos[0], target_pos[1], duration=1)
        time.sleep(0.5)
        pyautogui.mouseUp()
        return True 