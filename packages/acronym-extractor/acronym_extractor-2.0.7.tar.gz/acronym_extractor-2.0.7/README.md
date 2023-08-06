# Acronym Extraction
The Acronym Extraction package is a Python package that extracts acronyms from a PDF file. It uses the [tika](https://tika.apache.org/) 
package to extract text from the PDF file and then uses regular expressions to extract acronyms from the text. The package also
supports extracting acronyms from a text file.

## Requirements
The package requires the following packages to be installed:
* [python](https://www.python.org/)
* [openjdk](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html) (for tika)
* [tika](https://tika.apache.org/)
* [nltk](https://www.nltk.org/)
* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [lxml](https://lxml.de/)

## Installation
You can install the package via pip. Open your terminal and run the following command:
```bash
pip install acronym-extractor
```

## Usage
Once you've installed the package, you can import it in your Python code and use it as follows:
```bash
from acronym_extraction import AcronymExtractor
extractor = AcronymExtractor()
acronyms = extractor.extract_acronyms('path/to/file')
print(acronyms)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)