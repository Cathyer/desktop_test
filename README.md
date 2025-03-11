# 桌面应用自动化测试框架

这是一个基于Python的桌面应用自动化测试框架，使用PyAutoGUI进行UI自动化操作。

## 功能特点

- 支持图像识别和自动化操作
- 提供完整的日志记录
- 灵活的超时和重试机制
- 支持忽略元素未找到的错误
- 自动生成测试报告

## 目录结构

```
desktop_test/
├── test_cases/      # 测试用例
├── test_data/       # 测试数据和图片
├── utils/           # 工具类
├── screenshots/     # 测试截图
├── logs/           # 测试日志
└── reports/        # 测试报告
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备测试图片：
```python
python -m desktop_test.utils.create_test_images
```

2. 运行测试：
```python
python -m pytest desktop_test/test_cases
```

## 主要类和方法

### TestHelper

- `find_element_on_screen`: 查找屏幕上的元素
- `click_element`: 点击元素
- `double_click_element`: 双击元素
- `wait_for_element`: 等待元素出现
- `take_screenshot`: 截取屏幕截图
- `compare_images`: 比较两张图片的相似度

### 配置说明

在 `config.py` 中可以修改以下配置：

- 超时时间
- 图片相似度阈值
- 截图延迟
- 日志格式
- 各种目录路径

## 注意事项

1. 确保测试图片清晰可识别
2. 适当调整超时时间和相似度阈值
3. 定期清理测试生成的文件