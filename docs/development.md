# Desktop Test 自动化测试框架开发文档

## 项目架构

### 目录结构
```
desktop_test/
├── utils/                # 工具类目录
│   ├── test_helper.py   # 核心UI操作类
│   ├── config.py        # 配置文件
│   ├── custom_logger.py # 日志工具
│   └── exceptions.py    # 自定义异常
├── pages/               # 页面对象目录
│   ├── base_page.py    # 基础页面类
│   └── [具体页面类]     # 各个具体页面的实现
└── test_cases/         # 测试用例目录
    └── test_examples.py # 示例测试用例

## 核心类说明

### TestHelper 类
核心的UI自动化操作类，提供最基础的UI交互功能：

#### 主要功能：
- 图片识别和定位
- 鼠标操作（点击、双击、右键等）
- 键盘操作（输入文本、快捷键等）
- 截图功能
- 图片对比功能

#### 关键方法：
- `find_on_screen`: 在屏幕上查找元素
- `perform_mouse_action`: 执行鼠标操作
- `perform_keyboard_action`: 执行键盘操作
- `take_screenshot`: 截取屏幕截图
- `compare_images`: 比较两张图片的相似度

### BasePage 类
页面对象的基类，提供高级的页面操作方法：

#### 主要功能：
- 元素查找和操作
- 等待机制
- 状态验证
- 滚动操作
- 重试机制

#### 关键方法：
- `find_element`: 查找页面元素
- `click_element`: 点击元素
- `double_click_element`: 双击元素
- `wait_for_element`: 等待元素出现
- `verify_element_state`: 验证元素状态

## 使用指南

### 创建新的页面类
```python
from desktop_test.pages.base_page import BasePage

class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        self.images = {
            'file_menu': 'path/to/file_menu.png',
            'edit_button': 'path/to/edit_button.png'
        }
    
    def click_file_menu(self):
        return self.click_element(self.images['file_menu'])
    
    def double_click_file(self):
        return self.double_click_element(self.images['file'])
```

### 编写测试用例
```python
def test_main_page():
    main_page = MainPage()
    
    # 等待页面加载
    assert main_page.wait_for_element('path/to/page_loaded.png')
    
    # 点击文件菜单
    assert main_page.click_file_menu()
    
    # 等待菜单显示
    assert main_page.wait_for_element('path/to/menu_shown.png')
```

## 最佳实践

### 1. 图片管理
- 使用统一的图片命名规范
- 按功能模块组织图片目录
- 保持图片大小适中，避免过大或过小

### 2. 等待策略
- 使用显式等待而不是固定延时
- 设置合适的超时时间
- 合理使用重试机制

### 3. 错误处理
- 捕获并记录所有可能的异常
- 提供清晰的错误信息
- 使用自定义异常类型

### 4. 日志记录
- 记录所有关键操作
- 包含足够的上下文信息
- 使用不同的日志级别

### 5. 性能优化
- 使用图片缓存
- 优化查找区域
- 合理设置操作间隔

## 常见问题

### 1. 图片识别失败
- 检查图片是否存在
- 验证图片质量
- 调整匹配置信度

### 2. 操作超时
- 检查等待时间是否合理
- 验证元素是否可见
- 考虑使用重试机制

### 3. 操作不稳定
- 添加适当的等待时间
- 使用重试机制
- 优化操作流程

## 扩展开发

### 1. 添加新的操作类型
1. 在 `TestHelper` 中添加基础操作
2. 在 `BasePage` 中封装高级操作
3. 更新文档和测试用例

### 2. 自定义等待条件
1. 实现新的等待方法
2. 设置合适的默认参数
3. 添加错误处理

### 3. 增加新的验证方法
1. 实现验证逻辑
2. 添加适当的日志记录
3. 编写测试用例 