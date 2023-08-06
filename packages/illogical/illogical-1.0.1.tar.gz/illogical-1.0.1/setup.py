"""Package setup"""

from setuptools import find_packages, setup

setup(
    packages=find_packages(
        include=["illogical"],
        exclude=["tests"],
    ),
)
