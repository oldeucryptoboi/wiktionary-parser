from enum import Enum


class GrammaticalCase(Enum):
    """ Enumeration of the grammatical case of a :@link IWiktionaryWordForm. """

    """ Indicates the subject of a finite verb. Ask "Wer/Was?" in
        German sentences (e.g., "_Peter_ liest"). """
    NOMINATIVE = 1

    """ Indicates the direct object of a verb. Ask "Wen/Was?" in
        German sentences (e.g., "Peter liest _ein Buch_"). """
    ACCUSATIVE = 2

    """ Indicates the indirect object of a verb. Ask "Wem?" in
        German sentences (e.g., "Peter liest _ihr_ vor")."""
    DATIVE = 3

    """ Indicates possession. Ask "Wessen?" in German sentences 
        (e.g., "_Peters_ Buch ist spannend")."""
    GENITIVE = 4


# ABLATIVE, # indicates movement from smth. or cause
# VOCATIVE, # indicates addressee
# LOCATIVE, # indicates locatoin
# INSTRUMENTAL, # indicates intrument used for action
