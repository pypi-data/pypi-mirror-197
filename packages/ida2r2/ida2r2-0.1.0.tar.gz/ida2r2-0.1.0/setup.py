from setuptools import setup

setup(
    name="ida2r2",
    version="0.1.0",
    description="IDA API adaptation layer to r2",
    url="https://github.com/FernandoDoming/ida2r2",
    author="Fernando Domínguez",
    author_email="fernando.dom.del@gmail.com",
    license="GNU GPL v3",
    packages=[
        "ida2r2",
    ],
    install_requires=[
        "r2pipe>=1.6.3",
    ],

    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ]
)