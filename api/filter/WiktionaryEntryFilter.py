from api.filter import WiktionaryPageFilter, IWiktionaryEntryFilter


class WiktionaryEntryFilter(WiktionaryPageFilter, IWiktionaryEntryFilter):
    """ Default implementation of the :@link IWiktionaryEntryFilter interface
        which inherits all filter options of the :@link WiktionaryPageFilter
        and additionally provides the possibility of filtering entries by word
        language and part of speech. """

    def __init__(self, allowedEntryLanguages=None, allowedPartsOfSpeech=None):
        """ Shorthand for setting the allowed entry language, word language,
            and parts of speech. Invoking this constructor is equivalent to
            using the default constructor and calling the corresponding
            setter methods. """

        super().__init__()
        if allowedEntryLanguages is None:
            self.allowedWordLanguages = set()
        else:
            self.allowedWordLanguages = allowedEntryLanguages

        if allowedPartsOfSpeech is None:
            self.allowedPartsOfSpeech = set()
        else:
            self.allowedPartsOfSpeech = allowedPartsOfSpeech

    # public WiktionaryEntryFilter(self, Set<ILanguage> ,
    #         final Set<ILanguage> allowedWordLanguages,
    #         final Set<PartOfSpeech> :
    #     this()
    #     setAllowedEntryLanguages(allowedEntryLanguages)
    #     setAllowedWordLanguages(allowedWordLanguages)
    #     setAllowedPartsOfSpeech(allowedPartsOfSpeech)

    def clear(self):
        super().clear()
        self.clearAllowedWordLanguages()
        self.clearAllowedPartsOfSpeech()

    # -- Word languages --

    def clearAllowedWordLanguages(self):
        """ Clears the list of allowed word languages. """
        self.allowedWordLanguages.clear()

    def getAllowedWordLanguages(self):
        """ Return an iterable of the list of all allowed word languages. """
        return self.allowedWordLanguages

    def setAllowedWordLanguages(self, allowedWordLanguages=None):
        self.clearAllowedWordLanguages()
        if allowedWordLanguages is not None:
            self.allowedWordLanguages.add(allowedWordLanguages)

    def acceptWordLanguage(self, entry):
        if not self.allowedWordLanguages:
            return True
        if entry.getWordLanguage() is None:
            return False

        return entry.getWordLanguage() in self.allowedWordLanguages

    # -- Parts of speech --

    def clearAllowedPartsOfSpeech(self):
        """ Clears the list of allowed parts of speech. """
        self.allowedPartsOfSpeech.clear()

    def getAllowedPartsOfSpeech(self):
        """ Return an iterable of the list of all allowed parts of speech. """
        return self.allowedPartsOfSpeech

    def setAllowedPartsOfSpeech(self, allowedPartsOfSpeech):
        """ Define the set of parts of speech which are allowed for a
            :@link IWiktionaryEntry. If no tag is specified, the restriction
            on the parts of speech will be cleared. """
        self.clearAllowedPartsOfSpeech()
        if allowedPartsOfSpeech is not None:
            self.allowedPartsOfSpeech.add(allowedPartsOfSpeech)

    def acceptPartOfSpeech(self, entry):
        if not self.allowedPartsOfSpeech:
            return True
        if entry.getPartOfSpeech() is None:
            return False

        return entry.getPartOfSpeech() in self.allowedPartsOfSpeech

    def accept(self, entry):
        if not self.accept(entry.getPage()):
            return False
        if not self.acceptWordLanguage(entry):
            return False
        if not self.acceptPartOfSpeech(entry):
            return False

        return True
