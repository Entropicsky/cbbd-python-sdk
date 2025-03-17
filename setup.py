"""
Setup script for the CBBD Python SDK.
"""

import os
from setuptools import setup, find_packages

# Get version from cbbd/__init__.py
with open("cbbd/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

# Get long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

# Get requirements from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="cbbd-python-sdk",
    version=version,
    description="Python SDK for the College Basketball Data API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stewart Chisam",
    author_email="stewart.chisam@example.com",
    url="https://github.com/entropicsky/cbbd-python-sdk",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="basketball, sports, api, sdk, cbbd, college",
    project_urls={
        "Bug Tracker": "https://github.com/entropicsky/cbbd-python-sdk/issues",
        "Documentation": "https://github.com/entropicsky/cbbd-python-sdk",
        "Source Code": "https://github.com/entropicsky/cbbd-python-sdk",
    },
) 