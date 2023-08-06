import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pphw-utils",
    version="1.0.0",
    author="Miy",
    author_email="mew.proxy@hotmail.com",
    description="Utilities for records pipeline processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mew-www/xy-pphw-utils",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
