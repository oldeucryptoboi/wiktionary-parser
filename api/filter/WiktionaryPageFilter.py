from api.filter.IWiktionaryPageFilter import IWiktionaryPageFilter


class WiktionaryPageFilter(IWiktionaryPageFilter):
    """ Default implementation of the :@link IWiktionaryPageFilter interface
        which provides the possibility of filtering out pages with certain
        entry languages. This is useful if a :@link IWiktionaryCollection is
        used to access multiple :@link IWiktionaryEditions of different
        entry languages. """

    def __init__(self):
        """ Initializes a page filter without any filter restrictions. """
        self.allowedEntryLanguages = set()

    def clear(self):
        """ Clears all filter options. """
        self.clearAllowedEntryLanguages()

    def clearAllowedEntryLanguages(self):
        """ Clears the list of allowed entry languages. """
        self.allowedEntryLanguages.clear()

    def getAllowedEntryLanguages(self):
        """ Return an iterable of the list of all allowed entry languages. """
        return self.allowedEntryLanguages

    def setAllowedEntryLanguages(self, allowedEntryLanguages):
        """ Define the set of entry languages which are allowed for a
            :@link IWiktionaryPage. If no language is specified, the restriction
            on the entry language will be cleared. """
        self.clearAllowedEntryLanguages()
        for language in allowedEntryLanguages:
            self.allowedEntryLanguages.add(language)

    def acceptEntryLanguage(self, page):
        if not self.allowedEntryLanguages:
            return True
        if page.getEntryLanguage() is None:
            return False

        return page.getEntryLanguage() in self.allowedEntryLanguages

    def accept(self, page):
        return self.acceptEntryLanguage(page)
