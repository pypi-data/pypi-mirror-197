# setup.py
from setuptools import setup, find_packages

setup(
    name="python-ss-logging-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pino",
        "nanoid",
        # Add other dependencies if needed
    ],
    author="Jimmy",
    author_email="jimm@xxx.com",
    description="A simple logger package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
