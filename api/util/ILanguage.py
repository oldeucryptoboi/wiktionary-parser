class ILanguage:
    """ Generic interface for languages used in Wiktionary. Instances of ILanguage
        are used in as entry language of :@link IWiktionaryPages, the word
        language of :@link IWiktionaryEntrys, and the target language
        of :@link IWiktionaryTranslations. Each language is encoded using the
        international standard of language classification (ISO 639). Languages
        are compared by their internal code. """

    def getCode(self):
        """ Returns the internal language code used by JWTKL. These codes roughly
            correspond to ISO 639-3, but also include language families,
            deprecated classifications, and not yet classified languages. """
        pass

    def getName(self):
        """ Returns the language name (in English language). """
        pass

    def getISO639_1(self):
        """ Returns the ISO 639-1 code or an empty string if none. """
        pass

    def getISO639_2B(self):
        """ Returns the ISO 639-2b code or an empty string if none. """
        pass

    def getISO639_2T(self):
        """ Returns the ISO 639-2t code or an empty string if none. """
        pass

    def getISO639_3(self):
        """ Returns the ISO 639-3 code or an empty string if none. """
        pass
