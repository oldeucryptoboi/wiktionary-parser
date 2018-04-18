from errors import RuntimeException


class WiktionaryException(RuntimeException):
    """ Runtime exception which is thrown by the API in different situations,
      especially when there are problems accessing the parsed Wiktionary data. """
    def __init__(self, message="", cause=None):
        super().__init__(message, cause)
