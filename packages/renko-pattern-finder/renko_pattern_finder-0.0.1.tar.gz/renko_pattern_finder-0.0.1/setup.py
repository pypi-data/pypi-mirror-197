from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="renko_pattern_finder",
    version="0.0.1",
    description="Renko Pattern Finder.",
    py_modules=["renko_pattern_finder"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/aticio/renko_pattern_finder",
    author="Özgür Atıcı",
    author_email="aticiozgur@gmail.com",
)
