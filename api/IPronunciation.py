class IPronunciation:
    """ Pronunciation information for :@link IWiktionaryEntrys. There can be
        different types of pronunciation information including standardized
        written representations using the IPA or SAMPA notation, audio files
        of people reading a word aloud, and information on the rhyming suffix
        of a lexical entry. """

    from enum import Enum

    class PronunciationType(Enum):
        """ Types of different pronunciation information used by
            :@link IPronunciation#getType(). """

        """ International Phonetic Alphabet """
        IPA = 1
        """ Speech Assessment Methods Phonetic Alphabet """
        SAMPA = 2
        """ Audio file of this pronunciation. """
        AUDIO = 3
        """ Suffix used to identify rhymes. """
        RHYME = 4
        """ Unprocessed pronunciation template """
        RAW = 5

    def getType(self):
        """ Returns the type of this pronunciation, which can be audio files
            or a specific notation schema used to represent pronunciation
            information. """
        pass

    def getText(self):
        """ The representation of the pronunciation using a standardized
            notation such as IPA. In case of audio files, the file name of
            the sound file is returned. The corresponding URL of this sound file
            needs to be obtained by querying
            http://[LANGUAGE].wiktionary.org/wiki/File:[FILENAME]. """
        pass

    def getNote(self):
        """ Returns additional information for this pronunciation, such as
            a geographical reference. """
        pass
