from enum import Enum


class GrammaticalPerson(Enum):
    """ Enumeration of the grammatical number of a :@link IWiktionaryWordForm. """

    """ The first person the speaker referred to by "I", "we". """
    FIRST = 1

    """ The second person the addressee referred to by "you". """
    SECOND = 2

    """ The third person the other referred to by "he", "she", 
         "it", "they". """
    THIRD = 3

    def __str__(self):
        return str(self.name)
