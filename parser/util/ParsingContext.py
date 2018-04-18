from api.util import Language


class ParsingContext:
    """ Data object for information on the :@link IWiktionaryEntryParser. This
        entry parser creates and maintains an instance of this type to share
        information on the dump file with all its registed
        :@link IBlockHandlers. """

    def __init__(self, page, entryFactory=None):
        """ Create a new parsing context for the given Wiktionary page and
            use the specified entry factory to construct lexical entries. """
        self.page = page
        self.entryFactory = entryFactory
        self.language = None
        self.header = None
        self.partOfSpeech = None
        self.etymology = None
        self.pronunciations = None

    def getPage(self):
        """ Returns the current :@link WiktionaryPage that is being parsed. """
        return self.page

    def findEntry(self):
        """ Returns the :@link WiktionaryEntry that is currently being
            parsed. """
        return self.entryFactory.findEntry(self)

    def getLanguage(self):
        """ Returns the :@link ILanguage of the current
            :@link IWiktionaryEntry. """
        return self.language

    def setLanguage(self, language):
        """ Save the specified language in the context object. If the language
            changes, the header, part of speech tag, etymology, and pronunciations
            are reset to <code>None</code>. """
        if not Language.isEqual(language, self.language):
            # Language has changed: reset part of speech, etymology, and pronunciation.
            self.language = language
            self.header = None
            self.partOfSpeech = None
            self.etymology = None
            self.pronunciations = None

    def getHeader(self):
        """ Returns the header of the current:@link IWiktionaryEntry. The header
            usually corresponds to the lemma of the dictionary article. """
        return self.header

    def setHeader(self, header):
        """ Save the specified header in the context object. """
        self.header = header

    def getPartOfSpeech(self):
        """ Returns the :@link PartOfSpeech of the current
            :@link IWiktionaryEntry. """
        return self.partOfSpeech

    def setPartOfSpeech(self, partOfSpeech):
        """ Save the specified part of speech in the context object. """
        self.partOfSpeech = partOfSpeech

    def getEtymology(self):
        """ Returns the etymology of the current :@link IWiktionaryEntry. """
        return self.etymology

    def setEtymology(self, etymology):
        """ Save the specified etymology in the context object. """
        self.etymology = etymology

    def getPronunciations(self):
        """ Returns the pronunciations of the current :@link IWiktionaryEntry. """
        return self.pronunciations

    def setPronunciations(self, pronunciations):
        """ Save the specified pronunciations in the context object. """
        self.pronunciations = pronunciations
