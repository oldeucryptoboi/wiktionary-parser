from api import IWiktionaryWordForm


class WiktionaryWordForm(IWiktionaryWordForm):
    """ Implementation of the :@link IWiktionaryWordForm interface. Instances
        of this class represent inflected word forms. """

    grammaticalNumber = None
    grammaticalCase = None
    grammaticalTense = None
    grammaticalMood = None
    grammaticalDegree = None
    grammaticalAspect = None
    nonFiniteForm = None
    grammaticalPerson = None

    def __init__(self, wordForm):
        """ Instantiates a new word form with the given written form. """
        self.wordForm = wordForm

    def getWordForm(self):
        return self.wordForm

    def setWordForm(self, wordForm):
        """ Assign the given written form to this instance. """
        self.wordForm = wordForm

    def getNumber(self):
        return self.grammaticalNumber

    """ Assign the given grammatical number to this word form. """
    def setNumber(self, grammaticalNumber):
        self.grammaticalNumber = grammaticalNumber

    def getCase(self):
        return self.grammaticalCase

    def setCase(self, grammaticalCase):
        """ Assign the given grammatical case to this word form. """
        self.grammaticalCase = grammaticalCase

    def getPerson(self):
        return self.grammaticalPerson

    def setPerson(self, grammaticalPerson):
        """ Assign the given grammatical person to this word form. """
        self.grammaticalPerson = grammaticalPerson

    def getTense(self):
        return self.grammaticalTense

    def setTense(self, grammaticalTense):
        """ Assign the given grammatical tense to this word form. """
        self.grammaticalTense = grammaticalTense

    def getMood(self):
        return self.grammaticalMood

    def setMood(self, grammaticalMood):
        """ Assign the given grammatical mood to this word form. """
        self.grammaticalMood = grammaticalMood

    def getDegree(self):
        return self.grammaticalDegree

    def setDegree(self, grammaticalDegree):
        """ Assign the given grammatical degree to this word form. """
        self.grammaticalDegree = grammaticalDegree

    def getAspect(self):
        return self.grammaticalAspect

    def setAspect(self, grammaticalAspect):
        """ Assign the given grammatical aspect to this word form. """
        self.grammaticalAspect = grammaticalAspect

    def getNonFiniteForm(self):
        return self.nonFiniteForm

    def setNonFiniteForm(self, nonFiniteForm):
        """ Assign the given type of non finite word form. """
        self.nonFiniteForm = nonFiniteForm
