class EnGlossEntry:
    """ Helper class for storing parsed sense definitions, examples, and quotations.
        Instances of this class only exist while parsing a dump file they will
        be converted into proper :@link IWiktionarySense as soon as the meaning
        constituent has been completely parsed. """

    def __init__(self, gloss):
        """ Initializes the entry with the specified definition. """
        self.definition = gloss

        # a list of examples
        self.exampleList = list()
        self.exampleTranslations = dict()
        # relations
        self.relations = dict()

        # a list of quotation
        self.quotationList = list()

    def getExampleList(self):
        """ Returns the list of example sentences. """
        return self.exampleList

    def getExampleTranslation(self, example):
        """ Returns the translation for the given example, or None. """
        return self.exampleTranslations.get(example)

    def addExample(self, example):
        """ Add the specified example sentence to the list. """
        self.exampleList.append(example)

    def appendExample(self, example, separator):
        """ Append the specified example sentence to the last example
         *  sentences. The two examples are combined with the separator and then
         *  trimmed. """
        if not self.exampleList:
            return
        example = self.exampleList[-1] + separator + example
        self.exampleList[-1] = example.strip()
        return

    def appendExampleTranslation(self, translation):
        if self.exampleList:
            self.exampleTranslations[self.exampleList[-1]] = translation

    def addRelation(self, type, term):
        terms = self.relations.get(type, list())
        terms.append(term)
        self.relations[type] = terms

    def addQuotation(self, quotation):
        """ Add specified quotation to the list. """
        self.quotationList.append(quotation)

    def getQuotations(self):
        """ Returns the list of quotations. """
        return self.quotationList

    def getDefinition(self):
        """ Returns the sense definition. """
        return self.definition

    def setGloss(self, definition):
        """ Replace the sense definition with the specified one. """
        self.definition = definition

    def getRelations(self):
        """ Returns the parsed relations for this gloss """
        return {**self.relations}.items()
