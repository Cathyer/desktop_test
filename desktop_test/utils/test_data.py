import os
import json
from desktop_test.utils.config import TEST_DATA_DIR

class TestData:
    """测试数据管理类"""
    
    def __init__(self):
        self.test_data_file = os.path.join(TEST_DATA_DIR, 'test_data.json')
        self.test_data = self._load_test_data()
    
    def _load_test_data(self):
        """加载测试数据"""
        if os.path.exists(self.test_data_file):
            with open(self.test_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_file_test_data(self):
        """获取文件测试数据"""
        return self.test_data.get('file', {
            'test_file': 'test.txt',
            'new_file': 'new.txt',
            'save_as_file': 'save_as.txt',
            'file_content': '测试文件内容'
        })
    
    def get_ocr_test_data(self):
        """获取OCR测试数据"""
        return self.test_data.get('ocr', {
            'test_image': 'test_image.png',
            'output_file': 'output.txt',
            'languages': ['chinese', 'english'],
            'accuracies': [0.5, 0.7, 0.9],
            'output_formats': ['txt', 'doc', 'pdf']
        })
    
    def get_scan_test_data(self):
        """获取扫描测试数据"""
        return self.test_data.get('scan', {
            'output_file': 'output.pdf',
            'resolutions': [100, 200, 300],
            'color_modes': ['color', 'gray', 'bw'],
            'paper_sizes': ['a4', 'a3', 'letter']
        })
    
    def get_calculator_test_data(self):
        """获取计算器测试数据"""
        return self.test_data.get('calculator', {
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
    
    def update_test_data(self, category, data):
        """更新测试数据"""
        self.test_data[category] = data
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4) 