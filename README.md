# Desktop Test 自动化测试框架

这是一个基于图像识别的桌面应用自动化测试框架，使用 Python 开发。该框架支持通过图像匹配来定位和操作界面元素，适用于各种桌面应用程序的自动化测试。

## 功能特点

- 基于图像识别的元素定位
- 支持多种文件操作（新建、打开、保存等）
- 内置 OCR 功能支持
- 扫描功能支持
- 完整的日志记录系统
- 自动截图和错误报告
- 支持测试用例重试机制
- HTML 格式的测试报告
- 支持多平台（Windows/macOS/Linux）
- 灵活的配置系统
- 详细的错误追踪和调试信息

## 系统要求

- Python 3.9 或更高版本
- 操作系统：Windows/macOS/Linux
- 依赖包：
  - pytest >= 7.4.0
  - pyautogui >= 0.9.53
  - pillow >= 9.0.0
  - opencv-python >= 4.7.0
  - python-magic >= 0.4.27
  - pytest-html >= 4.1.1
  - pytest-rerunfailures >= 15.0

## 安装

1. 克隆仓库：
```bash
git clone <repository_url>
cd desktop_test
```

2. 安装依赖：
```bash
pip install -e .
```

3. 验证安装：
```bash
pytest --version
python -c "import desktop_test"
```

## 项目结构

```
desktop_test/
├── conftest.py           # pytest配置文件
├── pytest.ini           # pytest初始化配置
├── requirements.txt     # 项目依赖
├── setup.py            # 安装配置
├── pages/              # 页面对象
│   ├── base_page.py    # 基础页面类
│   ├── main_page.py    # 主页面
│   ├── file_page.py    # 文件页面
│   ├── ocr_page.py     # OCR页面
│   └── scan_page.py    # 扫描页面
├── test_cases/         # 测试用例
│   └── test_examples.py # 示例测试用例
├── test_data/          # 测试数据和图片
│   ├── common/         # 通用图片
│   ├── toolbar/        # 工具栏图片
│   ├── file_list/      # 文件列表图片
│   ├── ocr/            # OCR相关图片
│   └── scan/           # 扫描相关图片
├── utils/              # 工具类
│   ├── config.py       # 配置文件
│   ├── custom_logger.py # 日志工具
│   ├── exceptions.py   # 自定义异常
│   ├── file_validator.py # 文件验证器
│   ├── image_paths.py  # 图片路径管理
│   └── test_helper.py  # 测试辅助工具
├── logs/               # 日志文件
├── screenshots/        # 截图文件
└── reports/           # 测试报告
```

## 使用方法

1. 准备测试环境：
   - 确保目标应用程序已安装
   - 准备必要的测试图片资源
   - 配置测试环境变量（可选）

2. 编写测试用例：
```python
from desktop_test.pages.main_page import MainPage
from desktop_test.pages.file_page import FilePage

def test_basic_file_operations():
    # 初始化页面对象
    main_page = MainPage()
    file_page = FilePage()
    
    # 执行测试步骤
    assert main_page.is_main_window_visible()
    assert file_page.create_new_file()
    assert file_page.input_file_name("test.txt")
    assert file_page.save_current_file()

def test_ocr_functionality():
    # OCR功能测试示例
    main_page = MainPage()
    ocr_page = OCRPage()
    
    # 打开OCR页面
    assert main_page.open_feature("ocr")
    
    # 设置OCR参数
    assert ocr_page.select_language("chinese")
    assert ocr_page.set_accuracy(0.8)
    
    # 执行OCR
    assert ocr_page.start_ocr()
    assert ocr_page.wait_for_completion()
    
    # 验证结果
    result = ocr_page.get_result()
    assert result != ""

def test_scan_document():
    # 扫描功能测试示例
    main_page = MainPage()
    scan_page = ScanPage()
    
    # 打开扫描页面
    assert main_page.open_feature("scan")
    
    # 配置扫描参数
    assert scan_page.set_resolution(300)
    assert scan_page.set_color_mode("color")
    assert scan_page.set_paper_size("a4")
    
    # 执行扫描
    assert scan_page.start_scan()
    assert scan_page.wait_for_completion()
```

3. 运行测试：
```bash
# 运行单个测试文件
pytest test_cases/test_examples.py -v

# 运行特定测试用例
pytest test_cases/test_examples.py::test_basic_file_operations -v

# 使用标记运行测试
pytest -v -m "file_operations"

# 生成HTML报告
pytest --html=reports/report.html

# 失败重试
pytest --reruns 3 --reruns-delay 1
```

## 配置说明

1. `pytest.ini` 配置示例：
```ini
[pytest]
testpaths = test_cases
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --reruns 3 --reruns-delay 1 --html=reports/report.html
timeout = 300
markers =
    file_operations: 文件操作相关测试
    ocr: OCR功能相关测试
    scan: 扫描功能相关测试
```

2. 环境变量：
```bash
# Windows
set TEST_ENV=dev
set TEST_PLATFORM=windows
set TEST_RESOLUTION=1920x1080

# Linux/macOS
export TEST_ENV=dev
export TEST_PLATFORM=macos
export TEST_RESOLUTION=1920x1080
```

3. 日志配置：
```python
# config.py
LOG_LEVEL = "INFO"
SCREENSHOT_DELAY = 0.5
RETRY_COUNT = 3
RETRY_INTERVAL = 1
DEFAULT_TIMEOUT = 10
IMAGE_MATCH_THRESHOLD = 0.95
```

## 日志系统

框架提供了完整的日志记录功能：
- 控制台日志：实时显示测试执行情况
- 文件日志：详细记录所有操作和错误信息
- HTML报告：包含测试结果、截图和性能数据
- 错误截图：自动保存失败时的屏幕状态
- 性能指标：记录各项操作的执行时间

日志示例：
```
2025-03-12 08:45:10 - INFO - 初始化主页面
2025-03-12 08:45:11 - INFO - 点击文件菜单
2025-03-12 08:45:12 - INFO - 创建新文件
2025-03-12 08:45:13 - ERROR - 未找到保存按钮
```

## 开发指南

1. 添加新的页面对象：
```python
from desktop_test.pages.base_page import BasePage

class NewPage(BasePage):
    def __init__(self):
        super().__init__()
        self.images = ImagePaths()._paths['NEW_PAGE']
        
    def custom_action(self):
        try:
            if self.click_element(self.images['button']):
                self.logger.info("操作成功")
                return True
            return False
        except Exception as e:
            self.logger.error(f"操作失败: {e}")
            return False
```

2. 添加新的测试用例：
```python
import pytest
from desktop_test.pages.new_page import NewPage

@pytest.mark.new_feature
def test_new_feature():
    page = NewPage()
    assert page.custom_action()
```

3. 维护图片资源：
   - 使用高质量截图工具
   - 保持图片分辨率一致
   - 定期更新匹配失败的图片
   - 使用版本控制管理图片资源

## 常见问题

1. 图片识别失败：
   - 检查图片质量和分辨率
   - 验证图片路径是否正确
   - 调整匹配阈值
   - 使用调试模式查看匹配结果
   - 考虑屏幕缩放因素

2. 测试超时：
   - 检查等待时间配置
   - 验证应用程序响应时间
   - 调整超时参数
   - 检查系统资源使用情况
   - 优化测试执行顺序

3. 环境问题：
   - 确保Python版本兼容
   - 检查依赖包版本
   - 验证操作系统兼容性
   - 确认屏幕分辨率设置
   - 检查文件权限

## 贡献指南

1. Fork 项目
2. 创建特性分支：`git checkout -b feature/new-feature`
3. 提交变更：`git commit -am 'Add new feature'`
4. 推送到分支：`git push origin feature/new-feature`
5. 创建 Pull Request

贡献要求：
- 遵循项目的代码风格
- 添加适当的测试用例
- 更新相关文档
- 提供清晰的提交信息

## 许可证

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.