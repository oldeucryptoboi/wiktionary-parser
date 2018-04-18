from api import IPronunciation


class Pronunciation(IPronunciation):
    """ Default implementation of the :@link IPronunciation interface.
        See there for details. """

    def __init__(self, type, text, note):
        """ Creates a new pronunciation for the given representation text,
            notation type and addition information. For audio files, the
            representation text refers to an audio file name. """
        self.type = type
        self.text = text
        self.note = note

    def getType(self):
        return self.type

    def getText(self):
        return self.text

    def getNote(self):
        return self.note
