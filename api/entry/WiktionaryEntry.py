from .WiktionarySense import WiktionarySense
from api import IWiktionaryEntry
from api.util import Language


class WiktionaryEntry(IWiktionaryEntry):
    """ Default implementation of the :@link IWiktionaryEntry interface.
        See there for details. """

    def __init__(self):
        self.partsOfSpeech = list()
        self.senses = list()
        self.senses.append(WiktionarySense())  # Dummy sense for all unassigned information.

        self.id = None
        self._page = None
        self.pageId = 0
        self.usageNotes = None
        self.header = None
        self._rawHeadwordLine = None
        self._wordLanguage = None
        self.wordLanguageStr = None
        self.genders = None
        self.wordForms = None
        self.entryLink = None
        self.entryLinkType = None
        self.pronunciations = None
        self.etymology = None
        self.index = 0

    def init(self, page):
        """ Initialize the entry using the given Wiktionary page. This is necessary
            to initialize the back references to the parent page, which are not
            explicitly stored in the database. """

        self._page = page
        self.pageId = page.getId()
        for sense in self.senses:
            sense.init(self)

    def createSense(self):
        """ Factory method for creating a new word sense. """
        result = WiktionarySense()
        result.init(self)
        return result

    # -- Identifier --

    def getKey(self):
        return str(self.pageId) + ":" + str(self.getIndex())

    def getId(self):
        return self.id

    def setId(self, id_):
        """ Assign the specified entry ID. """
        self.id = id_

    def getIndex(self):
        return self.index

    # -- Parent --

    def getPage(self):
        return self._page

    def getPageId(self):
        return self.pageId

    # -- Entry --

    def getWord(self):
        return self.getPage().getTitle()

    def getHeader(self):
        return self.header

    def setHeader(self, header):
        """ Assigns the given header text (i.e., the first headline of the entry,
            which normally corresponds to a word's lemma). """
        self.header = header

    def getRawHeadwordLine(self):
        return self._rawHeadwordLine

    def setRawHeadwordLine(self, rawHeadwordLine):
        self._rawHeadwordLine = rawHeadwordLine

    def getWordLanguage(self):
        if self._wordLanguage is None and self.wordLanguageStr is not None:
            self._wordLanguage = Language.get(self.wordLanguageStr)
        return self._wordLanguage

    def setWordLanguage(self, wordLanguage):
        """ Assigns the given word language. """
        self._wordLanguage = wordLanguage
        if wordLanguage is not None:
            self.wordLanguageStr = wordLanguage.getCode()

    def getPartOfSpeech(self):
        return self.partsOfSpeech[0] if self.partsOfSpeech else None

    def getPartsOfSpeech(self):
        return self.partsOfSpeech

    def addPartOfSpeech(self, partOfSpeech):
        """ Adds the given part of speech to the list of part of speech tags. """
        self.partsOfSpeech.append(partOfSpeech)

    def getGender(self):
        if not self.genders:
            return None
        return self.genders[0]

    def getGenders(self):
        return self.genders

    def addGender(self, gender):
        """ Adds the given grammatical gender to the list of genders. """
        if self.genders is None:
            self.genders = list()
        self.genders.append(gender)

    def getWordEtymology(self):
        return self.etymology

    def setWordEtymology(self, etymology):
        """ Assigns the given etymology text. """
        self.etymology = etymology

    def getEntryLink(self):
        return self.entryLink

    def getEntryLinkType(self):
        return self.entryLinkType

    def setEntryLink(self, entryLink, entryLinkType):
        """ Assigns the given entry link. """
        self.entryLink = entryLink
        self.entryLinkType = entryLinkType

    def addPronunciation(self, pronunciation):
        """ Adds the given pronunciation. """
        if self.pronunciations is None:
            self.pronunciations = list()
        self.pronunciations.append(pronunciation)

    def getPronunciations(self):
        return self.pronunciations

    def addWordForm(self, wordForm):
        """ Adds the given word form. """
        if self.wordForms is None:
            self.wordForms = list()
        self.wordForms.append(wordForm)

    def getWordForms(self):
        return self.wordForms

    # -- Senses --

    def addSense(self, sense):
        """ Add the given sense to the list of senses. """
        sense.setIndex(len(self.senses))
        self.senses.append(sense)

    def getUnassignedSense(self):
        return self.senses[0]

    def setUnassignedSense(self, unassignedSense):
        self.senses[0] = unassignedSense

    def getSense(self, index):
        return self.senses[index]
    
    def getSenseCount(self):
        return len(self.senses) - 1  # don't count the unassigned sense.

    def getSenses(self, includeUnassignedSense=False):
        # This cast is used to transform the internal representation using
        # the WiktionarySense type to the interface type IWiktionarySense.
        # Although this might not be the cleanest way to do that, exposing
        # the interface type prevents the user from changing the data without
        # raising a performance bottleneck of returning a newly created list
        # of the senses. It is the user's responsibility to not make any
        # changes to this exposed internal representation.
        if includeUnassignedSense:
            return self.senses
        else:
            return self.senses[1:]

    def senses(self):
        """ Internal interface that is used by the parsers. """
        return self.senses
    
    def findSenseByMarker(self, marker):
        """ Identify the first sense of this entry with the given marker. """
        for sense in self.senses:
            if marker == sense.getMarker():
                return sense

        return None

    # -- Combination --

    def getGlosses(self):
        result = list()
        for sense in self.getSenses(True):
            gloss = sense.getGloss()
            if gloss is not None and len(gloss.getText()) > 0:
                result.extend(gloss)

        return result

    def getExamples(self):
        result = list()
        for sense in self.getSenses(True):
            examples = sense.getExamples()
            if examples is not None:
                result.extend(examples)

        return result

    def getQuotations(self):
        result = list()
        for sense in self.getSenses(True):
            quotations = sense.getQuotations()
            if quotations is not None:
                result.extend(quotations)

        return result

    def getRelations(self, relationType=None):
        result = list()
        for sense in self.getSenses(True):
            relations = sense.getRelations(relationType)
            if relations is not None:
                result.extend(relations)

        return result

    def getReferences(self):
        result = list()
        for sense in self.getSenses(True):
            references = sense.getReferences()
            if references is not None:
                result.extend(references)

        return result

    def getTranslations(self, language=None):
        result = list()
        for sense in self.getSenses(True):
            translations = sense.getTranslations(language)
            if translations is not None:
                result.extend(translations)

        return result

    def getUsageNotes(self):
        return self.usageNotes

    def setUsageNotes(self, usageNotes):
        self.usageNotes = usageNotes

    def __str__(self):
        return self.__class__.__name__ + ":" + str(self.index) + ":" + self.wordLanguageStr + ":" + str(self.getPartOfSpeech())
