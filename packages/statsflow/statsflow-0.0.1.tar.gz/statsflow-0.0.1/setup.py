from setuptools import setup
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='statsflow',
    version='0.0.1',
    description='This Python package consist of various statistical modules and function that can be  very useful for data preprocessing,data transformation,EDA and seamlessly improves the performance of Ml-Pipeline',
    author= 'Ragul s',
    url = 'https://github.com/ragulslrk/statsflow_pkgs',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    long_description=long_description,
    keywords=['statistics', 'plotting', 'probplot','data transformation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=['statsflow'],
    package_dir={'src':'src'},
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        

    ]
)