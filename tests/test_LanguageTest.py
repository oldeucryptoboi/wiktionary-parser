import unittest
from api.util import Language


class TestLanguage(unittest.TestCase):
    """ Test case for {@link Language}. """

    def testConstants(self):
        self.assertEqual("eng", Language.ENGLISH.getCode())
        self.assertEqual("English", Language.ENGLISH.getName())
        # self.assertEqual("deu", Language.GERMAN.getCode())
        # self.assertEqual("German", Language.GERMAN.getName())
        # self.assertEqual("rus", Language.RUSSIAN.getCode())
        # self.assertEqual("Russian", Language.RUSSIAN.getName())

    def testGet(self):
        self.assertEqual("eng", Language.get("eng").getCode())
        self.assertEqual("deu", Language.get("deu").getCode())
        self.assertIsNone(Language.get("en"))
        self.assertIsNone(Language.get("de"))
        self.assertIsNone(Language.get("ger"))

    def testFindByCode(self):
        self.assertEqual("eng", Language.findByCode("eng").getCode())
        self.assertEqual("deu", Language.findByCode("deu").getCode())
        self.assertEqual("eng", Language.findByCode("en").getCode())
        self.assertEqual("deu", Language.findByCode("de").getCode())
        self.assertEqual("deu", Language.findByCode("ger").getCode())

    def testFindByName(self):
        self.assertEqual("eng", Language.findByName("English").getCode())
        self.assertEqual("deu", Language.findByName("German").getCode())
        self.assertEqual("zza", Language.findByName("Dimili").getCode())
        self.assertEqual("zza", Language.findByName("Kirmanjki").getCode())
        self.assertEqual("zza", Language.findByName("Kirdki").getCode())
        self.assertEqual("zza", Language.findByName("Dimli").getCode())
        self.assertEqual("zza", Language.findByName("Zazaki").getCode())
        self.assertEqual("zza", Language.findByName("Zaza").getCode())

        self.assertEqual("eng", Language.findByName("english").getCode())
        self.assertEqual("eng", Language.findByName("ENGLISH").getCode())
        self.assertEqual("deu", Language.findByName("german").getCode())
        self.assertEqual("deu", Language.findByName("GERMAN").getCode())

        self.assertEqual("Xart-tok", Language.findByName("tokipona").getCode())
        self.assertEqual("nmn", Language.findByName("!xóõ").getCode())
        self.assertEqual("nmn", Language.findByName("!Xóõ").getCode())
        self.assertEqual("nmn", Language.findByName("!Xóõ").getCode())
        self.assertEqual("nmn", Language.findByName("!Xóõ").getCode())
        self.assertEqual("nmn", Language.findByName("!xóõ").getCode())
        self.assertEqual("nmn", Language.findByName("ǃXóõ").getCode())

    def testISOCodes(self):
        self.assertEqual("en", Language.findByName("English").getISO639_1())
        self.assertEqual("eng", Language.findByName("English").getISO639_2B())
        self.assertEqual("eng", Language.findByName("English").getISO639_2T())
        self.assertEqual("eng", Language.findByName("English").getISO639_3())

        self.assertEqual("de", Language.findByName("German").getISO639_1())
        self.assertEqual("ger", Language.findByName("German").getISO639_2B())
        self.assertEqual("deu", Language.findByName("German").getISO639_2T())
        self.assertEqual("deu", Language.findByName("German").getISO639_3())

        self.assertEqual("", Language.findByName("Dimili").getISO639_1())
        self.assertEqual("zza", Language.findByName("Dimili").getISO639_2B())
        self.assertEqual("zza", Language.findByName("Dimili").getISO639_2T())
        self.assertEqual("zza", Language.findByName("Dimili").getISO639_3())

        self.assertEqual("", Language.findByName("Aasáx").getISO639_1())
        self.assertEqual("", Language.findByName("Aasáx").getISO639_2B())
        self.assertEqual("", Language.findByName("Aasáx").getISO639_2T())
        self.assertEqual("aas", Language.findByName("Aasáx").getISO639_3())

        self.assertEqual("", Language.findByName("Tokipona").getISO639_1())
        self.assertEqual("", Language.findByName("Tokipona").getISO639_2B())
        self.assertEqual("", Language.findByName("Tokipona").getISO639_2T())
        self.assertEqual("", Language.findByName("Tokipona").getISO639_3())


if __name__ == '__main__':
    unittest.main()
