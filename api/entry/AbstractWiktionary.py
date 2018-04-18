from api import IWiktionary


class AbstractWiktionary(IWiktionary):
    """ Default implementation of the :@link IWiktionary interface. """

    # -- Pages --

    def getPagesForWord(self, word, filter_=None, normalize=False):
        pass

    def getAllPages(self, filter_=None, sortByTitle=False, normalize=False):
        pass

    # -- Entries --

    def getEntriesForWord(self, word, filter_=None, normalize=False):
        pass

    def getAllEntries(self, filter_=None, sortByTitle=False, normalize=False):
        pass

    # -- Senses --

    def getSensesForWord(self, word, filter_=None, normalize=False):
        pass

    def getAllSenses(self, filter_=None, sortByTitle=False, normalize=False):
        pass
