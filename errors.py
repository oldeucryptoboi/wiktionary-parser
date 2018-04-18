import xml.sax


class IOException(Exception):
    pass


# noinspection PyUnusedLocal
class RuntimeException(Exception):
    def __init__(self, message, cause=None):
        raise Exception(message)
        pass


class WiktionaryException(Exception):
    pass


class DatabaseException(Exception):
    pass


class IllegalArgumentException(Exception):
    pass


class NoSuchElementException(Exception):
    pass


class UnsupportedOperationException(StopIteration):
    pass


class IllegalStateException(Exception):
    pass


class ParseException(Exception):
    pass


class FactoryConfigurationError(Exception):
    pass


class SAXException(xml.sax.SAXException):
    pass


class ParserConfigurationException(xml.sax.SAXException):
    pass


class NullPointerException(Exception):
    pass
