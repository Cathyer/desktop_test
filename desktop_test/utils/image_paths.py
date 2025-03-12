import os
from desktop_test.utils.config import TEST_DATA_DIR
from desktop_test.utils.file_validator import FileValidator

class ImagePaths:
    """图像路径管理类"""
    
    _instance = None
    _paths = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImagePaths, cls).__new__(cls)
            cls._instance._initialize_paths()
        return cls._instance
    
    def _initialize_paths(self):
        """初始化图片路径"""
        # 主页面图片
        self._paths['MAIN'] = {
            'file_menu': self._get_common_path('file_menu.png'),
            'edit_menu': self._get_common_path('edit_menu.png'),
            'view_menu': self._get_common_path('view_menu.png'),
            'tools_menu': self._get_common_path('tools_menu.png'),
            'help_menu': self._get_common_path('help_menu.png'),
            'new_button': self._get_toolbar_path('new_button.png'),
            'open_button': self._get_toolbar_path('open_button.png'),
            'save_button': self._get_toolbar_path('save_button.png'),
            'print_button': self._get_toolbar_path('print_button.png'),
            'ocr_button': self._get_toolbar_path('ocr_button.png'),
            'scan_button': self._get_toolbar_path('scan_button.png')
        }
        
        # 文件操作页面图片
        self._paths['FILE'] = {
            'new_file': self._get_file_list_path('new_file.png'),
            'open_file': self._get_file_list_path('open_file.png'),
            'save_file': self._get_file_list_path('save_file.png'),
            'save_as': self._get_file_list_path('save_as.png'),
            'close_file': self._get_file_list_path('close_file.png'),
            'exit': self._get_file_list_path('exit.png'),
            'file_name_input': self._get_file_list_path('file_name_input.png'),
            'file_type_dropdown': self._get_file_list_path('file_type_dropdown.png'),
            'save_button': self._get_file_list_path('save_button.png'),
            'cancel_button': self._get_file_list_path('cancel_button.png'),
            'txt_option': self._get_file_list_path('txt_option.png'),
            'doc_option': self._get_file_list_path('doc_option.png'),
            'pdf_option': self._get_file_list_path('pdf_option.png')
        }
        
        # OCR页面图片
        self._paths['OCR'] = {
            'start_button': self._get_ocr_path('start_button.png'),
            'stop_button': self._get_ocr_path('stop_button.png'),
            'settings_button': self._get_ocr_path('settings_button.png'),
            'language_dropdown': self._get_ocr_path('language_dropdown.png'),
            'accuracy_slider': self._get_ocr_path('accuracy_slider.png'),
            'output_format_dropdown': self._get_ocr_path('output_format_dropdown.png'),
            'chinese_option': self._get_ocr_path('chinese_option.png'),
            'english_option': self._get_ocr_path('english_option.png'),
            'txt_option': self._get_ocr_path('txt_option.png'),
            'doc_option': self._get_ocr_path('doc_option.png'),
            'pdf_option': self._get_ocr_path('pdf_option.png'),
            'result_area': self._get_ocr_path('result_area.png'),
            'progress_bar': self._get_ocr_path('progress_bar.png')
        }
        
        # 扫描页面图片
        self._paths['SCAN'] = {
            'start_button': self._get_scan_path('start_button.png'),
            'stop_button': self._get_scan_path('stop_button.png'),
            'preview_button': self._get_scan_path('preview_button.png'),
            'settings_button': self._get_scan_path('settings_button.png'),
            'resolution_dropdown': self._get_scan_path('resolution_dropdown.png'),
            'color_mode_dropdown': self._get_scan_path('color_mode_dropdown.png'),
            'paper_size_dropdown': self._get_scan_path('paper_size_dropdown.png'),
            'resolution_100': self._get_scan_path('resolution_100.png'),
            'resolution_200': self._get_scan_path('resolution_200.png'),
            'resolution_300': self._get_scan_path('resolution_300.png'),
            'color_mode_color': self._get_scan_path('color_mode_color.png'),
            'color_mode_gray': self._get_scan_path('color_mode_gray.png'),
            'color_mode_bw': self._get_scan_path('color_mode_bw.png'),
            'paper_size_a4': self._get_scan_path('paper_size_a4.png'),
            'paper_size_a3': self._get_scan_path('paper_size_a3.png'),
            'paper_size_letter': self._get_scan_path('paper_size_letter.png'),
            'preview_area': self._get_scan_path('preview_area.png'),
            'progress_bar': self._get_scan_path('progress_bar.png')
        }
        
        # 验证所有图片路径
        self._validate_paths()
    
    def _validate_paths(self):
        """验证所有图片路径"""
        for category, paths in self._paths.items():
            for name, path in paths.items():
                if not FileValidator.is_valid_image(path):
                    raise ValueError(f"无效的图片路径: {category}.{name} -> {path}")
    
    def _get_common_path(self, filename):
        """获取通用图片路径"""
        return os.path.join(TEST_DATA_DIR, 'common', filename)
    
    def _get_toolbar_path(self, filename):
        """获取工具栏图片路径"""
        return os.path.join(TEST_DATA_DIR, 'toolbar', filename)
    
    def _get_file_list_path(self, filename):
        """获取文件列表图片路径"""
        return os.path.join(TEST_DATA_DIR, 'file_list', filename)
    
    def _get_ocr_path(self, filename):
        """获取OCR图片路径"""
        return os.path.join(TEST_DATA_DIR, 'ocr', filename)
    
    def _get_scan_path(self, filename):
        """获取扫描图片路径"""
        return os.path.join(TEST_DATA_DIR, 'scan', filename)
    
    def get_path(self, category, name):
        """获取图片路径
        
        Args:
            category: 类别（'MAIN', 'FILE', 'OCR', 'SCAN'）
            name: 图片名称
            
        Returns:
            str: 图片路径
        """
        if category not in self._paths:
            raise ValueError(f"无效的类别: {category}")
        if name not in self._paths[category]:
            raise ValueError(f"无效的图片名称: {category}.{name}")
        return self._paths[category][name]
    
    @classmethod
    def instance(cls):
        """获取单例实例"""
        return cls() 