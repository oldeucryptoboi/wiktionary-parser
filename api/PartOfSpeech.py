from enum import Enum
from compat import Logger


class PartOfSpeech(Enum):
    """ Generic representation of the parts of speech used in Wiktionary. The
      part of speech is defined for a certain :@link IWiktionaryEntry.
      @see IWiktionaryEntry#getPartOfSpeech() """

    """ Noun. """
    NOUN = 1
    """ Proper noun (names, locations, organizations) """
    PROPER_NOUN = 2
    """ First/given name (e.g. Nadine). """
    FIRST_NAME = 3
    """ Last/family name (e.g. Miller). """
    LAST_NAME = 4
    """ Toponym (i.e., a place name). """
    TOPONYM = 5

    """ Only takes the singular form. """
    SINGULARE_TANTUM = 6
    """ Only takes the plural form. """
    PLURALE_TANTUM = 7

    """ Measure words (e.g., litre). """
    MEASURE_WORD = 8

    """ Verb. """
    VERB = 9
    """ Auxiliary verb (can, might, must, etc.). """
    AUXILIARY_VERB = 10

    """ Adjective. """
    ADJECTIVE = 11
    """ Adverb. """
    ADVERB = 12

    """ Interjection. """
    INTERJECTION = 13
    """ Salutation (e.g., good afternoon). """
    SALUTATION = 14
    """ Onomatopoeia (e.g., peng, tic-tac). """
    ONOMATOPOEIA = 15

    """ Phrase. """
    PHRASE = 16
    """ Idiom (e.g., rock 'n' roll). """
    IDIOM = 17
    """ Collocation (e.g., strong tea). """
    COLLOCATION = 18
    """ Proverb (e.g., that's the way life is). """
    PROVERB = 19
    """ Mnemonic (e.g., "My Very Educated Mother Just Served Us Nachos"
       for planet names). """
    MNEMONIC = 20

    """ Pronoun. """
    PRONOUN = 21
    """ (Irreflexive) personal pronoun (I, you, he, she, we, etc.). """
    PERSONAL_PRONOUN = 22
    """ Reflexive personal pronoun (myself, herself, ourselves, etc.). """
    REFLEXIVE_PRONOUN = 23
    """ Possessive pronoun (mine, your, our, etc.). """
    POSSESSIVE_PRONOUN = 24
    """ Demonstrative pronoun (_This_ is fast). """
    DEMONSTRATIVE_PRONOUN = 25
    """ Relative pronoun (She sold the car, _which_ was very old ). """
    RELATIVE_PRONOUN = 26
    """ Indefinite pronoun (_Nobody_ bought the car ). """
    INDEFINITE_PRONOUN = 27

    """ Interrogative pronoun (who, what, etc.). """
    INTERROGATIVE_PRONOUN = 28
    """ Interrogative adverb (how, when, etc.). """
    INTERROGATIVE_ADVERB = 29

    """ Particle. """
    PARTICLE = 30
    """ Answer particle (yes, no, etc.). """
    ANSWERING_PARTICLE = 31
    """ Negative particle (neither...nor, etc.). """
    NEGATIVE_PARTICLE = 32
    """ Comparative particle (She is taller _than_ me). """
    COMPARATIVE_PARTICLE = 33
    """ Focus particle (also, only, even, etc.). """
    FOCUS_PARTICLE = 34
    """ Intensifying particle (very, low, etc.). """
    INTENSIFYING_PARTICLE = 35
    """ Modal particle (express attitude, e.g., German: Sprich _doch mal_ mit ihr ). """
    MODAL_PARTICLE = 36

    """ Article (a, the, etc.). """
    ARTICLE = 37
    """ Determiner (few, most, etc.). """
    DETERMINER = 38

    """ Abbreviation. """
    ABBREVIATION = 39
    """ Acronym (pronounced as a word, e.g., "ROM", "NATO", "sonar") """
    ACRONYM = 40
    """ Initialism (pronounced as letter by letter, e.g., "CD", "URL") """
    INITIALISM = 41
    """ Contraction (e.g., it's). """
    CONTRACTION = 42

    """ Conjunction (and, or, etc.). """
    CONJUNCTION = 43
    """ Subordinating conjunction (as soon as, after, etc.). """
    SUBORDINATOR = 44

    """ Preposition (e.g., underneath). """
    PREPOSITION = 45
    """ Postposition (e.g., ago). """
    POSTPOSITION = 46

    """ Affix. """
    AFFIX = 47
    """ Prefix. """
    PREFIX = 48
    """ Suffix. """
    SUFFIX = 49
    """ Place name suffix (e.g., -burg). """
    PLACE_NAME_ENDING = 50
    """ Bound lexeme. """
    LEXEME = 51

    """ Character. """
    CHARACTER = 52
    """ Letter of the alphabet (A, B, C, etc.). """
    LETTER = 53
    """ Number and numeral (e.g., two, fifteen, etc.). """
    NUMBER = 54
    """ Number and numeral (e.g., two, fifteen, etc.). """
    NUMERAL = 55
    """ Punctuation mark (., ?, , etc.). """
    PUNCTUATION_MARK = 56
    """ Symbol (+, §, $, etc.). """
    SYMBOL = 57
    """ Chinese Hanzi character. """
    HANZI = 58
    """ Japanese Kanji character. """
    KANJI = 59
    """ Japanese Katakana character. """
    KATAKANA = 60
    """ Japanese Hiragana character. """
    HIRAGANA = 61

    """ Gismu (a root word in Lojban). """
    GISMU = 62

    """ Inflected word form. """
    WORD_FORM = 63
    """ Participle. """
    PARTICIPLE = 64
    """ Transliterated word form. """
    TRANSLITERATION = 65

    """ @deprecated No longer used. """
    COMBINING_FORM = 66
    """ @deprecated No longer used. """
    EXPRESSION = 67
    """ @deprecated No longer used. """
    NOUN_PHRASE = 68

    logger = Logger.getLogger("PartOfSpeech")

    # protected static Set<String> unknownPos

    @classmethod
    def findByName(cls, name, additionalMap=None):
        """ Find the part of speech with the given name. The method checks both
           for the canonical English name as well as alternative names in
           other languages, which can be specified by passing a custom
           additional map. If no part of speech could be found,
           <code>None</code> is returned. """
        if not name:
            return None

        label = ""

        for p in name.strip():
            if p == ' ' or p == '\n' or p == '\r' or p == '\t':
                label += '_'
            else:
                label += p.upper()

        result = None
        if additionalMap is not None:
            result = additionalMap.get(label, None)

        if result is None:
            try:
                result = cls[label]
            except KeyError:
                # cls.logger.finer("Unknown part of speech: " + str(label))
                pass

        return result

    def __eq__(self, other):
        if other is None or not isinstance(other, PartOfSpeech):
            return False
        else:
            return self.value == other.value
