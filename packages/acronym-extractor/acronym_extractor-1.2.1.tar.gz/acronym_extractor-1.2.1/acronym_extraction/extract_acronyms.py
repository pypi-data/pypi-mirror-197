import re
import sys
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from tika import tika, parser
from typing import Tuple, Dict
from .preprocessing import Preprocessor

try:
    tika.checkTikaServer()
except tika.TikaServerEndpointError:
    print("Tika server is not running")
    sys.exit(1)


class AcronymExtractor:
    def __init__(self):
        self.stopword_list = stopwords.words('english')

    def convert_pdf_to_text(self, pdf_path: str) -> str:
        """ Convert a PDF file to text.
        :param pdf_path: path to the PDF file.
        :return: raw text content.
        """
        try:
            raw = parser.from_file(pdf_path, xmlContent=True)
            xhtml_metadata = raw['metadata']
            xhtml_content = BeautifulSoup(raw['content'], features='lxml')
            process = Preprocessor(self.stopword_list, xhtml_metadata, xhtml_content)
            xhtml_content = process.clean_xhtml()
            text = ''.join(xhtml_content.findAll(text=True))
        except Exception as e:
            print(f"Error while converting PDF to text: {e}")
            sys.exit(1)
        
        return text

    def extract_acronyms(self, pdf_path: str, extraction_patterns: bool = True) -> Tuple[Dict, Dict]:
        """ Extract acronym-expansion pairs from a PDF file.
        :param extraction_patterns: extract acronyms using extraction patterns (optional).
        :param pdf_path: path to the PDF file.
        :return: a dictionary of acronyms and definitions.
        """

        # check if the file is a PDF or a text file
        if pdf_path.endswith('.txt'):
            text = open(pdf_path, 'r', encoding='utf-8').read()
        else:
            text = self.convert_pdf_to_text(pdf_path)
    
        if not text.strip():
            return "No text found in the file."

        text = re.sub(r'[\n\t\r]+', ' ', text)      # remove extra lines and spaces
        text = re.sub(r' +', ' ', text).strip()     # remove extra spaces
        text = re.sub(r"(-\s+)", '', text).strip()  # tika fix: freq- uency --> frequency

        # Generate a pattern to extract acronyms
        re_pattern = r"\b[A-Z][A-Za-z\-]*[A-Z]s?\b"
        acronyms = re.finditer(re_pattern, text)
        definitions = {}

        for match in acronyms:
            acronym = match.group()
            start, end = match.start(), match.end()
            window_size = 60 if len(acronym) < 4 else 100
            left_window, right_window = text[start - window_size: end + 1], text[start: start + window_size]
            p0, p1, pl = acronym[0], acronym[1], acronym[-1]

            try:
                # forward search: short-form (long-form)
                forward = rf"{acronym}[^A-Z0-9\(\)\s-]*\s\(([a-z]|{p0})[a-z\s]*{p1}?[a-z\s]+[{pl}][a-z]+\)"
                success = self.search(forward, right_window, acronym, "forward")

                if success:
                    if not definitions.get(acronym) or definitions[acronym].startswith("(Context)"):
                        definitions[acronym] = success
                    elif success not in definitions[acronym]:
                        definitions[acronym] += '; ' + success
                    continue

                # backward search: long-form (short-form)
                reverse = rf"(?<!{p0})(?<=\s){p0}[a-z\s-]*{p1}?[a-z\s]*\s?{pl}[a-z\s]*\s(?<=)\({acronym}\)"
                success = self.search(reverse, left_window, acronym, "reverse")
                if success:
                    if not definitions.get(acronym) or definitions[acronym].startswith("(Context)"):
                        definitions[acronym] = success
                    elif success not in definitions[acronym]:
                        definitions[acronym] += '; ' + success
                    continue

                # extract acronyms using extraction patterns
                if extraction_patterns:
                    capture_def = rf"({p0}[a-z]+\s?{p1}[a-z\s]*(\b{pl}(?:[a-z]+)?))"
                    pattern = rf"{acronym},?\s?(?:which|that|also)?\s?(?:is|are|a)?\s?" \
                            rf"(?:abbreviated|termed|represented|denoted)?\s?(?:an acronym|an abbreviation|short|" \
                            rf"shorthand|contraction|also known|AKA|stands|denotes)?\s?(?:commonly)?\s?" \
                            rf"(?:referred to|known)?\s?(?:by|for|as|the)?\s?{capture_def}"
                    definition = re.search(pattern, right_window, re.IGNORECASE | re.VERBOSE)
                    if definition:
                        if not definitions.get(acronym) or definitions[acronym].startswith("(Context)"):
                            definition = definition.group(1)
                            definitions[acronym] = definition
                            continue

            except re.error:
                continue

            # otherwise, return the first occurrence of the acronym in context
            if not definitions.get(acronym):
                sentence = left_window[len(left_window) // 4:-1] + right_window[len(acronym):len(right_window) // 4]
                context = "(Context) " + sentence.strip()
                definitions[acronym] = context

        print("Acronyms extracted: ", len(definitions))
        print("Acronyms in context: ", len([d for d in definitions.values() if d.startswith("(Context)")]))
        print("Acronyms with definitions: ", len([d for d in definitions.values() if not d.startswith("(Context)")]))

        definitions = dict(sorted(definitions.items(), key=lambda x: x[1]))
        return definitions


    def search(self, regex_pattern: str, text: str, acronym: str, direction: str) -> str:
        """ Search for the definition of an acronym in the text.
        :param regex_pattern: regex pattern to extract the definition.
        :param text: raw text content.
        :param acronym: acronym to be defined.
        :param direction: forward or backward search.
        :return: the definition of the acronym.
        """
        match = re.search(regex_pattern, text, re.IGNORECASE)
        if not match:
            return None

        definition = str(match.group())
        if direction == "reverse":
            while len(definition.split()[:-1]) > len(acronym):
                filtered = re.search(regex_pattern, definition, re.IGNORECASE)
                if not filtered:
                    break
                definition = filtered.group().strip()

            # reject a definition of n words if it contains more than (n - 1) stopwords
            reject = len([c for c in definition.split()[:-1] if c in self.stopword_list]) > (len(acronym) - 1)

            if not reject:
                definition = definition.split("(")[0].strip()
            else:
                return None
        else:
            definition = definition.split("(")[1][:-1].strip()
            if len(definition.split()) == 1 and not definition.startswith(acronym[0]):
                return None
        return definition