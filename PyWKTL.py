from errors import IOException, RuntimeException
from compat import Properties, Object

from api.entry.WiktionaryCollection import WiktionaryCollection
from api.entry.DBWiktionaryEdition import DBWiktionaryEdition
from parser.WiktionaryDumpParser import WiktionaryDumpParser
from parser.WiktionaryArticleParser import WiktionaryArticleParser


class PyWKTL(Object):
    """
     * Main entry point of the JWKTL API. Use this class to initiate the parsing
     * of a Wiktionary XML dump file and for accessing already parsed dump files.
    """

    @classmethod
    def getVersion(cls):
        """ Returns the software version. """
        try:
            properties = Properties()
            stream = cls.getResourceAsStream("/META-INF/pywktl-version.properties")
            properties.load(stream)
            return properties.getProperty("pywktl.version")
        except IOException as e:
            raise RuntimeException(e)

    # -- Open parsed editions --

    @staticmethod
    def openCollection(parsedDumps, cacheSize=None):
        """ Opens the parsed Wiktionary language edition stored at the given
         #  locations and aggregated them in a :@link IWiktionaryCollection.
         #  This method uses the given cache size for connecting to the
         #  DataBase.
         #  @throws WiktionaryException in case of any JWKTL-related error. """
        result = WiktionaryCollection()
        for parsedDump in parsedDumps:
            result.addEdition(PyWKTL.openEdition(parsedDump, cacheSize))
        return result

    @staticmethod
    def openEdition(parsedDump, cacheSize=None):
        """ Opens the parsed Wiktionary language edition stored at the given
         #  location. This method uses the given cache size for connecting
         #  to the DataBase.
         #  @throws WiktionaryException in case of any JWKTL-related error. """
        return DBWiktionaryEdition(parsedDump, cacheSize)

    # -- Parse dump files --
    
    @staticmethod
    def parseWiktionaryDump(dumpFile, targetDirectory, overwriteExisting=False, parseWikiSaurus=False):
        """ Parses the given XML dump file of Wiktionary and stores the parsed data
         *  within the specified target directory. Note that each target
         *  directory can only contain one parsed Wiktionary database. This
         *  method is equivalent to :@link WiktionaryDumpParser#parse(File) using
         *  a registered :@link WiktionaryArticleParser. Optionally, information
         *  from Wikisaurus is added to the parsed database using the
         *  :@link WikisaurusArticleParser.
         *  @param dumpFile file name of the Wiktionary dump in XML format.
         *     @param targetDirectory directory for storing the parsed data.
         *     @param overwriteExisting if <code>True</code>, previously parsed
         *         Wiktionary data files are removed from the targetDirectory.
         * @param parseWikiSaurus parses Wikisaurus pages and adds the parsed
         *         information to the corresponding articles.
         *     @throws WiktionaryException in case of any parser errors. """
        from parser import WritableDBWiktionaryEdition
        wiktionaryDB = WritableDBWiktionaryEdition(targetDirectory, overwriteExisting)
        parser = WiktionaryDumpParser()
        parser.register(WiktionaryArticleParser(wiktionaryDB))
        if parseWikiSaurus:
            # parser.register(WikisaurusArticleParser(wiktionaryDB))
            pass
        parser.parseFile(dumpFile)

    @staticmethod
    def deleteEdition(parsedData):
        """ Deletes all files from a previously parsed Wiktionary from the
         *  specified directory. This method is equivalent to
         *  :@link DBWiktionaryEdition#deleteParsedWiktionary(File). """
        DBWiktionaryEdition.deleteParsedWiktionary(parsedData)
