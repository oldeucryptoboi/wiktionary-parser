from api import IWiktionarySense


class WiktionarySense(IWiktionarySense):
    """ Default implementation of the :@link IWiktionarySense interface.
        See there for details. """

    def __init__(self):
        self.entry = None
        self.entryId = None
        self.index = 0
        self.marker = None
        self.gloss = None
        self.examples = None
        self.quotations = None
        self.relations = None
        self.references = None
        self.translations = None

    def init(self, entry):
        """ Initialize the sense using the given Wiktionary entry. This is necessary
            to initialize the back references to the parent entry, which are not
            explicitly stored in the database. """
        self.entry = entry
        self.entryId = entry.getId()

    # -- Identifier --

    def getKey(self):
        return self.getEntry().getKey() + ":" + self.getId()

    def getId(self):
        return str(self.index)

    def getEntryId(self):
        """ Shorthand for <code>getEntry().getId()</code>. """
        return self.entryId

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        """ Assigns the given index to this sense. """
        self.index = index

    def getMarker(self):
        return self.marker

    def setMarker(self, marker):
        """ Assigns the given sense marker to this sense. """
        self.marker = marker

    # -- Parent --

    def getEntry(self):
        return self.entry

    def getPage(self):
        return self.entry.getPage()

    # -- Sense --

    def getGloss(self):
        return self.gloss

    def setGloss(self, gloss):
        """ Add the given sense definition to this sense. """
        self.gloss = gloss

    def addExample(self, example):
        """ Add the given example to this sense. """
        if self.examples is None:
            self.examples = list()
        self.examples.append(example)

    def getExamples(self):
        return self.examples

    def addQuotation(self, quotation):
        """ Add the given quotation to this sense. """
        if self.quotations is None:
            self.quotations = list()
        self.quotations.append(quotation)

    def getQuotations(self):
        return self.quotations

    def addReference(self, reference):
        """ Add the given reference to this sense. """
        if self.references is None:
            self.references = list()
        self.references.append(reference)

    def getReferences(self):
        return self.references

    def addRelation(self, relation):
        """ Add the given relation to this sense. """
        if self.relations is None:
            self.relations = list()
        self.relations.append(relation)

    def getAllRelations(self):
        return self.relations

    def getRelations(self, relationType=None):
        if relationType is None:
            return self.relations

        if self.relations is not None:
            return list(filter(lambda relation: relation.getRelationType() == relationType, self.relations))
        else:
            return list()

    def addTranslation(self, translation):
        """ Add the given translation to this sense. """
        if self.translations is None:
            self.translations = list()
        self.translations.append(translation)

    def getTranslations(self, language=None):
        if self.translations is not None:
            return list(filter(
                lambda translation: language is None or language == translation.getLanguage() or language.equals(
                    translation.getLanguage()), self.translations))
        else:
            return list()

    # -- Subsenses --

    # noinspection PyMethodMayBeStatic
    def getSenses(self):
        return None

    def __str__(self):
        return __class__.__name__ + ":" + str(self.index) + ":" + self.gloss
