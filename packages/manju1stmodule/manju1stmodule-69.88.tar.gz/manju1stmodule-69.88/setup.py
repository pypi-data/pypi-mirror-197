from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='manju1stmodule',
    version=69.88,
    long_description=Path(r'C:\Users\Lenova\botcode\README.md').read_text(),
    packages=find_packages(exclude=["test", "data"])
)
