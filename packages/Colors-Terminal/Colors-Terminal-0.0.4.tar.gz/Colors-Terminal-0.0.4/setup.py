import setuptools

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Colors-Terminal",
    version="0.0.4",
    author="xXBlackDev9010Xx",
    author_email="tecnoblue9010@gmail.com",
    description="colors_terminal this tool help decorate your terminal in Python fast and easy :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xXBlackDev9010Xx/colors_terminal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
