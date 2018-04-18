from api import PartOfSpeech
from parser.entry import EntryFactory


class ENEntryFactory(EntryFactory):
    """ A factory creates PosEntry objects """

    @classmethod
    def findPartOfSpeech(cls, name):
        return PartOfSpeech.findByName(name, ENEntryFactory.posMap)

    posMap = {
        "ABBREVIATION": PartOfSpeech.ABBREVIATION,
        "ACRONYM": PartOfSpeech.ACRONYM,
        "ADJECTIVE": PartOfSpeech.ADJECTIVE,
        "ADVERB": PartOfSpeech.ADVERB,
        "ARTICLE": PartOfSpeech.ARTICLE,
        "COMBINING_FORM": PartOfSpeech.COMBINING_FORM,
        "CONJUNCTION": PartOfSpeech.CONJUNCTION,
        "CONTRACTION": PartOfSpeech.CONTRACTION,
        "DETERMINER": PartOfSpeech.DETERMINER,
        "GISMU": PartOfSpeech.GISMU,
        "IDIOM": PartOfSpeech.IDIOM,
        "INITIALISM": PartOfSpeech.INITIALISM,
        "INTERJECTION": PartOfSpeech.INTERJECTION,
        "LETTER": PartOfSpeech.LETTER,
        "NOUN": PartOfSpeech.NOUN,
        "NOUN_PHRASE": PartOfSpeech.NOUN_PHRASE,
        "NUMBER": PartOfSpeech.NUMBER,
        "PARTICIPLE": PartOfSpeech.PARTICIPLE,
        "PARTICLE": PartOfSpeech.PARTICLE,
        "POSTPOSITION": PartOfSpeech.POSTPOSITION,
        "PREFIX": PartOfSpeech.PREFIX,
        "PREPOSITION": PartOfSpeech.PREPOSITION,
        "PRONOUN": PartOfSpeech.PRONOUN,
        "PROPER_NOUN": PartOfSpeech.PROPER_NOUN,
        "PROVERB": PartOfSpeech.PROVERB,
        "SUFFIX": PartOfSpeech.SUFFIX,
        "SYMBOL": PartOfSpeech.SYMBOL,
        "VERB": PartOfSpeech.VERB,

        "HAN_CHARACTER": PartOfSpeech.CHARACTER,
        "HANJI": PartOfSpeech.CHARACTER,
        "KANJI": PartOfSpeech.KANJI,
        "HIRAGANA_CHARACTER": PartOfSpeech.HIRAGANA,
        "KATAKANA_CHARACTER": PartOfSpeech.KATAKANA,
        "ROMAJI": PartOfSpeech.CHARACTER,
        "HANJA": PartOfSpeech.CHARACTER,

        "NUMERAL": PartOfSpeech.NUMERAL,
        "CARDINAL_NUMBER": PartOfSpeech.NUMBER,
        "CARDINAL_NUMERAL": PartOfSpeech.NUMERAL,
        "ORDINAL_NUMBER": PartOfSpeech.NUMBER,
        "ORDINAL_NUMERAL": PartOfSpeech.NUMERAL,
        "PROPERR_NOUN": PartOfSpeech.PROPER_NOUN,
        "PROPER_OUN": PartOfSpeech.PROPER_NOUN,

        "EXPRESSION": PartOfSpeech.EXPRESSION,
        "PHRASE": PartOfSpeech.PHRASE,
        "PREPOSITIONAL_PHRASE": PartOfSpeech.PHRASE,
        "CMAVO": PartOfSpeech.EXPRESSION,
        "NOUN_FORM": PartOfSpeech.WORD_FORM,
        "VERB_FORM": PartOfSpeech.WORD_FORM,
        "INFIX": PartOfSpeech.AFFIX,
    }
