
from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='deepseek-ocr-cli',  # 模块名
    version='0.1.2',  # 当前版本
    description='deepseek OCR command line tool',  # 简短描述
    packages=find_packages(include=['dsocr', 'dsocr.*']),  # 包含dsocr和dsocr下的所有子包
    
    # 以下均为可选参数
    long_description="deepseek OCR command line tool",# 长描述
    url='https://github.com/whitewatercn/deepseek-ocr-cli', # 主页链接
    author='whitewatercn', # 作者名
    author_email='whitewatercn@outlook.com', # 作者邮箱
    classifiers=[
        'Intended Audience :: Developers', # 模块适用人群
        'Topic :: Software Development :: Build Tools', # 给模块加话题标签

    ],
    keywords=['deepseek','ocr','command line tool','python'],  # 模块的关键词，使用空格分割
    install_requires=['requests',
					  'argparse'], # 依赖模块
    python_requires='>=3.0',  # 模块支持的Python版本
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'dsocr=dsocr.main:main',
        ],
        },
        project_urls={  # 项目相关的额外链接
        'Bug Reports': 'https://github.com/whitewatercn/deepseek-ocr-cli/issues',
        'Source': 'https://github.com/whitewatercn/deepseek-ocr-cli',
    },
)
