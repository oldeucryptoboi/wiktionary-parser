from errors import IllegalArgumentException
from compat import File
import sys


def PyWiktionaryCli():
    """
     * Offers a command line interface to Wiktionary. You can type a word and
     * after pressing &ltenter&gt the information of corresponding entries will
     * be printed. In order to quit the interface just hit enter
    """

    """
     # @param args path to parsed Wiktionary data
    """
    if len(sys.argv) != 2:
        raise IllegalArgumentException("Too few arguments. Required arguments: <PARSED-WIKTIONARY>")

    PROMPT = "> "
    END = ""

    wktPath = sys.argv[1]

    from api.WiktionaryFormatter import WiktionaryFormatter
    formatter = WiktionaryFormatter.instance()

    try:
        from PyWKTL import PyWKTL
        wkt = PyWKTL.openEdition(File("", wktPath))

        while True:

            line = input(PROMPT)
            if line == END:
                break

            page = wkt.getPageForWord(line)
            if page is None or page.getEntryCount() == 0:
                print(line + " is not in Wiktionary")
            else:
                print(formatter.formatPage(page))
    except EOFError:
        print("exit")


if __name__ == "__main__":
    PyWiktionaryCli()
