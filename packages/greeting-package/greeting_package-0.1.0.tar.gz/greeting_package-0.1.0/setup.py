import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="greeting_package",
    version="0.1.0",
    author="Jeff Osundwa",
    author_email="mulamajeff@tuta.io",
    description="A package for generating greeting messages",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifier=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
