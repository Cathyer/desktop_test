import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import TEST_DATA_DIR
from desktop_test.utils.custom_logger import CustomLogger
from desktop_test.utils.image_paths import ImagePaths
from desktop_test.utils.exceptions import FileOperationError, ElementNotFoundError, ElementNotVisibleError
from desktop_test.utils.test_data import TestData

class FilePage(BasePage):
    """文件操作页面类"""
    
    def __init__(self):
        super().__init__()
        self.images = ImagePaths.FILE
        self.test_data = TestData()
        # 文件菜单项
        self.new_file = os.path.join(TEST_DATA_DIR, 'file_list', 'new_file.png')
        self.open_file = os.path.join(TEST_DATA_DIR, 'file_list', 'open_file.png')
        self.save_file = os.path.join(TEST_DATA_DIR, 'file_list', 'save_file.png')
        self.save_as = os.path.join(TEST_DATA_DIR, 'file_list', 'save_as.png')
        self.close_file = os.path.join(TEST_DATA_DIR, 'file_list', 'close_file.png')
        self.exit = os.path.join(TEST_DATA_DIR, 'file_list', 'exit.png')
        
        # 文件对话框元素
        self.file_name_input = os.path.join(TEST_DATA_DIR, 'file_list', 'file_name_input.png')
        self.file_type_dropdown = os.path.join(TEST_DATA_DIR, 'file_list', 'file_type_dropdown.png')
        self.save_button = os.path.join(TEST_DATA_DIR, 'file_list', 'save_button.png')
        self.cancel_button = os.path.join(TEST_DATA_DIR, 'file_list', 'cancel_button.png')
        
        # 文件类型选项
        self.txt_option = os.path.join(TEST_DATA_DIR, 'file_list', 'txt_option.png')
        self.doc_option = os.path.join(TEST_DATA_DIR, 'file_list', 'doc_option.png')
        self.pdf_option = os.path.join(TEST_DATA_DIR, 'file_list', 'pdf_option.png')
    
    def create_new_file(self):
        """创建新文件"""
        self.logger.info("创建新文件")
        try:
            if not self.click_element(self.images['new_file']):
                raise ElementNotFoundError("新建文件按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("创建新文件", "", str(e))
    
    def open_existing_file(self):
        """打开现有文件"""
        self.logger.info("打开现有文件")
        try:
            if not self.click_element(self.images['open_file']):
                raise ElementNotFoundError("打开文件按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("打开文件", "", str(e))
    
    def save_current_file(self):
        """保存当前文件"""
        self.logger.info("保存当前文件")
        try:
            if not self.click_element(self.images['save_file']):
                raise ElementNotFoundError("保存按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("保存文件", "", str(e))
    
    def save_file_as(self):
        """另存为"""
        self.logger.info("另存为")
        try:
            if not self.click_element(self.images['save_as']):
                raise ElementNotFoundError("另存为按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("另存为", "", str(e))
    
    def close_current_file(self):
        """关闭当前文件"""
        self.logger.info("关闭当前文件")
        try:
            if not self.click_element(self.images['close_file']):
                raise ElementNotFoundError("关闭文件按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("关闭文件", "", str(e))
    
    def exit_application(self):
        """退出应用程序"""
        self.logger.info("退出应用程序")
        try:
            if not self.click_element(self.images['exit']):
                raise ElementNotFoundError("退出按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("退出应用", "", str(e))
    
    def input_file_name(self, file_name):
        """输入文件名"""
        self.logger.info(f"输入文件名: {file_name}")
        try:
            if not self.is_element_visible(self.images['file_name_input']):
                raise ElementNotVisibleError("文件名输入框")
            return self.input_text(file_name)
        except Exception as e:
            raise FileOperationError("输入文件名", file_name, str(e))
    
    def select_file_type(self, file_type):
        """选择文件类型"""
        self.logger.info(f"选择文件类型: {file_type}")
        try:
            if not self.click_element(self.images['file_type_dropdown']):
                raise ElementNotFoundError("文件类型下拉框", self.timeout)
            
            option_key = f"{file_type.lower()}_option"
            if option_key not in self.images:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
            if not self.click_element(self.images[option_key]):
                raise ElementNotFoundError(f"{file_type}选项", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("选择文件类型", file_type, str(e))
    
    def click_save(self):
        """点击保存按钮"""
        self.logger.info("点击保存按钮")
        try:
            if not self.click_element(self.images['save_button']):
                raise ElementNotFoundError("保存按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("点击保存", "", str(e))
    
    def click_cancel(self):
        """点击取消按钮"""
        self.logger.info("点击取消按钮")
        try:
            if not self.click_element(self.images['cancel_button']):
                raise ElementNotFoundError("取消按钮", self.timeout)
            return True
        except Exception as e:
            raise FileOperationError("点击取消", "", str(e))
    
    def is_file_dialog_visible(self):
        """检查文件对话框是否可见"""
        try:
            return self.is_element_visible(self.images['file_name_input'])
        except Exception as e:
            self.logger.error(f"检查文件对话框可见性失败: {str(e)}")
            return False
    
    def create_new_file_with_content(self, file_name, content=None):
        """创建新文件并输入内容"""
        self.logger.info(f"创建新文件并输入内容: {file_name}")
        try:
            # 创建新文件
            self.create_new_file()
            
            # 输入文件名
            self.input_file_name(file_name)
            
            # 选择文件类型
            file_type = file_name.split('.')[-1].lower()
            self.select_file_type(file_type)
            
            # 点击保存
            self.click_save()
            
            # 如果提供了内容，则输入内容
            if content:
                self.input_text(content)
            
            return True
        except Exception as e:
            raise FileOperationError("创建新文件并输入内容", file_name, str(e)) 