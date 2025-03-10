"""
生成测试用的图片文件
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_button_image(text, output_path, size=(100, 30), bg_color=(240, 240, 240), text_color=(0, 0, 0)):
    """
    创建一个按钮样式的图片
    """
    # 创建图片
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 添加文字
    try:
        font = ImageFont.truetype("Arial", 12)
    except:
        font = ImageFont.load_default()
        
    # 计算文字位置使其居中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, fill=text_color, font=font)
    
    # 保存图片
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

def create_grayscale_result_image(output_path, size=(200, 150)):
    """
    创建一个灰度图像示例
    """
    # 创建灰度图像
    img = Image.new('L', size)
    draw = ImageDraw.Draw(img)
    
    # 添加一些灰度渐变
    for i in range(size[0]):
        for j in range(size[1]):
            gray_value = int((i + j) / (size[0] + size[1]) * 255)
            draw.point((i, j), fill=gray_value)
    
    # 保存图片
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

def main():
    """
    生成所有需要的测试图片
    """
    # 基础路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_data_dir = os.path.join(base_dir, 'test_data')
    
    # 创建common目录下的图片
    create_button_image(
        "采编王",
        os.path.join(test_data_dir, 'common', 'calculator_icon.png'),
        size=(64, 64),
        bg_color=(200, 200, 255)
    )
    
    create_button_image(
        "关闭",
        os.path.join(test_data_dir, 'common', 'close_button.png'),
        size=(30, 20),
        bg_color=(255, 200, 200)
    )
    
    create_button_image(
        "确定",
        os.path.join(test_data_dir, 'common', 'confirm_button.png'),
        size=(60, 25),
        bg_color=(200, 255, 200)
    )
    
    # 创建batch目录下的图片
    create_button_image(
        "色彩模式",
        os.path.join(test_data_dir, 'batch', 'color_mode_button.png'),
        size=(80, 30),
        bg_color=(200, 255, 200)
    )
    
    create_button_image(
        "灰度",
        os.path.join(test_data_dir, 'batch', 'grayscale_option.png'),
        size=(60, 25),
        bg_color=(220, 220, 220)
    )
    
    create_grayscale_result_image(
        os.path.join(test_data_dir, 'batch', 'grayscale_result.png')
    )

if __name__ == '__main__':
    main() 