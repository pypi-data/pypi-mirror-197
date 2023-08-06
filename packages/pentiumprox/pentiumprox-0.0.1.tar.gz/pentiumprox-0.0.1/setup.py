from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Library for programs'
LONG_DESCRIPTION = 'A package that simple programs'

# Setting up
setup(
    name="pentiumprox",
    version=VERSION,
    author="Anonymous",
    author_email="<mohammedfaisal3366@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'programs'],
	setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)