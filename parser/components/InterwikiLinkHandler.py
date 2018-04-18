from .BlockHandler import BlockHandler


class InterwikiLinkHandler(BlockHandler):
    """ Generic parser component for extracting interwiki links (e.g., [de:dog])
        from the Wiktionary article pages. """

    def __init__(self, categoryHead):
        """ Initializes the handler for the specified category head
            (e.g., "Category"). The category head is required for distinugishing
            between categories and interwiki links. """
        self.categoryHead = categoryHead

        self.language = None

    def canHandle(self, blockHeader):
        # Check if the line encodes an interwiki link.
        line = blockHeader.strip()
        isBracketed = line.startswith("[[") and line.endswith("]]")
        return ":" in line and self.categoryHead not in line and isBracketed

    def processHead(self, textLine, context):
        # Extract the language of the interwiki link.
        self.language = None
        line = textLine.strip()
        colonIndex = line.find(":")
        if colonIndex != -1:
            self.language = line[2:colonIndex].strip()

        return True

    def fillContent(self, context):
        # Add the interwiki link to the current page.
        if self.language is not None:
            context.getPage().addInterWikiLink(self.language)
