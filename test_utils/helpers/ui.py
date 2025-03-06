import os
import time
import cv2
import numpy as np
import pyautogui
from datetime import datetime
from .config import *
from .custom_logger import CustomLogger
from PIL import Image
from loguru import logger

class TestHelper:
    _logger = CustomLogger()
    
    @staticmethod
    def setup_logging():
        """配置日志系统"""
        # 日志系统现在由CustomLogger管理
        logger.add(
            os.path.join(LOGS_DIR, "test_{time}.log"),
            rotation="500 MB",
            retention="10 days",
            level="INFO"
        )

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

    @staticmethod
    def double_click_element(image_path, confidence=0.9, timeout=DEFAULT_TIMEOUT):
        """
        双击屏幕上的元素
        :param image_path: 要双击的元素图片路径
        :param confidence: 匹配置信度
        :param timeout: 超时时间（秒）
        :return: 是否双击成功
        """
        try:
            location = TestHelper.find_element_on_screen(image_path, confidence, timeout)
            if location:
                pyautogui.doubleClick(location)
                TestHelper._logger.log_step(f"双击元素: {image_path}", "成功")
                return True
            return False
        except Exception as e:
            TestHelper._logger.log_test_error("双击元素", str(e), "双击失败")
            raise

    @staticmethod
    def element_exists(image_path, confidence=0.9):
        """
        检查元素是否存在（不等待）
        :param image_path: 要查找的元素图片路径
        :param confidence: 匹配置信度
        :return: 元素是否存在
        """
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            return location is not None
        except pyautogui.ImageNotFoundException:
            return False

    @staticmethod
    def click_and_drag(image_path, start_x, start_y, end_x, end_y, duration=0.5):
        """点击并拖动
        
        Args:
            image_path: 元素图片路径
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 拖动持续时间
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                # 计算相对于图片的坐标
                rel_start_x = location.left + start_x
                rel_start_y = location.top + start_y
                rel_end_x = location.left + end_x
                rel_end_y = location.top + end_y
                
                # 执行拖动
                pyautogui.moveTo(rel_start_x, rel_start_y)
                pyautogui.mouseDown()
                pyautogui.moveTo(rel_end_x, rel_end_y, duration=duration)
                pyautogui.mouseUp()
                logger.info(f"拖动元素: {image_path}")
            else:
                raise Exception(f"未找到元素: {image_path}")
        except Exception as e:
            logger.error(f"拖动元素失败: {str(e)}")
            raise

    @staticmethod
    def scroll_element(image_path, scroll_amount, direction='down', duration=0.5):
        """滚动元素
        
        Args:
            image_path: 元素图片路径
            scroll_amount: 滚动距离
            direction: 滚动方向（'up' 或 'down'）
            duration: 滚动持续时间
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                # 计算滚动方向
                if direction.lower() == 'up':
                    scroll_amount = -scroll_amount
                
                # 移动到元素中心
                center = pyautogui.center(location)
                pyautogui.moveTo(center)
                
                # 执行滚动
                pyautogui.scroll(scroll_amount)
                logger.info(f"滚动元素: {image_path}, 方向: {direction}, 距离: {scroll_amount}")
            else:
                raise Exception(f"未找到元素: {image_path}")
        except Exception as e:
            logger.error(f"滚动元素失败: {str(e)}")
            raise

    @staticmethod
    def drag_and_drop(source_image_path, target_image_path, duration=0.5):
        """拖放操作
        
        Args:
            source_image_path: 源元素图片路径
            target_image_path: 目标元素图片路径
            duration: 拖动持续时间
        """
        try:
            # 查找源元素
            source_location = pyautogui.locateOnScreen(source_image_path, confidence=0.8)
            if not source_location:
                raise Exception(f"未找到源元素: {source_image_path}")
            
            # 查找目标元素
            target_location = pyautogui.locateOnScreen(target_image_path, confidence=0.8)
            if not target_location:
                raise Exception(f"未找到目标元素: {target_image_path}")
            
            # 执行拖放
            source_center = pyautogui.center(source_location)
            target_center = pyautogui.center(target_location)
            
            pyautogui.moveTo(source_center)
            pyautogui.mouseDown()
            pyautogui.moveTo(target_center, duration=duration)
            pyautogui.mouseUp()
            
            logger.info(f"拖放操作: 从 {source_image_path} 到 {target_image_path}")
        except Exception as e:
            logger.error(f"拖放操作失败: {str(e)}")
            raise

    @staticmethod
    def match_image(image_path, threshold=0.8):
        """匹配图片
        
        Args:
            image_path: 图片路径
            threshold: 匹配阈值
            
        Returns:
            bool: 是否匹配
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=threshold)
            return location is not None
        except Exception as e:
            logger.error(f"图片匹配失败: {str(e)}")
            return False

    @staticmethod
    def write_text(text):
        """输入文本
        
        Args:
            text: 要输入的文本
        """
        try:
            pyautogui.write(text)
            logger.info(f"输入文本: {text}")
        except Exception as e:
            logger.error(f"输入文本失败: {str(e)}")
            raise

    @staticmethod
    def key_press(key):
        """按下按键
        
        Args:
            key: 按键名称
        """
        try:
            pyautogui.keyDown(key)
            logger.info(f"按下按键: {key}")
        except Exception as e:
            logger.error(f"按下按键失败: {str(e)}")
            raise

    @staticmethod
    def key_release(key):
        """释放按键
        
        Args:
            key: 按键名称
        """
        try:
            pyautogui.keyUp(key)
            logger.info(f"释放按键: {key}")
        except Exception as e:
            logger.error(f"释放按键失败: {str(e)}")
            raise 