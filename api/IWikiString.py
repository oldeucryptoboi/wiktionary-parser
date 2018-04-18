class IWikiString:
    """ Represents a text that contains wiki markup. In addition to the original
        text containing the wiki markup, the interface allows extracting a list
        of wiki-internal and external links as well as a plain text representation
        (i.e., a text without markup). """

    def getText(self):
        """ Returns the original text including all wiki markup. """
        pass

    def getPlainText(self):
        """ Parses the original text to filter out all wiki markup and thus
            returns a human-readable version of the text. Note that the parsing
            might be done on demand, so avoid invoking this method repeatedly
            for the same text. """
        pass

    def getWikiLinks(self):
        """ Returns a list of wiki-internal links. That is, all substrings
            enclosed by two square brackets. Link captions will be removed.
            If no wiki links are found, an empty list will be returned. Note that
            the parsing might be done on demand, so avoid invoking this method
            repeatedly for the same text. """
        pass

    # def getExternalLinks(self):
    #     """ Returns a list of external links. That is, all valid URLs in the
    #      original text. If no external links are found, an empty list will
    #      be returned. Note that the parsing might be done on demand, so
    #      avoid invoking this method repeatedly for the same text. """
    #     pass
