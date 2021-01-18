import os
from configparser import ConfigParser
from setuptools import setup, find_packages

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser()
config.read(os.path.join(ROOT_PATH, "tuya_bulb_control/project.ini"))


def _read(filename):
    try:
        return open(os.path.join(ROOT_PATH, filename)).read()
    except IOError:
        return None


install_requires = [
    line
    for line in _read("requirements.txt").split("\n")
    if line and not line.startswith("#")
]

long_description = _read(os.path.join(ROOT_PATH, "README.md"))

setup(
    name=config.get("Info", "project"),
    version=config.get("Info", "version"),
    description="Tuya Bulb Control - API wrapper for you smart bulbs developed by Tuya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=config.get("Info", "author"),
    url="https://github.com/Octoober/tuya-bulb-control",
    license=config.get("Info", "license"),
    keywords="iot tuya api wrapper",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)
