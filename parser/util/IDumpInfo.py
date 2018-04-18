class IDumpInfo:
    """ Data object for information on the :@link IWiktionaryDumpParser. This
        dump parser creates and maintains an instance of this type to share
        information on the dump file with all its registed
        :@link IWiktionaryPageParser. """

    def getDumpFile(self):
        """ Returns the current Wiktionary XML dump file, which is being parsed. """
        pass

    def getDumpLanguage(self):
        """ Returns the language of the Wiktionary edition this dump file
            belongs to. The language is automatically determined from the
            base URL of the Wiktionary edition. """
        pass

    def getNamespaces(self):
        """ Returns a set containing all namespaces registered in the siteinfo
            header of the XML dump file. """
        pass

    def hasNamespace(self, namespace):
        """ Returns <code>True</code> if the specified namespace has been
            defined within the siteinfo header of the XML dump file. """
        pass

    def getProcessedPages(self):
        """ Returns the number of pages in the dump file that have been
            processed. """
        pass

    def getParser(self):
        """ Returns the Wiktionary dump parser instance that maintains this
            dump info object. """
        pass

    def reset(self):
        """ Reset the dump information, such the number of processed pages. This
            is to be called before a new dump file is being processed. Users of
            this interface should normally not invoke this method. """
        pass
