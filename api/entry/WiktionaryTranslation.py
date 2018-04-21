from api.util import Language
from api import IWiktionaryTranslation


class WiktionaryTranslation(IWiktionaryTranslation):
    """ Default implementation of the :@link IWiktionaryTranslation interface.
        See there for details. """

    def __init__(self, language=None, translation=None):
        """ Creates a new translation for the given language and translation
         *  string. """
        self._language = language
        if language is not None:
            self.languageStr = language.getCode()
        self.translation = translation
        self.transliteration = None
        self.additionalInformation = None
        self.rawSense = None
        self.checkNeeded = None
        self.gender = None

    def getLanguage(self):
        if self._language is None and self.languageStr is not None:
            self._language = Language.get(self.languageStr)
        return self._language

    def getTranslation(self):
        return self.translation

    def getTransliteration(self):
        return self.transliteration

    def setTransliteration(self, transliteration):
        """ Assigns the given transliteration to this translation. """
        self.transliteration = transliteration

    def getAdditionalInformation(self):
        return self.additionalInformation

    def setAdditionalInformation(self, additionalInformation):
        """ Assigns the given additional information to this translation. """
        self.additionalInformation = additionalInformation

    def getRawSense(self):
        return self.rawSense

    def setRawSense(self, rawSense):
        self.rawSense = rawSense

    def isCheckNeeded(self):
        return self.checkNeeded

    def setCheckNeeded(self, checkNeeded):
        self.checkNeeded = checkNeeded

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        self.gender = gender

    def __str__(self):
        return self.languageStr + ":" + self.translation
