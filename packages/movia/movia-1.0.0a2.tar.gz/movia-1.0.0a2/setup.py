#!/usr/bin/env python3

"""
** Configuration file for pip. **
---------------------------------
"""

import os
import sys

from setuptools import find_packages, setup, Command

import movia


if sys.version_info < (3, 9):
    print(
        "Movia requires Python 3.9 or newer. "
        f"Python {sys.version_info[0]}.{sys.version_info[1]} detected"
    )
    sys.exit(-1)


with open("README.rst", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="movia",
    version=movia.__version__,
    author="Robin RICHARD (robinechuca)",
    author_email="serveurpython.oz@gmail.com",
    description="video editing softwear",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://framagit.org/robinechuca/movia/-/blob/main/README.md",
    data_files=[
        # ("movia/examples/", os.listdir("movia/examples")),
        ("movia/", ["README.rst", ".pylintrc"]),
    ],
    packages=find_packages(),
    install_requires=[ # dependences: apt install graphviz-dev ffmpeg
        "av", # apt install ffmpeg python3-av
        "black",
        "click", # apt install python3-click
        "networkx", # apt install python3-networkx
        "numpy >= 1.22", # apt install python3-numpy
        "opencv-contrib-python-headless", # apt install python3-opencv
        "pdoc3",
        "pygraphviz", # pygraphviz https://pygraphviz.github.io/documentation/stable/install.html
        "pyqt6", # apt install python3-pyqt6[.sip]
        "sympy", # apt install python3-sympy
        "unidecode", # apt install python3-unidecode
    ],
    extras_require={
        "dev": ["pylint", "pytest"] # apt install pylint, python3-pylint-common, python3-pytest
    },
    entry_points={
        "console_scripts": [
            "movia=movia.__main__:main",
            "movia-test=movia.testing.runtests:test",
        ],
        "gui_scripts": [
            "movia-qt=movia.gui.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Mixers",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Multimedia :: Video :: Display",
        "Topic :: Multimedia :: Video :: Non-Linear Editor",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    keywords=[
        "video",
        "editing",
        "ffmpeg",
        "graphical",
    ],
    python_requires=">=3.9,<3.12",
    project_urls={
        "Source Repository": "https://framagit.org/robinechuca/movia/",
        # "Bug Tracker": "https://github.com/engineerjoe440/ElectricPy/issues",
        # "Documentation": "http://python-docs.ddns.net/raisin/",
        # "Packaging tutorial": "https://packaging.python.org/tutorials/distributing-packages/",
        },
    include_package_data=True,
)
