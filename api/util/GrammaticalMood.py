from enum import Enum


class GrammaticalMood(Enum):
    """ Enumeration of the grammatical mood of a :@link IWiktionaryWordForm. """

    """ The declarative mode (modus indicativus) indicates real events.
        For example: "He built a house." """
    INDICATIVE = 1

    """ The commanding mode (imperare). 
        For example: "Built a house!" """
    IMPERATIVE = 2

    """ The conjunctive or subjunctive mode (modus coniunctivus) 
        indicates unreal events. For example: "The house that he build." 
        (instead of "builds") "The house that he shall build." Used to
        express the German "Konjunktiv" ("Er hätte ein Haus gebaut"). """
    CONJUNCTIVE = 3

#    CONDITIONAL,
#    OPTATIVE,
#    JUSSIVE,
#    POTENTIAL,
#    INTERROGATIVE
