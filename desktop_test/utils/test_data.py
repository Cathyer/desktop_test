import os
import json
import logging
import fcntl
from typing import Dict, Any, Optional
from desktop_test.utils.exceptions import ValidationError
from desktop_test.utils.file_validator import FileValidator
from desktop_test.utils.config import TEST_DATA_DIR

logger = logging.getLogger(__name__)

class TestData:
    """测试数据管理类"""
    
    _instance = None
    _data_cache = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestData, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """初始化测试数据管理器"""
        self.test_data_file = os.path.join(TEST_DATA_DIR, 'test_data.json')
        self._data_schemas = {
            'file': {
                'required': ['test_file', 'new_file', 'save_as_file', 'file_content'],
                'types': {
                    'test_file': str,
                    'new_file': str,
                    'save_as_file': str,
                    'file_content': str
                }
            },
            'ocr': {
                'required': ['test_image', 'output_file', 'languages', 'accuracies', 'output_formats'],
                'types': {
                    'test_image': str,
                    'output_file': str,
                    'languages': list,
                    'accuracies': list,
                    'output_formats': list
                }
            },
            'scan': {
                'required': ['output_file', 'resolutions', 'color_modes', 'paper_sizes'],
                'types': {
                    'output_file': str,
                    'resolutions': list,
                    'color_modes': list,
                    'paper_sizes': list
                }
            },
            'calculator': {
                'required': ['basic_operations', 'advanced_operations'],
                'types': {
                    'basic_operations': list,
                    'advanced_operations': list
                }
            }
        }
        self._load_test_data()
    
    def _validate_data(self, category: str, data: Dict[str, Any]) -> None:
        """验证测试数据格式
        
        Args:
            category: 数据类别
            data: 待验证的数据
            
        Raises:
            ValidationError: 数据格式无效
        """
        if category not in self._data_schemas:
            raise ValidationError(f"无效的数据类别: {category}", "category", category)
            
        schema = self._data_schemas[category]
        
        # 检查必需字段
        for field in schema['required']:
            if field not in data:
                raise ValidationError(
                    f"缺少必需字段: {field}",
                    "missing_field",
                    field
                )
        
        # 检查字段类型
        for field, expected_type in schema['types'].items():
            if field in data and not isinstance(data[field], expected_type):
                raise ValidationError(
                    f"字段类型错误: {field}",
                    "field_type",
                    {'field': field, 'expected': expected_type.__name__, 'actual': type(data[field]).__name__}
                )
    
    def _load_test_data(self) -> None:
        """加载测试数据"""
        try:
            FileValidator.validate_file_exists(self.test_data_file)
            FileValidator.validate_file_readable(self.test_data_file)
            
            with open(self.test_data_file, 'r', encoding='utf-8') as f:
                # 获取文件锁
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                    # 验证所有类别的数据
                    for category, category_data in data.items():
                        self._validate_data(category, category_data)
                    self._data_cache = data
                finally:
                    # 释放文件锁
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    
        except FileNotFoundError:
            logger.warning(f"测试数据文件不存在: {self.test_data_file}")
            self._data_cache = {}
        except json.JSONDecodeError as e:
            logger.error(f"测试数据文件格式错误: {e}")
            raise ValidationError("测试数据文件格式错误", "json_format", str(e))
        except Exception as e:
            logger.error(f"加载测试数据失败: {e}")
            raise
    
    def _get_category_data(self, category: str, default: Optional[Dict] = None) -> Dict:
        """获取指定类别的测试数据
        
        Args:
            category: 数据类别
            default: 默认数据
            
        Returns:
            Dict: 测试数据
        """
        if self._data_cache is None:
            self._load_test_data()
        return self._data_cache.get(category, default or {})
    
    def get_file_test_data(self) -> Dict:
        """获取文件测试数据"""
        return self._get_category_data('file', {
            'test_file': 'test.txt',
            'new_file': 'new.txt',
            'save_as_file': 'save_as.txt',
            'file_content': '测试文件内容'
        })
    
    def get_ocr_test_data(self) -> Dict:
        """获取OCR测试数据"""
        return self._get_category_data('ocr', {
            'test_image': 'test_image.png',
            'output_file': 'output.txt',
            'languages': ['chinese', 'english'],
            'accuracies': [0.5, 0.7, 0.9],
            'output_formats': ['txt', 'doc', 'pdf']
        })
    
    def get_scan_test_data(self) -> Dict:
        """获取扫描测试数据"""
        return self._get_category_data('scan', {
            'output_file': 'output.pdf',
            'resolutions': [100, 200, 300],
            'color_modes': ['color', 'gray', 'bw'],
            'paper_sizes': ['a4', 'a3', 'letter']
        })
    
    def get_calculator_test_data(self) -> Dict:
        """获取计算器测试数据"""
        return self._get_category_data('calculator', {
            'basic_operations': [
                {'operation': '1+1', 'expected': '2'},
                {'operation': '2-1', 'expected': '1'},
                {'operation': '2*3', 'expected': '6'},
                {'operation': '6/2', 'expected': '3'}
            ],
            'advanced_operations': [
                {'operation': '1+2*3', 'expected': '7'},
                {'operation': '(1+2)*3', 'expected': '9'},
                {'operation': '2^3', 'expected': '8'}
            ]
        })
    
    def update_test_data(self, category: str, data: Dict) -> None:
        """更新测试数据
        
        Args:
            category: 数据类别
            data: 新的测试数据
        """
        # 验证数据格式
        self._validate_data(category, data)
        
        try:
            FileValidator.validate_file_exists(self.test_data_file)
            FileValidator.validate_file_writable(self.test_data_file)
            
            with open(self.test_data_file, 'r+', encoding='utf-8') as f:
                # 获取文件锁
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    # 读取现有数据
                    current_data = json.load(f)
                    # 更新数据
                    current_data[category] = data
                    # 重置文件指针
                    f.seek(0)
                    f.truncate()
                    # 写入新数据
                    json.dump(current_data, f, ensure_ascii=False, indent=4)
                    # 更新缓存
                    self._data_cache = current_data
                finally:
                    # 释放文件锁
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    
        except Exception as e:
            logger.error(f"更新测试数据失败: {e}")
            raise
    
    @classmethod
    def instance(cls) -> 'TestData':
        """获取单例实例"""
        return cls() 