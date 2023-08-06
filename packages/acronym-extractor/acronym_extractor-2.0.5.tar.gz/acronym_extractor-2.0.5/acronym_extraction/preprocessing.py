import re
from bs4 import BeautifulSoup

class Preprocessor:
    def __init__(self, stopwords, xhtml_metadata, xhtml_content):
        self.stopwords = stopwords
        self.xhtml_metadata = xhtml_metadata
        self.xhtml_content = xhtml_content

    def clean_xhtml(self):
        """ Clean the xml of the PDF.
        :return: cleaned xml.
        """

        # remove headers from xml
        self.xhtml_content = self.remove_headers()

        # remove references section from xml
        self.xhtml_content = self.remove_references_section()

        # remove figure captions from xml
        self.xhtml_content = self.remove_fig_captions()

        # remove links from xml
        self.xhtml_content = self.remove_links()

        # remove tables from xml
        self.xhtml_content = self.remove_para_tags()

        return self.xhtml_content


    def remove_headers(self):
        """ Remove headers from the xml.
        Methodology: If the regex: <p>Author.*</p> is found,
        remove data starting from the word 'Author' to the last </p> tag.
        :param content: xml of the given PDF.
        :param metadata: metadata of the given PDF.
        :return: modified xml without the headers.
        """

        author_names = []
        subject = ""
        try:
            authors = self.xhtml_metadata.get('Author', [])
            if authors:
                for author in authors:
                    names = author.split(' ')
                    # names could include periods like 'Izhar Ali' could be 'I. Ali'
                    names = [name for name in names if '.' not in name]
                    author_names.extend(names)
            else:
                return self.xhtml_content

            subject_meta = self.xhtml_metadata.get('subject', '')
            if subject_meta:
                # get the first alphabetic part of the subject
                for char in subject_meta:
                    if not char.isnumeric():
                        subject += char
                    else:
                        break

                subject = subject.strip()
                if not subject[-1].isalpha():
                    subject = subject[:-1]
            else:
                return self.xhtml_content

        except KeyError:
            return content

        match_headers = re.compile(r'<p>[^<>]*(' +
                                '|'.join(x for x in author_names) +
                                r')? (' +
                                subject +
                                r'.*?).*?</p>',
                                flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

        content = match_headers.sub('', str(self.xhtml_content))
        content = BeautifulSoup(content, features='lxml')
        return content


    def remove_references_section(self):
        """ Remove the references section from the xml.
        Methodology: If the regex: <p>References.*</p> is found,
        remove data starting from the word 'References' to the last </p> tag.
        :param content: xml of the given PDF.
        :return: modified xml without the references section.
        """

        match_references = re.compile(r'<p>References.*</p>',
                                    flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        content = match_references.sub('', str(self.xhtml_content))
        content = BeautifulSoup(content, features='lxml')
        return content


    def remove_fig_captions(self):
        """ Remove figure captions from the xml.
        Methodology: If the regex: <p>Fig.*</p> is found,
        remove data starting from the word 'Fig' to the last </p> tag.
        :param content: xml of the given PDF.
        :return: modified xml without the figure captions.
        """

        match_captions = re.compile(r'<p>[Ff]ig\..*?</p>|<p>[Ff]igure.*?</p>',
                                    flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        content = match_captions.sub('', str(self.xhtml_content))
        content = BeautifulSoup(content, features='lxml')
        return content


    def remove_links(self):
        """ Remove links from the xml.
        Methodology: If the regex: <a.*</a> is found,
        remove data starting from the word '<a' to the last </a> tag.
        :param content: xml of the given PDF.
        :return: modified xml without the links.
        """

        for tag in self.xhtml_content.find_all('div', attrs={'class': 'annotation'}):
            tag.extract()
        return self.xhtml_content


    def remove_para_tags(self):
        """ Remove all paragraph tags that do not contain a single stopword.
        This is a good approach to (mostly) remove images, tables, headers, links,
        embedded math formulas, etc.
        :param xhtml_content: xml of the given PDF.
        :return: modified xml without specified p tags.
        """

        for tag in self.xhtml_content.find_all('p'):
            if tag.text.strip() != "":
                words = tag.text.split()
                found = False
                for word in words:
                    if word in self.stopwords:
                        found = True
                        break

                # if the given tag had no single stopword, remove it
                if not found:
                    tag.extract()
        return self.xhtml_content