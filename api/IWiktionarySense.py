class IWiktionarySense:
    """ A :@link IWiktionarySense represents one word sense of a lexical entry
      (also called a lexical unit). Each :@link IWiktionarySense belongs to
      exactly one :@link IWiktionaryEntry. Note that
      :@link IWiktionaryEntry#getUnassignedSense() returns a dummy word sense
      carrying all information that has not been assigned to a particular
      sense - for this case, the :@link IWiktionarySense does not model an
      actual word sense, """

    # -- Identifier --

    def getKey(self):
        """ Returns a unique ID for this word sense. The ID is unique for all
           :@link IWiktionarySenses of the :@link IWiktionaryEdition. Note
           however that the ID of a sense may differ between different software
           versions or dump dates. """
        pass

    def getId(self):
        """ Returns an ID of this sense that is unique for all senses
           of the containing :@link IWiktionaryEntry. Use :@link #getKey()
           for a globally unique identifier. """
        pass

    def getIndex(self):
        """ Returns the index of this sense. That is, the running number of
           the sense in accordance to the list of senses of the
           :@link IWiktionaryEntry. The first sense has index 1.
           Note that this is not generally the index marker used in Wiktionary:
           the first sense has for example always index 1, although it might
           be marked with "[2]" or "[1a]". See :@link #getMarker() for details. """
        pass

    def getMarker(self):
        """ Returns the marker for this sense as defined in Wiktionary. This
           can be different for each type of Wiktionary edition for example,
           running numbers, short textual labels,... """
        pass

    # -- Parent --

    def getEntry(self):
        """ Returns a reference to the :@link IWiktionaryEntry that contains
           this sense. """
        pass

    def getPage(self):
        """ Returns a reference to the :@link IWiktionaryPage that contains
           this sense. """
        pass

    # -- Sense --

    def getGloss(self):
        """ Returns the sense description as a :@link IWikiString. """
        pass

    def getExamples(self):
        """ Returns a list of sense examples or <code>None</code> if no sense
           examples are encoded. """
        pass

    def getQuotations(self):
        """ Returns a list of quotations or <code>None</code> if no
           quotations are encoded. """
        pass

    def getRelations(self, relationType):
        """ Returns the list of sense relations of the given relation type.
           If there are no relations of this type, an empty list will be
           returned. """
        pass

    def getReferences(self):
        """ Returns a list of references for this sense or
           <code>None</code> if no referemces are encoded. """
        pass

    def getTranslations(self, language):
        """ Returns the list of translations into the given language.
           If there are no translations of this type, an empty list will be
           returned. """
        pass

    # -- Subsenses --
