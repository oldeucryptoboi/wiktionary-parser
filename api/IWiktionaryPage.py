class IWiktionaryPage:
    """ A :@link IWiktionaryPage corresponds to a unique URL of Wiktionary. That
      is, a distinct web page, such as http://en.wiktionary.org/wiki/plant. The
      notion is mostly equivalent to the lexicographic definition of a lexical
      item. Since non-linguistically pages are filtered out, an
      :@link IWiktionaryPage encodes linguistic information on a certain word
      form (e.g., plant) using multiple :@link IWiktionaryEntrys (distinguishing
      the English noun, the English verb, the Dutch noun, etc. Each
      :@link IWiktionaryPage belongs to exactly one :@link IWiktionaryEdition. """

    # -- Identifier --

    def getKeys(self):
        """ Returns a unique ID for this page. The ID is unique for all
           :@link IWiktionaryPages of the :@link IWiktionaryEdition and
           remains persistent regardless of the JWKTL software version or
           the date of the XML data dump of Wiktionary. """
        pass

    def getId(self):
        """ Returns the unique ID for this page. This method is equivalent
           to :@link #getKey(), but returns the ID as a numerical value. """
        pass

    # -- Page --

    def getTitle(self):
        """ Returns the title of this Wiktionary page which usually corresponds
           to the lemma of all lexical entries described on this page. """
        pass

    def getTimestamp(self):
        """ Returns the timestamp of this revision - i.e., the date of the
           last change of the page. """
        pass

    def getRevision(self):
        """ Returns the ID of this revision - i.e., a unique number of the
           last change made to the page. """
        pass

    def getAuthor(self):
        """ Returns the author of this revision - i.e., the name of the user
           that made the last change to the page. """
        pass

    def getEntryLanguage(self):
        """ Returns the language that this page is written in. This is always
           the language of the whole Wiktionary language edition - i.e. equivalent
           to :@link IWiktionaryEdition#getLanguage(). As opposed to that,
           the language of a word can be retrieved by
           :@link IWiktionaryEntry#getWordLanguage(). There is, for example,
           a Wiktionary page "plant" in the German Wiktionary language edition
           that encodes a lexical entry on the word "plant" of the English
           language. The entry language would be German and the word language
           would be English in this case. """
        pass

    def getCategories(self):
        """ Returns all categories of the Wiktionary page that are manually
           defined. Categories being derived automatically by using templates
           are not returned. The returned list is never <code>None</code>. """
        pass

    def getInterWikiLinks(self):
        """ Returns a list of inter-wiki links of this Wiktionary page. Inter-wiki
           links are links to other language editions of Wiktionary - e.g., from
           the English page "plant" to the German page "plant". Note that this
           is not a translation, but always the same word form. Use
           :@link IWiktionarySense#getTranslations() for word translations.
           The returned list is never <code>None</code>. """
        pass

    def getRedirectTarget(self):
        """ Returns the page title that a redirect page targets at. The method
           returns <code>None</code> if the page is not a redirection page. """
        pass

    # -- Entries --

    def getEntry(self, index):
        """ Returns the :@link IWiktionaryEntry with the given index. The index
           is a running number starting at zero.
           @throws ArrayIndexOutOfBoundsException if there is no entry with
             the given index. """
        pass

    def getEntryCount(self):
        """ Returns the number of :@link IWiktionaryEntrys encoded on this
           page. """
        pass

    def getEntries(self):
        """ Returns the list of all :@link IWiktionaryEntrys. The list is
           never <code>None</code> and yields equivalent results to using
           :@link #getEntry(int) for all indices from zero to
           :@link #getEntryCount(). """
        pass
