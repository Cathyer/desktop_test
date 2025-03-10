import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.image_paths import ImagePaths

class MainPage(BasePage):
    """主页面类"""
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.MAIN
        
    def click_file_menu(self):
        """点击文件菜单"""
        self.logger.info("点击文件菜单")
        return self.click_element(self.images['file_menu'])
    
    def click_edit_menu(self):
        """点击编辑菜单"""
        self.logger.info("点击编辑菜单")
        return self.click_element(self.images['edit_menu'])
    
    def click_view_menu(self):
        """点击视图菜单"""
        self.logger.info("点击视图菜单")
        return self.click_element(self.images['view_menu'])
    
    def click_tools_menu(self):
        """点击工具菜单"""
        self.logger.info("点击工具菜单")
        return self.click_element(self.images['tools_menu'])
    
    def click_help_menu(self):
        """点击帮助菜单"""
        self.logger.info("点击帮助菜单")
        return self.click_element(self.images['help_menu'])
    
    def click_new(self):
        """点击新建按钮"""
        self.logger.info("点击新建按钮")
        return self.click_element(self.images['new_button'])
    
    def click_open(self):
        """点击打开按钮"""
        self.logger.info("点击打开按钮")
        return self.click_element(self.images['open_button'])
    
    def click_save(self):
        """点击保存按钮"""
        self.logger.info("点击保存按钮")
        return self.click_element(self.images['save_button'])
    
    def click_print(self):
        """点击打印按钮"""
        self.logger.info("点击打印按钮")
        return self.click_element(self.images['print_button'])
    
    def open_calculator(self):
        """打开计算器"""
        self.logger.info("打开计算器")
        return self.click_element(self.images['calculator_icon'])
    
    def open_ocr(self):
        """打开OCR功能"""
        self.logger.info("打开OCR功能")
        return self.click_element(self.images['ocr_button'])
    
    def open_scan(self):
        """打开扫描功能"""
        self.logger.info("打开扫描功能")
        return self.click_element(self.images['scan_button'])
    
    def is_main_window_visible(self):
        """检查主窗口是否可见"""
        return self.is_element_visible(self.images['file_menu']) 