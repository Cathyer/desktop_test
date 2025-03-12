import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.image_paths import ImagePaths
from desktop_test.utils.exceptions import ElementNotFoundError, ElementNotVisibleError
from desktop_test.utils.config import *

class MainPage(BasePage):
    """主页面类，处理主界面的操作"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("初始化主页面")
        self.images = ImagePaths()._paths['MAIN']
        self._menu_items = {
            'file': self.images['file_menu'],
            'edit': self.images['edit_menu'],
            'view': self.images['view_menu'],
            'tools': self.images['tools_menu'],
            'help': self.images['help_menu']
        }
        self._toolbar_buttons = {
            'new': self.images['new_button'],
            'open': self.images['open_button'],
            'save': self.images['save_button'],
            'print': self.images['print_button'],
            'calculator': self.images['calculator_icon'],
            'ocr': self.images['ocr_button'],
            'scan': self.images['scan_button']
        }
    
    def click_menu(self, menu_name):
        """点击菜单项"""
        self.logger.info(f"点击{menu_name}菜单")
        if menu_name not in self._menu_items:
            raise ValueError(f"不支持的菜单项: {menu_name}")
        try:
            if not self.wait_and_click(self._menu_items[menu_name]):
                raise ElementNotFoundError(f"{menu_name}菜单", self.timeout)
            return True
        except Exception as e:
            self.logger.error(f"点击{menu_name}菜单失败: {str(e)}")
            self.take_screenshot(f"click_menu_{menu_name}_failed")
            raise
    
    def click_toolbar(self, button_name):
        """点击工具栏按钮"""
        self.logger.info(f"点击{button_name}按钮")
        if button_name not in self._toolbar_buttons:
            raise ValueError(f"不支持的工具栏按钮: {button_name}")
        try:
            if not self.wait_and_click(self._toolbar_buttons[button_name]):
                raise ElementNotFoundError(f"{button_name}按钮", self.timeout)
            return True
        except Exception as e:
            self.logger.error(f"点击{button_name}按钮失败: {str(e)}")
            self.take_screenshot(f"click_toolbar_{button_name}_failed")
            raise
    
    def verify_menu_state(self, menu_name, expected_state="enabled"):
        """验证菜单项状态"""
        self.logger.info(f"验证{menu_name}菜单状态: {expected_state}")
        if menu_name not in self._menu_items:
            raise ValueError(f"不支持的菜单项: {menu_name}")
        try:
            return self.verify_element_state(self._menu_items[menu_name], expected_state)
        except Exception as e:
            self.logger.error(f"验证{menu_name}菜单状态失败: {str(e)}")
            self.take_screenshot(f"verify_menu_{menu_name}_{expected_state}_failed")
            raise
    
    def verify_toolbar_state(self, button_name, expected_state="enabled"):
        """验证工具栏按钮状态"""
        self.logger.info(f"验证{button_name}按钮状态: {expected_state}")
        if button_name not in self._toolbar_buttons:
            raise ValueError(f"不支持的工具栏按钮: {button_name}")
        try:
            return self.verify_element_state(self._toolbar_buttons[button_name], expected_state)
        except Exception as e:
            self.logger.error(f"验证{button_name}按钮状态失败: {str(e)}")
            self.take_screenshot(f"verify_toolbar_{button_name}_{expected_state}_failed")
            raise
    
    def wait_for_main_window(self, timeout=None):
        """等待主窗口显示"""
        self.logger.info("等待主窗口显示")
        try:
            menu_images = list(self._menu_items.values())
            return self.wait_for_all_elements(menu_images, timeout)
        except Exception as e:
            self.logger.error(f"等待主窗口显示失败: {str(e)}")
            self.take_screenshot("wait_for_main_window_failed")
            raise
    
    def is_main_window_visible(self):
        """检查主窗口是否可见"""
        try:
            return self.element_exists(os.path.join(TEST_DATA_DIR, "common/main_window.png"))
        except Exception as e:
            self.logger.log_test_error("检查主窗口", str(e))
            return False
    
    def open_feature(self, feature_name):
        """打开特定功能"""
        self.logger.info(f"打开{feature_name}功能")
        try:
            if feature_name == "calculator":
                return self.click_toolbar("calculator")
            elif feature_name == "ocr":
                return self.click_toolbar("ocr")
            elif feature_name == "scan":
                return self.click_toolbar("scan")
            else:
                raise ValueError(f"不支持的功能: {feature_name}")
        except Exception as e:
            self.logger.error(f"打开{feature_name}功能失败: {str(e)}")
            self.take_screenshot(f"open_feature_{feature_name}_failed")
            raise
    
    def verify_feature_available(self, feature_name):
        """验证特定功能是否可用"""
        self.logger.info(f"验证{feature_name}功能是否可用")
        try:
            if feature_name == "calculator":
                return self.verify_toolbar_state("calculator")
            elif feature_name == "ocr":
                return self.verify_toolbar_state("ocr")
            elif feature_name == "scan":
                return self.verify_toolbar_state("scan")
            else:
                raise ValueError(f"不支持的功能: {feature_name}")
        except Exception as e:
            self.logger.error(f"验证{feature_name}功能可用性失败: {str(e)}")
            self.take_screenshot(f"verify_feature_{feature_name}_failed")
            raise
    
    def open_file_page(self):
        """打开文件页面"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "common/file_button.png")):
                self.logger.info("打开文件页面成功")
                return True
            self.logger.error("未找到文件按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("打开文件页面", str(e))
            return False
    
    def open_ocr(self):
        """打开OCR页面"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "common/ocr_button.png")):
                self.logger.info("打开OCR页面成功")
                return True
            self.logger.error("未找到OCR按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("打开OCR页面", str(e))
            return False
    
    def open_scan(self):
        """打开扫描页面"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "common/scan_button.png")):
                self.logger.info("打开扫描页面成功")
                return True
            self.logger.error("未找到扫描按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("打开扫描页面", str(e))
            return False
    
    def close_application(self):
        """关闭应用程序"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "common/close_button.png")):
                self.logger.info("关闭应用程序成功")
                return True
            self.logger.error("未找到关闭按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("关闭应用程序", str(e))
            return False 