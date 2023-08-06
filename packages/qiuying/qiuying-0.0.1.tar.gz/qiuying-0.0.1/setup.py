"""
Setup everything.

By Allen Tao
Created at 2023/3/17 16:05
"""

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

    setuptools.setup(
        name="qiuying",
        version="0.0.1",
        author="Allen Tao, Ziqiu Li",
        author_email="allen@tkzt.cn, lcmail1001@163.com",
        description="A plain, simple and this-is-the-way library for RPA developing.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/qiuying-rpa/qiuying",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )