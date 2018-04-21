import unicodedata
import re

from api.util import Language
from .WiktionaryEntry import WiktionaryEntry
from api import IWiktionaryPage


class WiktionaryPage(IWiktionaryPage):
    """ Default implementation of the :@link IWiktionaryPage interface.
        See there for details. """

    def __init__(self):
        """ Initialize the page and all of its entries. """
        self.entries = list()
        self.categories = list()
        self.interWikiLinks = set()

        self.id = None
        self.title = None
        self.normalizedTitle = None
        self.revision = None
        self._entryLanguage = None
        self.redirectTarget = None
        self.author = None
        self.timestamp = None
        self.entryLanguageStr = None

    def init(self):
        for entry in self.entries:
            entry.init(self)

    def createEntry(self):
        """ Factory method for creating a new entry. """
        result = WiktionaryEntry()
        result.init(self)
        result.setHeader(self.title)
        return result
    
    # -- Identifier --
    
    def getKey(self):
        return str(self.id)
    
    def getId(self):
        return self.id

    def setId(self, id):
        """ Assign the specified page ID. """
        self.id = id
    
    # -- Page --
    
    def getTitle(self):
        return self.title

    def setTitle(self, title):
        """ Assigns the given title to this page. """
        self.title = title
        self.normalizedTitle = self.normalizeTitle(title)

    def getTimestamp(self):
        return self.timestamp
    
    def setTimestamp(self, timestamp):
        """ Assigns the given timestamp to this page. """
        self.timestamp = timestamp
    
    def getRevision(self):
        return self.revision
    
    def setRevision(self, revision):
        """ Assigns the given revision ID to this page. """
        self.revision = revision
    
    def getAuthor(self):
        return self.author
    
    def setAuthor(self, author):
        """ Assigns the given author name to this page. """
        self.author = author

    def getEntryLanguage(self):
        if self._entryLanguage is None and self.entryLanguageStr is not None:
            self._entryLanguage = Language.get(self.entryLanguageStr)
        return self._entryLanguage
    
    def setEntryLanguage(self, entryLanguage):
        """ Assigns the given entry language to this page. """
        self._entryLanguage = entryLanguage
        if entryLanguage is not None:
            self.entryLanguageStr = entryLanguage.getCode()

    def addCategory(self, category):
        """ Add the given category to the list of categories. """
        self.categories.append(category)
    
    def getCategories(self):
        return self.categories
    
    def addInterWikiLink(self, language):
        """ Add the given interwiki link to the list of interwiki links. """
        self.interWikiLinks.add(language)

    def getInterWikiLinks(self):
        return self.interWikiLinks
    
    def getRedirectTarget(self):
        return self.redirectTarget

    def setRedirectTarget(self, redirectTarget):
        """ Assigns the given redirect target to this page. """
        self.redirectTarget = redirectTarget

    # -- Entries --
    
    def addEntry(self, entry):
        """ Add the given entry to the list of senses. """
        entry.index = len(self.entries)
        entry.setId(entry.getIndex())
        self.entries.append(entry)

    def getEntry(self, index):
        return self.entries[index]
    
    def getEntryCount(self):
        return len(self.entries)

    def getEntries(self):
        return self.entries

    def entries(self):
        """ Internal interface that is used by the parsers. """
        return self.entries

    def __str__(self):
        return self.__class__.__name__ + ":" + str(self.id) + ":" + self.title

    # -- Normalize --

    @staticmethod
    def normalizeTitle(title):
        """ Static helper method for normalizing the title. That is, the title
            is converted into lower case and non-ASCII characters are removed. """
        if title is None:
            return None

        return re.sub(r'[^\x00-\x7F]', "", unicodedata.normalize('NFC', title).lower())
