class DesktopTestError(Exception):
    """桌面测试基础异常类"""
    pass

class ElementNotFoundError(DesktopTestError):
    """元素未找到异常"""
    def __init__(self, element_name, timeout):
        self.element_name = element_name
        self.timeout = timeout
        super().__init__(f"未找到元素: {element_name}, 超时时间: {timeout}秒")

class ElementNotVisibleError(DesktopTestError):
    """元素不可见异常"""
    def __init__(self, element_name):
        self.element_name = element_name
        super().__init__(f"元素不可见: {element_name}")

class ElementNotEnabledError(DesktopTestError):
    """元素不可用异常"""
    def __init__(self, element_name):
        self.element_name = element_name
        super().__init__(f"元素不可用: {element_name}")

class FileOperationError(DesktopTestError):
    """文件操作异常"""
    def __init__(self, operation, file_path, error_msg):
        self.operation = operation
        self.file_path = file_path
        self.error_msg = error_msg
        super().__init__(f"文件操作失败: {operation}, 文件路径: {file_path}, 错误信息: {error_msg}")

class OCRError(DesktopTestError):
    """OCR操作异常"""
    def __init__(self, operation, error_msg):
        self.operation = operation
        self.error_msg = error_msg
        super().__init__(f"OCR操作失败: {operation}, 错误信息: {error_msg}")

class ScanError(DesktopTestError):
    """扫描操作异常"""
    def __init__(self, operation, error_msg):
        self.operation = operation
        self.error_msg = error_msg
        super().__init__(f"扫描操作失败: {operation}, 错误信息: {error_msg}") 