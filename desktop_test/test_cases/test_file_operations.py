import pytest
from pages.file_page import FilePage
from utils.exceptions import FileOperationError

class TestFileOperations:
    """文件操作测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.file_page = FilePage()
        yield
        # 测试后清理
        try:
            self.file_page.close_current_file()
        except FileOperationError:
            pass
    
    def test_create_new_file(self):
        """测试创建新文件"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 输入文件名
        file_name = "test_new_file.txt"
        assert self.file_page.input_file_name(file_name), "输入文件名失败"
        
        # 选择文件类型
        assert self.file_page.select_file_type("txt"), "选择文件类型失败"
        
        # 点击保存
        assert self.file_page.click_save(), "点击保存按钮失败"
    
    def test_open_existing_file(self):
        """测试打开现有文件"""
        # 点击打开文件按钮
        assert self.file_page.open_existing_file(), "打开文件按钮点击失败"
        
        # 验证文件对话框是否可见
        assert self.file_page.is_file_dialog_visible(), "文件对话框未显示"
    
    def test_save_file(self):
        """测试保存文件"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 输入文件名和内容
        file_name = "test_save_file.txt"
        content = "测试保存文件内容"
        assert self.file_page.create_new_file_with_content(file_name, content), "创建文件并输入内容失败"
        
        # 保存文件
        assert self.file_page.save_current_file(), "保存文件失败"
    
    def test_save_file_as(self):
        """测试另存为"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 输入初始文件名
        initial_name = "initial_file.txt"
        assert self.file_page.create_new_file_with_content(initial_name), "创建初始文件失败"
        
        # 另存为
        assert self.file_page.save_file_as(), "点击另存为按钮失败"
        
        # 输入新文件名
        new_name = "new_save_file.txt"
        assert self.file_page.input_file_name(new_name), "输入新文件名失败"
        
        # 选择文件类型
        assert self.file_page.select_file_type("txt"), "选择文件类型失败"
        
        # 点击保存
        assert self.file_page.click_save(), "点击保存按钮失败"
    
    def test_close_file(self):
        """测试关闭文件"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 输入文件名
        file_name = "test_close_file.txt"
        assert self.file_page.create_new_file_with_content(file_name), "创建文件失败"
        
        # 关闭文件
        assert self.file_page.close_current_file(), "关闭文件失败"
    
    def test_exit_application(self):
        """测试退出应用程序"""
        # 点击退出按钮
        assert self.file_page.exit_application(), "退出应用程序失败"
    
    def test_file_type_selection(self):
        """测试文件类型选择"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 测试不同文件类型
        file_types = ["txt", "doc", "pdf"]
        for file_type in file_types:
            assert self.file_page.select_file_type(file_type), f"选择{file_type}文件类型失败"
    
    def test_cancel_operation(self):
        """测试取消操作"""
        # 创建新文件
        assert self.file_page.create_new_file(), "创建新文件失败"
        
        # 输入文件名
        file_name = "test_cancel_file.txt"
        assert self.file_page.input_file_name(file_name), "输入文件名失败"
        
        # 点击取消
        assert self.file_page.click_cancel(), "点击取消按钮失败" 