import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="treasure-trove",
    version="0.1",
    author="Zach Hafen-Saavedra",
    author_email="zachary.h.hafen@gmail.com",
    description="Data and pipeline management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhafen/trove",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'h5py>=3.8.0',
        'mock>=5.0.1',
        'nbconvert>=6.5.4',
        'nbformat>=5.7.3',
        'numpy>=1.23.5',
        'setuptools>=65.6.3',
        'simple_augment>=1.0',
    ],
)
