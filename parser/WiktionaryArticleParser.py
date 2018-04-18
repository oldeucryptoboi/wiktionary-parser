from errors import WiktionaryException, DatabaseException
from compat import Logger
from api.util import Language
from api.entry import WiktionaryPage
from parser.en import ENWiktionaryEntryParser

from parser import *


class WiktionaryArticleParser(WiktionaryPageParser):
    """ Parses a Wiktionary XML dump and stores the parsed information as a
        DataBase within a specified directory. The parsed Wiktionary dump
        can then be accessed using the main JWKTL API. This implementation
        parses only article pages within the main namespace discussions, user
        pages, revisions, etc. are not handled. An article page's text is
        passed to an implementation of :@link IWiktionaryEntryParser, which
        is either automatically detected from the Wiktionary's base URL, or
        specified in the constructor. Note that each directory can only
        contain one Wiktionary database. """

    logger = Logger.getLogger("WiktionaryArticleParser")
    
    def __init__(self, wiktionaryDB, entryParser=None):  # throws WiktionaryException :
        """ Creates a caching article parser that saves the parsed Wiktionary
            data into a DataBase within the given target directory. A
            previously parsed Wiktionary database is replaced if overwriteExisting
            is True. The specified entry parser is used rather than auto detecting
            the language specific parser.
            @throws WiktionaryException if the target dictionary is not empty
                and overwriteExisting was set to False. """
        super().__init__()
        self.wiktionaryDB = wiktionaryDB
        self.entryParser = entryParser
    
    def onSiteInfoComplete(self, dumpInfo):
        super().onSiteInfoComplete(dumpInfo)
        language = dumpInfo.getDumpLanguage()
        if self.wiktionaryDB is not None:
            self.wiktionaryDB.setLanguage(language)
        
        if self.entryParser is not None:
            return
        if Language.ENGLISH.equals(language):
            self.entryParser = ENWiktionaryEntryParser()
        else:
            raise WiktionaryException("Language " + language + " is not supported")

        WiktionaryArticleParser.logger.info("Automatically determined dump format: " + language)
    
    def onPageEnd(self):
        self.saveParsedWiktionaryPage()
        super().onPageEnd()

    def onClose(self, dumpInfo):
        super().onClose(dumpInfo)
        if self.wiktionaryDB is None:
            return
        
        self.wiktionaryDB.saveProperties(dumpInfo)
        
        # It is important to close the DataBase handler to avoid data loss.
        try:
            self.wiktionaryDB.close()
        except DatabaseException as e:
            raise WiktionaryException("Unable to close Wiktionary DB", e)
        
    def createPage(self):
        return WiktionaryPage()
    
    def setText(self, text):
        if self.isAllowed(self.page):
            self.entryParser.parse(self.page, text)

    def saveParsedWiktionaryPage(self):
        if not self.isAllowed(self.page):
            WiktionaryArticleParser.logger.finer("Ignoring page " + self.page.getTitle())
            return

        if self.wiktionaryDB is None:
            return
        
        try:
            self.wiktionaryDB.savePage(self.page)

            if self.dumpInfo.getProcessedPages() % 25000 == 0:
                self.wiktionaryDB.commit()
        except DatabaseException as e:
            raise WiktionaryException("Unable to save page " + self.page.getTitle(), e)

    # noinspection PyUnusedLocal
    def isAllowed(self, page):
        return self.currentNamespace is None
