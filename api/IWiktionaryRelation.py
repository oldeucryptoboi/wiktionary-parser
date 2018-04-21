class IWiktionaryRelation:
    """ Represents a paradigmatic relation between lexical entries or word senses.
        A relations consists of a source and a target as well as additional
        information on this relationship, such as a type identifier (e.g.,
        synonymy, hyponymy, antonymy). The source of the relation is always a
        :@link IWiktionarySense. For relations that have not yet been attached
        to a certain word sense or that are not depending on a certain word sense
        (e.g., for derived terms that hold for an entire lexical entry), the
        unassigned sense (self):@link IWiktionaryEntry#getUnassignedSense()) is
        used. The target of a relation is given as a word form, sometimes
        including additional hints on the word sense, such as sense indices
        or grammatical information. """

    from enum import Enum

    class LinkType(Enum):
        """ Types of a link used by :@link IWiktionaryRelation#getLinkType(). """

        """ The link was found on the original article page. """
        ARTICLE = 1

        """ The link was found in the Wikisaurus (thesaurus) extension. """
        WIKISAURUS = 2

        # DANGLING, NOT_LINKED,

        def __str__(self):
            return self.name

    def getTarget(self):
        """ Returns the target word form of this relation. """
        pass

    def getTargetSense(self):
        """ Returns additional information on the word sense of the relation's
           target. This is not yet structured information, but the bare
           piece of text encoded in Wiktionary. """
        pass

    def getRelationType(self):
        """ Returns the type of this relation (never <code>None</code>). """
        pass

    def getLinkType(self):
        """ Returns the :@link LinkType that is used to encode the relation's
           target. """
        pass
