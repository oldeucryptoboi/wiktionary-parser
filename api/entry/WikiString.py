from api import IWikiString
import re


class WikiString(IWikiString):
    """  Implementation of :@link IWikiString that parses the original text (in
        wiki markup language) on demand instead of storing the parsed information
        in the database. """

    # noinspection PyMissingConstructor
    def __init__(self, text):
        """ Create a new wiki string for the given wiki markup text. """
        self.text = text

    def getText(self):
        return self.text

    def setText(self, text):
        """ Assign the given text as the new wiki markup text. """
        self.text = text

    def getTextIncludingWikiMarkup(self):
        """ @see #getText(). """
        return self.getText()

    COMMENT_PATTERN = re.compile("<!--.+?-->")
    QUOTES_PATTERN = re.compile("'''?")
    WIKILINK_PATTERN = re.compile("\\[\\[((?:[^|\\]]+?\\|)*)([^|\\]]+?)\\]\\]")
    # EXTERNAL_LINK_PATTERN = re.compile("\\[\\w+://\\w+\\]")
    TEMPLATE_PATTERN = re.compile("{{.+?\\}\\}")
    REFERENCES_PATTERN = re.compile("<ref[^>]*>.+?</ref>")
    HTML_PATTERN = re.compile("<[^>]+>")
    WHITESPACE_PATTERN = re.compile("\\s\\s+")

    def getPlainText(self):
        return self.makePlainText(self.text)

    def getWikiLinks(self):
        result = list()
        startIndex = self.text.find("[[")
        while startIndex != -1:
            endIndex = self.text.find("]]", startIndex)
            if endIndex != -1:
                wikifyBlock = self.text[startIndex + 2: endIndex]
                midIndex = wikifyBlock.lastIndexOf("|")
                if midIndex != -1:
                    word = wikifyBlock[midIndex + 1: len(wikifyBlock)]
                    result.append(word)
                else:
                    result.append(wikifyBlock)
                startIndex = self.text.find("[[", endIndex)
            else:
                startIndex = -1

        return result

    def __str__(self):
        return self.getPlainText()

    def makePlainText(self, wikiText):
        """ Transforms the given wiki markup text into a plain text version.
            That is, wiki links, templates, and typographic markers are being
            removed or substituted in order to obtain a human-readable text. """
        result = wikiText
        result = result.replace("\t", " ")
        result = re.sub(self.COMMENT_PATTERN, "", result)
        result = re.sub(self.QUOTES_PATTERN, "", result)
        result = self.removeWikiLinks(result)
        # result = self.EXTERNAL_LINK_PATTERN.matcher(result).replaceAll("")
        result = re.sub(self.REFERENCES_PATTERN, "", result)
        result = re.sub(self.TEMPLATE_PATTERN, "", result)
        result = re.sub(self.HTML_PATTERN, "", result)
        result = result.replace("’", "'")
        result = result.replace("�", "'")
        result = result.replace("°", "")
        result = re.sub(self.WHITESPACE_PATTERN, " ", result)
        while len(result) > 0 and result[0:1] in "*: ":
            result = result[1:]
        return result.strip()

    @classmethod
    def removeWikiLinks(cls, text):
        return re.sub(cls.WIKILINK_PATTERN, r'\2', text)
