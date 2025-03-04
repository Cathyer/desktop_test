import os
import time
import cv2
import numpy as np
import pyautogui
from datetime import datetime
from .config import *
from .custom_logger import CustomLogger

class TestHelper:
    _logger = CustomLogger()
    
    @staticmethod
    def setup_logging():
        """配置日志系统"""
        # 日志系统现在由CustomLogger管理
        pass

    @staticmethod
    def take_screenshot(name):
        """
        截取屏幕截图并保存
        :param name: 截图名称
        :return: 截图文件路径
        """
        time.sleep(SCREENSHOT_DELAY)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            TestHelper._logger.log_step(f"截图保存: {filepath}")
            return filepath
        except Exception as e:
            TestHelper._logger.log_test_error("截图操作", str(e), "截图失败")
            raise

    @staticmethod
    def compare_images(image1_path, image2_path):
        """
        比较两张图片的相似度
        :param image1_path: 第一张图片路径
        :param image2_path: 第二张图片路径
        :return: 相似度得分 (0-1)
        """
        try:
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None or img2 is None:
                TestHelper._logger.log_test_error("图片比较", "无法读取图片文件", "文件读取错误")
                return 0
                
            # 确保两张图片尺寸相同
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                
            # 计算图片相似度
            diff = cv2.absdiff(img1, img2)
            diff_norm = np.sum(diff) / (img1.shape[0] * img1.shape[1] * img1.shape[2] * 255.0)
            similarity = 1 - diff_norm
            
            TestHelper._logger.log_assertion("图片相似度", f"{similarity:.4f}")
            return similarity
        except Exception as e:
            TestHelper._logger.log_test_error("图片比较", str(e), "比较失败")
            raise

    @staticmethod
    def find_element_on_screen(image_path, confidence=0.9, timeout=DEFAULT_TIMEOUT):
        """
        在屏幕上查找元素
        :param image_path: 要查找的图片路径
        :param confidence: 匹配置信度
        :param timeout: 超时时间（秒）
        :return: 元素位置 (x, y) 或 None
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location:
                    TestHelper._logger.log_step(f"查找元素: {image_path}", "成功")
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.5)
            
        TestHelper._logger.log_element_not_found(image_path, timeout)
        return None

    @staticmethod
    def click_element(image_path, confidence=0.9, timeout=DEFAULT_TIMEOUT):
        """
        点击屏幕上的元素
        :param image_path: 要点击的元素图片路径
        :param confidence: 匹配置信度
        :param timeout: 超时时间（秒）
        :return: 是否点击成功
        """
        try:
            location = TestHelper.find_element_on_screen(image_path, confidence, timeout)
            if location:
                pyautogui.click(location)
                TestHelper._logger.log_step(f"点击元素: {image_path}", "成功")
                return True
            return False
        except Exception as e:
            TestHelper._logger.log_test_error("点击元素", str(e), "点击失败")
            raise

    @staticmethod
    def wait_for_element(image_path, timeout=DEFAULT_TIMEOUT, confidence=0.9):
        """
        等待元素出现
        :param image_path: 要等待的元素图片路径
        :param timeout: 超时时间（秒）
        :param confidence: 匹配置信度
        :return: 是否找到元素
        """
        return TestHelper.find_element_on_screen(image_path, confidence, timeout) is not None 