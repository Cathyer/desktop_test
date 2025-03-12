import os
from desktop_test.pages.base_page import BasePage
from desktop_test.utils.test_helper import TestHelper
from desktop_test.utils.config import TEST_DATA_DIR, DEFAULT_TIMEOUT
from desktop_test.utils.custom_logger import CustomLogger
from desktop_test.utils.image_paths import ImagePaths
from desktop_test.utils.exceptions import FileOperationError, ElementNotFoundError, ElementNotVisibleError, TimeoutError
from desktop_test.utils.test_data import TestData

class FilePage(BasePage):
    """文件页面类，处理文件相关操作"""
    
    SUPPORTED_FILE_TYPES = ['txt', 'doc', 'pdf']
    
    def __init__(self):
        super().__init__()
        self.logger.info("初始化文件页面")
        self.images = ImagePaths()._paths['FILE']
        self.test_data = TestData()
        self._initialize_elements()
    
    def _initialize_elements(self):
        """初始化页面元素"""
        # 文件菜单项
        self._menu_items = {
            'new': self.images['new_file'],
            'open': self.images['open_file'],
            'save': self.images['save_file'],
            'save_as': self.images['save_as'],
            'close': self.images['close_file'],
            'exit': self.images['exit']
        }
        
        # 文件对话框元素
        self._dialog_elements = {
            'file_name': self.images['file_name_input'],
            'file_type': self.images['file_type_dropdown'],
            'save': self.images['save_button'],
            'cancel': self.images['cancel_button']
        }
        
        # 文件类型选项
        self._file_type_options = {
            'txt': self.images['txt_option'],
            'doc': self.images['doc_option'],
            'pdf': self.images['pdf_option']
        }
    
    def _validate_file_type(self, file_type):
        """验证文件类型"""
        if file_type.lower() not in self.SUPPORTED_FILE_TYPES:
            raise ValueError(f"不支持的文件类型: {file_type}. 支持的类型: {self.SUPPORTED_FILE_TYPES}")
    
    def _handle_file_operation(self, operation_name, action):
        """处理文件操作"""
        self.logger.info(f"执行文件操作: {operation_name}")
        try:
            result = self.retry_action(action)
            if not result:
                raise FileOperationError(operation_name, "", "操作失败")
            return result
        except Exception as e:
            self.logger.error(f"{operation_name}失败: {str(e)}")
            self.take_screenshot(f"{operation_name}_failed")
            raise FileOperationError(operation_name, "", str(e))
    
    def create_new_file(self):
        """创建新文件"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "file/new_file_button.png")):
                self.logger.info("点击新建文件按钮成功")
                return True
            self.logger.error("未找到新建文件按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("创建新文件", str(e))
            return False
    
    def input_file_name(self, file_name: str):
        """输入文件名
        
        Args:
            file_name: 文件名
        """
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "file/file_name_input.png")):
                self.type_text(file_name)
                self.logger.info(f"输入文件名成功: {file_name}")
                return True
            self.logger.error("未找到文件名输入框")
            return False
        except Exception as e:
            self.logger.log_test_error("输入文件名", str(e))
            return False
    
    def save_current_file(self):
        """保存当前文件"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "file/save_button.png")):
                self.logger.info("保存文件成功")
                return True
            self.logger.error("未找到保存按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("保存文件", str(e))
            return False
    
    def open_file(self, file_path: str):
        """打开文件
        
        Args:
            file_path: 文件路径
        """
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "file/open_button.png")):
                self.type_text(file_path)
                self.press_key('enter')
                self.logger.info(f"打开文件成功: {file_path}")
                return True
            self.logger.error("未找到打开按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("打开文件", str(e))
            return False
    
    def close_current_file(self):
        """关闭当前文件"""
        try:
            if self.click_element(os.path.join(TEST_DATA_DIR, "file/close_file_button.png")):
                self.logger.info("关闭文件成功")
                return True
            self.logger.error("未找到关闭文件按钮")
            return False
        except Exception as e:
            self.logger.log_test_error("关闭文件", str(e))
            return False
    
    def select_file_type(self, file_type):
        """选择文件类型"""
        self.logger.info(f"选择文件类型: {file_type}")
        try:
            self._validate_file_type(file_type)
            
            # 点击文件类型下拉框
            if not self.wait_and_click(self._dialog_elements['file_type']):
                raise ElementNotFoundError("文件类型下拉框")
            
            # 选择文件类型选项
            if not self.wait_and_click(self._file_type_options[file_type.lower()]):
                raise ElementNotFoundError(f"{file_type}选项")
            
            return True
        except Exception as e:
            self.logger.error(f"选择文件类型失败: {str(e)}")
            self.take_screenshot(f"select_file_type_{file_type}_failed")
            raise FileOperationError("选择文件类型", file_type, str(e))
    
    def click_save(self):
        """点击保存按钮"""
        return self._handle_file_operation(
            "点击保存",
            lambda: self.wait_and_click(self._dialog_elements['save'])
        )
    
    def click_cancel(self):
        """点击取消按钮"""
        return self._handle_file_operation(
            "点击取消",
            lambda: self.wait_and_click(self._dialog_elements['cancel'])
        )
    
    def is_file_dialog_visible(self, timeout=DEFAULT_TIMEOUT):
        """检查文件对话框是否可见"""
        try:
            return self.wait_for_element(self._dialog_elements['file_name'], timeout)
        except Exception as e:
            self.logger.error(f"检查文件对话框可见性失败: {str(e)}")
            return False
    
    def wait_for_file_dialog(self, timeout=DEFAULT_TIMEOUT):
        """等待文件对话框显示"""
        self.logger.info("等待文件对话框显示")
        try:
            dialog_elements = [
                self._dialog_elements['file_name'],
                self._dialog_elements['file_type'],
                self._dialog_elements['save']
            ]
            return self.wait_for_all_elements(dialog_elements, timeout)
        except TimeoutError:
            self.logger.error("等待文件对话框超时")
            self.take_screenshot("wait_for_file_dialog_timeout")
            return False
        except Exception as e:
            self.logger.error(f"等待文件对话框失败: {str(e)}")
            return False
    
    def create_new_file_with_content(self, file_name, content=None, timeout=DEFAULT_TIMEOUT):
        """创建新文件并输入内容"""
        self.logger.info(f"创建新文件并输入内容: {file_name}")
        try:
            # 获取文件类型
            file_type = file_name.split('.')[-1].lower()
            self._validate_file_type(file_type)
            
            # 创建新文件
            self.create_new_file()
            
            # 等待文件对话框显示
            if not self.wait_for_file_dialog(timeout):
                raise TimeoutError("等待文件对话框显示超时")
            
            # 输入文件名
            self.input_file_name(file_name)
            
            # 选择文件类型
            self.select_file_type(file_type)
            
            # 点击保存
            self.click_save()
            
            # 如果提供了内容，则输入内容
            if content:
                self.input_text(content)
                # 保存文件内容
                self.save_current_file()
            
            return True
        except Exception as e:
            self.logger.error("创建新文件并输入内容失败")
            self.take_screenshot("create_new_file_with_content_failed")
            raise FileOperationError("创建新文件并输入内容", file_name, str(e)) 