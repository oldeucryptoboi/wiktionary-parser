from datetime import datetime

from parser import *

from api.entry import DBWiktionaryEdition
from compat import *
from errors import *

import PyWKTL


class WritableDBWiktionaryEdition(DBWiktionaryEdition, IWritableWiktionaryEdition):
    """ Extends the DataBase implementation by providing the possibility for
        modifying the contents. This is required by the parsers which need writing
        access to the database, but not by the querying and iterating interface. """

    def __init__(self, dbPath, overwriteExisting, cacheSize=None):
        """ Instantiates the writable Wiktionary database for the given
            database path.
            @param overwriteExisting if set to <code>False</code>, parsing a
                Wiktionary dump using this database will cause an exception if the
                database path is not empty. Otherwise, an existing parsed Wiktionary
                database will be overwritten.
            @param cacheSize denotes the size of the cache (in Bytes) used by the
                DataBase. """
        if cacheSize is None:
            import os
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
            mem_gib = mem_bytes / (1024. ** 3)  # e.g. 3.74
            cacheSize = int(mem_gib / 2)

        super().__init__(dbPath, isReadOnly=False, allowCreateNew=True, overwriteExisting=overwriteExisting, cacheSize=cacheSize)

        self.pageCount = 0
        self.entryCount = 0
        self.senseCount = 0

        self.entryById = None
        self.entryIndexByTitle = None
        self.language = None

    def connect(self, isReadOnly, allowCreateNew, overwriteExisting, cacheSize):  # throws DatabaseException
        if allowCreateNew:
            self.prepareTargetDirectory(self.dbPath, overwriteExisting)
        super().connect(isReadOnly, allowCreateNew, overwriteExisting, cacheSize)

    def getEntryIndexByTitle(self):
        """ Returns the setting if :@link IWiktionaryEntrys should be ordered
            alphabetically. """
        return self.entryIndexByTitle

    def setEntryIndexByTitle(self, entryIndexByTitle):
        self.entryIndexByTitle = entryIndexByTitle

    def setLanguage(self, language):
        self.language = language

    def commit(self):  # throws WiktionaryException
        isReadOnly = self.env.getConfig().getReadOnly()
        cacheSize = self.env.getConfig().getCacheSize()
        self.env.sync()
        self.doClose()
        self.connect(isReadOnly, False, False, cacheSize)

    def saveProperties(self, dumpInfo):  # throws WiktionaryException
        # Assign numeric ids to the WiktionaryEntries in alphabetical
        # order. This used to be the case in old versions and thus
        # is done for compatibility reasons.
        if self.entryIndexByTitle:
            pageId = 0
            entryId = 0
            self.entryById = None
            pageCursor = self.pageByTitle.entities()
            while pageCursor.next() is not None:
                page = pageCursor.current()
                if page.getEntryCount() > 0:
                    for entry in page.entries:
                        entry.setId(entryId)
                        entryId += 1
                    pageCursor.update(page)
                    self.pageById.put(page)  # Save
                    self.pageById.putNoReturn(page)

                pageId += 1
                if pageId % 100000 == 0:
                    lastKey = page.getTitle()
                    pageCursor.close()
                    self.commit()
                    pageCursor = self.pageByTitle.entities(lastKey, False, None, False)
                    print("Indexed " + pageId + " pages")

            pageCursor.close()
            self.entryById = self.store.getSecondaryIndex(self.entryByKey, Long.__class__, "entryId")

        try:
            # Saves a property file along with the database storage files that
            # contains information about language and size of the parsed data.
            props = {"wiktionary.language": self.language.getCode(),
                     "wiktionary.dumpfile": str(dumpInfo.getDumpFile()),
                     "database.creation": datetime.now().strftime("%Y-%m-%d %H:%M"),
                     "database.path": str(self.dbPath),
                     "database.pages": str(self.pageCount),
                     "database.entries": str(self.entryCount),
                     "database.sense": str(self.senseCount),
                     "pywktl.version": PyWKTL.getVersion()}

            i = 1
            for pageParser in dumpInfo.getParser().getPageParsers():
                props["pywktl.parser_" + str(i)] = pageParser.__class__.__name__
                i += 1

            writer = PrintWriter(File(self.dbPath, DBWiktionaryEdition.PROPERTY_FILE_NAME), "UTF-8")
            writer.println("# PyWKTL " + PyWKTL.getVersion() + " parsed dump file.")
            lastKey = None
            try:
                for key, value in props.items():
                    keyGroup = key
                    idx = keyGroup.find('.')
                    if idx >= 0:
                        keyGroup = keyGroup[:idx]
                    if not keyGroup == lastKey:
                        writer.println()
                        lastKey = keyGroup

                    writer.println(key + "=" + value)
                    self.properties[key] = value

            finally:
                writer.close()

        except IOException as e:
            raise WiktionaryException("Unable to save property file", e)

    def savePage(self, page):  # throws DatabaseException
        """ Adds the given Wiktionary page to the database.
            @throws DatabaseException if the page could not be stored, which is,
                i.e. the case if the DB is in read-only mode. """
        existing = self.pageById.put(page)
        if existing is None:
            for entry in page.entries:
                self.entryByKey.put(DBWiktionaryEdition.WiktionaryEntryProxy(entry))
                for sense in entry.senses:
                    # Inserts an entity and returns null, or updates it if the primary key
                    # already exists and returns the existing entity.

                    self.senseByKey.put(DBWiktionaryEdition.WiktionarySenseProxy(sense))
                    self.senseCount += 1

                self.entryCount += 1

            self.pageCount += 1
