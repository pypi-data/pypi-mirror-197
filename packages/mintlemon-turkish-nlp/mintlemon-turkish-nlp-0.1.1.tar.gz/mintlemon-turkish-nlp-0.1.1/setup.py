import io
import os

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.rst"), encoding="utf-8") as f:
        return f.read()

def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content

setuptools.setup(
    name="mintlemon-turkish-nlp",
    version=read("mintlemon", "VERSION"),
    author="Mint & Lemon",
    email="tarikkaan1koc@gmail.com",
    license="Apache License, Version 2.0",
    description="Mint & Lemon Turkish NLP Library developed by Mint & Lemon Development Team.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Teknofest-Nane-Limon/mintlemon-turkish-nlp",
    Tracker="https://github.com/Teknofest-Nane-Limon/mintlemon-turkish-nlp/issues",
    Documentation="https://mintlemon-turkish-nlp.readthedocs.io",
    packages=setuptools.find_packages(exclude=["tests"]),
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
    keywords="machine-learning, deep-learning, ml, nlp, turkish-nlp"
)
