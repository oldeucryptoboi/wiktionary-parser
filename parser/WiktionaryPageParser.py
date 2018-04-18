from parser import *

from api.entry import WiktionaryPage


class WiktionaryPageParser(WiktionaryPage, IWiktionaryPageParser):
    """ Abstract base class for implementations of the
        :@link IWiktionaryPageParser interface. The class manages the dump info
        and the current namespace, as well as the creation of a
        :@link WiktionaryPage.
        @param <PageType> The type of page to create, usually
        :@link WiktionaryPage. """

    def __init__(self):
        self.page = None
        self.dumpInfo = None
        self.currentNamespace = None

    def onParserStart(self, dumpInfo):
        self.dumpInfo = dumpInfo

    def onSiteInfoComplete(self, dumpInfo):
        pass

    def onParserEnd(self, dumpInfo):
        pass

    def onClose(self, dumpInfo):
        pass

    def onPageStart(self):
        self.page = self.createPage()
        self.page.setEntryLanguage(self.dumpInfo.getDumpLanguage())

    def onPageEnd(self):
        pass

    def createPage(self):
        return None

    def setPageId(self, pageId):
        self.page.setId(pageId)

    def setTitle(self, title, namespace):
        self.currentNamespace = namespace
        self.page.setTitle(title)

    def setAuthor(self, author):
        self.page.setAuthor(author)

    def setRevision(self, revisionId):
        self.page.setRevision(revisionId)

    def setTimestamp(self, timestamp):
        self.page.setTimestamp(timestamp)

    def setText(self, text):
        pass
