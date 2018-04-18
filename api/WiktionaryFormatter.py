class WiktionaryFormatter:
    """ Utility class for producing simple string representations for the most
      commonly used JWKTL data objects. The string representations are designed
      for human perception rather than as an interoperable data exchange format. """

    __shared_dict = {}

    def __init__(self):
        self.__dict__ = self.__shared_dict

    @classmethod
    def instance(cls):
        return cls

    # -- Format methods --

    @classmethod
    def formatHeaderForPage(cls, page):
        """ Returns the ID and the title of the given page. """
        if page is None:
            return ""
        return page.getId() + " " + page.getTitle()

    @classmethod
    def formatHeaderForEntry(cls, entry):
        """ Returns the entry key, word, word language, and part of speech
           of the given entry. """
        if entry is None:
            return ""
        else:
            return entry.getKey() + " " + \
                   entry.getWord() + " (" + \
                   entry.getWordLanguage() + ", " + \
                   entry.getPartOfSpeech() + ")"

    @classmethod
    def formatHeaderForSense(cls, sense):
        """ Returns the sense key, word, sense index, and definition of
           the given word sense. """
        return "" + sense.getKey() + " " \
               + sense.getEntry().getWord() \
               + " [" + sense.getIndex() \
               + "]: " + sense.getGloss().getPlainText()

    @classmethod
    def formatPage(cls, page, languages):
        """ Returns a string representation of the given page using separate
           prefixed lines for each information type. """
        result = ""
        for entry in page.getEntries():
            # Restrict to the specified languages (if any).
            if languages is not None and len(languages) > 0:
                found = False
                for language in languages:
                    if language == entry.getWordLanguage():
                        found = True
                        break

                if not found:
                    continue

            result += cls.formatEntry(entry)

        for ws in page.getCategories():
            result += "  CAT: " + ws + "\n"
        iwl = set(page.getInterWikiLinks())
        result += "  INT: " + str(list(iwl)) + "\n"

        return result

    @classmethod
    def formatEntry(cls, entry):
        """ Returns a string representation of the given entry using separate
           prefixed lines for each information type. """
        result = ""
        result += entry.getWord() + "/" + entry.getPartOfSpeech() + " " + cls.formatLanguage(entry.getPage().getEntryLanguage()) + "/" + cls.formatLanguage(entry.getWordLanguage()) + "\n"

        if entry.getPronunciations() is not None:
            for p in entry.getPronunciations():
                result += "  PRO: " + p.getType().name() + " " + p.getText() + "\n"

        if entry.getWordEtymology() is not None:
            result += "  ETY: " + entry.getWordEtymology().getText() + "\n"

        for sense in entry.getSenses():
            result += cls.formatSense(sense)

        for ws in entry.getReferences():
            result += "  REF: " + ws.getText() + "\n"
        if entry.getEntryLink() is not None:
            result += "  LNK: " + entry.getEntryLinkType() + ": " + entry.getEntryLink() + "\n"

        return result

    @classmethod
    def formatSense(cls, sense):
        """ Returns a string representation of the given word sense using separate
           prefixed lines for each information type. """
        result = ""
        senseIdx = "-" if sense.getIndex() == 0 else str(sense.getIndex())

        if sense.getGloss() is not None:
            result += "  GLS [" + senseIdx + "] " + sense.getGloss().getText() + "\n"

        if sense.getExamples() is not None:
            for ws in sense.getExamples():
                result += "  EXP [" + senseIdx + "] " + ws.getText() + "\n"

        if sense.getQuotations() is not None:
            for quotation in sense.getQuotations():
                result += "  QTN [" + senseIdx + "] " + quotation.getSource().getText() + "\n"
                for ws in quotation.getLines():
                    result += "    " + ws.getText() + "\n"

        if sense.getRelations() is not None:
            result += ''.join(sorted(map(lambda relation: "  REL [" + senseIdx + "] " + relation.getRelationType() + ": " + relation.getTarget(), sense.getRelations())))
        if sense.getTranslations() is not None:
            result += ''.join(sorted(map(lambda translation: "  TRL [" + senseIdx + "] " + cls.formatLanguage(translation.getLanguage()) + ": " + translation.getTranslation(), sense.getTranslations())))

        return result

    @classmethod
    def formatLanguage(cls, language):
        if language is None:
            return "NULL"
        else:
            return language.getName().upper()
