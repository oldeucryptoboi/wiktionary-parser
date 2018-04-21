from enum import Enum


class RelationType(Enum):
    """ Represents the relation types used for :@link IWiktionaryRelations. In the
      examples below, $ARTICLE refers to the :@link IWiktionarySense (the
      relation's source) and $LINK refers to the hyperlink text (i.e., the
      referenced word the relation's target). """

    """ Synonymy - $LINK carries the same meaning as $ARTICLE 
       (e.g., "plant" and "factory"). """
    SYNONYM = 1

    """ Antonymy - $LINK has the opposite meaning of $ARTICLE
       (e.g., "bright" and "dark"). """
    ANTONYM = 2

    """ Hypernymy - $LINK is more general than $ARTICLE  
       (e.g., "building" and "factory"). """
    HYPERNYM = 3

    """ Hyponymy - $LINK is more specialized than $ARTICLE
       (e.g., "factory" and "building"). """
    HYPONYM = 4

    """ Holonymy - $LINK is the whole of $ARTICLE 
       (e.g., "tree" and "leaf"). """
    HOLONYM = 5

    """ Meronymy - $LINK is a part of $ARTICLE 
       (e.g., "leaf" and "tree"). """
    MERONYM = 6

    """ Cohyponymy - $LINK and $ARTICLE share the same hypernym, but are 
       not synonyms or antonyms 
       (e.g., "dog "and "cat", which are both animals). """
    COORDINATE_TERM = 7

    """ Troponymy - $LINK is a certain manner of $ARTICLE 
       (e.g., "(to) slice" is "(to) cut" in a certain manner). 
       Note: Although the common definition of troponymy applies to 
       verbs, this relation is also used between other parts of speech
       within Wiktionary. """
    TROPONYM = 8

    """ Other semantic relation - $LINK is related to $ARTICLE in some 
       (associative) way (e.g., "product" and "multiplication"). """
    SEE_ALSO = 9

    """ Morphological derivation - $LINK is derived from $ARTICLE
       (e.g., "driver" is derived from "drive" using the -er suffix). """
    DERIVED_TERM = 10

    """ Etymological relation - $LINK and $ARTICLE share the same etymology, 
       but are not morphological derivations
       (e.g., "datum" and "data" share the same origin, but are not 
       morphologically related). """
    ETYMOLOGICALLY_RELATED_TERM = 11

    """ Etymological relation - $LINK is derived from $ARTICLE
       (e.g., "taxi" is a descendent of "taximeter")
       This type of relation usually targets at a foreign language word, 
       i.e. the language of $LINK borrowed/inherited the lexical entry 
       $ARTICLE (e.g., the German verb "zoomen" is a descendent of the
       English "(to) zoom"). """
    DESCENDANT = 12

    """ Collocation - $LINK represents a word or phrase that co-occurs 
       frequently with $ARTICLE (e.g., "strong" co-occurs often with 
       "tea" - "strong tea" is usually used although "powerful tea" would
       essentially denote the same meaning.
       Note: $LINK can be a phrase including $ARTICLE (e.g., "strong tea") 
       or just a single word without $ARTICLE (e.g., "strong") that co-occurs
       anywhere with the word $ARTICLE. """
    CHARACTERISTIC_WORD_COMBINATION = 13

    def __str__(self):
        return str(self.name)
