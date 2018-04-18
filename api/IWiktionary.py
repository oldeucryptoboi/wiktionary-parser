class IWiktionary:
    """ Base interface for the Wiktionary language edition and collection modelling
        common methods for querying and iterating over the encoded entries. """

    # -- Pages --

    def getPagesForWord(self, word, filter_, normalize):
        """ Returns the page with the given title. The method returns also pages,
            whose title matches in a case insensitive or string-normalized manner.
            The latter means that strings are converted to lower case, and
            umlauts or accents are substituted by their canonical form. The
            word "prêt-à-porter" is, e.g., normalized to "pret-a-porter". Using the
            given :@link IWiktionaryPageFilter, unwanted pages can be ignored.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getAllPages(self, filter_, sortByTitle, normalize):
        """ Returns an iterator over all :@link IWiktionaryPages within
            the Wiktionary edition. Using the given :@link IWiktionaryPageFilter,
            unwanted pages can be ignored.
            @param sortByTitle if <code>True</code> sort by page title
                otherwise by page id.
            @param normalize if <code>True</code> sort case insensitive
                otherwise case sensitive (only affects sorting by title). """
        pass

    # -- Entries --

    def getEntriesForWord(self, word, filter_, normalize):
        """ Returns a list of :@link IWiktionaryEntrys encoded on a page with
            the given title. Using the given  :@link IWiktionaryEntryFilter,
            unwanted entries can be ignored.
            @param normalize if <code>True</code>, match the page title in a
            case insensitive manner.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getAllEntries(self, filter_, sortByTitle, normalize):
        """ Returns an iterator over all :@link IWiktionaryEntrys within
            the Wiktionary edition. This is equivalent to iterating over all
            pages using :@link IWiktionaryEdition#getAllPages(boolean, boolean)
            and then over the page's entries using
            :@link IWiktionaryPage#getEntries().
            The pages are sorted according to the method's parameters the
            entries are sorted by their index. Using the given
            :@link IWiktionaryEntryFilter, unwanted entries can be ignored.
            @param sortByTitle if <code>True</code> sort by page title
                otherwise by page id.
            @param normalize if <code>True</code> sort case insensitive
            otherwise case sensitive (only affects sorting by title). """
        pass

    # -- Senses --

    def getSensesForWord(self, word, filter_, normalize):
        """ Returns a list of :@link IWiktionarySenses encoded on a page with
            the given title. Using the given  :@link IWiktionarySenseFilter,
            unwanted word senses can be ignored.
            @param normalize if <code>True</code>, match the page title in a
            case insensitive manner.
            @throws IllegalStateException if the connection has already been closed.
            @throws WiktionaryException upon database errors. """
        pass

    def getAllSenses(self, filter_, sortByTitle, normalize):
        """ Returns an iterator over all :@link IWiktionaryEntrys within
            the Wiktionary edition. This is equivalent to iterating over all
            pages using :@link IWiktionaryEdition#getAllPages(boolean, boolean)
            and then over the page's entries using
            :@link IWiktionaryPage#getEntries() and then over the entry's
            senses using :@link IWiktionaryEntry#getSenses().
            The pages are sorted according to the method's parameters the
            entries and senses are sorted by their index. Using the given
            :@link IWiktionarySenseFilter, unwanted word senses can be ignored.
            @param sortByTitle if <code>True</code> sort by page title
            otherwise by page id.
            @param normalize if <code>True</code> sort case insensitive
            otherwise case sensitive (only affects sorting by title). """
        pass

    # -- Close --

    def close(self):
        """ Disconnects from the database. This is necessary to ensure the
            consistency of the data. No retrieval methods can be called after
            closing the connection, so this should be done prior to terminating
            the application. Nothing happens on calling the method more than
            once. """
        pass

    def isClosed(self):
        """ Returns <code>True</code> if the database connection has already been
            closed using the :@link #close() method. """
        pass
