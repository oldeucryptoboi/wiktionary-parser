from parser.en.components.ENBlockHandler import ENBlockHandler
from api.entry.WikiString import WikiString
from api.entry.Quotation import Quotation


class ENQuotationHandler(ENBlockHandler):
    """ Parser component for extracting quotations from the English Wiktionary. """

    def __init__(self):
        """ Initializes the block handler for parsing all sections starting with
         *  one of the specified labels. """
        super().__init__("Quotations")

        self.quotations = None

    def processHead(self, textLine, context):
        self.quotations = list()
        return super().processHead(textLine, context)

    def processBody(self, textLine, context):
        line = textLine.strip()
        if line.startswith("|"):
            return self.extractQuotation("*" + line, True, context)
        else:
            return self.extractQuotation(line, False, context)

    # noinspection PyUnusedLocal
    def extractQuotation(self, textLine, additionalLine, context):
        """ Extract a quotation from the given line and add it to the internal list.
            @param textLine
            @param additionalLine if <code>False</code> adds a new quotation to
                the list and otherwise appends the quotation to the last one.
            @param context """
        line = textLine.strip()
        if not line.startswith("*"):
            return False

        line = line[1:].strip()
        if line.startswith(":"):
            if self.quotations:
                q = self.quotations[-1]
                while line.startswith(":"):
                    line = line[1:]
                q.addLine(WikiString(line.strip()))

        elif additionalLine:
            if self.quotations:
                quot = self.quotations[-1]
                idx = len(quot.getLines()) - 1
                if idx >= 0:
                    line = quot.getLines()[idx].getText() + " " + line
                    quot.getLines()[idx] = WikiString(line.strip())
                else:
                    quot.getLines().add(WikiString(line.strip()))

        else:
            quotationEntry = Quotation()
            if line.startswith("{{"):
                quotationEntry.addLine(WikiString(line.strip()))
            else:
                quotationEntry.setSource(WikiString(line.strip()))
            self.quotations.append(quotationEntry)

        return False

    def fillContent(self, context):
        posEntry = context.findEntry()
        for quotation in self.quotations:
            posEntry.getUnassignedSense().addQuotation(quotation)

    def getQuotations(self):
        """ Returns the list of all quotations. """
        return self.quotations
