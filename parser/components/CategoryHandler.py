from errors import IllegalStateException
from .BlockHandler import BlockHandler
import re


class CategoryHandler(BlockHandler):
    """
     * Extract categories.
     """

    categories = set()

    def __init__(self, categoryHead):
        """ Instantiate the categories worker using the given categories head. This
         *  is to be the prefix appearing in categories templates (e.g.,
         *  "Kategorie" for German). """
        self.categoryPattern = re.compile("\\[\\[:?" + categoryHead + ":([^\\]]+)\\]\\]")

    def canHandle(self, blockHeader):
        return blockHeader is not None and bool(re.search(self.categoryPattern, blockHeader))

    def processHead(self, textLine, context):
        if textLine is None:
            raise IllegalStateException()

        for matcher in re.finditer(self.categoryPattern, textLine):
            category = matcher.group(1)
            sortKeyStart = category.find("|")
            if sortKeyStart != -1:
                self.categories.add(category[0:sortKeyStart])
            else:
                self.categories.add(category)

        if not self.categories:
            raise IllegalStateException("Category pattern did not match")

        return True

    def fillContent(self, context):
        for category in self.categories:
            context.getPage().addCategory(category)

        self.categories.clear()
