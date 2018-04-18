from enum import Enum


class NonFiniteForm(Enum):
    """ Enumeration for modelling non-finite :@link IWiktionaryWordForms.
        Although other form properties (like :@link GrammaticalTense) are
        predominantly used to represent finite forms, such properties can
        also be used to describe non-finite forms. For example, the English
        present participle (tense = PRESENT) and past participle (tense = PAST). """

    """ The infinitive form of a verb (e.g., "(to) do"). """
    INFINITIVE = 1

    """ The participle form of a verb (e.g., "done"). Participle forms should
        be combined with a :@link GrammaticalTense. """
    PARTICIPLE = 2

#  ATTRIBUTIVE
#  CONVERB
#  GERUNDIVE
#  GERUND
