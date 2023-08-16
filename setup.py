from setuptools import setup
from io import open
import os

fpath = os.path.join(os.path.dirname(__file__), "README.md")
readme = open(fpath, "r", encoding="utf-8").read()


setup(
    name="excel2xx",
    version="0.9.1",
    packages=["excel2xx"],
    url="https://github.com/cupen/excel2xx",
    license="WTFPL",
    author="cupen",
    author_email="xcupen@gmail.com",
    description="Extract data from excel file, and export to json, msgpack, or any code(mako template).",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        "xlrd == 1.2.*",
        "docopt >= 0.6.0",
        "mako == 1.1.*",
        "msgpack-python >= 0.4.8",
    ],
    entry_points={
        "console_scripts": [
            "excel2xx=excel2xx.main:main_docopt",
        ],
    },
    python_requires=">=3.6,!=3.6.1",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
