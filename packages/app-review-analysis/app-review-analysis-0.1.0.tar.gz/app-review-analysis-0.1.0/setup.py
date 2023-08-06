from setuptools import setup, find_packages

setup(
    name="app-review-analysis",
    version="0.1.0",
    author="Jiayang Cheng",
    author_email="jiayangcheng21@gmail.com",
    description="A package for analyzing app reviews",
    packages=find_packages(),
    install_requires=["app_store_scraper"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
