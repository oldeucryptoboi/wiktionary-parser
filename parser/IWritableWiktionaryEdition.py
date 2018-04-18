from api import IWiktionaryEdition


class IWritableWiktionaryEdition(IWiktionaryEdition):
    """ Generic interface for writable Wiktionary language editions used by the
        parsers to store the extracted entries and information types.
        Implementations of this class may provide a database or file system
        connection to persistently store the extracted information. """

    def getPageForId(self, id_):
        pass
    
    def getPageForWord(self, word):
        pass

    def saveProperties(self, dumpInfo):   # throws WiktionaryException
        """ Hotspot called after parsing has finished to save the metadata
            of the dump file and the basic parsing statistics. """
        pass

    def savePage(self, page):
        """ Adds the given page to the Wiktionary edition (e.g., storing it
            in a database). """
        pass

    def commit(self):
        """ Force a database commit of the pages saved so far. """
        pass

    def setLanguage(self, language):
        """ Assigns the given language to the Wiktionary edition. """
        pass

    # def setEntryIndexByTitle(self, entryIndexByTitle):
    #     """ Sorts the entries by word form before assigning an ID to them.
    #         THIS METHOD IS KEPT FOR COMPATIBILITY. YOU SHOULD NOT USE THIS
    #      *  METHOD. """
    #     pass
