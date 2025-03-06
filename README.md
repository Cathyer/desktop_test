# 采编王自动化测试项目

本项目是采编王桌面应用的自动化测试解决方案，使用Python实现UI自动化测试。

## 项目结构

```
desktop_test/
├── test_cases/              # 测试用例
│   ├── base_test.py        # 测试基类
│   ├── test_fixtures.py    # 测试夹具
│   ├── test_batch_operations.py     # 批量操作测试
│   ├── test_document_operations.py  # 文档处理测试
│   ├── test_toolbar_operations.py   # 工具栏操作测试
│   ├── test_file_list_operations.py # 文件列表操作测试
│   └── test_scan_operations.py      # 扫描页面测试
├── test_data/              # 测试数据
│   ├── batch/             # 批量操作相关图片
│   ├── document/          # 文档处理相关图片
│   ├── toolbar/           # 工具栏操作相关图片
│   ├── file_list/         # 文件列表相关图片
│   ├── scan/             # 扫描页面相关图片
│   └── common/           # 通用图片（如图标、按钮等）
├── utils/                 # 工具类
│   ├── custom_logger.py  # 日志工具
│   ├── test_helper.py    # 测试助手
│   └── config.py         # 配置文件
└── reports/              # 测试报告
```

## 测试数据组织

测试数据按功能模块分类存储在 `test_data` 目录下：

1. `common/` - 存放通用的UI元素图片：
   - `caibian_icon.png` - 应用图标
   - `main_window.png` - 主窗口
   - `import_button.png` - 导入按钮
   - `open_button.png` - 打开按钮
   - `confirm_button.png` - 确认按钮
   - `close_button.png` - 关闭按钮
   - `confirm_close.png` - 关闭确认按钮

2. `batch/` - 批量操作相关图片：
   - `test_image1.png` - 测试图片1
   - `test_image2.png` - 测试图片2
   - `test_image3.png` - 测试图片3
   - `batch_operation_button.png` - 批量操作按钮
   - `color_mode_button.png` - 色彩模式按钮
   - `grayscale_option.png` - 灰度选项
   - 等

3. `document/` - 文档处理相关图片：
   - `test_doc.pdf` - 测试PDF文件
   - `ocr_button.png` - OCR按钮
   - `language_chinese.png` - 中文选项
   - `pdf_button.png` - PDF按钮
   - 等

4. `toolbar/` - 工具栏相关图片：
   - `crop_tool.png` - 裁剪工具
   - `selection_tool.png` - 框选工具
   - `zoom_tool.png` - 缩放工具
   - `image_area.png` - 图片区域
   - 等

5. `file_list/` - 文件列表相关图片：
   - `file_list_item.png` - 文件列表项
   - `insert_button.png` - 插入按钮
   - `file_item_1.png` - 文件项1
   - 等

6. `scan/` - 扫描页面相关图片：
   - `scan_tab.png` - 扫描标签页
   - `color_mode_dropdown.png` - 色彩模式下拉框
   - `scan_type_dropdown.png` - 扫描类型下拉框
   - 等

## 使用方法

1. 环境准备：
   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   # 安装依赖
   pip install -r requirements.txt
   ```

2. 准备测试数据：
   - 将需要的测试图片和文件放入对应的测试数据目录
   - 确保图片命名与代码中的路径一致

3. 运行测试：
   ```bash
   # 运行所有测试
   pytest

   # 运行指定模块的测试
   pytest test_cases/test_batch_operations.py
   pytest test_cases/test_document_operations.py
   pytest test_cases/test_toolbar_operations.py
   pytest test_cases/test_file_list_operations.py
   pytest test_cases/test_scan_operations.py

   # 运行指定测试用例
   pytest test_cases/test_batch_operations.py::TestBatchOperations::test_batch_color_mode
   ```

4. 查看测试报告：
   - 测试完成后，可以在 `reports` 目录下查看测试报告
   - 测试日志会记录每个步骤的执行情况
   - 失败的测试会包含截图和错误信息

## 开发指南

1. 添加新的测试用例：
   - 在 `test_cases` 目录下创建新的测试类
   - 继承 `BaseTest` 类
   - 使用 `TestFixtures` 进行前置和后置操作
   - 使用 `TestHelper` 进行UI操作
   - 使用 `verify_operation_result` 验证结果

2. 添加新的测试数据：
   - 在对应的测试数据目录下添加图片
   - 图片命名要清晰表达用途
   - 通用的UI元素图片放在 `common` 目录

3. 修改配置：
   - 在 `config.py` 中修改相关配置
   - 可以调整超时时间、等待间隔等参数

## 注意事项

1. 图片要求：
   - 分辨率要清晰
   - 要能准确识别UI元素
   - 最好是PNG格式

2. 运行环境：
   - 确保屏幕分辨率与录制时一致
   - 不要在测试过程中移动鼠标
   - 测试过程中不要切换窗口

3. 测试数据：
   - 测试数据要有代表性
   - 文件大小要适中
   - 中文内容要使用UTF-8编码

4. 异常处理：
   - 所有测试都要有适当的异常处理
   - 要记录详细的错误信息
   - 失败时要保存截图

## 常见问题

1. 图片识别失败：
   - 检查图片是否清晰
   - 检查分辨率是否一致
   - 调整等待时间

2. 测试不稳定：
   - 增加等待时间
   - 添加重试机制
   - 检查环境因素

3. 测试报告问题：
   - 检查日志配置
   - 确保目录权限
   - 查看磁盘空间 