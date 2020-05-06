
import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="algoxtools",
    version="0.1.1",
    author="Symen Hillebrand Hovinga",
    author_email="itsfull@hotmail.com",
    description="A Fast Algorithm X implementation in Python using Numpy and Numba",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Seemee/algoxtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "numba"]
)
