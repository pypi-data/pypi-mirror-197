import re
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from requests import get
import string

stopword_list = stopwords.words('english')

def clean_text(text):
    """ Clean the text. Remove punctuation and extra spaces.
    :param text: raw text content.
    :return: cleaned text.
    """
    cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text

def extract_acronyms(text, extraction_patterns=True):
    """ Extract acronym-expansion pairs from the text.
    :param extraction_patterns: extract acronyms using extraction patterns (optional).
    :param text: raw text content.
    :return: a dictionary of acronyms and definitions.
    """

    # clean the text
    text = re.sub(r'[\n\t\r]+', ' ', text)  # remove extra lines and spaces
    text = re.sub(r' +', ' ', text).strip()  # remove extra spaces
    text = re.sub(r"(-\s+)", '', text).strip()  # tika fix: freq- uency --> frequency

    # Generate a pattern to extract acronyms
    re_pattern = r"\b[A-Z][A-Za-z\-]*[A-Z]s?\b"
    acronyms = re.finditer(re_pattern, text)

    definitions = {}
    frequencies = {}

    for match in acronyms:
        acronym = match.group()
        frequencies[acronym] = frequencies.get(acronym, 0) + 1

        start, end = match.start(), match.end()
        window_size = 60 if len(acronym) < 4 else 100
        left_window, right_window = text[start - window_size: end + 1], text[start: start + window_size]
        p0, p1, pl = acronym[0], acronym[1], acronym[-1]

        try:
            # forward search: short-form (long-form)
            forward = rf"{acronym}[^A-Z0-9\(\)\s-]*\s\(([a-z]|{p0})[a-z\s]*{p1}?[a-z\s]+[{pl}][a-z]+\)"
            success = search(forward, right_window, acronym, "forward")

            if success:
                if not definitions.get(acronym) or definitions[acronym].startswith("(Context)"):
                    definitions[acronym] = success
                elif success not in definitions[acronym]:
                    definitions[acronym] += '; ' + success
                continue

            # backward search: long-form (short-form)
            reverse = rf"(?<!{p0})(?<=\s){p0}[a-z\s-]*{p1}?[a-z\s]*\s?{pl}[a-z\s]*\s(?<=)\({acronym}\)"
            # reverse = rf"\b{p0}[a-z]+\s?[^{p0}]+(?:(?!\s{p1}?).)*{pl}[a-z]*(?:\s+\d+)?\s+\({acronym}\)"
            success = search(reverse, left_window, acronym, "reverse")
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

    definitions = dict(sorted(definitions.items(), key=lambda x: x[1]))
    return definitions, frequencies


def search(regex_pattern, text, acronym, direction):
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
        reject = len([c for c in definition.split()[:-1] if c in stopword_list]) > (len(acronym) - 1)

        if not reject:
            definition = definition.split("(")[0].strip()
        else:
            return None
    else:
        definition = definition.split("(")[1][:-1].strip()
        if len(definition.split()) == 1 and not definition.startswith(acronym[0]):
            return None

    return definition
