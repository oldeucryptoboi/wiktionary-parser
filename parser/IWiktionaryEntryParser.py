from api import WiktionaryException
from errors import WiktionaryException


class IWiktionaryEntryParser:
    """ A parser for separating an article page's text into individual
        Wiktionary word entries. """

    def parse(self, page, text):
        """ Creates Wiktionary word entry instances from the provided text, and
            adds them to the given article page.
            @throws WiktionaryException in case of any parser errors. """
        raise WiktionaryException()
