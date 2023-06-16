"""Package configuration."""
from os.path import abspath, dirname
from setuptools import find_packages, setup
from spithon import (
    __version__,
    PROJECT_DESCRIPTION,
    PROJECT_AUTHOR,
    PROJECT_EMAIL,
    PROJECT_LICENSE,
    PROJECT_URL,
    PROJECT_CLASSIFIERS,
)

THIS_DIR = abspath(dirname(__file__))

with open(f"{THIS_DIR}/requirements.txt") as req_file:
    REQUIRES = [line.rstrip() for line in req_file]

with open(f"{THIS_DIR}/README.md") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

PACKAGES = find_packages()

setup(
    name="spithon",
    version=__version__,
    description=PROJECT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    license=PROJECT_LICENSE,
    url=PROJECT_URL,
    packages=PACKAGES,
    install_requires=REQUIRES,
    include_package_data=True,
    classifiers=PROJECT_CLASSIFIERS,
    entry_points={"console_scripts": ["spithon=spithon.cli:cli"]},
)
