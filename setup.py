import setuptools


with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="pyMenuConf",
    version="0.0.1",
    author="ChunYoLin",
    author_email="jeff042099@gmail.com",
    description="A simple command-line menu creation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChunYoLin/pyMenuConf.git",
    packages=setuptools.find_packages(),
    classifiers=(
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    ),
)
