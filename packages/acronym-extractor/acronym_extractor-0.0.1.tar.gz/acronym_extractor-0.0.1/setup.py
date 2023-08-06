from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Extracting acronym-definition pairs from pdf files'
LONG_DESCRIPTION = 'This package is used to extract acronym-definition pairs from pdf files. It uses tika to extract text from pdf files and then uses regex to extract acronyms and definitions.'

# Setting up
setup(
    name="acronym_extractor",
    version=VERSION,
    author="Izhar Ali",
    author_email="<izharali.skt@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'nltk', 'tika', 'beautifulsoup4'],
    keywords=['python', 'acronyms', 'extraction', 'analysis'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)