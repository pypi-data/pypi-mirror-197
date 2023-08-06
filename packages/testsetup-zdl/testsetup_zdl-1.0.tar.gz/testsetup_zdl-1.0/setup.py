from setuptools import setup, find_packages

setup(
    name="testsetup_zdl",
    version="1.0",
    author="Zhang Daoliang",
    author_email="zdkyzhangdl@gmail.com",

    description="Learn to Pack Python Module",

    python_requires='>=3.7',

    # 项目主页
    url="http://www.baidu.com/",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)