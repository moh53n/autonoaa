#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autonoaa",
    version="0.0.1",
    author="Mohsen Tahmasebi",
    author_email="moh53n@outlook.com",
    description="An automatic weather satellite receiver for SDR dongles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moh53n/autonoaa",
    project_urls={
        "Bug Tracker": "https://github.com/moh53n/autonoaa/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    license='MIT',
    install_requires=['pyrtlsdr', 'numpy', 'scipy', 'Pillow', 'pyorbital'],
)
