from setuptools import setup

setup(
    name="r2magicstrings",
    version="0.1.0",
    description="IDAMagicStrings ported to radare2",
    url="https://github.com/FernandoDoming/r2magicstrings",
    author="Fernando Domínguez",
    author_email="fernando.dom.del@gmail.com",
    license="GNU GPL v3",
    packages=[
        "r2magicstrings",
    ],
    install_requires=[
        "ida2r2>=0.1.0",
    ],

    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    entry_points = {
        "console_scripts": ["r2magicstrings=r2magicstrings.r2_magic_strings:main"]
    }
)