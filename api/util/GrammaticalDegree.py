from enum import Enum


class GrammaticalDegree(Enum):
    """ Enumeration of the grammatical degree of a :@link IWiktionaryWordForm. """

    """ Denotes an a property (e.g., "Your flowers are _pretty_"). """
    POSITIVE = 1

    """ Indicates a greater degree (e.g., "Your flowers are 
     *  _prettier_ than mine"). """
    COMPARATIVE = 2

    """ Indicates the greatest degree (e.g., "Your flowers are 
        _prettiest_"). """
    SUPERLATIVE = 3

#   RELATIVE,
