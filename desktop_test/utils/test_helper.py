import os
import sys
import time
import cv2
import numpy as np
import pyautogui
import pyperclip
import pytesseract
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from functools import lru_cache
from desktop_test.utils.config import *
from desktop_test.utils.custom_logger import CustomLogger
from desktop_test.utils.exceptions import (
    ElementNotFoundError,
    ElementNotVisibleError,
    ImageMatchError,
    TimeoutError
)
from PIL import Image

class TestHelper:
    """测试辅助类，提供UI自动化测试所需的各种功能"""
    
    _logger = CustomLogger()
    _image_cache: Dict[str, Any] = {}
    _last_found_positions: Dict[str, Tuple[int, int]] = {}
    
    def __init__(self):
        self.logger = CustomLogger(self.__class__.__name__)
    
    @staticmethod
    def setup_logging():
        """配置日志系统"""
        # 使用CustomLogger的单例模式，不需要额外配置
        pass
    
    @staticmethod
    @lru_cache(maxsize=100)
    def _load_image(image_path: str) -> Optional[np.ndarray]:
        """加载并缓存图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            np.ndarray: 图片数据
        """
        try:
            if image_path not in TestHelper._image_cache:
                image = cv2.imread(image_path)
                if image is None:
                    raise ImageMatchError(f"无法加载图片: {image_path}")
                TestHelper._image_cache[image_path] = image
            return TestHelper._image_cache[image_path]
        except Exception as e:
            TestHelper._logger.log_test_error("加载图片", str(e), f"加载失败: {image_path}")
            return None
    
    @staticmethod
    def take_screenshot(name: str, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """截取屏幕截图并保存
        
        Args:
            name: 截图名称
            region: 截图区域 (left, top, width, height)
            
        Returns:
            str: 截图文件路径
        """
        time.sleep(SCREENSHOT_DELAY)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        
        try:
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(filepath)
            TestHelper._logger.log_step(f"截图保存: {filepath}")
            return filepath
        except Exception as e:
            TestHelper._logger.log_test_error("截图操作", str(e), "截图失败")
            raise
    
    @staticmethod
    def compare_images(
        image1_path: str,
        image2_path: str,
        threshold: float = 0.95
    ) -> Tuple[float, Optional[np.ndarray]]:
        """比较两张图片的相似度
        
        Args:
            image1_path: 第一张图片路径
            image2_path: 第二张图片路径
            threshold: 相似度阈值
            
        Returns:
            Tuple[float, Optional[np.ndarray]]: (相似度得分, 差异图)
        """
        try:
            img1 = TestHelper._load_image(image1_path)
            img2 = TestHelper._load_image(image2_path)
            
            if img1 is None or img2 is None:
                raise ImageMatchError("无法读取图片文件")
                
            # 确保两张图片尺寸相同
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                
            # 计算图片相似度
            diff = cv2.absdiff(img1, img2)
            diff_norm = np.sum(diff) / (img1.shape[0] * img1.shape[1] * img1.shape[2] * 255.0)
            similarity = 1 - diff_norm
            
            # 生成差异图
            if similarity < threshold:
                diff_img = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, diff_img = cv2.threshold(diff_img, 30, 255, cv2.THRESH_BINARY)
            else:
                diff_img = None
            
            TestHelper._logger.log_assertion("图片相似度", f"{similarity:.4f}")
            return similarity, diff_img
        except Exception as e:
            TestHelper._logger.log_test_error("图片比较", str(e), "比较失败")
            raise
    
    @staticmethod
    def find_element_on_screen(
        image_path: str,
        confidence: float = 0.8,
        timeout: float = DEFAULT_TIMEOUT,
        region: Optional[Tuple[int, int, int, int]] = None,
        use_last_position: bool = True
    ) -> Optional[Tuple[int, int]]:
        """在屏幕上查找元素
        
        Args:
            image_path: 要查找的图片路径
            confidence: 匹配置信度
            timeout: 超时时间（秒）
            region: 搜索区域 (left, top, width, height)
            use_last_position: 是否使用上次找到的位置
            
        Returns:
            Optional[Tuple[int, int]]: 元素位置 (x, y) 或 None
        """
        if not os.path.exists(image_path):
            raise ElementNotFoundError(f"图片文件不存在: {image_path}", timeout)
            
        # 如果启用了上次位置，先在上次位置附近搜索
        if use_last_position and image_path in TestHelper._last_found_positions:
            last_x, last_y = TestHelper._last_found_positions[image_path]
            search_region = (
                max(0, last_x - 50),
                max(0, last_y - 50),
                100,
                100
            )
            try:
                location = pyautogui.locateCenterOnScreen(
                    image_path,
                    confidence=confidence,
                    region=search_region
                )
                if location:
                    TestHelper._last_found_positions[image_path] = location
                    TestHelper._logger.log_step(f"在上次位置找到元素: {image_path}")
                    return location
            except:
                pass
        
        # 在指定区域或全屏搜索
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateCenterOnScreen(
                    image_path,
                    confidence=confidence,
                    region=region
                )
                if location:
                    TestHelper._last_found_positions[image_path] = location
                    TestHelper._logger.log_step(f"查找元素: {image_path}", "成功")
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                TestHelper._logger.log_test_error("查找元素", str(e), f"查找失败: {image_path}")
                return None
            time.sleep(0.2)
            
        raise ElementNotFoundError(f"未找到元素: {image_path}", timeout)
    
    @staticmethod
    def click_element(
        image_path: str,
        confidence: float = 0.8,
        timeout: float = DEFAULT_TIMEOUT,
        region: Optional[Tuple[int, int, int, int]] = None,
        clicks: int = 1,
        interval: float = 0.25,
        button: str = 'left'
    ) -> bool:
        """点击屏幕上的元素
        
        Args:
            image_path: 要点击的元素图片路径
            confidence: 匹配置信度
            timeout: 超时时间（秒）
            region: 搜索区域
            clicks: 点击次数
            interval: 点击间隔
            button: 鼠标按键 ('left', 'right', 'middle')
            
        Returns:
            bool: 是否点击成功
        """
        try:
            location = TestHelper.find_element_on_screen(
                image_path,
                confidence,
                timeout,
                region
            )
            if location:
                pyautogui.click(
                    location,
                    clicks=clicks,
                    interval=interval,
                    button=button
                )
                TestHelper._logger.log_step(f"点击元素: {image_path}", "成功")
                return True
            return False
        except Exception as e:
            TestHelper._logger.log_test_error("点击元素", str(e), "点击失败")
            raise
    
    @staticmethod
    def wait_for_element(
        image_path: str,
        timeout: float = DEFAULT_TIMEOUT,
        confidence: float = 0.8,
        region: Optional[Tuple[int, int, int, int]] = None,
        check_interval: float = 0.2
    ) -> bool:
        """等待元素出现
        
        Args:
            image_path: 要等待的元素图片路径
            timeout: 超时时间（秒）
            confidence: 匹配置信度
            region: 搜索区域
            check_interval: 检查间隔
            
        Returns:
            bool: 是否找到元素
        """
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if TestHelper.element_exists(image_path, confidence, region):
                    return True
                time.sleep(check_interval)
            raise TimeoutError("等待元素超时", timeout)
        except Exception as e:
            TestHelper._logger.log_test_error("等待元素", str(e), "等待失败")
            return False
    
    @staticmethod
    def element_exists(
        image_path: str,
        confidence: float = 0.8,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """检查元素是否存在（不等待）
        
        Args:
            image_path: 要查找的元素图片路径
            confidence: 匹配置信度
            region: 搜索区域
            
        Returns:
            bool: 元素是否存在
        """
        try:
            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=confidence,
                region=region
            )
            return location is not None
        except:
            return False
    
    @staticmethod
    def drag_and_drop(
        source_image_path: str,
        target_image_path: str,
        source_offset: Tuple[int, int] = (0, 0),
        target_offset: Tuple[int, int] = (0, 0),
        duration: float = 0.5
    ) -> bool:
        """拖放操作
        
        Args:
            source_image_path: 源元素图片路径
            target_image_path: 目标元素图片路径
            source_offset: 源元素偏移量 (x, y)
            target_offset: 目标元素偏移量 (x, y)
            duration: 拖动持续时间
            
        Returns:
            bool: 是否成功
        """
        try:
            # 查找源元素
            source_location = TestHelper.find_element_on_screen(source_image_path)
            if not source_location:
                raise ElementNotFoundError(f"未找到源元素: {source_image_path}", DEFAULT_TIMEOUT)
                
            # 查找目标元素
            target_location = TestHelper.find_element_on_screen(target_image_path)
            if not target_location:
                raise ElementNotFoundError(f"未找到目标元素: {target_image_path}", DEFAULT_TIMEOUT)
            
            # 计算实际位置
            source_x = source_location[0] + source_offset[0]
            source_y = source_location[1] + source_offset[1]
            target_x = target_location[0] + target_offset[0]
            target_y = target_location[1] + target_offset[1]
            
            # 执行拖放
            pyautogui.moveTo(source_x, source_y)
            pyautogui.mouseDown()
            pyautogui.moveTo(target_x, target_y, duration=duration)
            pyautogui.mouseUp()
            
            TestHelper._logger.log_step(
                f"拖放操作: {source_image_path} -> {target_image_path}",
                "成功"
            )
            return True
        except Exception as e:
            TestHelper._logger.log_test_error("拖放操作", str(e), "拖放失败")
            raise
    
    @staticmethod
    def type_text(
        text: str,
        interval: float = 0.1,
        press_enter: bool = False
    ) -> None:
        """输入文本
        
        Args:
            text: 要输入的文本
            interval: 输入间隔
            press_enter: 是否按回车键
        """
        try:
            pyautogui.write(text, interval=interval)
            if press_enter:
                pyautogui.press('enter')
            TestHelper._logger.log_step(f"输入文本: {text}", "成功")
        except Exception as e:
            TestHelper._logger.log_test_error("输入文本", str(e), "输入失败")
            raise
    
    @staticmethod
    def press_key(
        key: str,
        presses: int = 1,
        interval: float = 0.1
    ) -> None:
        """按键操作
        
        Args:
            key: 按键名称
            presses: 按键次数
            interval: 按键间隔
        """
        try:
            pyautogui.press(key, presses=presses, interval=interval)
            TestHelper._logger.log_step(f"按键操作: {key} x {presses}", "成功")
        except Exception as e:
            TestHelper._logger.log_test_error("按键操作", str(e), "按键失败")
            raise
    
    @staticmethod
    def clear_image_cache() -> None:
        """清除图片缓存"""
        TestHelper._image_cache.clear()
        TestHelper._last_found_positions.clear()
        TestHelper._load_image.cache_clear()

    @staticmethod
    def double_click_element(image_path, confidence=0.8, timeout=DEFAULT_TIMEOUT):
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
                TestHelper._logger.log_step(f"拖动元素: {image_path}")
            else:
                raise Exception(f"未找到元素: {image_path}")
        except Exception as e:
            TestHelper._logger.log_test_error("拖动元素", str(e), "拖动失败")
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
                TestHelper._logger.log_step(f"滚动元素: {image_path}, 方向: {direction}, 距离: {scroll_amount}")
            else:
                raise Exception(f"未找到元素: {image_path}")
        except Exception as e:
            TestHelper._logger.log_test_error("滚动元素", str(e), "滚动失败")
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
            matched = location is not None
            if matched:
                TestHelper._logger.log_step(f"图片匹配: {image_path}", "成功")
            else:
                TestHelper._logger.log_step(f"图片匹配: {image_path}", "未匹配")
            return matched
        except Exception as e:
            TestHelper._logger.log_test_error("图片匹配", str(e), "匹配失败")
            return False

    @staticmethod
    def write_text(text):
        """输入文本
        
        Args:
            text: 要输入的文本
        """
        try:
            pyautogui.write(text)
            TestHelper._logger.log_step(f"输入文本: {text}")
        except Exception as e:
            TestHelper._logger.log_test_error("输入文本", str(e), "输入失败")
            raise

    @staticmethod
    def key_press(key):
        """按下按键
        
        Args:
            key: 按键名称
        """
        try:
            pyautogui.keyDown(key)
            TestHelper._logger.log_step(f"按下按键: {key}")
        except Exception as e:
            TestHelper._logger.log_test_error("按下按键", str(e), "按键失败")
            raise

    @staticmethod
    def key_release(key):
        """释放按键
        
        Args:
            key: 按键名称
        """
        try:
            pyautogui.keyUp(key)
            TestHelper._logger.log_step(f"释放按键: {key}")
        except Exception as e:
            TestHelper._logger.log_test_error("释放按键", str(e), "释放失败")
            raise

def create_directory(directory):
    """创建目录"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"已创建目录: {directory}")
    return directory

def setup_test_environment():
    """设置测试环境"""
    # 创建必要的目录
    create_directory(TEST_DATA_DIR)
    create_directory(SCREENSHOTS_DIR)
    create_directory(LOGS_DIR)
    create_directory(REPORTS_DIR)
    
    # 创建测试数据子目录
    create_directory(os.path.join(TEST_DATA_DIR, "common"))
    create_directory(os.path.join(TEST_DATA_DIR, "toolbar"))
    create_directory(os.path.join(TEST_DATA_DIR, "file_list"))
    create_directory(os.path.join(TEST_DATA_DIR, "ocr"))
    create_directory(os.path.join(TEST_DATA_DIR, "scan"))

if __name__ == "__main__":
    setup_test_environment() 