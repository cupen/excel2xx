from setuptools import setup, find_packages
from io import open
import os

root_dir = os.path.dirname(__file__)


def _open(fname):
    return open(os.path.join(root_dir, fname), "r", encoding="utf-8")


with _open("README.md") as fp:
    readme = fp.read()
    pass

with _open("requirements.txt") as fp:
    deps = map(str.strip, fp.readlines())
    deps = filter(lambda line: bool(line), deps)
    deps = list(deps)
    pass

print(f"requirements={deps}")

setup(
    name="excel2xx",
    version="0.11.8",
    url="https://github.com/cupen/excel2xx",
    license="WTFPL",
    author="cupen",
    author_email="xcupen@gmail.com",
    description="Extract data from excel file, and export to json, msgpack, or any code(mako template).",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=deps,
    entry_points={
        "console_scripts": [
            "excel2xx=excel2xx.main:main_docopt",
        ],
    },
    # python_requires=">=3.6,!=3.6.1",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Code Generators",
    ],
    packages=find_packages(),
)
