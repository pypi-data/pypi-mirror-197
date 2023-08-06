# Databricks notebook source
import setuptools

# COMMAND ----------
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="module_dataquality",
    version="1.0.4",
    author="Balbir",
    author_email="Balbir250894@gmail.com",
    description="data profiling and basic data quality rules check",
    long_description=long_description,
    long_description_content_type='text/markdown',
    # packages=setuptools.find_packages(include=['*']),
    packages=['dataqualitycheck', 'dataqualitycheck.datasources'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    #.....assuming pyspark, pyarrow is preinstalled 
    install_requires=['polars'],
    python_requires='>=3.8',
)

# COMMAND ----------


