from enum import Enum


class GrammaticalNumber(Enum):
    """ Enumeration of the grammatical number of a :@link IWiktionaryWordForm. """

    """ A single item (e.g., "a book", "one pen", "the guy"). """
    SINGULAR = 1

    """ Multiple items (e.g., "books", "two pens", "the guys"). """
    PLURAL = 2

#  SINGULATIVE,
#  COLLECTIVE,
#  DUAL, # 2 items
#  TRIAL, # 3 items
#  QUADRAL, # 4 items
#  PAUCAL, # few items
#  DISTRIBUTIVE_PLURAL, # independent instances
