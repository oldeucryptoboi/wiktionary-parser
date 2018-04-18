class IWiktionaryDumpParser:
    """ Parser for Wiktionary dump files obtained from
        http://download.wikimedia.org/backup-index.html. """

    def parseFile(self, dumpFile):  # throws WiktionaryException
        """ Starts the parsing of the given dump file. The file can be either
            bzip2-compressed or the extracted XML version.

            @param dumpFile the dumpFile
            @throws WiktionaryException in case of any parser errors. """
        pass

    def register(self, pageParser):
        """ Register the given :@link IWiktionaryPageParser. The registered
            parser will then be notified once a Wiktionary-related XML tag
            has been processed. """
        pass

    def getPageParsers(self):
        """ Returns the list of all registered :@link IWiktionaryPageParsers. """
        pass
