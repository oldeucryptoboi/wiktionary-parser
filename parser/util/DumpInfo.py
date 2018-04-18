from .IDumpInfo import IDumpInfo


class DumpInfo(IDumpInfo):
    """ Default implementation of the :@link IDumpInfo interface. """

    def __init__(self, dumpFile, parser):
        """ Instanciate the dump info object for the given dump file and parser
         *  object. """
        self.dumpFile = dumpFile
        self.parser = parser
        self.reset()

        self.dumpLanguage = None
        self.namespaces = None
        self.processedPages = None

    def reset(self):
        self.namespaces = set()
        self.processedPages = 0

    def getDumpFile(self):
        return self.dumpFile

    def getDumpLanguage(self):
        return self.dumpLanguage

    def setDumpLanguage(self, dumpLanguage):
        """ Assign the specified dump language. """
        self.dumpLanguage = dumpLanguage

    def getNamespaces(self):
        return self.namespaces

    def hasNamespace(self, namespace):
        return namespace in self.namespaces

    def addNamespace(self, namespace):
        """ Add the given namespace to the list of namespaces defined for
         *  this dump file. """
        self.namespaces.add(namespace)

    def getProcessedPages(self):
        return self.processedPages

    def incrementProcessedPages(self):
        """ Increment the number of processed pages by one. """
        self.processedPages += 1

    def getParser(self):
        return self.parser
