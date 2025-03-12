class DesktopTestError(Exception):
    """桌面测试基础异常类"""
    def __init__(self, message, details=None):
        self.details = details
        super().__init__(message)

class ElementNotFoundError(DesktopTestError):
    """元素未找到异常"""
    def __init__(self, element_name, timeout):
        message = f"未找到元素: {element_name}"
        details = {
            "元素名称": element_name,
            "超时时间": f"{timeout}秒"
        }
        super().__init__(message, details)

class ElementNotVisibleError(DesktopTestError):
    """元素不可见异常"""
    def __init__(self, element_name):
        message = f"元素不可见: {element_name}"
        details = {"元素名称": element_name}
        super().__init__(message, details)

class ElementNotEnabledError(DesktopTestError):
    """元素不可用异常"""
    def __init__(self, element_name):
        message = f"元素不可用: {element_name}"
        details = {"元素名称": element_name}
        super().__init__(message, details)

class FileOperationError(DesktopTestError):
    """文件操作异常"""
    def __init__(self, operation, file_path, error_msg):
        message = f"文件操作失败: {operation}"
        details = {
            "操作类型": operation,
            "文件路径": file_path,
            "错误信息": error_msg
        }
        super().__init__(message, details)

class OCRError(DesktopTestError):
    """OCR操作异常"""
    def __init__(self, operation, error_msg):
        message = f"OCR操作失败: {operation}"
        details = {
            "操作类型": operation,
            "错误信息": error_msg
        }
        super().__init__(message, details)

class ScanError(DesktopTestError):
    """扫描操作异常"""
    def __init__(self, operation, error_msg):
        message = f"扫描操作失败: {operation}"
        details = {
            "操作类型": operation,
            "错误信息": error_msg
        }
        super().__init__(message, details)

class ImageMatchError(DesktopTestError):
    """图片匹配异常"""
    def __init__(self, image_path, similarity=None, threshold=None):
        message = f"图片匹配失败: {image_path}"
        details = {
            "图片路径": image_path,
            "实际相似度": f"{similarity:.2f}" if similarity is not None else "未知",
            "匹配阈值": f"{threshold:.2f}" if threshold is not None else "未知"
        }
        super().__init__(message, details)

class TimeoutError(DesktopTestError):
    """超时异常"""
    def __init__(self, operation, timeout):
        message = f"操作超时: {operation}"
        details = {
            "操作类型": operation,
            "超时时间": f"{timeout}秒"
        }
        super().__init__(message, details)

class ValidationError(DesktopTestError):
    """验证异常"""
    def __init__(self, message, validation_type, value):
        details = {
            "验证类型": validation_type,
            "验证值": value
        }
        super().__init__(message, details) 