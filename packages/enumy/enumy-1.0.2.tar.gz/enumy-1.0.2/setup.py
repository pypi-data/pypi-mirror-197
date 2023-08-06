from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

SRC_DIR = "src"

setup(
    name="enumy",
    version="1.0.2",
    author="ByteSentinel",
    author_email="info@bytesentinel.io",
    description="Module to set predefined allowed values for a variable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytesentinel/enumy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    package_dir={"": SRC_DIR},
    packages=find_packages(SRC_DIR)
)