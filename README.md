# 采编王自动化测试框架

基于 Python 的采编王桌面应用自动化测试框架，使用 PyAutoGUI 实现界面自动化操作。

## 项目结构

```
desktop_test/
├── core/                    # 核心功能模块
│   ├── base/               # 基础类
│   │   ├── __init__.py
│   │   └── base_test.py    # 测试基类
│   ├── config/             # 配置相关
│   │   ├── __init__.py
│   │   └── settings.py     # 配置管理
│   └── logging/            # 日志相关
│       ├── __init__.py
│       └── logger.py       # 日志管理
│
├── test_cases/             # 测试用例
│   ├── __init__.py
│   ├── batch/              # 批量操作测试
│   │   ├── __init__.py
│   │   └── test_batch_operations.py
│   ├── document/           # 文档处理测试
│   │   ├── __init__.py
│   │   └── test_document_operations.py
│   ├── file_list/          # 文件列表测试
│   │   ├── __init__.py
│   │   └── test_file_list_operations.py
│   ├── scan/               # 扫描操作测试
│   │   ├── __init__.py
│   │   └── test_scan_operations.py
│   └── toolbar/            # 工具栏测试
│       ├── __init__.py
│       └── test_toolbar_operations.py
│
├── test_utils/             # 测试工具
│   ├── __init__.py
│   ├── assertions/         # 断言相关
│   │   ├── __init__.py
│   │   ├── element.py     # 元素断言
│   │   ├── image.py       # 图像断言
│   │   └── file.py        # 文件断言
│   ├── fixtures/          # 夹具相关
│   │   ├── __init__.py
│   │   ├── app.py        # 应用夹具
│   │   ├── document.py   # 文档夹具
│   │   └── scan.py       # 扫描夹具
│   └── helpers/          # 辅助工具
│       ├── __init__.py
│       ├── ui.py         # UI操作
│   │   └── image.py      # 图像处理
│   │   └── file.py       # 文件处理
│   └── helpers/          # 辅助工具
│       ├── __init__.py
│       ├── ui.py         # UI操作
│       └── image.py      # 图像处理
│
├── test_data/            # 测试数据目录
│   ├── batch/           # 批量操作测试图片
│   ├── common/          # 通用测试图片
│   ├── document/        # 文档处理测试图片
│   ├── file_list/       # 文件列表测试图片
│   ├── scan/           # 扫描操作测试图片
│   └── toolbar/        # 工具栏操作测试图片
├── screenshots/         # 测试截图目录
├── logs/               # 日志文件目录
└── reports/            # 测试报告目录
```

## 主要功能

1. 批量操作测试
   - 批量色彩模式转换
   - 批量裁剪
   - 批量规格化

2. 文档处理测试
   - OCR 文字识别
   - PDF 转换
   - OFD 文件处理

3. 文件列表操作测试
   - 文件导入
   - 文件插入
   - 文件重排序

4. 扫描操作测试
   - 色彩模式设置
   - 扫描类型设置
   - 扫描功能

5. 工具栏操作测试
   - 裁剪工具
   - 框选工具
   - 缩放工具

## 环境要求

- Python 3.8+
- 操作系统：统信 UOS
- 显示器分辨率：1920x1080 或更高
- 采编王应用版本：1.0.0 或更高

## 依赖包

- PyAutoGUI：用于模拟鼠标和键盘操作
- OpenCV：用于图像处理和匹配
- pytest：测试框架
- loguru：日志记录
- python-magic：文件类型检测
- pytest-xdist：并行测试执行
- pytest-timeout：测试超时控制
- pytest-rerunfailures：失败重试机制

## 安装步骤

1. 克隆项目到本地：
```bash
git clone https://github.com/your-username/desktop_test.git
cd desktop_test
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 根据需要修改 .env 文件中的配置
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试类
pytest test_cases/test_batch_operations.py

# 运行特定测试方法
pytest test_cases/test_batch_operations.py::TestBatchOperations::test_batch_color_mode
```

## 日志和报告

- 测试日志保存在 `logs` 目录
- 测试截图保存在 `screenshots` 目录
- 测试报告保存在 `reports` 目录

## 注意事项

1. 运行测试前确保采编王应用已安装
2. 测试过程中请勿手动操作鼠标和键盘
3. 确保测试图片资源完整且正确
4. 建议在测试环境中运行，避免影响生产环境

## 开发指南

1. 新增测试用例
   - 在 `test_cases` 目录下创建新的测试类
   - 继承 `BaseTest` 类
   - 实现 `setup_method` 和 `teardown_method`

2. 添加测试数据
   - 在 `test_data` 目录下创建相应的子目录
   - 准备测试所需的图片资源
   - 确保图片命名规范且具有描述性

3. 使用测试工具类
   - `TestHelper`: 提供基础的 UI 操作
   - `TestAssertions`: 提供断言方法
   - `TestFixtures`: 提供测试夹具

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 