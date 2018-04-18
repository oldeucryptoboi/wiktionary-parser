class IWiktionaryTranslation:
    """ Represents a lexical translation of a :@link IWiktionarySense.
      A translation is defined by the translated word form and the target language
      the translated word form belongs to. In addition to that, there can be
      a transliteration (if the target language uses a different script) or
      grammatical information given to clarify the usage of a certain translation.
      Although each translation belongs to a certain word sense (e.g., retrieved by
      :@link IWiktionarySense#getTranslations()) there can be translations that
      have not (yet) been assigned to a word sense. Use the unassigned sense
      (self):@link IWiktionaryEntry#getUnassignedSense()) to retrieve them. """

    def getLanguage(self):
        """ @return the target language of the translation. """
        pass

    def getTranslation(self):
        """ @return the translated word form (belonging to target language). """
        pass

    def getTransliteration(self):
        """ @return a transliteration to the script of the encoding Wiktionary.
           A Russian translation within the English Wiktionary could, for
           example, be transliterated from the Cyrillic to the Latin script.
           Returns <code>None</code> if no transliteration is specified. """
        pass

    def getAdditionalInformation(self):
        """ @return additional information on the translation, including usage
           notes, meaning-related information, and grammatical properties. """
        pass

    def getRawSense(self):
        """ @return the raw sense as specified in the translation section or None """
        pass

    def isCheckNeeded(self):
        """ @return if the translation is marked as "needs checking" """
        pass
