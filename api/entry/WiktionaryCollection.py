from .AbstractWiktionary import AbstractWiktionary
from api import IWiktionaryCollection
from api.util import HierarchicalWiktionaryIterator

from errors import IllegalStateException
from compat import List


class WiktionaryCollection(AbstractWiktionary, IWiktionaryCollection):
    """ Default implementation of the :@link IWiktionaryCollection interface. The
        implementation can be initialized with multiple :@link IWiktionaryEditions
        in order to access parsed Wiktionary information of multiple language
        editions. """

    def __init__(self):
        """ Initializes the Wiktionary collection. """
        self.editions = List()

    def addEdition(self, edition):
        if not self.editions and self.isClosed():
            raise IllegalStateException("WiktionaryCollection was already closed.")
        self.editions.append(edition)

    def getEditions(self):
        return self.editions

    def removeEdition(self, edition):
        self.editions.remove(edition)

    # -- Pages --

    def getPagesForId(self, id_):
        result = list()
        for edition in self.editions:
            page = edition.getPageForId(id_)
            if page is not None:
                result.append(page)

        return result

    def getPageForId(self, id_, entryLanguage):
        for edition in self.editions:
            if entryLanguage == edition.getLanguage():
                return edition.getPageForId(id)

        return None

    def getPagesForWord_(self, word, filter_=None, normalize=False):
        result = list()
        for edition in self.editions:
            page = edition.getPageForWord(word)
            if page is not None and (filter_ is None or filter_.accept(page)):
                result.append(page)

        return result

    def getPagesForWord(self, word, filter_=None, normalize=False):
        result = list()
        for edition in self.editions:
            result.append(edition.getPagesForWord(word, filter_, normalize))
        return result

    def getAllPages(self, filter_=None, sortByTitle=False, normalize=False):
        normalize = False

        def getInnerIterator(_, edition):
            return edition.getAllPages(filter_, sortByTitle, normalize)

        iterator = type("_HierarchicalWiktionaryIterator", (HierarchicalWiktionaryIterator,), {"getInnerIterator": getInnerIterator})
        return iterator(self.editions.iterator())

    # -- Entries --

    def getEntriesForWord(self, word, filter_=None, normalize=False):
        result = list()
        for edition in self.editions:
            result.append(*edition.getEntriesForWord(word, filter_, normalize))
        return result

    def getAllEntries(self, filter_=None, sortByTitle=False, normalize=False):

        def getInnerIterator(_, edition):
            return edition.getAllEntries(filter_, sortByTitle, normalize)

        iterator = type("_HierarchicalWiktionaryIterator", (HierarchicalWiktionaryIterator,), {"getInnerIterator": getInnerIterator})
        return iterator(self.editions.iterator())

    # -- Senses --

    def getSenseForKey(self, key, language):
        for edition in self.editions:
            if edition.getLanguage() == language:
                return edition.getSenseForKey(key)
        return None

    def getSensesForWord(self, word, filter_=None, normalize=False):
        result = list()
        for edition in self.editions:
            result.append(edition.getSensesForWord(word, filter_, normalize))
        return result

    def getAllSenses(self, filter_=None, sortByTitle=False, normalize=False):

        def getInnerIterator(_, edition):
            return edition.getAllSenses(filter_, sortByTitle, normalize)

        iterator = type("_HierarchicalWiktionaryIterator", (HierarchicalWiktionaryIterator,), {"getInnerIterator": getInnerIterator})
        return iterator(self.editions.iterator())

    # -- Close --

    def close(self):
        for edition in self.editions:
            edition.close()

    def isClosed(self):
        if not self.editions:
            return True

        for edition in self.editions:
            if edition.isClosed():
                return True

        return False
