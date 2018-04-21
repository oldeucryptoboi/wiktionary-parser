import itertools

from errors import IllegalStateException

from .AbstractWiktionary import AbstractWiktionary
from api import IWiktionaryEdition
from api.util import WiktionaryIterator


def flatMap(lst):
    itertools.chain(*lst)


class WiktionaryEdition(AbstractWiktionary, IWiktionaryEdition):
    """ Abstract base class for implementations of :@link IWiktionaryEditions. """

    def __init__(self):
        """ Initializes the Wiktionary edition. """
        self.isClosed = False

    # -- Entries --

    def getEntryForPageId(self, pageId, entryIdx):
        self.ensureOpen()
        page = self.getPageForId(pageId)
        return None if page is None else page.getEntries().get(entryIdx)

    def getEntryForWord(self, word, entryIdx):
        page = self.getPageForWord(word)
        return None if page is None else page.getEntries().get(entryIdx)

    def getEntriesForWord(self, word, filter_=None, normalize=False):
        self.ensureOpen()
        if word is None or not len(word):
            return list()
        else:
            return list(entry for entry in flatMap(self.getPagesForWord(word, normalize)) if
                        filter_ is None or filter_.accept(entry))

    def getAllEntries(self, filter_=None, sortByTitle=False, normalize=False):
        self.ensureOpen()

        # noinspection PyShadowingNames
        def fetchNext(self):
            while True:
                # If there are no entries left, try to fetch the next page.
                if self.entries is None or not self.entries.hasNext():
                    if self.fetchNextPage() is None:
                        return None  # No page left.

                # As long as entries are left, return them!
                if self.entries is not None and self.entries.hasNext():
                    result = self.entries.next()
                    if filter_ is None or filter_.accept(result):
                        return result

        # noinspection PyShadowingNames
        def fetchNextPage(self):
            if not self.allPages.hasNext():
                return None

            result = self.allPages.next()
            self.entries = result.getEntries().iterator()
            return result

        iterator = type(
            "_WiktionaryIterator",
            (WiktionaryIterator,),
            {
                "allPages": self.getAllPages(None, sortByTitle, normalize),
                "fetchNext": fetchNext,
                "fetchNextPage": fetchNextPage,
                "doClose": self.allPages.close,
            }
        )
        return iterator()

    # -- Senses --

    def getSenseForId(self, entryId, senseIdx):
        self.ensureOpen()
        entry = self.getEntryForId(entryId)
        return None if entry is None else entry.getSense(senseIdx)

    def getSenseForPageId(self, pageId, entryIdx, senseIdx):
        self.ensureOpen()
        entry = self.getEntryForPageId(pageId, entryIdx)
        return None if entry is None else entry.getSense(senseIdx)

    def getSensesForWord_(self, word, entryIdx, senseIdx=None):
        self.ensureOpen()
        entry = self.getEntryForWord(word, entryIdx)
        if senseIdx is None:
            result = [sense for sense in entry.getSenses()]
            return result
        else:
            entry = self.getEntryForWord(word, entryIdx)
            return None if entry is None else entry.getSense(senseIdx)

    def getSensesForWord(self, word, filter_=None, normalize=False):
        self.ensureOpen()
        result = list()
        if not word:
            return result

        pages = self.getPagesForWord(word, normalize)
        for page in pages:
            for entry in page.getEntries():
                for sense in entry.getSenses():
                    if filter_ is None or filter_.accept(sense):
                        result.append(sense)

        return result

    def getAllSenses(self, filter_=None, sortByTitle=False, normalize=False):
        self.ensureOpen()

        # noinspection PyShadowingNames
        def fetchNext(self):
            while True:
                if self.senses is None or not self.senses.hasNext():
                    if self.fetchNextEntry() is None:
                        return None

                if self.senses is not None and self.senses.hasNext():
                    result = self.senses.next()
                    if filter_ is None or filter_.accept(result):
                        return result

        # noinspection PyShadowingNames
        def fetchNextEntry(self):
            if not self.allEntries.hasNext():
                return None

            result = self.allEntries.next()
            self.senses = result.getSenses().iterator()
            return result

        # noinspection PyShadowingNames
        def doClose(self):
            self.allEntries.close()

        return type("_WiktionaryIterator", (WiktionaryIterator,),
                    {"allEntries": self.getAllEntries(sortByTitle, normalize), "fetchNext": fetchNext, "fetchNextEntry": fetchNextEntry,
                     "doClose": doClose})()

    # -- Close --

    def close(self):
        """ Disconnects from the database. This is necessary to ensure the
         *  consistency of the data. No retrieval methods can be called after
         *  closing the connection, so this should be done prior to terminating
         *  the application. Nothing happens on calling the method more than
         *  once. """
        if self.isClosed:
            return

        self.doClose()
        self.isClosed = True

    def isClosed(self):
        """ Returns if the connection has already been closed. If so, no
         *  retrieval method can be called anymore. To close an open
         *  connection, use the :@link #close() method. """
        return self.isClosed

    def doClose(self):
        pass

    def ensureOpen(self):
        """ @throws IllegalStateException if the connection has already been
         *         closed. This method is to be called from each retrieval method.  """
        if self.isClosed:
            raise IllegalStateException("Wiktionary was already closed.")
