from io import open
from os import environ

from setuptools import setup


def read(filename):
    with open(filename, encoding="utf-8") as file:
        return file.read()


def requirements():
    with open("requirements.txt", "r") as req:
        return [r for r in req.read().split("\n") if r]


setup(
    name="pycups_po",
    version=environ.get("TAG_VERSION").replace("v", ""),
    packages=[
        "pycups_po",
        "pycups_po.models",
    ],
    url="https://github.com/WhiteApfel/pycups_po",
    license="Mozilla Public License 2.0",
    author="WhiteApfel",
    author_email="white@pfel.ru",
    description="CUPS print options generator from PPD",
    install_requires=requirements(),
    project_urls={
        "Source code": "https://github.com/WhiteApfel/pycups_po",
        "Write me": "https://t.me/whiteapfel",
    },
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="pycups cups ppd options",
)
