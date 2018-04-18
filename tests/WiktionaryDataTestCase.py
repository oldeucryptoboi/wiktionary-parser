from compat import File

from api.util import Language
from parser import WiktionaryArticleParser, WiktionaryDumpParser, WritableDBWiktionaryEdition

from PyWKTL import PyWKTL
from tests import *


class WiktionaryDataTestCase(WiktionaryTestCase):
    """  Abstract test case for:@link IWiktionaryEdition} and
        :@link IWiktionaryCollection}. """

    class DumpEntry:

        def __init__(self, id_, word, language, page):
            self.id_ = id_
            self.word = word
            self.language = language
            self.page = page

        def getId(self):
            return self.id_

        def getWord(self):
            return self.word

        def getLanguage(self):
            return self.language

        def getPage(self):
            return self.page

    class WiktionaryTestData:

        def __init__(self, dumpFile, language, langCode, entries):
            self.dumpFile = dumpFile
            self.language = language
            self.langCode = langCode
            self.entries = entries

            self.parsedData = None

        def getDumpFile(self):
            return self.dumpFile

        def getLanguage(self):
            return self.language

        def getEntries(self):
            return self.entries

        def parseFile(self, targetDirectory):
            self.parsedData = targetDirectory
            db = WritableDBWiktionaryEdition(targetDirectory, True)
            db.setEntryIndexByTitle(True)
            parser = WiktionaryDumpParser(WiktionaryArticleParser(db))
            parser.parseFile(self.dumpFile)

        def getParsedData(self):
            return self.parsedData

    EN_PARAMETER = DumpEntry(0, "parameter", Language.ENGLISH, 11095)
    EN_PLACE1 = DumpEntry(1, "place", Language.ENGLISH, 11094)
    EN_PLACE2 = DumpEntry(2, "place", Language.ENGLISH, 11094)
    EN_PLACE3 = DumpEntry(3, "place", Language.ENGLISH, 11094)
    EN_PLACE4 = DumpEntry(4, "place", Language.ENGLISH, 11094)
    EN_PLACE5 = DumpEntry(5, "place", Language.ENGLISH, 11094)
    EN_PLACE6 = DumpEntry(6, "place", Language.ENGLISH, 11094)
    EN_PLACE7 = DumpEntry(7, "place", Language.ENGLISH, 11094)

    def getSimpleENDump(self):
        entries = list()
        entries.append(self.EN_PARAMETER)
        entries.append(self.EN_PLACE1)
        entries.append(self.EN_PLACE2)
        entries.append(self.EN_PLACE3)
        entries.append(self.EN_PLACE4)
        entries.append(self.EN_PLACE5)
        entries.append(self.EN_PLACE6)
        entries.append(self.EN_PLACE7)
        return WiktionaryDataTestCase(File(WiktionaryTestCase.RESOURCE_PATH, "WiktionaryTestData_en_20080613.xml"), Language.ENGLISH, "en", entries)

    wktEN = None

    def setUp(self):  # throws Exception:
        super().setUp()
        self.wktEN = self.getSimpleENDump()
        self.wktEN.parseFile(File(self.workDir, "/en"))

    def tearDown(self):  # throws Exception:
        PyWKTL.deleteEdition(self.wktEN.getParsedData())
        super().tearDown()

    def assertIterable(self, actual, *expected):
        iterator = actual.iterator()
        for e in expected:
            self.assertTrue(iterator.hasNext())
            self.assertEqual(e, iterator.next())

        self.assertFalse(iterator.hasNext())
