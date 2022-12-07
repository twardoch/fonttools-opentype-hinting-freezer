#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from setuptools import find_packages, setup

NAME = "opentype_hinting_freezer"


def get_version(*args):
    verstrline = open(Path(NAME, "__init__.py"), "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    return mo[1] if (mo := re.search(VSRE, verstrline, re.M)) else "undefined"


setup(
    name=f"{NAME}",
    version=get_version(),
    description="A tool that applies the hinting of an OT font to the contours at a specified PPM size, and outputs the font with modified contours.",
    long_description=open(
        Path(Path(__file__).parent, "README.md"), "r", encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    keywords=[
        "fonts",
    ],
    url=f"https://github.com/twardoch/fonttools-opentype-feature-freezer",
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    license="Apache 2.0",
    python_requires=">=3.9",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Text Processing :: Fonts",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    entry_points = {
        'console_scripts': [f'pyfthintfreeze={NAME}.__main__:cli'],
    }
)
