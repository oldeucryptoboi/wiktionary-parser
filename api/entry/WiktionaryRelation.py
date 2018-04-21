from api import IWiktionaryRelation


class WiktionaryRelation(IWiktionaryRelation):
    """ Default implementation of the :@link IWiktionaryRelation interface.
        See there for details. """

    def __init__(self, target, type):
        """ Creates a new relation for the given target and relation type. """
        self.target = target
        self.type = type
        # self.entryLanguageStr = RelationSourceType.ENTRY
        self.targetSense = None

        self.linkType = None

    def getRelationType(self):
        return self.type

    def getTarget(self):
        return self.target

    def getTargetSense(self):
        return self.targetSense

    def setTargetSense(self, targetSense):
        """ Specifies additional information on the target word sense. """
        self.targetSense = targetSense

    def getLinkType(self):
        return self.linkType

    def setLinkType(self, linkType):
        """ Assigns a new link type for this relation. """
        self.linkType = linkType

    def __str__(self):
        return self.type + ":" + self.target
