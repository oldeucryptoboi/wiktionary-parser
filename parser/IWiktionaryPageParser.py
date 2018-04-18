# noinspection PyIncorrectDocstring
class IWiktionaryPageParser:
    """ Generic interface for parsing XML dumps in a MediaWiki format. """

    def onParserStart(self, dumpInfo):
        """ Hotspot that is invoked upon starting the parser. """
        pass

    def onSiteInfoComplete(self, dumpInfo):
        """ Hotspot that is invoked after the siteinfo header has been read. At
            this point in time, the dump info contains all information,
            including dump language and namespaces. """
        pass

    def onParserEnd(self, dumpInfo):
        """ Hotspot that is invoked when the parser is about to end. Use this
            method for writing any owing information to a file or database. For
            closing and cleaning up resources, you should, however, use the
            :@link #onClose(IDumpInfo) hotspot. """
        pass

    def onClose(self, dumpInfo):
        """ Hotspot that is invoked after the parser has finished its work. This
            method is supposed to close and cleanup any resources (e.g., closing
            a database connection). It is called after all
            :@link #onParserEnd(IDumpInfo) calls have been handled. """
        pass

    def onPageStart(self):
        """ Hotspot that is invoked upon starting a new article page. """
        pass

    def onPageEnd(self):
        """ Hotspot that is invoked upon finishing the current article page. """
        pass

    def setAuthor(self, author):
        """ Hotspot that is invoked after the current page's author is read. """
        pass

    def setRevision(self, revisionId):
        """ Hotspot that is invoked after the current page's revision id is read. """
        pass

    def setTimestamp(self, timestamp):
        """ Hotspot that is invoked after the current page's timestamp is read. """
        pass

    def setPageId(self, pageId):
        """ Hotspot that is invoked after the current page's id is read. """
        pass

    def setTitle(self, title, namespace):
        """ Hotspot that is invoked after the current page's title is read.
            @param title
            @param namespace """
        pass

    def setText(self, text):
        """ Hotspot that is invoked after the current page's text is read. """
        pass
