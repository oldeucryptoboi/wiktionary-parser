from api import IWiktionary


class IWiktionaryEdition(IWiktionary):
    """ Models a single Wiktionary language edition (e.g., the English Wiktionary)
      for which this interface provides multiple querying and iteration methods. """

    def getLanguage(self):
        """ Returns the language of the Wiktionary edition, which is equivalent
            to the entry language of the contained entries. """
        pass

    def getDBPath(self):
        """ Returns the file path of the parsed database. """
        pass

    # -- Pages --

    def getPageForId(self, id_):
        """ Returns the page with the given unique id.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getPageForWord(self, word):
        """ Returns the page with the given title. The method only returns the
            page if its title matches exactly. Use
            :@link #getPagesForWord(String, boolean) for case insensitive and
            string-normalized matching.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    # -- Entries --

    def getEntryForId(self, entryId):
        """ Returns the :@link IWiktionaryEntry with the given entry id. Note
            that this id is only stable over the same XML dump and JWKTL version.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getEntryForPageId(self, pageId, entryIdx):
        """ Returns the :@link IWiktionaryEntry with the given page id and
            entry index. Note that this id combination is only stable over the
            same XML dump and JWKTL version.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getEntryForWord(self, word, entryIdx):
        """ Returns the :@link IWiktionaryEntry encoded on a page with
            the given title and being part of an entry with the specified entry
            index. The method only returns the entries if the page title
            matches exactly.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    # -- Senses --

    def getSenseForKey(self, id_):
        """ Returns the word sense with the given unique id. Note that this id
           is only stable over the same XML dump and JWKTL version.
           @throws IllegalStateException if the connection has already been closed.
           @throws WiktionaryException upon database errors. """
        pass

    def getSenseForId(self, entryId, senseIdx):
        """ Returns the word sense with the given entry id and sense index. Note
           that this id combination is only stable over the same XML dump and
           JWKTL version.
           @throws IllegalStateException if the connection has already been closed.
           @throws WiktionaryException upon database errors. """
        pass

    def getSenseForPageId(self, pageId, entryIdx, senseIdx):
        """ Returns the word sense with the given page id, entry index, and sense
           index. Note that this id combination is only stable over the same XML
           dump and JWKTL version.
           @throws IllegalStateException if the connection has already been closed.
           @throws WiktionaryException upon database errors. """
        pass

    def getSensesForWord_(self, word, entryIdx, senseIdx):  # TODO: Rename it.
        """ Returns the :@link IWiktionarySense encoded on the page with
           the given title and being part of the entry with the specified entry
           index at the specified sense index. The method only returns the
           sense if the page title matches exactly.
           @throws IllegalStateException if the connection has already been closed.
           @throws WiktionaryException upon database errors. """
        pass
