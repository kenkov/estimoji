#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="estimoji",
    packages=["estimoji"],
    install_requires=[
        "emoji>=0.5.0",
        "scikit-learn>=0.19.2",
        ],
    version="0.1.1",
    author="kenkov",
    author_email="kenkovtan@gmail.com",
    url="http://kovlang.jp",
)
