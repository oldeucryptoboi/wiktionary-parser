class IWiktionaryWordForm:
    """ Represents an (inflected) word form of a :@link IWiktionaryEntry. The
      class can be used to model any different type of modification of a word
      including verb conjugation and noun/adjective declension. For the former,
      both finite and non-finite verb forms may be represented. Certain inflected
      word forms usually found in a dictionary are represented by a combination
      of the grammatical properties.
      <p>Common English word forms</p><ul>
      <li>Noun:
        number = :SINGULAR, PLURAL</li>
      <li>Verb, third person singular, present tense:
        person = THIRD, number = SINGULAR, tense = PRESENT</li>
      <li>Verb, present participle:
        tense = PRESENT, nonFiniteForm = PARTICIPLE</li>
      <li>Verb, simple past:
        tense = PAST</li>
      <li>Verb, past participle:
        tense = PAST, nonFiniteForm = PARTICIPLE</li>
      <li>Adjective/Adverb:
        degree = :POSITIVE, COMPARABLE, SUPERLATIVE</li></ul>
      <p>Common German word forms</p><ul>
      <li>Noun:
        number = :SINGULAR, PLURAL, case = :NOMINATIVE, GENITIVE, DATIVE, ACCUSATIVE</li>
      <li>Verb, present tense:
        mood = INDICATIVE, person = :FIRST, SECOND, THIRD, number = :SINGULAR, PLURAL, tense = PRESENT</li>
      <li>Verb, past tense:
        mood = INDICATIVE, person = :FIRST, SECOND, THIRD, number = :SINGULAR, PLURAL, tense = PAST</li>
      <li>Verb, imperative:
        mood = IMPERATIVE, person = :FIRST, SECOND, THIRD, number = :SINGULAR, PLURAL</li>
      <li>Verb, conjunctive present (Konjunktiv I):
        mood = CONJUNCTIVE, tense = PRESENT</li>
      <li>Verb, conjunctive past (Konjunktiv II):
        mood = CONJUNCTIVE, tense = PAST</li>
      <li>Verb, present participle (Partizip I):
        aspect = IMPERFECT, nonFiniteForm = PARTICIPLE</li>
      <li>Verb, perfect participle (Partizip II):
        aspect = PERFECT, nonFiniteForm = PARTICIPLE</li>
      <li>Adjective/Adverb:
        degree = :POSITIVE, COMPARABLE, SUPERLATIVE</li></ul> """

    def getWordForm(self):
        """ Returns the word form or <code>None</code> if no such word form
           exists (but specified). An example for the latter is the English noun
           "information", which does not have a plural form. """
        pass

    def getNumber(self):
        """ Returns the :@link GrammaticalNumber of this word form or
           <code>None</code> if no number is specified or applicable. """
        pass

    def getCase(self):
        """ Returns the :@link GrammaticalCase of this word form or
           <code>None</code> if no case is specified or applicable. """
        pass

    def getPerson(self):
        """ Returns the :@link GrammaticalPerson of this word form or
           <code>None</code> if no person is specified or applicable. """
        pass

    def getTense(self):
        """ Returns the :@link GrammaticalTense of this word form or
           <code>None</code> if no tense is specified or applicable. """
        pass

    def getMood(self):
        """ Returns the :@link GrammaticalMood of this word form or
           <code>None</code> if no mood is specified or applicable. """
        pass

    def getDegree(self):
        """ Returns the :@link GrammaticalDegree of this word form or
           <code>None</code> if no degree is specified or applicable. """
        pass

    def getAspect(self):
        """ Returns the :@link GrammaticalAspect of this word form or
           <code>None</code> if no aspect is specified or applicable. """
        pass

    def getNonFiniteForm(self):
        """ Returns the :@link NonFiniteForm type of this word form or
           <code>None</code> if no type is specified or applicable. """
        pass
