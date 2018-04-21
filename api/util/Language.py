from .ILanguage import ILanguage
from collections import OrderedDict as TreeMap
from errors import IOException, RuntimeException
import os


class Language(ILanguage):
    """ Implementation of the :@link ILanguage interface. This class should
        not be instantiated by yourself. Use the static methods to find registered
        instances - either by language code or name. """

    # noinspection PyMissingConstructor
    def __init__(self, code, name, iso639_3, iso639_2b, iso639_2t, iso639_1):
        self.code = code
        self.name = name
        self.iso639_3 = iso639_3
        self.iso639_2b = iso639_2b
        self.iso639_2t = iso639_2t
        self.iso639_1 = iso639_1

    def getCode(self):
        return self.code

    def getName(self):
        return self.name

    def getISO639_3(self):
        return self.iso639_3

    def getISO639_2B(self):
        return self.iso639_2b

    def getISO639_2T(self):
        return self.iso639_2t

    def getISO639_1(self):
        return self.iso639_1

    def compareTo(self, other):
        return 0 if self == other else self.code.compareTo(other.getCode())

    def __eq__(self, other):
        if other is None or not isinstance(other, ILanguage):
            return False
        else:
            return self.code == other.getCode()

    def __str__(self):
        return self.name

    # -- Static interface --

    """ The English language. """
    ENGLISH = None
    """ The German language. """
    GERMAN = None
    """ The Russian language. """
    RUSSIAN = None

    initialized = False
    languageIndex = None
    additionalCodeIndex = None
    additionalNameIndex = None

    # Avoid two threads interleaving!
    @classmethod
    def initialize(cls):
        if cls.initialized:
            return

        cls.languageIndex = TreeMap()
        cls.additionalCodeIndex = TreeMap()
        cls.additionalNameIndex = TreeMap()

        try:
            with open(os.path.join(os.path.dirname(__file__), "language_codes.txt"), "r", encoding="utf-8") as reader:
                for line in reader.readlines():
                    line = line.rstrip('\n')

                    # Extract the fields.
                    fields = ['']*8
                    idx = 0
                    while True:
                        i = line.find("\t")
                        if i >= 0:
                            fields[idx] = line[: i]
                            idx += 1
                            line = line[i + 1:]
                        else:
                            break

                    if idx < 0:
                        continue

                    fields[idx] = line

                    # Save the main language entry.
                    language = Language(*fields[:6])
                    cls.languageIndex[language.getCode()] = language
                    cls.additionalCodeIndex[language.getCode()] = language.getCode()
                    cls.additionalNameIndex[language.getName().lower()] = language.getCode()

                    # Save additional language codes.
                    additionalCodes = fields[6]

                    if additionalCodes:
                        while True:
                            i = additionalCodes.find(';')
                            if i >= 0:
                                addCode = additionalCodes[:i]
                                cls.additionalCodeIndex[addCode] = language.getCode()
                                additionalCodes = additionalCodes[i + 1:]
                            else:
                                break

                        cls.additionalCodeIndex[additionalCodes] = language.getCode()

                    # Save additional language names.
                    additionalNames = fields[7]
                    if additionalNames:
                        while True:
                            i = additionalNames.find(';')
                            if i >= 0:
                                addName = additionalNames[:i]
                                cls.additionalNameIndex[addName.lower()] = language.getCode()
                                additionalNames = additionalNames[i + 1:]
                            else:
                                break

                        cls.additionalNameIndex[additionalNames.lower()] = language.getCode()

            Language.initialized = True

        except IOException as e:
            raise RuntimeException("Unable to load language code index", e)

    @classmethod
    def get(cls, code):
        return cls.getLanguage(code)

    @classmethod
    def getLanguage(cls, code):
        """ Returns the language with the given internal code. Note that the
            internal codes roughly correspond to ISO 639-3 code, but also model
            some extensions to self. Use :@link #findByCode(String) if you are
            unsure about your code. If no language could be found,
            <code>None</code> is returned. """
        cls.initialize()
        return None if code is None else cls.languageIndex.get(code, None)

    @classmethod
    def findByCode(cls, code):
        """ Find the language with the given code. The method checks both for the
            internal language codes and for any ISO 639 code. If no language
            could be found, <code>None</code> is returned. """
        cls.initialize()
        return cls.get(cls.additionalCodeIndex.get(code, None))

    @classmethod
    def findByName(cls, name):
        """ Find the language with the given name. The method checks both for the
            canonical English name as well as alternative names in other languages
            or spelling errors found in Wiktionary. If no language could be found,
            <code>None</code> is returned. """
        if name is None:
            return None
        cls.initialize()
        return cls.get(cls.additionalNameIndex.get(name.strip().lower(), None))


""" The English language. """
Language.ENGLISH = Language.get("eng")
""" The German language. """
# GERMAN = Language.get("deu")
""" The Russian language. """
# RUSSIAN = Language.get("rus")
