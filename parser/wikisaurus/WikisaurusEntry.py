from api import IWiktionaryRelation
from api.entry import WiktionaryRelation


class WikisaurusEntry:
    """ Intermediate representation of Wikisaurus articles used by the
        :@link WikisaurusArticleParser. The information stored in this
        class will be transfered to the main article structure (i.e., the """

    def __init__(self, title, partOfSpeech, language, senseDefinition):
        """ Instantiates a new entry with the given title, part of speech,
            language, and sense definition (optional)"""
        self.title = title
        self.partOfSpeech = partOfSpeech
        self.language = language
        self.senseDefinition = senseDefinition
        self.relations = set()

    def addRelation(self, target, targetSense, type_):
        """ Adds a new :@link WiktionaryRelation to this entry based on the
            given parameters. """
        newRelation = WiktionaryRelation(target, type_)
        if targetSense is not None:
            newRelation.setTargetSense(targetSense)
        newRelation.setLinkType(IWiktionaryRelation.LinkType.WIKISAURUS)
        self.relations.add(newRelation)

    def getTitle(self):
        """ Returns the page title. """
        return self.title

    def getPartOfSpeech(self):
        """ Returns the part of speech tag. """
        return self.partOfSpeech

    def getLanguage(self):
        """ Returns the word language. """
        return self.language

    def getSenseDefinition(self):
        """ Returns the sense definition. """
        return self.senseDefinition

    def getRelations(self):
        """ Returns the semantic relations. """
        return self.relations

    def __str__(self):
        return self.title + "/" + self.partOfSpeech + "/" + self.language + "<" + self.senseDefinition + ">"
