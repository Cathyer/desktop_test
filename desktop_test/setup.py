from setuptools import setup, find_packages

setup(
    name="desktop_test",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pytest>=7.4.3',
        'pyautogui>=0.9.54',
        'PyQt5>=5.15.9',
        'PySide2>=5.15.2.1',
        'Pillow>=10.0.0',
        'pytest-html>=4.1.1',
        'opencv-python>=4.8.0.74',
        'numpy>=1.24.3',
        'loguru>=0.7.0',
    ],
    python_requires='>=3.8',
) 