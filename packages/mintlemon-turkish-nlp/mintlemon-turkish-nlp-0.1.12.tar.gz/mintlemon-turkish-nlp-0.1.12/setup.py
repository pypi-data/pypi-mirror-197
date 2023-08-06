import io
import os
from setuptools import setup, find_packages
import re


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.rst"), encoding="utf-8") as f:
        return f.read()


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "mintlemon", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


setup(
    name="mintlemon-turkish-nlp",
    version=get_version(),
    author="Nane&Limon",
    email="tarikkaan1koc@gmail.com",
    license="Apache License, Version 2.0",
    description="Mint & Lemon Turkish NLP Library developed by Mint & Lemon Development Team.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Teknofest-Nane-Limon/mintlemon-turkish-nlp",
    project_urls={
        "Tracker": "https://github.com/Teknofest-Nane-Limon/mintlemon-turkish-nlp/issues",
        "Documentation": "https://mintlemon-turkish-nlp.readthedocs.io",
    },
    packages = find_packages(exclude=["tests", "docs","examples"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="machine-learning, deep-learning, ml, nlp, turkish-nlp",
    python_requires=">=3.7.0",
)

