"""
Setup script for Random Sampling Point Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="random-sampling-generator",
    version="1.0.0",
    author="Cole Regnier",
    author_email="nr466@cornell.edu",
    description="Generate random sampling points inside polygon boundaries with minimum distance spacing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random_sampling_generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "random-sampling=random_sampling.cli:main",
        ],
    },
    keywords="sampling, kml, gis, agriculture, fieldwork, random points",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/random_sampling_generator/issues",
        "Source": "https://github.com/yourusername/random_sampling_generator",
        "Documentation": "https://github.com/yourusername/random_sampling_generator/tree/main/docs",
    },
) 