from setuptools import setup, find_packages
import codecs
import os

DESCRIPTION = 'Tech_In_Seconds'
LONG_DESCRIPTION = 'A package to genral and mathamathical operations'
# https://github.com/Avinash6798/avi_package
# Setting up
setup(
    name="Tech_In_Seconds",
    author="Aadesh Lokhande",
    author_email="aadeshlokhande11@gmail.com",
    version="1.0.4",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'tables','barakhadi','mean','contact', 'aadesh lokhande', 'tech in seconds', 'excel formulas', 'periodic table', 'elements'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
# https://github.com/Avinash6798/avi_package
# python setup.py sdist bdist_wheel
# twine upload dist/*
