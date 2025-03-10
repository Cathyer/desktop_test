import os
from desktop_test.utils.config import TEST_DATA_DIR

class ImagePaths:
    """图片路径管理类"""
    
    @staticmethod
    def get_common_path(filename):
        """获取通用图片路径"""
        return os.path.join(TEST_DATA_DIR, 'common', filename)
    
    @staticmethod
    def get_toolbar_path(filename):
        """获取工具栏图片路径"""
        return os.path.join(TEST_DATA_DIR, 'toolbar', filename)
    
    @staticmethod
    def get_file_list_path(filename):
        """获取文件列表图片路径"""
        return os.path.join(TEST_DATA_DIR, 'file_list', filename)
    
    @staticmethod
    def get_ocr_path(filename):
        """获取OCR图片路径"""
        return os.path.join(TEST_DATA_DIR, 'ocr', filename)
    
    @staticmethod
    def get_scan_path(filename):
        """获取扫描图片路径"""
        return os.path.join(TEST_DATA_DIR, 'scan', filename)
    
    # 主页面图片
    MAIN = {
        'file_menu': get_common_path('file_menu.png'),
        'edit_menu': get_common_path('edit_menu.png'),
        'view_menu': get_common_path('view_menu.png'),
        'tools_menu': get_common_path('tools_menu.png'),
        'help_menu': get_common_path('help_menu.png'),
        'new_button': get_toolbar_path('new_button.png'),
        'open_button': get_toolbar_path('open_button.png'),
        'save_button': get_toolbar_path('save_button.png'),
        'print_button': get_toolbar_path('print_button.png'),
        'calculator_icon': get_common_path('calculator_icon.png'),
        'ocr_button': get_toolbar_path('ocr_button.png'),
        'scan_button': get_toolbar_path('scan_button.png')
    }
    
    # 文件操作页面图片
    FILE = {
        'new_file': get_file_list_path('new_file.png'),
        'open_file': get_file_list_path('open_file.png'),
        'save_file': get_file_list_path('save_file.png'),
        'save_as': get_file_list_path('save_as.png'),
        'close_file': get_file_list_path('close_file.png'),
        'exit': get_file_list_path('exit.png'),
        'file_name_input': get_file_list_path('file_name_input.png'),
        'file_type_dropdown': get_file_list_path('file_type_dropdown.png'),
        'save_button': get_file_list_path('save_button.png'),
        'cancel_button': get_file_list_path('cancel_button.png'),
        'txt_option': get_file_list_path('txt_option.png'),
        'doc_option': get_file_list_path('doc_option.png'),
        'pdf_option': get_file_list_path('pdf_option.png')
    }
    
    # OCR页面图片
    OCR = {
        'start_button': get_ocr_path('start_button.png'),
        'stop_button': get_ocr_path('stop_button.png'),
        'settings_button': get_ocr_path('settings_button.png'),
        'language_dropdown': get_ocr_path('language_dropdown.png'),
        'accuracy_slider': get_ocr_path('accuracy_slider.png'),
        'output_format_dropdown': get_ocr_path('output_format_dropdown.png'),
        'chinese_option': get_ocr_path('chinese_option.png'),
        'english_option': get_ocr_path('english_option.png'),
        'txt_option': get_ocr_path('txt_option.png'),
        'doc_option': get_ocr_path('doc_option.png'),
        'pdf_option': get_ocr_path('pdf_option.png'),
        'result_area': get_ocr_path('result_area.png'),
        'progress_bar': get_ocr_path('progress_bar.png')
    }
    
    # 扫描页面图片
    SCAN = {
        'start_button': get_scan_path('start_button.png'),
        'stop_button': get_scan_path('stop_button.png'),
        'preview_button': get_scan_path('preview_button.png'),
        'settings_button': get_scan_path('settings_button.png'),
        'resolution_dropdown': get_scan_path('resolution_dropdown.png'),
        'color_mode_dropdown': get_scan_path('color_mode_dropdown.png'),
        'paper_size_dropdown': get_scan_path('paper_size_dropdown.png'),
        'resolution_100': get_scan_path('resolution_100.png'),
        'resolution_200': get_scan_path('resolution_200.png'),
        'resolution_300': get_scan_path('resolution_300.png'),
        'color_mode_color': get_scan_path('color_mode_color.png'),
        'color_mode_gray': get_scan_path('color_mode_gray.png'),
        'color_mode_bw': get_scan_path('color_mode_bw.png'),
        'paper_size_a4': get_scan_path('paper_size_a4.png'),
        'paper_size_a3': get_scan_path('paper_size_a3.png'),
        'paper_size_letter': get_scan_path('paper_size_letter.png'),
        'preview_area': get_scan_path('preview_area.png'),
        'progress_bar': get_scan_path('progress_bar.png')
    } 