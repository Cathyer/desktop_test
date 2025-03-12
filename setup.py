from setuptools import setup, find_packages

setup(
    name="desktop_test",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pytest>=7.4.4',
        'pyautogui>=0.9.54',
        'PyQt6>=6.6.1',
        'PySide6>=6.6.1',
        'Pillow>=11.1.0',
        'pytest-html>=4.1.1',
        'opencv-python>=4.11.0.86',
        'numpy>=1.26.3',
        'python-magic>=0.4.27',
        'pytesseract>=0.3.13',
    ],
    python_requires='>=3.9',
) 