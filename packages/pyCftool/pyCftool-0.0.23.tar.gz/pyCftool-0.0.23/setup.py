from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

here = os.path.abspath(os.path.dirname(__file__))


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.23'
DESCRIPTION = 'Interactive python fitting interface'

# Setting up
setup(
    name="pyCftool",
    version=VERSION,
    author="Andreas Forum (TehForum)",
    author_email="<andforum@hotmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['pyCftool','export','loadgui','mplwidget','options']),
    include_package_data=True,
    install_requires=['PySide6','numpy','scipy','matplotlib',],
    keywords=['python', 'fit','statistics','modelling','science'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)