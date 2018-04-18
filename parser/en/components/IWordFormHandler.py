class IWordFormHandler:

    def parse(self, line):
        """ Start parsing the specified text for inflected word forms. The
            extracted forms can be accessed using :@link #getWordForms()
            once all lines have been parsed.

            @param line a line of wikitext
            @return whether the handler could parse the line """
        pass

    def getWordForms(self):
        """
         * @return a list of extracted word forms, or an empty list.
         """
        pass

    def getGenders(self):
        """
         * @return the extracted genders (might be None).
         """
        pass

    def getRawHeadwordLine(self):
        """
         * @return the unprocessed headline
         * @see <a href="https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Headword_line">WT:EL Headword line</a>
         """
        pass
