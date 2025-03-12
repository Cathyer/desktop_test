import os
import magic
from desktop_test.utils.exceptions import ValidationError

class FileValidator:
    """文件验证器类"""
    
    _mime = None  # 缓存magic实例
    
    @classmethod
    def _get_mime(cls):
        """获取magic实例（单例模式）"""
        if cls._mime is None:
            cls._mime = magic.Magic(mime=True)
        return cls._mime
    
    @classmethod
    def validate_file_exists(cls, file_path):
        """验证文件是否存在"""
        if not os.path.exists(file_path):
            raise ValidationError(
                f"文件不存在: {file_path}",
                "file_exists",
                file_path
            )
    
    @classmethod
    def validate_file_readable(cls, file_path):
        """验证文件是否可读"""
        if not os.access(file_path, os.R_OK):
            raise ValidationError(
                f"文件不可读: {file_path}",
                "file_readable",
                file_path
            )
    
    @classmethod
    def validate_file_writable(cls, file_path):
        """验证文件是否可写"""
        if not os.access(file_path, os.W_OK):
            raise ValidationError(
                f"文件不可写: {file_path}",
                "file_writable",
                file_path
            )
    
    @classmethod
    def validate_file_size(cls, file_path, max_size=None):
        """验证文件大小"""
        size = cls.get_file_size(file_path)
        if max_size and size > max_size:
            raise ValidationError(
                f"文件大小超过限制: {size} > {max_size} 字节",
                "file_size",
                size
            )
        return size
    
    @classmethod
    def is_valid_image(cls, file_path):
        """验证是否为有效的图片文件"""
        try:
            cls.validate_file_exists(file_path)
            cls.validate_file_readable(file_path)
            file_type = cls._get_mime().from_file(file_path)
            return file_type.startswith('image/')
        except Exception:
            return False
    
    @classmethod
    def is_valid_text(cls, file_path):
        """验证是否为有效的文本文件"""
        try:
            cls.validate_file_exists(file_path)
            cls.validate_file_readable(file_path)
            file_type = cls._get_mime().from_file(file_path)
            return file_type.startswith('text/')
        except Exception:
            return False
    
    @classmethod
    def is_valid_pdf(cls, file_path):
        """验证是否为有效的PDF文件"""
        try:
            cls.validate_file_exists(file_path)
            cls.validate_file_readable(file_path)
            file_type = cls._get_mime().from_file(file_path)
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
    
    @classmethod
    def is_file_empty(cls, file_path):
        """检查文件是否为空"""
        return cls.get_file_size(file_path) == 0
        
    @classmethod
    def validate_file_type(cls, file_path, expected_type):
        """验证文件类型
        
        Args:
            file_path: 文件路径
            expected_type: 期望的文件类型（'image', 'text', 'pdf'）
        """
        validators = {
            'image': cls.is_valid_image,
            'text': cls.is_valid_text,
            'pdf': cls.is_valid_pdf
        }
        
        if expected_type not in validators:
            raise ValueError(f"不支持的文件类型: {expected_type}")
            
        if not validators[expected_type](file_path):
            raise ValidationError(
                f"文件类型不匹配: {file_path}",
                "file_type",
                expected_type
            ) 