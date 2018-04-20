class EntryFactory:
    """ Factory for :@link WiktionaryEntrys used by the parsers. """

    def findEntry(self, context):
        """ Checks if the current page contains a :@link WiktionaryEntry
            matching for the current context (part of speech, language, etc.)
            and returns it. If no entry could be found, a new one is created
            (using :@link #createEntry(ParsingContext)). """
        language = context.getLanguage()
        partOfSpeech = context.getPartOfSpeech()

        posEntryList = list(filter(lambda entry: language == entry.getWordLanguage(),
                                   list(
                                       filter(lambda entry: partOfSpeech == entry.getPartOfSpeech(),
                                              context.getPage().entries))))

        if not posEntryList:
            entry = self.createEntry(context)
            context.getPage().addEntry(entry)
            return entry
        else:
            return posEntryList[-1]

    @classmethod
    def createEntry(cls, context):
        """ Create a new :@link WiktionaryEntry  based on the current context.
            This method always creates a new entry. Use
            :@link #findEntry(ParsingContext) if you want to use existing
            entries (which is usually the case). """

        language = context.getLanguage()
        partOfSpeech = context.getPartOfSpeech()
        header = context.getHeader()

        entry = context.getPage().createEntry()
        entry.setWordLanguage(language)
        entry.addPartOfSpeech(partOfSpeech)
        if header is not None:
            entry.setHeader(header)
        entry.setWordEtymology(context.getEtymology())
        return entry

    def findPartOfSpeech(self, name):
        """ Converts the given string into a part of speech enum type. """
        pass
