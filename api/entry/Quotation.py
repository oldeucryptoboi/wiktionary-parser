from api import IQuotation


class Quotation(IQuotation):
    """ A quotation consists of a quotation source and a list of real quotations.
        For example:
        quotation source:2001 — Eoin Colfer, Artemis Fowl, p 221
        quotations:Then you could say that the doorway exploded.  But the particular verb doesn't do the action justice.  Rather, it shattered into infinitesimal pieces. """

    def __init__(self):
        """ The source of a quotation, i.e. its author and publishing reference.
            A list of text lines sharing the same source.
            Initializes the list of text lines. """
        self.lines = list()
        self.source = None

    def getSource(self):
        return self.source

    def setSource(self, source):
        """ Assigns the given :@link WikiString as the source of the quotation,
            i.e. its author and publishing reference. """
        self.source = source

    def addLine(self, line):
        """ Add a quotation line, i.e. the text of a quotation. """
        self.lines.append(line)

    def getLines(self):
        return self.lines

    def __str__(self):
        result = self.source.getPlainText() + "\n"
        for statement in self.lines:
            result += statement.getPlainText() + "\n"
        return result
