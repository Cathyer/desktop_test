import os
import magic

class FileValidator:
    """文件验证器类"""
    
    @staticmethod
    def is_valid_image(file_path):
        """验证是否为有效的图片文件"""
        if not os.path.exists(file_path):
            return False
        
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type.startswith('image/')
        except Exception:
            return False
    
    @staticmethod
    def is_valid_text(file_path):
        """验证是否为有效的文本文件"""
        if not os.path.exists(file_path):
            return False
        
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type.startswith('text/')
        except Exception:
            return False
    
    @staticmethod
    def is_valid_pdf(file_path):
        """验证是否为有效的PDF文件"""
        if not os.path.exists(file_path):
            return False
        
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type == 'application/pdf'
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path):
        """获取文件大小（字节）"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def get_file_extension(file_path):
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def is_file_empty(file_path):
        """检查文件是否为空"""
        return FileValidator.get_file_size(file_path) == 0 