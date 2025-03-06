# 采编王桌面应用自动化测试项目

## 项目简介
本项目是采编王桌面应用的自动化测试框架，使用Python和pytest实现。主要测试内容包括文件操作、OCR识别和扫描功能。

## 项目结构
```
desktop_test/
├── test_cases/          # 测试用例目录
│   ├── base_test.py     # 基础测试类
│   ├── test_file_operations.py  # 文件操作测试
│   ├── test_ocr.py      # OCR功能测试
│   ├── test_scan.py     # 扫描功能测试
│   └── test_examples.py # 示例测试用例
├── pages/               # 页面对象目录
│   ├── base_page.py     # 基础页面类
│   ├── main_page.py     # 主页面
│   ├── file_page.py     # 文件操作页面
│   ├── ocr_page.py      # OCR页面
│   └── scan_page.py     # 扫描页面
├── utils/               # 工具类目录
│   ├── config.py        # 配置文件
│   ├── logger.py        # 日志工具
│   ├── image_paths.py   # 图片路径管理
│   ├── exceptions.py    # 自定义异常
│   └── test_data.py     # 测试数据管理
├── test_data/           # 测试数据目录
│   ├── images/          # 图片资源
│   ├── document/        # 文档资源
│   └── common/          # 公共资源
├── screenshots/         # 截图目录
├── logs/                # 日志目录
├── reports/             # 测试报告目录
├── conftest.py          # pytest配置文件
├── pytest.ini           # pytest配置
└── requirements.txt     # 项目依赖
```

## 环境要求
- Python 3.8+
- 操作系统：Windows/macOS/Linux
- 屏幕分辨率：1920x1080（推荐）

## 依赖包
```
pytest==7.4.4          # 测试框架
pyautogui==0.9.54      # 自动化操作
PyQt5==5.15.10         # GUI测试支持
PySide2==5.15.2.1      # GUI测试支持
Pillow==10.2.0         # 图像处理
pytest-html==4.1.1     # HTML报告生成
opencv-python==4.9.0.80 # 图像处理
numpy==1.26.3          # 数值计算
loguru==0.7.2          # 日志管理
```

## 安装说明
1. 克隆项目
```bash
git clone https://github.com/Cathyer/desktop_test.git
cd desktop_test
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 测试说明
1. 运行所有测试
```bash
pytest
```

2. 运行特定测试
```bash
# 运行冒烟测试
pytest -m smoke

# 运行回归测试
pytest -m regression

# 运行性能测试
pytest -m performance
```

3. 生成HTML报告
```bash
pytest --html=reports/report.html
```

## 测试标记说明
- `@pytest.mark.smoke`: 冒烟测试用例
- `@pytest.mark.regression`: 回归测试用例
- `@pytest.mark.integration`: 集成测试用例
- `@pytest.mark.slow`: 运行时间较长的测试用例
- `@pytest.mark.critical`: 关键功能测试用例
- `@pytest.mark.bugfix`: 问题修复测试用例
- `@pytest.mark.performance`: 性能测试用例
- `@pytest.mark.security`: 安全测试用例
- `@pytest.mark.ui`: 界面测试用例
- `@pytest.mark.api`: 接口测试用例

## 测试报告
测试报告包含以下内容：
- 测试用例执行结果
- 失败用例的截图
- 测试执行时间统计
- 测试环境信息

## 注意事项
1. 运行测试前请确保采编王应用已启动
2. 测试过程中请勿手动操作鼠标和键盘
3. 如遇到测试失败，请查看logs目录下的日志文件
4. 测试报告保存在reports目录下

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证
本项目采用 MIT 许可证 