from enum import Enum


class GrammaticalGender(Enum):
    """ Enumeration for modeling the grammatical gender of a :@link IWiktionaryEntry. """

    """ Masculine gender (e.g., the German "Hund"). """
    MASCULINE = 1

    """ Feminine gender (e.g., the German "Katze"). """
    FEMININE = 2

    """ Neuter gender (e.g., the German "Haus"). """
    NEUTER = 3

#    ANIMATE
#    INANIMATE
#    HUMAN
#    NON_HUMAN
#    ANIMAL
#    OTHER

    def __str__(self):
        return str(self.name)
