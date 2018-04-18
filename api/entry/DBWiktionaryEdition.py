from compat import *
from errors import *

from database import StoreConfig, EntityStore, CursorConfig

from api.util import Language
from api.entry import WiktionaryEdition, WiktionaryPage, DBWiktionaryIterator


class DBWiktionaryEdition(WiktionaryEdition):
    """ Implementation of the :@link IWiktionaryEdition interface, which makes
     use of a DataBase to store and retrieve the parsed Wiktionary
     information. """

    class WiktionaryEntryProxy:
        """ Proxy object for referencing to a :@link IWiktionaryEntry. The proxy
         objects serve as a secondary database index. """

        def __init__(self, entry):
            self.entryId = None
            self.entryKey = None
            self.pageId = None
            self.entryIndex = None
            self.init(entry)

        def init(self, entry):
            """ Instantiates an entry proxy to the given referenced entry. """
            self.entryId = entry.getId()
            self.entryKey = entry.getKey()
            self.pageId = entry.getPageId()
            self.entryIndex = entry.getIndex()

        def getEntryKey(self):
            """ Return the entry key of the referenced :@link IWiktionaryEntry. """
            return self.entryKey

        def getEntryId(self):
            """ Return the entry ID of the referenced :@link IWiktionaryEntry. """
            return self.entryId

        def getPageId(self):
            """ Return the page ID of the referenced :@link IWiktionaryEntry. """
            return self.pageId

        def getEntryIndex(self):
            """ Return the entry index of the referenced :@link IWiktionaryEntry. """
            return self.entryIndex

    class WiktionarySenseProxy:
        """ Proxy object for referencing to a :@link IWiktionarySense. The proxy
         objects serve as a secondary database index. """

        def __init__(self, sense):
            """ Instantiates an sense proxy to the given referenced sense. """
            self.senseKey = sense.getKey()
            self.pageId = sense.getPage().getId()
            self.entryIndex = sense.getEntry().getIndex()
            self.senseIndex = sense.getIndex()

        def getSenseKey(self):
            """ Return the sense key of the referenced :@link IWiktionarySense. """
            return self.senseKey

        def getPageId(self):
            """ Return the page ID of the referenced :@link IWiktionarySense. """
            return self.pageId

        def getEntryIndex(self):
            """ Return the entry index of the referenced :@link IWiktionarySense. """
            return self.entryIndex

        def getSenseIndex(self):
            """ Return the sense index of the referenced :@link IWiktionarySense. """
            return self.senseIndex

    logger = Logger.getLogger("DBWiktionaryEdition")

    """ The internal name of the parsed Wiktionary database. """
    DATABASE_NAME = "WIKTIONARY"

    """ The name of the property file containing info about the parsed DB. """
    PROPERTY_FILE_NAME = "wiktionary.properties"

    # noinspection PyMissingConstructor
    def __init__(self, parsedWiktionaryDump, isReadOnly=True, allowCreateNew=False, overwriteExisting=False, cacheSize=None):
        self.dbPath = None
        self.env = None
        self.store = None
        self.dbPath = None
        self.properties = None
        self.language = None

        self.pageById = None
        self.pageByTitle = None
        self.pageByNormalizedTitle = None
        self.entryByKey = None
        self.entryById = None
        self.senseByKey = None
        self.openCursors = None
        self.init(parsedWiktionaryDump, isReadOnly, allowCreateNew, overwriteExisting, cacheSize)

    def init(self, parsedWiktionaryDump, isReadOnly, allowCreateNew, overwriteExisting, cacheSize):
        self.dbPath = parsedWiktionaryDump

        try:
            self.connect(isReadOnly, allowCreateNew, overwriteExisting, cacheSize)
        except (DatabaseException, IllegalArgumentException) as e:
            raise WiktionaryException("Unable to establish a db connection", e)

    def connect(self, isReadOnly, allowCreateNew, overwriteExisting, cacheSize):  # throws DatabaseException
        # Configure DB environment.

        envConfig = EnvironmentConfig()
        envConfig.setAllowCreate(allowCreateNew)
        envConfig.setReadOnly(isReadOnly)
        envConfig.setTransactional(False)
        if cacheSize is not None:
            envConfig.setCacheSize(cacheSize)

        self.env = Environment(self.dbPath, envConfig)

        # Configure store.
        storeConfig = StoreConfig()
        storeConfig.setAllowCreate(allowCreateNew)
        storeConfig.setTransactional(False)
        storeConfig.setReadOnly(isReadOnly)
        self.store = EntityStore(self.env, DBWiktionaryEdition.DATABASE_NAME, storeConfig)

        # Load properties.
        self.properties = Properties()
        propFile = File(self.dbPath, DBWiktionaryEdition.PROPERTY_FILE_NAME)
        if propFile.exists():
            try:
                reader = FileReader(propFile)
                self.properties.load(reader)
            except IOException as e:
                raise DatabaseException("Unable to load property file", e)

            lang = self.properties.getProperty("wiktionary.language")
            if lang is None:
                lang = self.properties.getProperty("entry_language")
            self.language = Language.get(lang)

        # Load index.
        self.pageById = self.store.getPrimaryIndex(Long.__class__, WiktionaryPage.__class__)
        self.pageByTitle = self.store.getSecondaryIndex(self.pageById, String.__class__, "title")
        self.pageByNormalizedTitle = self.store.getSecondaryIndex(self.pageById, String.__class__, "normalizedTitle")

        self.entryByKey = self.store.getPrimaryIndex(String.__class__, DBWiktionaryEdition.WiktionaryEntryProxy.__class__)
        self.entryById = self.store.getSecondaryIndex(self.entryByKey, Long.__class__, "entryId")
        self.senseByKey = self.store.getPrimaryIndex(String.__class__, DBWiktionaryEdition.WiktionarySenseProxy.__class__)

        self.openCursors = set()

    def prepareTargetDirectory(self, targetDirectory, overwriteExisting):  # throws WiktionaryException :
        """ Creates the given target dictionary if necessary. Removes a previously
           parsed Wiktionary database from the target folder if there exists
           one and overwriteExisting is set to True.
           @throws WiktionaryException if the target dictionary is not empty
                 and overwriteExisting was set to False. """
        if not targetDirectory.exists():
            DBWiktionaryEdition.logger.info("Creating target directory " + targetDirectory.getAbsolutePath())
            if not targetDirectory.mkdirs():
                raise WiktionaryException("Unable to create target directory")
        else:
            if not overwriteExisting and len(targetDirectory.list()) > 0:
                raise WiktionaryException("Target directory is not empty")

            self.deleteParsedWiktionary(targetDirectory)

    @classmethod
    def deleteParsedWiktionary(cls, targetDirectory):
        """ Removes all files belonging to a previously parsed Wiktionary database
           from the given target directory. If not Wiktionary could be found
           there, nothing is changed. """
        DBWiktionaryEdition.logger.info("Removing parsed Wiktionary from " + targetDirectory)
        files = [file for file in targetDirectory.listFiles()]
        # for file in targetDirectory.listFiles:
        #     name = file.getName()
        #     if name.endswith(".jdb"):
        #         return True
        #
        #     if name == "je.lck":
        #         return True
        #     if name == "wiktionary.properties":
        #         return True
        #
        #     return False

        for file in files:
            if not file.delete():
                DBWiktionaryEdition.logger.warning("Unable to delete file: " + str(file))

    # -- Pages --

    def getPageForId(self, id_):
        self.ensureOpen()
        try:
            return self.loadPage(self.pageById.get(id_), None)
        except DatabaseException as e:
            raise WiktionaryException(e)

    def getPageForWord(self,  word):
        self.ensureOpen()
        if word is None:
            return None

        try:
            return self.loadPage(self.pageByTitle.get(word), None)
        except DatabaseException as e:
            raise WiktionaryException(e)

    def getPagesForWord(self, word, filter_, normalize):
        self.ensureOpen()
        if word is None:
            return None

        try:
            result = list()
            if normalize:
                t = WiktionaryPage.normalizeTitle(word)
                cursor = self.pageByNormalizedTitle.entities(None, t, True, t, True, CursorConfig.DEFAULT)
                while cursor.next() is not None:
                    page = self.loadPage(cursor.current(), filter_)
                    if page is not None:
                        result.append(page)
                cursor.close()
            else:
                page = self.loadPage(self.pageByTitle.get(word), filter_)
                if page is not None:
                    result.append(page)  # can be only one result!

            return result
        except DatabaseException as e:
            raise WiktionaryException(e)

    def getAllPages(self, filter_, sortByTitle, normalize):
        self.ensureOpen()
        try:
            if sortByTitle:
                cursor = self.pageByNormalizedTitle.entities() if normalize else self.pageByTitle.entities()
            else:
                cursor = self.pageById.entities()

            return type("_DBWiktionaryIterator", (DBWiktionaryIterator,), {"loadEntity": lambda _, entity: self.loadPage(entity, filter_)})(self, cursor)

        except DatabaseException as e:
            raise WiktionaryException(e)

    # noinspection PyMethodMayBeStatic
    def loadPage(self, page, filter_=None):
        if page is not None and (filter_ is None or filter_.accept(page)):
            page.init()
            return page
        else:
            return None

    # -- Entries --

    def getEntryForId(self, entryId):
        self.ensureOpen()
        entry = self.entryById.get(entryId)
        return self.getEntryForPageId(entry.getPageId(), entry.getEntryIndex())

    # -- Senses --

    def getSenseForKey(self, key):
        self.ensureOpen()
        sense = self.senseByKey.get(key)
        return self.getSenseForPageId(sense.getPageId(), sense.getEntryIndex(), sense.getSenseIndex())

    # -- Properties --

    """ Returns the internal name of the DataBase. """
    @classmethod
    def getDBName(cls):
        return cls.DATABASE_NAME

    def getDBPath(self):
        return self.dbPath

    def getLanguage(self):
        return self.language

    # -- Close --

    def doClose(self):
        """ Hotspot for closing the connection.
           @throws WiktionaryException if the connection could not be closed. """
        if self.store is None:
            return  # DB already closed.

        try:
            for cursor in self.openCursors:
                cursor.close()

            self.openCursors.clear()

            self.store.close()
            self.env.close()

            self.env = None
            self.store = None
        except DatabaseException as e:
            raise WiktionaryException("Unable to close database", e)
