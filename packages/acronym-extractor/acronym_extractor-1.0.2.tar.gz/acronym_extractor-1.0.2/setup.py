from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'Extracting acronym-definition pairs from pdf files'
LONG_DESCRIPTION = """
# Acronym Extractor
This package is used to extract acronym-definition pairs from pdf files.

## Prerequisites
If the file is a pdf, it uses tika to convert it to text. If the file is a text file, it reads the text from the file.
Before extracting acronyms, it cleans the text by removing extra lines, spaces, and redundant punctuations.

## How it works
The package uses a combination of regular expressions, extraction patterns, and context to extract acronyms. 
1. It first extracts acronyms using regular expressions. The regular expression is based on the assumption that acronyms are usually written in capital letters.
Therefore, it extracts acronyms that start with a capital letter and end with a capital letter but can have lowercase letters in between.

2. It then extracts acronyms using extraction patterns. The extraction patterns are based on the assumption that acronyms are usually defined in the following format:
> acronym, which is an abbreviation for long-form.
> acronym, which is a short-form for long-form.
> acronym, which is a contraction of long-form.
> ...

3. If the above two methods fail to extract an acronym, it returns the context of the acronym and leaves it to the user to decide whether it is an acronym or not.
"""

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
    install_requires=['nltk', 'tika', 'beautifulsoup4', 'lxml'],
    keywords=['python', 'acronyms', 'extraction', 'analysis'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={"Source Code": "https://github.com/ali-izhar/acronym_extraction"}
)