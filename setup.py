from setuptools import setup, find_packages
import os

# Lee el contenido de README.md si existe
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="qastats",
    version="3.0.1",
    author="Jesus Cuesta",
    author_email="jcx@quantarmy.com",
    description="Advanced Reporting and Equity Statistics for Python",
    long_description=long_description or "Advanced Reporting and Equity Statistics for Python.",
    long_description_content_type="text/markdown",
    url="https://github.com/quantarmyz/QAStats",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "empyrical-reloaded",
        "pyfolio-reloaded",
        "ffn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)