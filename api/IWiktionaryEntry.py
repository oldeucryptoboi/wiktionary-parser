class IWiktionaryEntry:
    """ A :@link IWiktionaryEntry corresponds to a lexical entry. That is, a
      word defined by the language it is used in, its part of speech, its
      etymology and all information encoded for this word. The word "plant" has,
      for instance, separate entries for the English noun, the English verb, and
      the Dutch noun. The meaning of an entry is expressed by multiple
      :@link IWiktionarySenses. Each :@link IWiktionaryEntry belongs to exactly
      one :@link IWiktionaryPage. """

    # -- Identifier --

    def getKey(self):
        """ Returns a unique ID for this lexical entry. The ID is unique for all
           :@link IWiktionaryEntrys of the :@link IWiktionaryEdition. Note
           however that the ID of an entry may differ between different software
           versions or dump dates. """
        pass

    def getId(self):
        """ Returns an ID of this entry that is unique for all entries
           of the containing :@link IWiktionaryPage. Depending on the parsing
           mode, the ID may be a running number of entries or a sense index.
           Use :@link #getKey()  for a globally unique identifier. Note
           however that the ID of an entry may differ between different software
           versions or dump dates.
           IMPORTANT: The entry ID is unstable w.r.t. to different API
             versions and dump files. Better rely on page IDs and eventually
             local indices. """
        pass

    def getIndex(self):
        """ Returns the index of this entry. That is, the running number of
           the entry in accordance to the list of entries of
           the :@link IWiktionaryPage (starting at 0). """
        pass

    # -- Parent --

    def getPage(self):
        """ Returns a reference to the :@link IWiktionaryPage that contains
           this entry. """
        pass

    def getPageId(self):
        """ Returns the ID of the :@link IWiktionaryPage that contains
           this entry. """
        pass

    # -- Entry --

    def getWord(self):
        """ Returns the lemma of this lexical entry denoted by the page title.
           This method is equivalent to <code>getPage().getTitle()</code>. """
        pass

    def getHeader(self):
        """ Returns the header of the lexical entry. This is usually the lemma
           of the entry (i.e. equivalent to :@link #getWord(), but there are
           some exceptions where the Wiktionary community uses a slightly
           different header. """
        pass

    def getRawHeadwordLine(self):
        """
           Returns the unparsed headword line. The format varies from
           language to language and can therefore not get completely
           processed. In simple cases the template used is
           <a href="https://en.wiktionary.org/wiki/Template:head">Template:head</a>. """
        pass

    def getWordLanguage(self):
        """ Returns the language of this lexical entry. This does not necessarily
           correspond to the language of the :@link IWiktionaryEdition e.g.,
           for French entries within the English Wiktionary edition. """
        pass

    def getPartOfSpeech(self):
        """ Returns the first part of speech tag encoded for this lexical entry.
           The first tag is usually the most important one, although there can
           be multiple tags. Use :link #getPartsOfSpeech() to access all
           part of speech tags encoded. If the part of speech is unknown
           or not specified, <code>None</code> will be returned. """
        pass

    def getPartsOfSpeech(self):
        """ Returns all part of speech tags encoded for this lexical entry.
           Most of the time, only one part of speech tag is used. However,
           there are some cases, where multiple tags are used - e.g., for
           German adjectives/adverbs having the same form or for syntactic
           additions, such as "plurale tantum" (only taking the plural form).
           The ordering of tags used in Wiktionary is preserved. The resulted
           list is never None and includes at least one element. """
        pass

    def getGender(self):
        """ Returns the grammatical gender of this lexical entry, which can
           be one of masculine, feminine, neuter. If no gender is specified,
           None is returned. In case of multiple genders, this method will
           return only the first one - use :@link #getGenders() to access
           genders. """
        pass

    def getGenders(self):
        """ Returns the grammatical genders of this lexical entry. Typically,
           this yields a list with a single entry (i.e., masculine, feminine,
           or neuter). For exceptional cases, multiple genders may be associated
           (e.g., for the German "Liter"). If no gender is specified, the result
           will be None. """
        pass

    def getWordEtymology(self):
        """ Returns the etymology of this lexical entry as a :@link IWikiString.
           The result might be <code>None</code> if no etymology has been
           encoded. """
        pass

    def getUsageNotes(self):
        """ Returns the usage notes of this lexical entry as a :@link IWikiString.
           The result might be <code>None</code> if no usage notes have been
           encoded. """
        pass

    def getEntryLink(self):
        """ Some lexical entries refer to other pages rather than encoding
           all information on the entry again. This is similar to a redirect
           (self):@link IWiktionaryPage#getRedirectTarget()), but limited to the
           entry level. In addition to that, there might be further information
           provided. """
        pass

    def getEntryLinkType(self):
        """ Returns the type of the :@link #getEntryLink(), for example, denoting
           that the entry is an old spelling variant of the linked entry. """
        pass

    def getPronunciations(self):
        """ Returns a list of pronunciations for this lexical entry. The
           list might be <code>None</code> if not pronunciations are
           encoded. """
        pass

    def getWordForms(self):
        """ Returns a list of word forms for this lexical entry. The
           list might be <code>None</code> if not word forms are
           encoded. """
        pass

    # -- Senses --

    def getUnassignedSense(self):
        """ Returns a dummy :@link IWiktionarySense that contains all
           information that has not been assigned to a particular sense. This
           is usually the case if the sense marker of an information does not
           match with any :@link IWiktionarySense#getMarker() - e.g., containing
           question marks. The unassigned sense is never <code>None</code>.
           This method is equivalent to <code>getSense(0)</code>. """
        pass

    def getSense(self, index):
        """ Returns the :@link IWiktionarySense with the given index.
           IMPORTANT: The index is a running number starting at 1. Providing
           parameter 0 yields the unassigned sense (equivalent to
           :@link #getUnassignedSense(). The maximum index is equivalent to
           :@link #getSenseCount() (rather than :@link #getSenseCount() - 1).
           @throws ArrayIndexOutOfBoundsException if there is no sense with
             the given index. """
        pass

    def getSenseCount(self):
        """ Returns the number of :@link IWiktionarySenses encoded for this
           lexical entry. """
        pass

    def getSenses(self, includeUnassignedSense):
        """ Returns the list of all :@link IWiktionarySenses. The list is
           never None nor empty. If the parameter is set to <code>True</code>,
           the first element (list index 0) is the unassigned sense (equivalent
           to :@link #getUnassignedSense(). The following elements are all
           senses of this entry, i.e. all senses with index 1 to
           :@link #getSenseCount(). """
        pass

    # -- Combination --

    def getGlosses(self):
        """ Returns a list containing all sense definitions of the entry's senses
           (including the unassigned sense). Hence, the method is a shorthand
           for invoking :@link IWiktionarySense#getGloss() for each sense.
           The list is never <code>None</code> but might be empty. """
        pass

    def getExamples(self):
        """ Returns a list containing all sense definitions of the entry's senses
               (including the unassigned sense). Hence, the method is a shorthand
           for invoking :@link IWiktionarySense#getExamples() for each sense.
           The list is never <code>None</code> but might be empty. """
        pass

    def getQuotations(self):
        """ Returns a list containing all quotations of the entry's senses
           (including the unassigned sense). Hence, the method is a shorthand
           for invoking :@link IWiktionarySense#getQuotations() for each sense.
           The list is never <code>None</code> but might be empty. """
        pass

    def getRelations(self, relationType):
        """ Returns a list containing all semantic relations of the entry's senses
           (including the unassigned sense) of the given type. Hence, the
           method is a shorthand for invoking
           :@link IWiktionarySense#getRelations(RelationType) for each sense.
           The list is never <code>None</code> but might be empty. """
        pass

    def getReferences(self):
        """ Returns a list containing all references of the entry's senses
           (including the unassigned sense). Hence, the method is a shorthand
           for invoking :@link IWiktionarySense#getReferences() for each sense.
           The list is never <code>None</code> but might be empty. """
        pass

    def getTranslations(self, language):
        """ Returns a list containing all translations of the entry's senses
           (including the unassigned sense) to the given language. Hence, the
           method is a shorthand for invoking
           :@link IWiktionarySense#getTranslations(ILanguage) for each sense.
           The list is never <code>None</code> but might be empty. """
        pass
