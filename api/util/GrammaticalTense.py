from enum import Enum


class GrammaticalTense(Enum):
    """ Enumeration of the grammatical tense of a :@link IWiktionaryWordForm.
        Note that tense is often combined with verb aspects (e.g., present
        perfect). Such combinations can be modeled in combination with
        enumeration values from :@link GrammaticalAspect. """

    """ The past an utterance refers to the time before a reference time. """
    PAST = 1

    """ The present an utterance refers to the reference time. """
    PRESENT = 2

    """ The future an utterance refers to the time after a reference time. """
    FUTURE = 3
