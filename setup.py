#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
    skip_if_exists,
)

HERE = os.path.dirname(os.path.abspath(__file__))


# The name of the project
name = "iturtle"

# Get the version
version = get_version(pjoin(name, "version.py"))


# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, "nbextension", "index.js"),
    pjoin(HERE, name, "labextension", "package.json"),
]


package_data_spec = {name: ["nbextension/**js*", "labextension/**"]}


data_files_spec = [
    ("share/jupyter/nbextensions/iturtle", "iturtle/nbextension", "**"),
    ("share/jupyter/labextensions/iturtle", "iturtle/labextension", "**"),
    ("share/jupyter/labextensions/iturtle", ".", "install.json"),
    ("etc/jupyter/nbconfig/notebook.d", ".", "iturtle.json"),
]


cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)
npm_install = combine_commands(
    install_npm(HERE, build_cmd="build:prod"),
    ensure_targets(jstargets),
)
cmdclass["jsdeps"] = skip_if_exists(jstargets, npm_install)


setup_args = dict(
    name=name,
    description="A Custom Jupyter Widget Library",
    version=version,
    scripts=glob(pjoin("scripts", "*")),
    cmdclass=cmdclass,
    packages=find_packages(),
    author="Samuel Zhang",
    author_email="qizh@datarho.tech",
    url="https://github.com/datarho/iturtle",
    license="MIT",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "Widgets", "IPython"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Jupyter",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "ipywidgets>=7.0.0",
        "svg.py>=1.4.2",
    ],
    extras_require={
        "test": [
            "pytest>=4.6",
            "pytest-cov",
            "nbval",
        ],
        "examples": [
            # Any requirements for the examples to run
        ],
        "docs": [
            "jupyter_sphinx",
            "nbsphinx",
            "nbsphinx-link",
            "pytest_check_links",
            "pypandoc",
            "recommonmark",
            "sphinx>=1.5",
            "sphinx_rtd_theme",
        ],
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
