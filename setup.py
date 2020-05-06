
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    test_suite='nose.collector',
    tests_require=['nose'],
)
