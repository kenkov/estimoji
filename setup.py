#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="estimoji",
    packages=["estimoji"],
    package_data={"estimoji": ["meoji_id.txt"]},
    version="0.1.0",
    author="kenkov",
    author_email="kenkovtan@gmail.com",
    url="http://kenkov.jp",
)
