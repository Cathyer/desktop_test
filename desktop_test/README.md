# 桌面应用自动化测试框架

这是一个基于Python的桌面应用自动化测试框架，专门设计用于统信系统下的应用测试。

## 特性

- 基于图像识别的UI元素定位
- 支持图像对比断言
- 详细的HTML测试报告
- 完整的日志记录
- 测试失败自动截图
- 模块化的测试用例组织

## 目录结构

```
desktop_test/
├── test_cases/        # 测试用例目录
├── test_data/         # 测试数据（如参考图片）
├── logs/              # 日志文件目录
├── reports/           # 测试报告目录
├── screenshots/       # 截图目录
├── utils/             # 工具类目录
└── requirements.txt   # 项目依赖
```

## 安装

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备测试数据：
   - 将需要的参考图片放在 `test_data` 目录下

2. 编写测试用例：
   - 继承 `BaseTest` 类
   - 使用提供的断言方法：
     - `assert_element_exists`: 断言元素存在
     - `assert_images_match`: 断言图片匹配

3. 运行测试：
```bash
pytest -v --html=reports/report.html
```

## 配置

可以在 `utils/config.py` 中修改以下配置：

- 图像相似度阈值
- 超时时间
- 截图延迟
- 日志格式
- 报告标题

## 注意事项

1. 确保测试环境中的显示设置（如分辨率、缩放）与参考图片一致
2. 测试用例执行前请确保目标应用处于正确的初始状态
3. 建议使用较高分辨率的参考图片以提高识别准确率

## 常见问题

1. 元素识别失败
   - 检查参考图片是否清晰
   - 调整相似度阈值
   - 确保屏幕显示正常

2. 测试报告无截图
   - 检查截图目录权限
   - 确保 PyAutoGUI 有截图权限

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个框架。

## 许可

MIT License 