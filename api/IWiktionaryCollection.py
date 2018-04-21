from api import IWiktionary


class IWiktionaryCollection(IWiktionary):
    """ Models a list of multiple Wiktionary language editions (e.g., the
        English and the German Wiktionary editions). Using the querying and
        iteration methods provided by this interface, the information from
        all attached language editions may be processed at once and their
        information can be combined. """

    def addEdition(self, edition):
        """ Add the specified Wiktionary language edition to the current
            collection. Querying the collection will then aggregate
            information from all added editions. """
        pass

    def getEditions(self):
        """ Returns a list of all Wiktionary langauge editions in
        this collection. """
        pass

    def removeEdition(self, edition):
        """ Removes the specified edition from the collection. Note that
            the removed edition is still open. If you do not need it anymore,
            call additionally the :@link IWiktionaryEdition#close() method. """
        pass

    # -- Pages --

    def getPageForId(self, id_, entryLanguage):
        """ Returns the page of the specified Wiktionary language edition with
            the given unique id.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getPagesForWord(self, word, filter_, normalize):
        """ Returns all pages with the given title. The method only returns the
            page if its title matches exactly. Use
            :param **kwargs:
            :@link #getPagesForWord(String, boolean) for case insensitive and
            string-normalized matching. Using the given
            :@link IWiktionaryPageFilter, unwanted pages can be ignored.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    # -- Entries --

    # -- Senses --

    def getSenseForKey(self, key, language):
        """ Returns the word sense with the given (edition-specific) unique id.
            Note that this id is only stable over the same XML dump and JWKTL
            version.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass
